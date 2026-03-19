---
source: hn
url: https://www.cmpnd.ai/blog/learn-dspy-deep-research.html
published_at: '2026-03-10T23:25:11'
authors:
- dbreunig
topics:
- dspy
- deep-research-agent
- llm-orchestration
- tool-use
- agent-workflow
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Build a deep researcher and learn DSPy Signatures and Modules

## Summary
This is an instructional article showing how to use DSPy to build a "deep research" agent from scratch, and gradually evolve a simple single-step call into a more reliable, controllable multi-stage research pipeline. Its core value is not proposing a new algorithm, but using DSPy's Signature and Module mechanisms to explain how to prototype, compose, and constrain LLM agents more quickly.

## Problem
- The article addresses the problem of how to build a deep research agent that can perform web search, clarify requirements, aggregate sources, and produce a research report, and how to make such an agent more reliable than a "single prompt + single model response" setup.
- This matters because real research agents often encounter engineering issues such as context bloat, messy citations, missing subtopics the user cares about, unauditable factual sources, and uncontrollable cost and latency.
- For product-oriented AI software development, the author emphasizes that long context windows and strong models alone are not enough; structured workflows that can be decomposed, evaluated, and optimized are needed.

## Approach
- Use a DSPy Signature to declare the task's inputs and outputs, for example `research_request: str -> report: str`, separating "what we want" from "how to do it," and letting the model infer the goal from field names, types, and docstrings.
- Use DSPy Modules to execute the task: the basic version uses `Predict` to turn the Signature into a prompt and extract structured output; the enhanced version uses `ReAct`, combined with the `internet_search` and `read_webpage` tools, to perform web research via "reasoning + tool use."
- Add a clarification step before research: first use a separate Signature/Module to generate clarification questions, then collect the user's answers and use the Q&A pairs as new input to the researcher, reducing misunderstandings of user intent.
- Break the large task into a multi-program pipeline, such as clarification, planning, source gathering, webpage processing, synthesis writing, and source annotation, in exchange for engineering benefits such as budget control, parallelization, auditability, easier evaluation, and easier optimization.
- The article also emphasizes using type constraints (such as `list[str]` and fixed-length `tuple`) and class-based Signature docstrings/field descriptions to guide model behavior more robustly and reduce brittle handwritten prompting and output parsing.

## Results
- The article shows that a minimal research agent can work with **2 lines of core code**: define a Signature and execute it with `dspy.Predict`; after adding tools, it becomes an internet-connected deep research agent.
- The version with clarification questions reportedly requires **fewer than 50 lines of code (including comments)**, while allowing the agent to ask the user questions before conducting research, making it "less likely to misunderstand intent and more likely to focus on what the user cares about."
- The article explicitly notes that if a fixed number of clarification questions is needed, `tuple[str, str, str]` can be used to generate **3** questions; alternatively, the number of questions can be controlled by using an `int` input parameter.
- For tool-based research, the author claims that after adding `ReAct` plus web search/reading, reports become "**more detailed**," often also "**more accurate**," and "**more timely**," but provides no standard dataset, evaluation metrics, or quantitative comparison against baselines.
- For the decomposed architecture, the article proposes configurable controls such as the **maximum number of subtopics, number of URLs per subtopic, and maximum number of searches**, and supports using different models at different stages and parallel calls for Gatherer/Processor, but these benefits are presented as design claims and **no experimental numbers are provided**.
- Overall, the article **does not provide formal quantitative experimental results**; its strongest concrete conclusion is that DSPy's Signature + Module + decomposed workflow can evolve a monolithic research agent into a research system that is more reliable, controllable, evaluable, and auditable.

## Link
- [https://www.cmpnd.ai/blog/learn-dspy-deep-research.html](https://www.cmpnd.ai/blog/learn-dspy-deep-research.html)
