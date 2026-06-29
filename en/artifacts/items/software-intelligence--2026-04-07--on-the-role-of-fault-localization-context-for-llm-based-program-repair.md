---
source: arxiv
url: http://arxiv.org/abs/2604.05481v1
published_at: '2026-04-07T06:21:55'
authors:
- Melika Sepidband
- Hung Viet Pham
- Hadi Hemmati
topics:
- program-repair
- fault-localization
- llm-code
- swe-bench
- empirical-study
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# On the Role of Fault Localization Context for LLM-Based Program Repair

## Summary
This paper studies how much fault-localization context helps LLM-based program repair. On 500 SWE-bench Verified tasks with GPT-5-mini, file-level context matters most, broader context helps only in some places, and extra line-level context often hurts.

## Problem
- LLM-based program repair still depends on fault localization, but prior work did not test how file-, element-, and line-level context affect repair success.
- More context can help the model understand a bug, but it can also add irrelevant code, raise token cost, and hide the real edit location.
- This matters for APR system design because localization drives both repair quality and inference cost on large repositories.

## Approach
- The authors run a factorial study over **61 fault-localization configurations** on **500 SWE-bench Verified** instances using **GPT-5-mini**.
- They vary context at three levels: **files** (none, buggy files, rule-based related files, LLM-retrieved files), **elements** (none, buggy elements, call-graph elements, LLM-retrieved elements), and **lines** (none, buggy lines, ±10-line windows, static slicing, LLM-retrieved lines).
- To isolate the effect of context quality, they use **ground-truth patch locations** to define the buggy files, elements, and lines, then test whether expanding beyond those locations helps.
- They compare semantic LLM retrieval against structural heuristics, and they also measure context size and token cost.

## Results
- **File-level context is the main driver**: adding file context gives a **15–17× improvement over the no-file baseline**.
- Successful repairs appear most often when the prompt includes about **6–10 relevant files**.
- **LLM-based file retrieval** beats rule-based file expansion in most settings and uses less context: **8.54 files / 58,273 tokens on average** for LLM retrieval versus **18.12 files / 96,237 tokens** for rule-based retrieval.
- Ground-truth buggy files average **1.25 files** and about **12,131 tokens** per instance.
- **Element-level context** helps over having no element information, but gains beyond buggy elements depend on file-context quality; **LLM-retrieved elements** do better than **call-graph elements** in most configurations.
- **Line-level expansion often hurts**: context windows and static slicing frequently reduce repair performance, while precise **buggy lines** work better; the excerpt does not report full repair-rate percentages for all 61 configurations.

## Link
- [http://arxiv.org/abs/2604.05481v1](http://arxiv.org/abs/2604.05481v1)
