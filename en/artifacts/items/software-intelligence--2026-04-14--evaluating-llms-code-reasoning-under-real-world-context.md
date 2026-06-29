---
source: arxiv
url: http://arxiv.org/abs/2604.12881v1
published_at: '2026-04-14T15:32:07'
authors:
- Changshu Liu
topics:
- code-reasoning
- benchmarking
- software-evaluation
- python-repositories
- llm-for-code
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Evaluating LLMs Code Reasoning Under Real-World Context

## Summary
R²Eval is a code reasoning benchmark built from real Python projects rather than short standalone snippets. It tests whether LLMs can predict program inputs and outputs when code depends on real repository context and complex data types.

## Problem
- Existing code reasoning benchmarks mostly use short generated snippets or programming-challenge solutions, so they miss real repository structure, dependencies, and object-heavy data.
- Many prior benchmarks restrict inputs and outputs to primitive types, which removes a common source of difficulty in production code.
- This matters because strong scores on simplified benchmarks can overstate how well LLMs will do on software tasks such as program repair, translation, and generation inside real projects.

## Approach
- The paper introduces **R²Eval**, a benchmark of **135** code reasoning problems collected from **10** popular Python projects: scikit-learn, django, requests, seaborn, sphinx, pytest, astropy, xarray, matplotlib, and sympy.
- Each problem is a triplet **(P, I, O)**: code with relevant method, dependency, and class context; serialized input; and serialized output.
- The main mechanism is program analysis that breaks complex, compound, and custom runtime objects into JSON-serializable parts, so models can see realistic inputs and outputs instead of only primitive values.
- To score predictions, the benchmark deserializes model outputs back into objects and checks correctness by running tests, which avoids false negatives from plain string matching.
- The evaluation compares R²Eval against a size-matched **135-problem** sample from CRUXEval on six LLMs using both input-prediction and output-prediction tasks.

## Results
- Across all six models, average accuracy drops from **81.23% to 16.91%** on **input prediction** when moving from CRUXEval to R²Eval, a **64.32 point** drop.
- Across all six models, average accuracy drops from **80.37% to 28.15%** on **output prediction**, a **52.22 point** drop.
- **o4-mini** falls from **92.59% to 20.00%** on input prediction and from **91.85% to 28.15%** on output prediction.
- **Gemini-2.5-Pro** falls from **91.85% to 15.56%** on input prediction and from **88.89% to 34.07%** on output prediction.
- **DeepSeek-R1** falls from **94.81% to 21.48%** on input prediction and from **87.41% to 31.85%** on output prediction.
- Reasoning-focused models outperform non-reasoning models by an average of **13.95 points** on input prediction and **12.22 points** on output prediction, but all models degrade sharply on the more realistic benchmark.

## Link
- [http://arxiv.org/abs/2604.12881v1](http://arxiv.org/abs/2604.12881v1)
