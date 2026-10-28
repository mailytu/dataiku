# Mandatory components

Every demo contains all of the components below. For each one: why it is there, what "done" means, and how to check it. Append new components at the end; the checklist in SKILL.md should mirror this list.

Every component is a demo of a capability, not a production solution: keep each one simple, readable and easy to explain in a sentence or two.

## 1. Data Quality checks
**Why**: shows governance and trust in the data, and gives the audience an immediate "aha" on messy real-world data.
**Done when**:
- Rules/checks exist on the raw datasets and cover the problems injected by the generator (missing values, duplicates, out-of-range values, inconsistent formats, orphan keys, stale records, as relevant).
- At least two or three of them visibly fail or warn on the raw data, each tied to a business consequence the audience understands (for example "sensor readings out of physical range").
- After the Prepare step, the matching checks on the prepared datasets pass.
- The data quality status is computed (not left "not computed").
**Check**: read the data quality status of raw and prepared datasets through the plugin tools.

## 2. Visual Prepare + another visual recipe
**Why**: shows low-code transformation that business analysts can read.
**Done when**: one Prepare recipe fixes the injected issues using visible, named steps (not a single code step), and at least one other visual recipe (Join, Group, Window, Stack, Pivot, Top N, Split, Sync, ...) builds something the ML or the app needs. These are minimums, and the flow must stay small: use as few components as possible, adding a visual recipe (join, group, window, split, ...) only when the use case would not be coherent without it. Each recipe must have a business reason; never add recipes to fill the flow. Apart from the data-generation recipe and the SQL recipe (component 7), keep Python out of the main path.
**Check**: list recipes and their types; each non-trivial recipe has a business description.

## 3. Machine Learning
**Why**: shows AutoML and explainability on a question the business cares about.
**Done when**: a visual ML analysis targets a business-meaningful outcome (a failure, a churn or renewal risk, a delay, a quality defect), a model is trained and deployed to the flow, and a scoring step produces predictions used by the webapp and/or the agent. Keep training quick; pick a metric the audience can read. The target and the explanatory variables must follow a clear business logic decided in the data script (see ML design in `data-generation.md`): several variables have a real impact on the model, and any variable without impact is deliberately so. Check the variable importance.
**Check**: the saved model has a version, the scored dataset is built and non-empty, and the variable importance matches the designed drivers.

## 4. Visual Agent with a Visual Tool and a Visual Skill
**Why**: shows agentic AI built visually, grounded in the project's own data.
**Done when**:
- A visual agent exists with clear instructions tied to the persona.
- At least one visual tool (chosen for the use case: dataset lookup, SQL query, knowledge bank search, model prediction, send message, ...) is attached and works.
- At least one visual skill (reusable, loaded on demand) is attached, holding task-specific guidance such as how to analyse an asset or draft a recommendation.
- Two or three realistic test questions give answers consistent with the data.
**Check**: run test queries; read the answers against the data.
For the agentic angle, the much longer list in `angles/agentic.md` applies.

## 5. Structured Agent (blocks)
**Why**: shows the control and reliability of a structured, step-by-step agent next to the more autonomous visual agent, on a process where order and rules matter.
**Done when**:
- A structured agent exists, built with blocks in a clear sequence suited to the use case (for example an LLM request to understand the case, a tool call to fetch data or a prediction, routing or a condition for different paths, and a final text output). Pick the blocks that fit the process; see `angles/agentic.md` for what each block is for.
- It uses at least one tool from the project (dataset lookup, model prediction, knowledge bank, ...) and has a different job from the visual agent (for example a deterministic triage or a decision workflow, where the visual agent is a free-form assistant).
- Clear instructions and a business description.
- Two or three realistic test questions give answers consistent with the data.
**Check**: run test queries and read the trace of blocks; the answers match the data.

## 6. Webapp connected to the project data
**Why**: the business-facing face of the demo, and the most memorable part.
**Done when**: a Dataiku webapp reads the project's datasets (typically the scored output), is designed for this use case following `webapp-design.md`, uses the requested accent colour, and shows the synthetic-data notice. It opens without errors and shows real figures.
**Check**: start the webapp, open it, confirm that data appears and that filters and actions work.

## 7. SQL recipe with the SQL assistant
**Why**: shows that technical users keep full control with SQL, and that the AI SQL assistant speeds them up.
**Done when**:
- A SQL recipe (in-database on Snowflake, or on the operational database if it fits) builds something the flow needs, typically an aggregation, a feature table or a business KPI that is natural in SQL. It is not a duplicate of a visual recipe.
- The query was written or refined with the SQL assistant: use the assistant to generate the query from a natural-language instruction, and keep that instruction in the recipe description or the wiki so the presenter can reproduce it live ("calculate the number of incidents and downtime per asset per month"). Also prepare one explain or fix request to show in the demo.
- The recipe builds and its output is non-empty.
**Check**: read the recipe settings, build it, sample the output. If the assistant cannot be driven programmatically, write the SQL yourself, write the natural-language instruction it would come from in the wiki, and list the assistant step as manual.

## 8. Prompt recipe from Prompt Studio, with RAG
**Why**: shows generative AI embedded in a data flow (batch enrichment of rows) and grounded in documents, next to the agents.
**Done when**:
- A Prompt Studio prompt exists, tested on a few examples, and the Prompt recipe uses it to process a dataset in the flow (for example summarise or classify free-text reports, draft a recommendation per row, or generate a customer message).
- The prompt is grounded by RAG: synthetic documents (procedures, policies, manuals, past reports) in a managed folder, embedded with an Embed recipe into a knowledge bank, and the prompt uses the retrieval-augmented LLM. Documents are generated by the skill with `scripts/generate_documents_template.py`: synthetic, coherent with the data (same entities, rules, thresholds), in the demo language, and in three formats at minimum: one PDF plus two other formats (for example DOCX and Markdown; HTML, TXT or PPTX also work). They are files, not counted in the dataset limit; upload them to the managed folder with the plugin.
- The output dataset has a sensible schema, a manageable number of rows (limit the rows processed to keep cost and time low) and non-empty answers that cite or reflect the documents.
**Check**: knowledge bank built and searchable (search it with the plugin tool), prompt recipe built, output sampled and coherent. This knowledge bank can also feed the agents' knowledge bank search tool, so reuse it.

## Always-on conventions (not components, but checked every time)
- Flow organised in named zones; objects described. The Default zone is renamed "Sources" and holds the data generation Python recipe and its input datasets (no empty Default zone).
- Wiki article with the story, a click-by-click demo script, and the questions to ask each agent.
- Language as requested (English by default).
