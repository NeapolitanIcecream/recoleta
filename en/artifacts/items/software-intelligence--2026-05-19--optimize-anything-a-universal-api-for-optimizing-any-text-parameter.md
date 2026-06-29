---
source: arxiv
url: https://arxiv.org/abs/2605.19633v1
published_at: '2026-05-19T10:18:12'
authors:
- Lakshya A Agrawal
- Donghyun Lee
- Shangyin Tan
- Wenjie Ma
- Karim Elmaaroufi
- Rohit Sandadi
- Sanjit A. Seshia
- Koushik Sen
- Dan Klein
- Ion Stoica
- Joseph E. Gonzalez
- Omar Khattab
- Alexandros G. Dimakis
- Matei Zaharia
topics:
- llm-optimization
- code-intelligence
- agent-architecture-search
- prompt-optimization
- multi-task-search
- automated-software-production
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# optimize_anything: A Universal API for Optimizing any Text Parameter

## Summary
optimize_anything turns many optimization tasks into the same loop: edit a text artifact, score it, feed diagnostic feedback to an LLM, and try a better artifact. The paper claims one API works for prompts, code, agents, scheduling policies, CUDA kernels, circle packing, images, and numerical solvers.

## Problem
- LLM optimization tools are usually tied to one artifact type, such as code, prompts, or agent graphs, so users need different systems for related search problems.
- Many evaluators produce useful diagnostics such as stack traces, profiler data, traces, cost breakdowns, or images, but prior tools expose this feedback through task-specific plumbing.
- A shared optimizer matters because software and engineering work often reduces to improving a serializable artifact against an automated test or score.

## Approach
- The user supplies a seed string or a natural-language goal, an evaluator, optional train/validation data, and optional background knowledge.
- The evaluator returns a scalar score plus a side_info dictionary with diagnostics; an LLM proposer reads that feedback and writes a revised candidate.
- The default backend extends GEPA-style Pareto search to arbitrary text artifacts, preserving candidates that are best on some example, task, or metric instead of only the best average score.
- It supports single-task search, multi-task search over related tasks, and generalization to held-out examples under the same API.
- Engineering pieces include a refiner for malformed generations, content-addressed evaluation caching, typed side information, image feedback, and backend adapters.

## Results
- ARC-AGI agent architecture search: Gemini Flash accuracy rises from 32.5% to 89.5%, a +57 point gain.
- Cloud scheduling: CloudCast cuts cost by 40.2% versus Dijkstra routing; Can’t Be Late cuts cost by 7.8%; ADRS aggregate score is 96.6 versus 92.9 for OpenEvolve and 72.0 for ShinkaEvolve.
- CUDA KernelBench: 87% of generated kernels match or beat PyTorch baselines, and the paper claims multi-task search beats matched-budget single-task runs.
- Prompt optimization: GPT-4.1-mini AIME-2025 accuracy improves from 46.67% to 60.00%, a +13.33 point gain.
- Coding agent skills on Bleve: Haiku 4.5 pass rate improves from 79.3% to 98.3%; Sonnet 4.5 improves from 94.8% to 100%; resolution time drops by 47%.
- Ablations report actionable side information gives 4–6x faster convergence and higher final scores than score-only feedback; circle packing beats AlphaEvolve for n=26, and math optimization wins 7/10 against Optuna in appendix claims.

## Link
- [https://arxiv.org/abs/2605.19633v1](https://arxiv.org/abs/2605.19633v1)
