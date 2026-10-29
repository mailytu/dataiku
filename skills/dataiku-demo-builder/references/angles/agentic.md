# Angle: agentic

Use when the user wants the demo to put agents at the centre. The five mandatory components still apply; this file raises the bar on the agent side so the demo showcases the breadth of Dataiku's agentic capabilities in a way that serves the use case. Pick the capabilities that make the story better; do not add one only to tick a box, but every item below must either be present or explicitly justified as skipped in the final message.

## Mandatory for every agentic demo
On top of the mandatory components (which already include the visual agent, the structured agent and the Prompt Studio prompt with RAG), an agentic demo always contains the six items below. They are not optional and cannot be skipped for story reasons; only a missing licence or add-on on the instance excuses one, and that must be reported. Each one must be wired into the flow and the story, never left as an orphan object:
1. **Prompt Studio** (item 11): the prompt is developed and compared in Prompt Studio, then deployed as a Prompt recipe that feeds something downstream (a dataset the agent, the webapp or the evaluation reads).
2. **Agent evaluation store with several tests** (item 9): a test dataset of 8–12 realistic cases (normal questions, out-of-scope question, ambiguous question, one that needs the documents, one that needs the ML score) with reference answers, the agent run on it, an Evaluate Agent recipe writing to an evaluation store, and at least two evaluation runs so the store shows a trend.
3. **GenAI comparison** (item 13): the same test cases evaluated with at least two variants (two LLMs, two agent versions, or base vs fine-tuned model), compared side by side in the evaluation store comparison view.
4. **Trace Explorer** (item 14): agent responses stored with their full traces, and the Trace Explorer opened on them so the presenter can show tool calls, skill loads and blocks step by step.
5. **Agent Hub** (item 15): the agents (visual and structured) published in an Agent Hub webapp so business users can chat with them; the agent descriptions and starter questions are filled in.
6. **Fine-tuned LLM** (item 12): a small fine-tuning on a supervised dataset built in the flow (for example incident report → classification), trained, and then **used**: the fine-tuned model powers one step of the story (an LLM Request block of the structured agent, or the Prompt recipe) and is one of the variants of the GenAI comparison.

These items add objects, so the agentic flow may grow to about 30 objects; keep each extra object justified and grouped in the agent, fine-tuning and evaluation zones.

Docs are the source of truth for exact settings and current behaviour. Fetch the relevant page when you build that piece rather than trusting memory, because agent features evolve quickly. Prefer the headless plugin tools; fall back to dataiku-cli, the Python API client or Cobuild.

## Capability checklist

### 1. Simple visual agent (always)
An LLM-driven ReAct agent: it chooses tools and skills autonomously from instructions. Use it for the open-ended assistant the persona talks to (a maintenance copilot, an account assistant).
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-simple-visual-agents.html

### 2. Structured visual agent (include when the process has rules)
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

### 3. Code agent (include only if there is a reason)
A Python agent for logic the visual editor cannot express. In a visual-first demo it should be small and justified (for example one custom orchestration step). Skip it otherwise and say so.
Docs: https://doc.dataiku.com/dss/latest/agents/code-agents.html

### 4. Visual tools (the core; pick the ones that fit the use case)
Categories: query data (Dataset Lookup, SQL query, Knowledge Bank Search), perform actions (Dataset Append, Model Prediction, Send Message), orchestration (Query Another Agent or LLM), integration (Jira, Salesforce, Google search, MCP). Choose the tools a real user of this use case would need: for a maintenance copilot, a lookup on equipment and interventions, a model prediction tool on the failure model, an append tool to log a work order. Attach each with a clear name and description, since the LLM chooses tools from them.
Docs: https://doc.dataiku.com/dss/latest/agents/tools/index.html and https://knowledge.dataiku.com/latest/genai/agents/concept-agent-tool-overview.html

### 5. Code tool (include one if the use case has a calculation or rule that a visual tool cannot express)
A small custom Python tool kept inside the project (for example a domain formula). Keep it short and readable.
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-agent-tool-overview.html

### 6. Visual skill (always, at least one; often two or three)
Skills are reusable instructions the agent loads only when relevant, which keeps context focused and cheap. Each has a name, description, optional metadata, instructions and optional assets (templates, sub-tasks). Write skills as business procedures (for example "how to assess a risky asset and propose next actions", "how to write an account brief"), and let the structured agent or simple agent load them.
Docs: https://knowledge.dataiku.com/latest/genai/agents/concept-agent-skills.html

### 7. Semantic model (include when the agent answers analytical questions over tables)
Gives the agent business meaning for tables, columns, measures and relationships so that it queries data correctly. Build it on the project's main tables with business-friendly names, descriptions and a few key measures.
Docs: https://knowledge.dataiku.com/latest/genai/agents/semantic-models-lab/tutorial-index.html

### 8. Agent review (include; it is a strong governance story)
Define a handful of realistic test cases (single-turn with reference answers, and one multi-turn with a simulated user), set traits, run a review and show the pass/fail view. It requires the Advanced LLM Mesh add-on; if it is not available, say so and skip.
Docs: https://doc.dataiku.com/dss/latest/agents/agent-review.html and https://knowledge.dataiku.com/latest/genai/agents/semantic-models-lab/tutorial-index.html

### 9. Agent evaluation store (always, with several tests)
Build a test dataset of 8–12 realistic cases with reference answers, run the agent on it (Prompt recipe on the agent), evaluate with the Evaluate Agent recipe into an evaluation store, and run it at least twice so the store shows a history. Choose metrics the audience understands (answer correctness, faithfulness, tool usage).
Docs: https://doc.dataiku.com/dss/latest/agents/evaluation.html and https://knowledge.dataiku.com/latest/deploy/genai-monitoring/tutorial-agent-evaluation.html

### 10. RAG (include when the use case has documents)
The Prompt recipe with RAG is already a mandatory component (see `mandatory-components.md`, component 8); reuse its knowledge bank and extend it here for the agents. Documents such as procedures, manuals, incident reports or policies embedded into a knowledge bank, then searched by a Knowledge Bank Search tool. This is natural whenever the use case has procedures, policies or reports (maintenance procedures, warranty policies, quality manuals). The documents are synthetic text generated by the data script or a small companion script. This adds a managed folder and an Embed recipe; keep the total flow size in check.
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
Agentic demos tend to grow. Keep the flow readable by putting agent-related objects in their own flow zone, reusing the same few datasets as tools and knowledge, and cutting any capability that does not serve the story. Four datasets and one Postgres/Databricks table still hold.

## Agentic acceptance checklist
- [ ] Simple visual agent working with 2+ tools and 1+ skill
- [ ] Structured visual agent (or a justified reason it is skipped) with routing and a mandatory step
- [ ] Tools chosen for the use case, with names and descriptions the LLM can use
- [ ] At least one skill loaded on demand and visible in a test trace
- [ ] Semantic model, RAG, code tool, code agent: each present or justified as skipped
- [ ] Agent review with test cases and a run (or noted unavailable)
- [ ] Prompt Studio prompt with at least two variants compared, deployed as a Prompt recipe with RAG whose output is used downstream
- [ ] Agent evaluation store with 8–12 test cases and at least two evaluation runs
- [ ] GenAI comparison of at least two variants (including the fine-tuned model) open in the evaluation store
- [ ] Trace Explorer opened on stored agent traces
- [ ] Visual and structured agents published in Agent Hub with descriptions and starter questions
- [ ] Fine-tuned LLM trained and used by the structured agent or the Prompt recipe
- [ ] Webapp offers a way to talk to the agent or to act on its output
- [ ] Wiki demo script walks through: ask, tool call, skill load, governed process, trace, evaluation and comparison, review
