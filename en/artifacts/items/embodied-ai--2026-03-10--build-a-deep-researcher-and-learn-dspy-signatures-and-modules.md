---
source: hn
url: https://www.cmpnd.ai/blog/learn-dspy-deep-research.html
published_at: '2026-03-10T23:25:11'
authors:
- dbreunig
topics:
- dspy
- research-agent
- react
- tool-using-llm
- workflow-decomposition
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Build a deep researcher and learn DSPy Signatures and Modules

## Summary
This is a hands-on technical article demonstrating how to use DSPy to build a “deep research” agent from scratch, and progressively expand a simple single-step Q&A system into a multi-stage system with retrieval, clarification, planning, and synthesis. Its core value is not proposing a new algorithm, but using Signatures and Modules to show how to prototype faster, control behavior more easily, and improve reliability.

## Problem
- The article aims to solve this: how to turn a large-model-dependent “deep research agent” from a simple prompt call into a usable, scalable, and maintainable research system.
- This matters because monolithic long-context agents are prone to context bloat, poor citation management, missing subtopics, unauditable sources, and difficulty controlling cost and latency.
- For developers, there are also engineering challenges: manually writing prompts, parsing outputs, connecting tools, and doing evaluation and optimization are all fragile and slow to iterate.

## Approach
- Use a DSPy **Signature** to first declare “what the input is and what the output is,” for example `research_request -> report`, separating the task objective from the specific prompt wording.
- Use a DSPy **Module** to execute those declarations: first use `Predict` for a minimum viable version, then use `ReAct` to let the model call web search and webpage reading tools, creating a research agent with external knowledge.
- Add a clarification step: first generate clarifying questions, then pass the user’s answers as additional input to the research agent to reduce misunderstanding of user intent.
- Further decompose the workflow into a multi-step program, such as clarification, planning, source gathering, webpage processing, synthesis writing, and annotation, in exchange for better budget control, evaluation, parallelization, model routing, and auditability.
- Emphasize that DSPy’s mechanism is to “declare the what, not hand-write the how”: use field names, types, docstrings, field descriptions, and module composition to constrain LLM behavior, rather than manually maintaining fragile prompts.

## Results
- The article does not provide standard academic experiments, benchmark datasets, or quantitative metrics, so there are **no reportable quantitative results**.
- The most concrete engineering result given is that after adding web tools, the reports are “more detailed, usually more accurate, and more up to date,” but no numbers are provided for accuracy, citation quality, or task success rate.
- After adding clarifying questions, the author claims the system is “less likely to misunderstand user intent and more likely to focus on what the user cares about”; implementing this version took “fewer than 50 lines of code (including comments).”
- The article shows a minimal example: the `Predict` version relies only on model parameters; the `ReAct + internet_search + read_webpage` version can perform multi-round tool calls and ultimately synthesize a report.
- For the benefits of the decomposed architecture, the article offers qualitative claims: you can set the number of subtopics, the number of URLs per subtopic, and the maximum number of searches; you can parallelize Gatherer/Processor; you can write evals by step; and you can trace facts back to URL sources, but no quantitative comparisons are provided.

## Link
- [https://www.cmpnd.ai/blog/learn-dspy-deep-research.html](https://www.cmpnd.ai/blog/learn-dspy-deep-research.html)
