# Data generation

One Python script generates all demo data, coherently, with deliberate quality problems, and writes it to the databases. It is the first object of the flow (a Python recipe) so the demo can be rebuilt from scratch in minutes.

## Rules
- **Keep it simple, but plausible and meaningful**: this is a demo, not an MVP. Few columns, only the ones the story uses, but realistic and meaningful for the audience (real-looking categories, units, ranges and vocabulary) so business users can project themselves into it. Relationships stay simple and explainable. The ML target (Y) and its explanatory variables must follow a clear business logic (see ML design below). Every column and table can be explained in one sentence.
- **At most 10 columns per dataset, as a hard ceiling, and only the columns that are needed.** Fewer is better: each input column is used somewhere (a Prepare step, a join key, an ML driver or a deliberate no-effect variable, a data quality check, an agent tool, the webapp) or carries the story. Do not add columns "for realism" or "just in case"; a column nobody uses in the demo is removed from the generator. The same ceiling applies to the datasets the flow produces: drop the columns that are no longer needed instead of carrying them along.
- **At most 4 datasets, 5 if truly necessary.** Think in business entities: for example a reference table (assets, contracts, customers), an event/fact table (interventions, orders, claims), a time-series or measurements table, and a text or outcome table. Merge entities rather than multiplying tables.
- **Placement**: exactly one dataset goes to the operational database (Postgres by default, Databricks if no working Postgres connection); all others go to Snowflake. If neither Postgres nor Databricks has a working connection (test it first), that dataset is generated in Snowflake like the others and the final message says so. Choose for the operational one the table that would realistically live in a transactional system (the referential or the live orders).
- **Coherent**: keys line up across tables, dates make sense, relationships carry signal the ML model can learn (for example failure probability increases with age, vibration and missed maintenance), and values stay inside realistic ranges for the domain.
- **Size**: enough to look real, small enough to build fast. Roughly 500 to 5,000 rows for entity tables and up to about 50,000 rows for events or measurements. Fixed random seed so the demo is reproducible; the seed is a variable.
- **Language**: names, categories, free text and country/city values follow the demo language.
- **Documents for RAG**: the Prompt recipe with RAG needs a small set of synthetic documents (for example 8 to 20 short procedures, policies or past reports as text or markdown files) in a managed folder. They are not datasets and do not count in the limit; generate them with `scripts/generate_documents_template.py` (one PDF plus at least two other formats), consistent with the data (same entities, rules and vocabulary) and in the demo language.
- **Synthetic**: never use real people, real company names or real identifiers. Use obviously fictional IDs (CTR-002409, EQ-0153). Add a column or table-level description saying the data is synthetic.

## ML design (decide it while generating)
The drivers always come from the use case in the prompt: its Y, its entities and its business logic decide which variables explain it. The names in the template script (`age_days`, `n_events`, `total_downtime`) are placeholders to show the mechanism; replace them, and never reuse them just because they are in the template.
Before writing the generator, write down the causal design for the target Y:
- **Drivers**: pick 3 to 5 explanatory variables that really cause Y, each with a direction and a weight, and each making business sense (for example failure risk rises with equipment age, number of past incidents and delayed maintenance). They must be real columns in the datasets the model will use (or aggregates of them), not hidden variables. At least two or three must have a clear impact on the model.
- **Variables with no effect**: not every variable has to matter. Some can have none (for example country or a label column), but this is a decision taken at generation time and recorded, never an accident. The model should rank them low.
- **Noise**: add enough noise for a credible model (AUC about 0.75 to 0.90).
- **Y is generated from the drivers** (for example a probability from a weighted sum, then sampled), never independently of them, and the injected data quality problems must not break the signal on the clean rows.
- The template script has `DRIVERS`, `NO_EFFECT` and `NOISE` and prints a driver check; the design also goes in the manifest and the wiki.
- After training in Dataiku, read the variable importance: the top variables must be the drivers, and the no-effect variables must rank low. If not, fix the generator and rebuild.

## Deliberate data quality problems
Inject a controlled amount (around 2 to 8 percent of rows per issue) so checks have something to catch and the Prepare recipe has something to fix. Pick 4 to 6 issues relevant to the use case, mixing types:
- missing values in an important column
- duplicate rows or duplicate keys
- out-of-range or physically impossible values (negative quantities, sensor readings beyond the range, dates in the future)
- inconsistent formats (country written "FR", "France", "fr"; mixed date formats; trailing spaces; mixed units)
- orphan foreign keys (an intervention referencing an unknown equipment)
- stale or contradictory records
- placeholder values ("N/A", "-999", "UNKNOWN")
Record in a small dictionary which issues were injected and at what rate. Use it to create the matching data quality rules and to write the wiki ("what the checks should find").

## Script contract
`scripts/generate_data_template.py` is the starting point. It provides: a seed, size parameters, helper functions for dates, ids and noise, helpers to inject each class of issue, a manifest of injected issues, and a writer that either saves CSVs locally (for a sanity check) or writes to Dataiku datasets inside a Python recipe. Adapt the entity functions to the use case; keep the helpers.

Run it locally first:
```
python scripts/generate_data_template.py --out ./out --seed 42
```
Check the printed manifest: row counts, injected issue rates, key coverage. Fix before pushing to the instance.

## In Dataiku
- Create the Python recipe with the script and set its outputs to the target datasets: Snowflake connection for most, the Postgres (or Databricks) connection for the one operational dataset, or Snowflake if neither works. Test the connections first.
- Name datasets clearly and in the demo language, with a `_raw` suffix for raw layers, and describe each dataset and its columns.
- Build the recipe, then check row counts with the dataset tools and confirm that the injected problems are really visible (profile or sample).
- If a connection is not writable, say so and continue with the other parts; do not silently fall back to CSV uploads.
