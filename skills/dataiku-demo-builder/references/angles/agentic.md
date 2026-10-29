# Angle: agentic

Use when the user wants the demo to put agents at the centre. The mandatory components still apply; this file raises the bar on the agent side so the demo showcases the full breadth of Dataiku's agentic capabilities in a way that serves the use case.

## All 15 capabilities are mandatory
Every item of the capability checklist below is present in every agentic demo, items 1 to 15 alike. None can be skipped for story or size reasons; only a missing licence or add-on on the instance excuses one (for example Agent Review without the Advanced LLM Mesh add-on), and that must be reported with the reason. A capability that exists but plays no role in the story does not count: each one is wired into the flow and the talk track, never left as an orphan object. The work is to find, for each capability, the place where it naturally serves the use case.

## Weave them into one story
Design the agentic part around one persona and one governed process before building anything, then give every capability its job in that story. Use this spine and adapt the vocabulary to the use case:

- **Knowledge layer.** The RAG documents (item 10) are embedded into one knowledge bank shared by the Prompt recipe and the agents. The semantic model (item 7) sits on the project's main prepared and scored tables so the agents answer analytical questions ("how many high-risk assets per site this month?") correctly.
- **Text at scale.** The Prompt recipe developed in Prompt Studio (item 11) classifies or summarises the text records of the use case (incident reports, claims, tickets). Its output feeds a dataset the agents or the webapp read. The fine-tuned LLM (item 12) is trained on the same task, from a supervised dataset built in the flow out of those records.
- **Exploration assistant.** The simple visual agent (item 1) is the copilot the persona talks to. Its visual tools (item 4) cover the real needs: a dataset or SQL lookup, a Knowledge Bank Search on the documents, a Model Prediction tool on the ML model, a Dataset Append tool that logs an action, and a Query Another Agent tool that delegates to the structured agent. Its visual skills (item 6, two or three) are business procedures it loads on demand.
- **Governed process.** The structured visual agent (item 2) runs the procedure with rules (triage, approval, escalation): intake, an LLM Request block powered by the fine-tuned model, a mandatory tool call that can never be skipped, routing on the result, and a skill or reflection step for the final answer.
- **Custom logic.** The code tool (item 5) holds the domain calculation or business rule a visual tool cannot express (a risk score formula, an SLA or cost calculation, an eligibility rule), and the agents call it. The code agent (item 3) stays small and has a clear reason to exist: for example a specialist sub-agent called by the structured agent through a Delegate block, or a deterministic orchestration step. Keep both short and explain in the wiki why code was the right choice there.
- **Trust and governance.** One shared test set of 8–12 cases feeds the agent evaluation store (item 9, at least two runs) and the GenAI comparison (item 13: base LLM vs fine-tuned model, or agent v1 vs v2). Agent Review (item 8) reuses a few of these cases plus one multi-turn conversation. The agent runs keep their full traces for the Trace Explorer (item 14).
- **Adoption.** Both visual agents are published in Agent Hub (item 15), next to the custom webapp, which still offers a way to talk to the agent or act on its output.

The wiki demo script walks through this spine in order, so every capability shows up as a step of the story, not as a feature tour.

These items add objects, so the agentic flow may grow to about 35 objects. Keep each extra object justified and grouped in named zones (for example Sources → Data Prep → Machine Learning → Knowledge → Agents → Fine-tuning → Evaluation → App).

### How to build them (learned on DSS 15)
- **What tools can do it**: Cobuild cannot create Prompt recipes, RAG LLMs, LLM evaluation recipes or configure Agent Hub. Use dku-cli: `dku rag create`, `dku recipe create-prompt`, `dku evaluation-store create --flavor LLM`, `dku recipe create-llm-eval`, `dku agent create --type STRUCTURED_AGENT` + `dku agent-block set-graph`, `dku webapp create --from-plugin traces-explorer --component traces-explorer`. Use Cobuild for zones, descriptions and the wiki.
- **Manual steps (UI only, list them in the final message with the click path)**: creating the Prompt Studio itself and its variants (no public API), and enrolling agents in Agent Hub (the hub config is browser-session only). Build the Prompt recipe by CLI with the same prompt so the flow works, then recreate it in Prompt Studio for the live demo.
- **Prompt recipe output storage**: `create-prompt` auto-creates its output on an arbitrary connection. Immediately fix the dataset definition (`type`, `params.connection`, `params.schema`, `params.table` like `${projectKey}_NAME`) to match the project's main connection, or the build fails.
- **Traces for Trace Explorer**: set the Prompt-on-agent recipe's `payload.rawResponseOutputMode` to `RAW` (an invalid value such as `RAW_WITH_TRACES` makes the job fail with a NullPointerException).
- **LLM evaluation recipe**: set its code env to the LLM evaluation env and `containerSelection` to `NONE` (the default env tries to run in a container). For a JSON classification task, `QUESTION_ANSWERING` with `answerCorrectness,answerSimilarity` against the expected completion works without a context column.
- **Fine-tuning**: start it first, since remote fine-tuning can wait in the provider queue for hours; meanwhile build the structured agent with the base model, then switch the qualification block's `llmId` to the fine-tuned model and rerun the comparison once it is deployed.
- **Delegation**: expose the structured agent to the visual agent through an `LLMMeshLLMQuery` tool on `agent:<structured_agent_id>`, and say in the visual agent's instructions when to delegate.

Docs are the source of truth for exact settings and current behaviour. Fetch the relevant page when you build that piece rather than trusting memory, because agent features evolve quickly. Prefer the headless plugin tools; fall back to dataiku-cli, the Python API client or Cobuild.

## Capability checklist

### 1. Simple visual agent (always)
An LLM-driven ReAct agent: it chooses tools and skills autonomously from instructions. Use it for the open-ended assistant the persona talks to (a maintenance copilot, an account assistant).
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-simple-visual-agents.html

### 2. Structured visual agent (always)
A sequence of blocks with deterministic logic around the LLM: intake and intent classification, routing, parallel lookups, loops, approvals. Use it where the business has a defined procedure that must be followed (triage, escalation, refund or work-order approval). A strong demo has both: a simple agent for exploration, a structured agent for the governed process, ideally with the structured one delegating or being called from the other.
Blocks to consider, and when each earns its place:
- Agentic Loop: LLM with tools inside a step; collect required fields over several turns
- LLM Request: a single controlled LLM call (classify, summarise, draft)
- Manual or Mandatory Tool Call: force a specific lookup so it can never be skipped
- Delegate: hand over to another agent
- Routing: branch on state (intent, severity, customer tier)
- For Each / Parallel: loop over items or fetch several things at once
- Reflection: have the agent check its own draft
- State and Scratchpad entries: remember data across blocks and turns
- Context compression, Generate Text Output, Python block, Semantic feedback: use if the story needs them
- Expressions and conversational disambiguation: use when the user may be vague
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-structured-visual-agents.html and https://doc.dataiku.com/dss/latest/agents/structured-visual-agents/overview.html
Concepts: https://doc.dataiku.com/dss/latest/agents/structured-visual-agents/concepts.html
Block reference index: https://doc.dataiku.com/dss/latest/agents/structured-visual-agents/blocks/index.html (one page per block: agentic-loop, llm-request, manual-mandatory-tool-call, delegate, routing, foreach, parallel, reflection, state-scratchpad, context-compression, generate-text-output, python, semantic-feedback)
Expressions: https://doc.dataiku.com/dss/latest/agents/structured-visual-agents/expressions.html
Disambiguation how-to: https://doc.dataiku.com/dss/latest/agents/structured-visual-agents/how-to/conversational-disambiguation.html

### 3. Code agent (always, small and justified)
A Python agent for logic the visual editor cannot express. In a visual-first demo it stays small and has a clear reason to exist (for example a specialist sub-agent called through a Delegate block, or one custom orchestration step). Explain that reason in the wiki.
Docs: https://doc.dataiku.com/dss/latest/agents/code-agents.html

### 4. Visual tools (always; the core, chosen for the use case)
Categories: query data (Dataset Lookup, SQL query, Knowledge Bank Search), perform actions (Dataset Append, Model Prediction, Send Message), orchestration (Query Another Agent or LLM), integration (Jira, Salesforce, Google search, MCP). Choose the tools a real user of this use case would need: for a maintenance copilot, a lookup on equipment and interventions, a model prediction tool on the failure model, an append tool to log a work order. Attach each with a clear name and description, since the LLM chooses tools from them.
Docs: https://doc.dataiku.com/dss/latest/agents/tools/index.html and https://knowledge.dataiku.com/latest/genai/agents/concept-agent-tool-overview.html

### 5. Code tool (always, at least one)
A small custom Python tool kept inside the project for the calculation or rule a visual tool cannot express (for example a domain formula). Find that calculation in the use case; keep it short and readable.
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-agent-tool-overview.html

### 6. Visual skill (always, at least one; often two or three)
Skills are reusable instructions the agent loads only when relevant, which keeps context focused and cheap. Each has a name, description, optional metadata, instructions and optional assets (templates, sub-tasks). Write skills as business procedures (for example "how to assess a risky asset and propose next actions", "how to write an account brief"), and let the structured agent or simple agent load them.
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-agent-skills.html

### 7. Semantic model (always)
The agents always get analytical questions to answer, so the semantic model always has a job. It gives the agent business meaning for tables, columns, measures and relationships so that it queries data correctly. Build it on the project's main tables with business-friendly names, descriptions and a few key measures.
Docs: https://knowledge.dataiku.com/latest/genai/agents/semantic-models-lab/tutorial-index.html

### 8. Agent review (always)
Define a handful of realistic test cases (single-turn with reference answers, and one multi-turn with a simulated user), set traits, run a review and show the pass/fail view. It requires the Advanced LLM Mesh add-on; if the add-on is missing, report it and skip this item only.
Docs: https://doc.dataiku.com/dss/latest/agents/agent-review.html and https://knowledge.dataiku.com/latest/genai/agents/semantic-models-lab/tutorial-index.html

### 9. Agent evaluation store (always, with several tests)
Build a test dataset of 8–12 realistic cases with reference answers, run the agent on it (Prompt recipe on the agent), evaluate with the Evaluate Agent recipe into an evaluation store, and run it at least twice so the store shows a history. Choose metrics the audience understands (answer correctness, faithfulness, tool usage).
Docs: https://doc.dataiku.com/dss/latest/agents/evaluation.html and https://knowledge.dataiku.com/latest/deploy/genai-monitoring/tutorial-agent-evaluation.html

### 10. RAG (always)
The Prompt recipe with RAG is already a mandatory component (see `mandatory-components.md`, component 8); reuse its knowledge bank and extend it here for the agents. Documents such as procedures, manuals, incident reports or policies embedded into a knowledge bank, then searched by a Knowledge Bank Search tool. Every use case has procedures, policies or reports to draw on (maintenance procedures, warranty policies, quality manuals). The documents are the synthetic files generated with `scripts/generate_documents_template.py`. This adds a managed folder and an Embed recipe; keep the total flow size in check.
Docs: https://knowledge.dataiku.com/latest/genai/rag/concept-rag.html

### 11. Prompt Studio (always)
A Prompt recipe to classify, extract or summarise text at scale (for example classify incident reports), developed and compared in Prompt Studio (show at least two prompt or LLM variants on the same examples), grounded with the RAG knowledge bank (mandatory component 8). Its output must be consumed downstream.
Docs: https://knowledge.dataiku.com/latest/genai/text-processing/concept-prompt-studio.html

### 12. Fine-tuned LLM (always)
Build a supervised dataset in the flow (input text → expected output, a few hundred rows, train/validation split), run the fine-tuning recipe, and use the resulting model in the story: one block of the structured agent or the Prompt recipe calls it, and it is a variant in the GenAI comparison. A fine-tuned model that nothing uses does not count. Keep the dataset small and the base model cheap so training is quick.
Docs: https://doc.dataiku.com/dss/latest/generative-ai/fine-tuning.html

### 13. GenAI comparison (always)
Evaluate the same test cases with at least two variants (for example GPT-class LLM vs fine-tuned model, or agent v1 vs v2) and open the comparison of the evaluations in the evaluation store, so the audience sees which variant wins on which metric.

### 14. Trace Explorer (always)
Keep the full traces of agent runs (the agent responses dataset with the raw response and trace columns) and open them in the Trace Explorer to show tool calls, skill loads and structured-agent blocks. Mention in the wiki which test case gives the most telling trace.

### 15. Agent Hub (always)
Publish the visual agent and the structured agent in an Agent Hub webapp with a business description and three starter questions each. It complements the custom webapp; it does not replace it.

## Fit with the flow-size rule
Agentic demos grow to about 35 objects. Keep the flow readable by grouping agent, knowledge, fine-tuning and evaluation objects in their own zones and reusing the same few datasets as tools, knowledge and test data. Cut detail inside a capability rather than a capability. Four datasets and one Postgres/Databricks table still hold.

## Agentic acceptance checklist
Every line is required. Only a missing licence or add-on excuses one, reported with the reason.
- [ ] 1. Simple visual agent working with its tools and skills, tested on realistic questions
- [ ] 2. Structured visual agent with routing, a mandatory tool call and an LLM Request block, running the governed process
- [ ] 3. Code agent, small, with its role in the story explained in the wiki
- [ ] 4. Visual tools chosen for the use case (lookup, Knowledge Bank Search, Model Prediction, Dataset Append, delegation), with names and descriptions the LLM can use
- [ ] 5. Code tool for a domain calculation or rule, called by an agent
- [ ] 6. Two or three visual skills, at least one loaded on demand and visible in a trace
- [ ] 7. Semantic model on the main tables, used by an agent to answer an analytical question
- [ ] 8. Agent Review with single-turn cases, one multi-turn case, traits and a run (or the missing add-on reported)
- [ ] 9. Agent evaluation store with 8–12 test cases and at least two evaluation runs
- [ ] 10. RAG knowledge bank shared by the Prompt recipe and a Knowledge Bank Search tool
- [ ] 11. Prompt Studio prompt with at least two variants compared, deployed as a Prompt recipe with RAG whose output is used downstream
- [ ] 12. Fine-tuned LLM trained and used by the structured agent or the Prompt recipe
- [ ] 13. GenAI comparison of at least two variants (including the fine-tuned model) open in the evaluation store
- [ ] 14. Trace Explorer opened on stored agent traces; the most telling test case named in the wiki
- [ ] 15. Visual and structured agents published in Agent Hub with descriptions and three starter questions each
- [ ] Webapp offers a way to talk to the agent or to act on its output
- [ ] Wiki demo script follows the story spine: ask, tool call, skill load, analytical question, governed process, custom logic, trace, evaluation and comparison, review, Agent Hub
