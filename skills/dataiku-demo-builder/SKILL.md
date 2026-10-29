---
name: dataiku-demo-builder
description: Build an end-to-end Dataiku demo project (synthetic data, flow, data quality, ML, visual agent, webapp) from a detailed business use-case description, using the dataiku-headless plugin and dataiku-cli. Use whenever the user asks to create, generate, rebuild or extend a Dataiku demo, POC showcase or demo project for any business use case (manufacturing, aftersales, or any other sector) or for a feature angle (overview, agentic, ML), even if they only say "make me a demo on predictive maintenance" or "crée-moi une démo Dataiku sur ...".
---

# Dataiku Demo Builder

Goal: turn a use-case description ("a demo for plant managers on batch quality", "a demo for aftersales teams on contract renewal, agentic angle") into a finished, presentable Dataiku project. The demo must showcase the Dataiku platform while telling a story that business people recognise and can project themselves into.

This skill encodes the author's fixed demo conventions. The use case itself comes from the user's prompt. Do not invent a different use case, and do not ask the user to restate conventions that are written here.

## Before anything else

1. Load the `dataiku-headless` skill (and `dataiku-headless-setup` if its tools are missing). It explains how to drive the instance; this skill only adds the demo conventions on top.
2. **Tool rule.** Every creation and every verification goes through the dataiku-headless plugin tools and dataiku-cli. The Dataiku Python API client is only a complement, for what neither covers or does badly (for example a specific agent block or a bulk edit). Prefer visual components over code wherever Dataiku offers one, because the audience is shown the platform, not the code.

## Read the request

Extract these from the prompt. Anything missing gets the default, and the choice is stated in one line at the top of the final message.

| Parameter | Default | Notes |
|---|---|---|
| Use case / sector | none (required) | If absent, ask one short question. |
| Feature angle | overview | `overview` needs no extra file. `agentic` → read `references/angles/agentic.md`; all 15 capabilities of its checklist are mandatory, woven into one coherent story. |
| Language | English | Everything visible in the demo (names, descriptions, wiki, prompts, webapp, data values) follows it. French only if the user asks. |
| Webapp accent colour | deep teal-green | The whole palette is derived from it (see webapp reference). |
| Operational database | Postgres | If no working Postgres connection, test Databricks. If neither works, generate that dataset in Snowflake like the others. Say which one was used. |

The use-case description in the prompt is the only source for the story: personas, entities, business questions, vocabulary, ML target and agent role. Before building, list in a few lines the assumptions you make for anything the prompt leaves open (persona, decision, the 3 to 4 datasets, the ML target, the agent's job) and carry on; ask a question only if the use case itself is unclear. Use general domain knowledge to make the data and vocabulary realistic.

## Non-negotiable conventions

These apply to every demo, whatever the sector or angle.

**Story**: one clear business question, one or two personas, and a result a business person can act on. Technical depth stays in the background.

**A demo, not an MVP**: the goal is to illustrate the use case and the logic of the flow clearly, never to build a complete or industrialised solution. Datasets, transformations, models, prompts and agents stay simple, readable and easy to explain out loud in one sentence each. Prefer the simple option every time (few columns that matter, a handful of Prepare steps, a default ML setup, short prompts, one clear tool per job). No edge-case handling, no heavy logic, no optimisation, no production concerns.

**Easy to pick up and to present**: the use case must let the audience project themselves into their own reality, but its translation into a Dataiku project stays simple to grasp and to demo. Someone opening the project for the first time understands the flow in a minute, and a presenter can walk through it without preparing for hours. When realism and ease of demo conflict, simplify the Dataiku side and keep the business vocabulary to carry the realism.

**Flow**: realistic enough to recognise a field reality, small enough to understand at a glance. Keep it as small as possible while the use case stays coherent: the fewest components that tell the story, roughly 15–22 objects organised in named flow zones (for example Sources → Data Prep → Machine Learning → Scoring → GenAI / Agent → App). The first zone, Sources, is always the project's Default zone renamed "Sources": it holds the data generation Python recipe and the input datasets it writes. Never create a separate zone for the sources and never leave the Default zone empty. Every object must have a business reason; if it grows past ~25 objects (~35 for the agentic angle, whose 15 mandatory capabilities add objects), simplify. Give every dataset, recipe and zone a business-readable name and a short description; zones in reading order, no needless crossing links. Delivery rules are in `references/demo-delivery.md`.

**Data** (details in `references/data-generation.md`):
- All datasets come from one Python script that generates coherent synthetic data. The script runs as a Python recipe at the start of the flow and writes the datasets to the databases.
- At most 10 columns per input dataset (a hard ceiling, not a target), and only the columns the demo actually uses. No useless columns in the input datasets, none added "for realism". Intermediate datasets aim for 10 columns or fewer too, but may have more when truly necessary.
- At most 4 datasets, 5 only if truly necessary. Exactly one lives in Postgres (or Databricks as fallback); all others live in Snowflake. If neither Postgres nor Databricks is available, that dataset is generated in Snowflake too, and this is reported.
- The data always contains deliberate quality problems, so the data quality checks have something real to catch.
- Every dataset always has metadata: a business description, tags, and a description on every column.
- Data is strictly synthetic and must say so wherever it is shown to an audience.

**Mandatory components** (checklist and acceptance criteria in `references/mandatory-components.md`; the list grows over time, so always read that file rather than relying on this summary):
- Data Quality rules/checks that visibly flag the injected problems
- A Visual Prepare recipe plus at least one other visual recipe (only add more if the use case would not be coherent without them)
- A Machine Learning model (visual ML) integrated in the flow
- A Visual Agent with at least one Visual Tool and one Visual Skill
- A Structured Agent (built with blocks)
- A SQL recipe, with the SQL assistant used to write it
- A Prompt recipe based on a Prompt Studio prompt, grounded with RAG (documents → Embed recipe → knowledge bank)
- A polished webapp connected to the project's data

**Delivery**: read `references/demo-delivery.md` before step 3 and apply it throughout (metadata everywhere, demo script, ready-to-present state, agent test scenarios, visual check of the webapp, credible ML, reruns and gates, build report).

**Execution**: by default, everything that could run containerised (Python and other code recipes, visual ML training, webapp backends, notebooks, and so on) runs on the DSS backend, not in containers. Check each object's container execution setting (the plugin has `list_container_exec_configs` and `set_container_exec_config`) and set it to the local backend, unless the user explicitly asks for containers or a task cannot run locally.

**Webapp**: designed for the use case, not copied from a template. Read `references/webapp-design.md` for the visual identity and the design principles before building it.

## Workflow

Keep a task list and update it as you go. Start building straight away once the use case is clear.

1. **Plan (short).** Decide: the business question, up to 4 datasets with their columns (10 at most each, and for each column what in the demo uses it), which quality problems to inject, flow zones, the ML target, the agent's job and tools, and the webapp's main screens. Write this into the project wiki as the "Demo guide" skeleton later; do not wait for approval unless the use case itself is ambiguous.
2. **Check the instance.** Confirm the current instance, list connections, and pick Snowflake plus Postgres (fallback Databricks, tested with `test_connection`; if neither works, everything goes to Snowflake). Check that the LLM connection needed for the agent exists. If something required is missing, say exactly what and continue with the rest.
3. **Create the project** in a sensible project folder, with the container execution default set to the backend (see Execution), with a readable project key, a description, and tags. Use project variables for anything that should be easy to change (for example the accent colour or a connection name).
4. **Generate the data.** Start from `scripts/generate_data_template.py`, adapt entities and quality issues to the use case, run it locally once to sanity-check, then put it in the Python recipe so it writes to the target connections. Keep that recipe and its output datasets in the Default zone (zone id `default`) and rename that zone "Sources" with a short description; do not move them to another zone. Verify row counts and that the injected issues are really present.
5. **Build the flow** with visual recipes first: Prepare to clean and enrich, then the other visual recipes the story needs (join, group, window, split, ...), the SQL recipe (written with the SQL assistant), then the ML step, scoring, and the outputs the webapp and agents consume. Add the GenAI part: synthetic documents generated with `scripts/generate_documents_template.py` (one PDF plus two other formats) uploaded to a managed folder, Embed recipe, knowledge bank, Prompt Studio prompt and Prompt recipe with RAG (components 7 and 8 in `references/mandatory-components.md`). Use flow zones.
6. **Data quality.** Add rules/checks on the raw datasets that fail or warn on the injected problems; after Prepare, the corresponding checks on prepared data should pass. The before/after is part of the story.
7. **Machine learning.** Train a visual ML model on a target that matches the business question; deploy it to the flow and score. Keep it quick and explainable (a sensible default algorithm set, a readable metric).
8. **Agents.** Build the visual agent with its tool(s) and skill, and the structured agent with its blocks (see `references/mandatory-components.md`). For the `agentic` angle also follow `references/angles/agentic.md`. Test each agent with realistic questions, keep the answers coherent with the data, and write the questions to ask each agent in the wiki.
9. **Webapp.** Build it from `references/webapp-design.md`, connected to the project datasets (and to the agent if the use case benefits from a conversation). Open it and check that it loads real data.
10. **Document.** Write a wiki article: the story, the personas, a 15–20 minute click-by-click demo script, and a "what is real, what is synthetic" note. Make sure every object has a description (see `references/demo-delivery.md`).
11. **Verify** with the checklist below, run the verification gates from `references/demo-delivery.md`, fix what fails, then summarise.

If a capability needed for a step is not exposed by the plugin tools (for example creating a given agent block), use Cobuild through the plugin first, then dataiku-cli, and the Python API client only as a complement. If it still cannot be done programmatically, finish everything else and tell the user precisely which manual steps remain and where to click.

## Final checklist

Do not report success until each item is true, or is explicitly listed as not done with the reason.

- [ ] Project opens, flow readable, zones named and ordered, the Default zone renamed "Sources" and holding the data generation recipe and input datasets (no empty Default zone, no other sources zone), objects described, every dataset has a description, tags and column descriptions
- [ ] Every input dataset has 10 columns or fewer, each one used in the demo (no useless input columns); intermediate datasets go above 10 only when necessary
- [ ] ≤ 4 datasets (5 if justified), 1 in Postgres/Databricks (Snowflake if neither is available, reported), the rest in Snowflake
- [ ] Data quality rules flag the injected problems; prepared data passes
- [ ] Visual Prepare + another visual recipe present; flow kept small (every object justified)
- [ ] SQL recipe present, built, with the SQL assistant instruction noted in the wiki
- [ ] RAG documents generated by the skill (1 PDF + 2 other formats); Prompt Studio prompt + Prompt recipe with RAG built; knowledge bank searchable; output coherent
- [ ] ML model trained, deployed to the flow, scoring output built; variable importance matches the designed drivers (real impact for several variables, no-effect ones deliberately chosen)
- [ ] Visual agent with visual tool and visual skill, tested on realistic questions
- [ ] Structured agent built with blocks, tested on realistic questions
- [ ] Questions to ask each agent written in the wiki, plus the SQL assistant instruction for the live demo
- [ ] Webapp loads, shows real project data, palette matches the requested colour, synthetic-data notice present
- [ ] Language matches the request
- [ ] Nothing runs in containers: recipes, ML and webapp use the backend (unless asked otherwise)
- [ ] Wiki demo guide written: 5–7 min talk track with wow moments, agent test questions, build report
- [ ] Simple enough to explain: every dataset, recipe and prompt can be described in one sentence
- [ ] Ready to present: everything built, webapp visually checked, ML metric credible (about 0.75–0.90)
- [ ] Angle-specific checklist done (for agentic: all 15 capabilities present and wired into the story; only a missing licence or add-on excuses one, reported)

## Final message

Short and useful: what was built, the demo's story in two sentences, where to open it (project, webapp), the defaults that were applied (language, database, colour), anything not done, and one natural next step. No recap of every step.

## Extending this skill

Add a feature angle: drop a file in `references/angles/` and add one line to the table above. Add a mandatory component: append it to `references/mandatory-components.md` with its acceptance criterion, and to the checklist above.
