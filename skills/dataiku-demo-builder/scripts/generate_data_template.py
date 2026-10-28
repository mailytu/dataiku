#!/usr/bin/env python3
"""Synthetic data generator template for Dataiku demos.

Adapt the `build_*` functions to the use case. Keep the helpers, the manifest of
injected data quality issues and the writer.

Local sanity check:
    python generate_data_template.py --out ./out --seed 42

Inside a Dataiku Python recipe: import the functions (or paste the file), call
`generate_all(seed)` and write each DataFrame with
`dataiku.Dataset("name").write_with_schema(df)`.
Placement rule: exactly one table goes to Postgres (or Databricks as fallback),
all the others to Snowflake. That is configured on the recipe outputs.
"""
import argparse
import json
import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Parameters (turn them into project variables if useful)
# --------------------------------------------------------------------------- #
N_ENTITIES = 600          # rows in the main entity table
N_EVENTS = 4000           # rows in the events table
LANG = "en"               # "en" (default) or "fr"
START = date(2024, 1, 1)
END = date(2026, 6, 30)

COUNTRIES = {"en": ["FR", "DE", "IT", "ES", "BE"], "fr": ["FR", "DE", "IT", "ES", "BE"]}

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def make_ids(prefix, n, width=6, start=1):
    return [f"{prefix}-{i:0{width}d}" for i in range(start, start + n)]


def random_dates(rng, n, start=START, end=END):
    span = (end - start).days
    return [start + timedelta(days=int(d)) for d in rng.integers(0, span, size=n)]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


# --------------------------------------------------------------------------- #
# Data quality issue injectors. Each returns the modified frame and logs a count.
# --------------------------------------------------------------------------- #

def inject_missing(df, col, rate, rng, manifest, table):
    idx = rng.choice(df.index, size=int(len(df) * rate), replace=False)
    df.loc[idx, col] = np.nan
    manifest.append({"table": table, "issue": "missing_values", "column": col, "rows": int(len(idx))})
    return df


def inject_duplicates(df, rate, rng, manifest, table):
    n = int(len(df) * rate)
    dup = df.sample(n=n, random_state=int(rng.integers(0, 10**6)))
    out = pd.concat([df, dup], ignore_index=True)
    manifest.append({"table": table, "issue": "duplicate_rows", "rows": int(n)})
    return out


def inject_out_of_range(df, col, rate, rng, manifest, table, bad_values):
    idx = rng.choice(df.index, size=int(len(df) * rate), replace=False)
    df.loc[idx, col] = rng.choice(bad_values, size=len(idx))
    manifest.append({"table": table, "issue": "out_of_range", "column": col, "rows": int(len(idx))})
    return df


def inject_inconsistent_labels(df, col, variants, rate, rng, manifest, table):
    """variants: dict canonical -> list of alternative spellings."""
    idx = rng.choice(df.index, size=int(len(df) * rate), replace=False)
    for i in idx:
        canon = df.at[i, col]
        if canon in variants:
            df.at[i, col] = random.Random(int(i)).choice(variants[canon])
    manifest.append({"table": table, "issue": "inconsistent_labels", "column": col, "rows": int(len(idx))})
    return df


def inject_orphan_keys(df, col, rate, rng, manifest, table, prefix):
    idx = rng.choice(df.index, size=int(len(df) * rate), replace=False)
    df.loc[idx, col] = [f"{prefix}-9{int(rng.integers(10000, 99999))}" for _ in idx]
    manifest.append({"table": table, "issue": "orphan_foreign_keys", "column": col, "rows": int(len(idx))})
    return df


# --------------------------------------------------------------------------- #
# Entity builders: ADAPT THESE to the use case
# --------------------------------------------------------------------------- #

def build_entities(rng, manifest):
    n = N_ENTITIES
    df = pd.DataFrame({
        "entity_id": make_ids("ENT", n),
        "country": rng.choice(COUNTRIES[LANG], size=n),
        "segment": rng.choice(["SME", "Mid-market", "Enterprise"], size=n, p=[0.5, 0.3, 0.2]),
        "start_date": random_dates(rng, n, START, date(2025, 6, 30)),
        "annual_value": np.round(rng.gamma(4.0, 3500.0, size=n), 0),
    })
    df["age_days"] = (pd.Timestamp(END) - pd.to_datetime(df["start_date"])).dt.days
    # Data quality issues
    df = inject_inconsistent_labels(df, "country", {"FR": ["France", "fr", "FR "], "DE": ["Germany", "de"]}, 0.05, rng, manifest, "entities")
    df = inject_missing(df, "segment", 0.03, rng, manifest, "entities")
    df = inject_duplicates(df, 0.02, rng, manifest, "entities")
    return df


def build_events(rng, entities, manifest):
    ids = entities["entity_id"].drop_duplicates().tolist()
    n = N_EVENTS
    df = pd.DataFrame({
        "event_id": make_ids("EVT", n, width=7),
        "entity_id": rng.choice(ids, size=n),
        "event_date": random_dates(rng, n),
        "event_type": rng.choice(["incident", "maintenance", "inspection"], size=n, p=[0.4, 0.4, 0.2]),
        "duration_days": np.round(rng.gamma(2.0, 2.0, size=n), 1),
        "cost": np.round(rng.gamma(2.0, 400.0, size=n), 0),
    })
    df = inject_out_of_range(df, "duration_days", 0.02, rng, manifest, "events", [-3, 999])
    df = inject_orphan_keys(df, "entity_id", 0.02, rng, manifest, "events", "ENT")
    return df


# ML design: decided at generation time, written down here.
# EXAMPLE ONLY: the columns, drivers and weights below are placeholders to show the
# mechanism. Replace ALL of them with the variables of the use case in the prompt
# (for a renewal use case: satisfaction, incidents, usage vs allowance; for quality:
# process parameters; etc.). Never keep these names by default.
# DRIVERS: observable columns that really cause the target, with their weight
#          (sign = direction). Each one must make business sense.
# NO_EFFECT: columns deliberately given no impact on the target (the model should
#          rank them low). Everything not listed in either place is a mistake.
DRIVERS = {"age_days": 0.8, "n_events": 0.9, "total_downtime": 0.7}
NO_EFFECT = ["country", "segment", "annual_value"]
NOISE = 0.8          # keeps the model credible (AUC about 0.75 to 0.90), not perfect


def zscore(x):
    x = pd.Series(x, dtype=float)
    return (x - x.mean()) / (x.std() or 1.0)


def build_outcomes(rng, entities, events, manifest):
    """Target table the ML will predict (Y). Y depends on DRIVERS plus noise only."""
    base = entities.drop_duplicates("entity_id").copy()
    agg = events.groupby("entity_id").agg(n_events=("event_id", "count"), total_downtime=("duration_days", "sum"))
    base = base.merge(agg, left_on="entity_id", right_index=True, how="left").fillna({"n_events": 0, "total_downtime": 0})
    base["total_downtime"] = base["total_downtime"].clip(lower=0, upper=200)  # ignore injected bad values
    logit = sum(w * zscore(base[c]).values for c, w in DRIVERS.items()) - 1.0
    logit = logit + rng.normal(0, NOISE, size=len(base))
    base["outcome"] = (rng.random(len(base)) < sigmoid(logit)).astype(int)
    # Sanity check: every driver must show a real link with Y, no-effect columns none
    print("Driver check (correlation with outcome):")
    for c in DRIVERS:
        print(f"  {c}: {base[c].corr(base['outcome']):+.2f}  (expected {'+' if DRIVERS[c] > 0 else '-'})")
    manifest.append({"table": "outcomes", "issue": "ml_design", "drivers": DRIVERS, "no_effect": NO_EFFECT, "noise": NOISE})
    out = base[["entity_id", "outcome"]].copy()
    out["observed_on"] = END
    return out


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #

def generate_all(seed=42):
    rng = np.random.default_rng(seed)
    random.seed(seed)
    manifest = []
    entities = build_entities(rng, manifest)
    events = build_events(rng, entities, manifest)
    outcomes = build_outcomes(rng, entities, events, manifest)
    return {"entities": entities, "events": events, "outcomes": outcomes}, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="./out")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    tables, manifest = generate_all(args.seed)
    os.makedirs(args.out, exist_ok=True)
    for name, df in tables.items():
        df.to_csv(os.path.join(args.out, f"{name}.csv"), index=False)
        print(f"{name}: {len(df)} rows, {df.shape[1]} columns")
    with open(os.path.join(args.out, "dq_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("Injected data quality issues:")
    for m in manifest:
        print(" -", m)


if __name__ == "__main__":
    main()
