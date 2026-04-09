---
source: arxiv
url: http://arxiv.org/abs/2604.04979v1
published_at: '2026-04-04T18:52:44'
authors:
- "\xC1d\xE1m Kov\xE1cs"
topics:
- coding-agents
- context-pruning
- tool-output-extraction
- code-intelligence
- swe-bench
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents

## Summary
Squeez targets a narrow but useful coding-agent task: given a query and one tool output, keep only the smallest verbatim block that matters for the next step. The paper releases a benchmark for this task and shows that a LoRA-tuned Qwen 3.5 2B model beats larger zero-shot models and simple pruning heuristics.

## Problem
- Coding agents repeatedly reread long tool outputs such as file reads, logs, stack traces, grep hits, and git history, even though only a small part matters for the next action.
- This wastes context and compute inside agent loops, especially for software debugging and repository work where relevant evidence may sit anywhere in the output.
- The paper focuses on single-observation pruning: extract the smallest verbatim evidence block for a focused query, so the agent keeps useful lines and drops the rest.

## Approach
- The authors define **task-conditioned tool-output pruning**: input is a short query plus one raw tool observation; output is one or more contiguous spans from the original text.
- They build a dataset of **11,477 examples** across **27 tool types**, combining **9,205 SWE-bench-derived** examples, **1,697 synthetic positives**, and **575 synthetic negatives**; the test set has **618 manually reviewed examples**.
- Labels are created with a two-stage teacher pipeline using **openai/gpt-oss-120b**, which writes a focused extraction query and selects the smallest supporting spans; released labels map back to raw text so targets stay verbatim.
- The model is **Qwen 3.5 2B** fine-tuned with **LoRA** to output extracted text inside `<relevant_lines>` tags. Evaluation uses line-level **recall**, **F1**, **exact match**, and **compression**.
- Baselines include zero-shot **Qwen 3.5 35B A3B**, **Kimi K2**, unfine-tuned **Qwen 3.5 2B**, and heuristic methods **BM25**, **First-N**, **Last-N**, and **Random**.

## Results
- On the **618-example** held-out test set, **Squeez-2B** reaches **0.86 recall**, **0.80 precision**, **0.80 F1**, **0.79 strict F1**, **0.49 exact match**, and **0.92 compression**, which means it removes **92%** of input tokens.
- Against the main zero-shot large-model baseline, **Qwen 3.5 35B A3B**, Squeez-2B improves **recall from 0.75 to 0.86** and **F1 from 0.73 to 0.80** at the same **0.92 compression**.
- Against the unfine-tuned **Qwen 3.5 2B** base model, Squeez-2B improves **recall from 0.53 to 0.86** and **F1 from 0.55 to 0.80**.
- Heuristic pruning is much weaker: **BM25** gets **0.22 recall** and **0.23 F1** at **0.90 compression**; **First-N** gets **0.14 recall**; **Last-N** gets **0.05 recall**.
- On **59 negative test examples**, Squeez-2B returns empty output **80%** of the time, versus **7%** for **Qwen 35B**, which shows better handling of cases where no relevant evidence exists.
- The paper does not report end-to-end agent task-completion gains, so the main claimed breakthrough is strong evidence preservation under heavy compression on a new benchmark for coding-agent tool outputs.

## Link
- [http://arxiv.org/abs/2604.04979v1](http://arxiv.org/abs/2604.04979v1)
