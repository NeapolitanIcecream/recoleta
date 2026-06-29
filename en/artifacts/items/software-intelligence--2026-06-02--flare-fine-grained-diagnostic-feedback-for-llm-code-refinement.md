---
source: arxiv
url: https://arxiv.org/abs/2606.03852v1
published_at: '2026-06-02T16:29:17'
authors:
- Yinsheng Yao
- Hongxiang Zhang
- Weixi Tong
- Tianyi Zhang
topics:
- code-intelligence
- llm-code-repair
- fault-localization
- iterative-refinement
- automated-software-production
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement

## Summary
FLARE improves iterative LLM code repair by adding line-level bug localization to execution feedback. It uses a small diagnostic model and top-k candidate search to guide refinements toward likely faulty lines.

## Problem
- LLMs often generate code that fails tests, and iterative repair is needed for code generation systems that users can trust.
- Test failures usually describe the failing behavior without naming the faulty line.
- Self-critiques and natural-language debugging can give broad advice that does not tell the model where to edit.

## Approach
- FLARE trains a 6-layer, 8-head bidirectional transformer diagnostic model on 10,504 Collu-Bench buggy code solutions with ground-truth bug locations.
- It aligns generator LLM subword probabilities to code lexical units such as identifiers, operators, and keywords.
- The diagnostic model combines lexical-unit text embeddings, syntactic token types, and aligned token probabilities, then scores each lexical unit for suspiciousness.
- It converts lexical scores to line scores with max pooling and sends the ranked suspicious line, the current program, and execution feedback to the refinement prompt.
- At each iteration, it searches over the top-k suspicious lines, generates one candidate revision per line, runs public tests, and keeps a passing candidate or the candidate that passes the most tests.

## Results
- On LiveCodeBench, FLARE with k=10 reaches Pass@1 scores of 46.86, 44.57, 33.71, 76.57, and 65.14 across the five base LLMs; the corresponding LLM-alone scores are 30.86, 26.86, 20.57, 46.86, and 44.00.
- On BigCodeBench, FLARE with k=10 reaches Pass@1 scores of 64.47, 55.79, 45.61, 72.81, and 69.65; NL-Debugging scores 55.00, 47.02, 40.35, 58.33, and 56.67.
- With k=1, FLARE beats NL-Debugging in 9 of 10 settings. The visible table shows gains over NL-Debugging from 0.18 to 7.42 percentage points in those 9 settings.
- Candidate search adds 8.50 percentage points on average over k=1. The reported gains are 4.57 to 12.00 points on LiveCodeBench and 5.08 to 13.42 points on BigCodeBench.
- The diagnostic model alone reaches 67% Top-1, 75% Top-3, and 89% Top-10 localization accuracy on 100 LiveCodeBench tasks, compared with LLMAO at 63%, 74%, and 87%.
- On GPT-4o-mini, full FLARE with k=10 reaches 65.14% Pass@1 on LiveCodeBench and 69.65% on BigCodeBench; execution-only feedback reaches 58.29% and 59.47%, while diagnostic-only feedback reaches 55.43% and 58.42%. Runtime is 73.76 seconds/task for k=1 and 610.19 seconds/task for k=10 on LiveCodeBench.

## Link
- [https://arxiv.org/abs/2606.03852v1](https://arxiv.org/abs/2606.03852v1)
