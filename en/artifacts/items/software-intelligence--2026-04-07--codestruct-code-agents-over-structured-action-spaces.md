---
source: arxiv
url: http://arxiv.org/abs/2604.05407v3
published_at: '2026-04-07T03:58:10'
authors:
- Myeongsoo Kim
- Joe Hsu
- Dingmin Wang
- Shweta Garg
- Varun Kumar
- Murali Krishna Ramanathan
topics:
- code-agents
- ast-based-editing
- software-engineering-benchmarks
- code-intelligence
- llm-tool-use
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# CODESTRUCT: Code Agents over Structured Action Spaces

## Summary
CodeStruct changes how code agents interact with repositories: instead of reading and editing raw text spans, they act on named AST entities such as functions, classes, and methods. This reduces brittle string-match failures and improves both task success and token efficiency on software engineering benchmarks.

## Problem
- Current LLM code agents treat repositories as flat text, so they read whole files or line ranges and edit code with string replacement.
- Text-based edits fail when formatting changes, target strings appear multiple times, or the model must reproduce unchanged code exactly; these failures matter because they waste calls, tokens, and patch attempts on repository-level bug fixing.
- Existing aids such as repo maps or symbol indices help agents find code, but the actual read and edit actions still use text and keep the same failure modes.

## Approach
- CodeStruct exposes the repository as a structured action space built from the abstract syntax tree (AST), where code elements have stable names like `file.py::ClassName::method`.
- It adds `readCode`, which returns complete syntactic units or structural summaries instead of arbitrary text slices. For large files, the agent can first read signatures, then request a specific function or method by selector.
- It adds `editCode`, which applies AST-level insert, replace, or removal operations to a selected entity. The tool preserves indentation and rejects edits that produce syntax errors.
- This means the agent states the target entity and the intended change, while the tool handles the source-text realization. The paper says this removes dependence on line numbers and exact string matches.
- The interface is exposed through MCP, so the authors can plug it into existing SWE-Agent-style workflows without changing the planner.

## Results
- On **SWE-Bench Verified** across six models, CodeStruct improves **Pass@1 by 1.2 to 5.0 points for frontier models**, with gains including **GPT-5: 66.0 -> 67.2 (+1.2)**, **GPT-5-mini: 60.4 -> 62.0 (+1.6)**, **Qwen3-Coder: 61.2 -> 66.2 (+5.0)**, and **Qwen3-32B: 14.8 -> 16.0 (+1.2)**.
- The largest SWE-Bench gain is for **GPT-5-nano: 19.6 -> 40.4 (+20.8 points)**. The abstract attributes this to fewer invalid or empty patches, with **empty-patch failures dropping from 46.6% to 7.2%**.
- SWE-Bench efficiency usually improves at the same time: **input tokens drop by 12% to 38% for most models**. Examples: **GPT-5 -19.1% cost**, **GPT-5-mini -32.6% cost**, **Qwen3-32B -17.4% cost**. One exception is **GPT-5-nano**, where accuracy rises but **cost increases by 40.8%**.
- On **CodeAssistBench**, accuracy improves for all tested models by **0.8 to 4.4 points**: **GPT-5 53.3 -> 54.1 (+0.8)**, **GPT-5-mini 51.1 -> 51.9 (+0.8)**, **GPT-5-nano 46.7 -> 48.1 (+1.4)**, **Qwen3-Coder 31.1 -> 31.9 (+0.8)**, **Qwen3-32B 15.6 -> 20.0 (+4.4)**, **Qwen3-8B 13.3 -> 14.1 (+0.8)**.
- CodeAssistBench costs also often fall, with examples including **GPT-5 -14.5%**, **GPT-5-mini -33.3%**, and **Qwen3-8B -17.6%**. A notable exception is **Qwen3-32B**, where accuracy improves by **4.4 points** but **cost rises by 23.7%**.
- The core claim is that structure-aware read and edit primitives give code agents a more reliable interface than text-based tools, especially for models whose main bottleneck is patch-format failure rather than reasoning.

## Link
- [http://arxiv.org/abs/2604.05407v3](http://arxiv.org/abs/2604.05407v3)
