# Demo delivery: making it ready to present

A demo is good when someone can present it calmly in front of business people. These rules cover what makes the difference between "built" and "ready to present". Apply them in the order of the workflow.

## 1. Metadata on everything (always)
Datasets always carry metadata. Never leave a dataset, recipe, zone, model, agent, tool or webapp without it.
- **Datasets**: a short business description (one sentence: what it is, where it comes from, who uses it), tags (for example `raw`, `prepared`, `scored`, `synthetic`), and a description on every column (meaning, unit, allowed values). Use the dataset column-description tools to set and check them.
- **Recipes, zones, model, agent, tools, skill, webapp**: a short business-readable description.
- **Project**: description, tags, a short project summary and a project owner.
- **Flow readability**: explicit business names, no crossing links where it can be avoided, zones ordered left to right in reading order (Sources → Data Prep → Machine Learning → Scoring → Agent / App), no orphan or leftover objects. Sources is the Default zone renamed, holding the data generation recipe and the input datasets; there is never an empty Default zone next to a separate sources zone.
- Check at the end: list the datasets and confirm none has an empty description or empty column descriptions.

## 2. Demo script (talk track)
Write it into the project wiki. 5 to 7 minutes for the short path, with an optional extended path up to 15–20 minutes. For each step: where to click, what to say in one or two business sentences per persona, and what the audience should conclude. Mark the **wow moments**, for example the data quality check that catches a real problem, the score that changes a decision, the agent that answers with its sources, the webapp action that closes the loop. A demo is carried by its story as much as by its objects.

## 3. "Ready to present" state
Nothing is left to build live. Before reporting success:
- all datasets and recipes built; the flow shows no failed or never-built objects
- the model is trained and deployed, scoring computed
- data quality rules run, with the injected problems visibly failing or warning on raw data, and passing after preparation (not everything green)
- the webapp is started and loads data; the agent has answered at least once
- optionally, a very light scenario that rebuilds the flow (no notification or extra logic unless it helps the story). A small native dashboard is optional too. Remember this is a demo, not an industrialised solution.

## 4. Agent test scenarios
For every agent in the project (visual and structured), prepare 3 to 5 realistic questions that work reliably, and write them in the wiki, grouped by agent, with the expected answer. Run them during the build and fix tool or skill descriptions until the answers are coherent with the data. With the `agentic` angle, these are the seed of the Agent Review tests.

## 5. Visual check of the webapp
Open the webapp in a browser once it runs. Click every filter and button, trigger the agent action, resize to 1280–1440 px, check empty and loading states and text overflow. Fix what you find. Do not report the webapp as done before this.

## 6. Credible machine learning
Aim for an AUC (or equivalent metric) around 0.75 to 0.90 with explanatory variables that the business recognises. A model at 0.99 is not believable; if the generated data is too easy, add noise in the data script. Check the variable importance: the top variables must be the drivers designed in the data script (see ML design in `data-generation.md`), and variables designed to have no effect must rank low. If they do not, fix the generator and rebuild.

## 7. Reruns and robustness
- Use a unique, readable project key with a suffix when needed; check whether the project already exists before creating it.
- Make each step safe to rerun without rebuilding everything; keep step status in the task list.
- Verification gates after each phase, using the plugin tools (dataset sample and profile, data quality status, job status, webapp state): after data, after flow, after ML, after agent, after webapp. Do not move on while a gate fails.

## 8. Build report
At the end, write a short build report (in the wiki and in the final message): what worked, what failed or is manual, the assumptions made, the defaults applied (language, database, colour), and the links or names to open (project, webapp, agent). Keep it short; it is also useful to improve this skill over time.

## Tools
Create, change and verify through the dataiku-headless plugin tools and dataiku-cli. The Dataiku Python API client is only a complement, for what neither covers or does badly.
