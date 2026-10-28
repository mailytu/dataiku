# Angle: agentic

Use when the user wants the demo to put agents at the centre. The five mandatory components still apply; this file raises the bar on the agent side so the demo showcases the breadth of Dataiku's agentic capabilities in a way that serves the use case. Pick the capabilities that make the story better; do not add one only to tick a box, but every item below must either be present or explicitly justified as skipped in the final message.

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

### 9. Agent evaluation (include when the user wants quality over time)
Evaluate agent runs with the evaluation tooling and show the results in the flow or an evaluation store.
Docs: https://doc.dataiku.com/dss/latest/agents/evaluation.html and https://knowledge.dataiku.com/latest/deploy/genai-monitoring/tutorial-agent-evaluation.html

### 10. RAG (include when the use case has documents)
The Prompt recipe with RAG is already a mandatory component (see `mandatory-components.md`, component 8); reuse its knowledge bank and extend it here for the agents. Documents such as procedures, manuals, incident reports or policies embedded into a knowledge bank, then searched by a Knowledge Bank Search tool. This is natural whenever the use case has procedures, policies or reports (maintenance procedures, warranty policies, quality manuals). The documents are synthetic text generated by the data script or a small companion script. This adds a managed folder and an Embed recipe; keep the total flow size in check.
Docs: https://knowledge.dataiku.com/latest/genai/rag/concept-rag.html

### 11. Prompt Studio (already covered by mandatory component 8; extend or add a second prompt if the story needs it)
A Prompt recipe to classify, extract or summarise text at scale (for example classify incident reports), developed and compared in Prompt Studio.
Docs: https://knowledge.dataiku.com/latest/genai/text-processing/concept-prompt-studio.html

### 12. Fine-tuned LLM (rarely)
Mention or build only if the user asks. It is heavy and rarely helps a short demo.
Docs: https://doc.dataiku.com/dss/latest/generative-ai/fine-tuning.html

## Fit with the flow-size rule
Agentic demos tend to grow. Keep the flow readable by putting agent-related objects in their own flow zone, reusing the same few datasets as tools and knowledge, and cutting any capability that does not serve the story. Four datasets and one Postgres/Databricks table still hold.

## Agentic acceptance checklist
- [ ] Simple visual agent working with 2+ tools and 1+ skill
- [ ] Structured visual agent (or a justified reason it is skipped) with routing and a mandatory step
- [ ] Tools chosen for the use case, with names and descriptions the LLM can use
- [ ] At least one skill loaded on demand and visible in a test trace
- [ ] Semantic model, RAG, code tool, code agent: each present or justified as skipped
- [ ] Agent review with test cases and a run (or noted unavailable)
- [ ] Agent evaluation set up if requested
- [ ] Webapp offers a way to talk to the agent or to act on its output
- [ ] Wiki demo script walks through: ask, tool call, skill load, governed process, review
