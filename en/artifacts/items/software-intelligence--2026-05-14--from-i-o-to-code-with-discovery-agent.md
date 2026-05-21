---
source: arxiv
url: https://arxiv.org/abs/2605.15334v1
published_at: '2026-05-14T18:57:32'
authors:
- Yihong Dong
- Jiaru Qian
- Haoran Zhang
- Peixu Wang
- Binhua Li
- Zhi Jin
- Yongbin Li
- Ge Li
- Xiaokang Yang
- Xue Jiang
topics:
- code-generation
- program-synthesis
- io2code
- llm-agents
- evolutionary-search
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# From I/O to Code with Discovery Agent

## Summary
DIO-Agent synthesizes code from input-output examples when no natural-language spec is available. It treats program induction as an LLM-guided evolutionary search, with execution errors and a simple-to-complex mutation order steering each edit.

## Problem
- IO2Code asks a model to infer a general program from visible input-output pairs and pass held-out tests.
- This matters for black-box API reverse engineering, legacy migration, scientific rule induction, and user intent capture through examples.
- Finite examples under-specify the target rule, so models can pass visible cases with lookup tables or overfit through case-specific logic.

## Approach
- The paper introduces DIO-Agent and IO2CodeBench, a benchmark with Base, Algorithm, Geometry, and Multimodal levels.
- DIO-Agent runs an island-based evolutionary loop: pick parent programs, ask an LLM for SEARCH/REPLACE code diffs, execute the child, score it, and keep useful variants.
- A curriculum reveals easier examples first, then adds harder cases while replaying earlier examples to avoid regressions.
- The Transformation Priority Premise guides edits in a simple-to-complex order: constants, variables, multiple statements, conditionals, arrays, loops, and functions.
- Error-grounded feedback gives the LLM concrete failing inputs, wrong outputs, runtime errors, and a score that penalizes code complexity and memorized examples.

## Results
- On IO2CodeBench with DeepSeek V3.2, DIO-Agent reaches 58.63 average pass rate, above CodeEvolve at 49.60, AlphaEvolve at 47.29, FunSearch at 45.01, E-PBE at 38.63, Direct at 32.18, and PBE at 14.58.
- By level, DIO-Agent scores 61.29 on Base, 71.43 on Algorithm, 61.11 on Geometry, and 40.67 on Multimodal.
- Against CodeEvolve, DIO-Agent improves Algorithm from 60.00 to 71.43, Geometry from 44.44 to 61.11, and Multimodal from 32.67 to 40.67, while using 3738.31 tokens per iteration versus 5829.32.
- Across base LLMs, DIO-Agent averages 58.63 with DeepSeek V3.2, 55.45 with Qwen-3.6-Plus, and 57.31 with Claude-Sonnet-4.6.
- Ablations lower average performance from 58.63 to 54.61 without error feedback, 53.80 without TPP, and 51.33 without curriculum evolution.
- With a matched 40-candidate budget, DIO-Agent scores 63.66 average pass rate, above Best-of-N at 40.28, Self-Consistency at 25.53, and Direct at 14.56.

## Link
- [https://arxiv.org/abs/2605.15334v1](https://arxiv.org/abs/2605.15334v1)
