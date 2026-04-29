---
source: arxiv
url: http://arxiv.org/abs/2604.18834v1
published_at: '2026-04-20T20:58:52'
authors:
- Dinithi Jayasuriya
- Aravind Saravanan
- Nilesh Ahuja
- Amanda Rios
- Amit Trivedi
topics:
- eda-code-generation
- structural-verification
- openroad
- code-intelligence
- tool-use
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging

## Summary
This paper argues that many LLM failures in OpenROAD script generation come from broken object and API dependencies, not syntax. It introduces pre-execution structural verification so the system can catch and repair those failures before running the EDA tool, which raises pass rate and cuts tool calls.

## Problem
- The paper targets natural-language-to-EDA code generation for OpenROAD, where generated scripts often fail because they follow invalid design-object paths, skip required intermediate objects, or call APIs on the wrong types.
- This matters because tool-in-the-loop debugging fixes errors by repeated execution and repair, which adds latency, increases tool usage, and scales poorly on multi-step workflows where early errors propagate.
- In EDA, execution depends on stateful design hierarchies and action preconditions, so syntax checks alone miss many real failures.

## Approach
- The method converts each task into a **structural dependency graph** whose nodes are typed design objects, conditions, and actions, and whose edges encode valid acquisition and dependency relations. The graph acts as an execution contract.
- It builds and validates that graph from the prompt against an OpenROAD API schema, filtering hallucinated nodes, invalid type transitions, and missing prerequisites before code synthesis.
- Retrieval and code generation are conditioned on the graph, so the model fetches API examples for specific object transitions and generates code that follows the required dependency path.
- A four-layer verifier checks syntax, causal flow, API alignment, and task-level semantics, then applies diagnosis-driven localized repair instead of full reruns in the external tool.
- For multi-step tasks, it runs the same process per subtask and adds trajectory-level reflection to diagnose cross-step failures; an uncertainty filter scores verifier-passed programs to reduce false accepts before execution.

## Results
- On **single-step** OpenROAD tasks, the full system reaches **82.5% pass rate**, above **73.0%** for **LLM+RAG** and **76.0%** for **LLM + tool-in-loop** with GPT-4.1-mini.
- On the same single-step setting, the method uses **1.00 tool calls per task** versus **1.77** for tool-in-loop and **3.54** for OpenROAD-Agent, with **120 total calls** versus **248** and **496**. The abstract states this is **more than 2× fewer** tool calls than tool-in-loop debugging.
- Single-step latency in Table 1 is **34.8 s** for the full pipeline, compared with **53.0 s** for tool-in-loop and **70.0 s** for OpenROAD-Agent; Table 2 reports **37.6 s** for GPT-4.1-mini tool-in-loop and **34.8 s** for the proposed method.
- On **multi-step** tasks, the abstract reports pass rate improving from **30.0% to 70.0%**, and then to **84.0%** when adding **trajectory-level reflection**.
- Uncertainty-aware filtering cuts verifier false positives from **20.0% to 6.7%** and raises precision from **80.0% to 93.3%**.
- Across generators, the full method reports **83.0%** pass with **GPT-4o** and **82.5%** with **GPT-4.1-mini**; a verifier added to OpenROAD-Agent raises it from **16.4% to 31.8%** while keeping **1.00** tool call per task.

## Link
- [http://arxiv.org/abs/2604.18834v1](http://arxiv.org/abs/2604.18834v1)
