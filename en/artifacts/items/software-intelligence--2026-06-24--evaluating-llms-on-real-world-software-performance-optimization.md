---
source: arxiv
url: https://arxiv.org/abs/2606.25530v1
published_at: '2026-06-24T08:07:41'
authors:
- "Ezgi Sar\u0131kayak"
- Wenchao Gu
- Hesham Ghonim
- Chunyang Chen
topics:
- llm-code-optimization
- software-benchmarking
- repository-level-code
- performance-engineering
- memory-profiling
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Evaluating LLMs on Real-World Software Performance Optimization

## Summary
SWE-Pro is a repository-level benchmark for testing whether LLMs can optimize real Python code for runtime and memory. The paper finds that current LLMs often apply patches and sometimes pass tests, but they rarely deliver measured performance gains.

## Problem
- Existing LLM code-optimization benchmarks often test isolated functions, one workload, or runtime only, so they miss repository dependencies, input sensitivity, memory cost, and measurement noise.
- This matters because generated code can add performance debt: slower execution, higher memory use, and higher compute cost in real software systems.
- Performance optimization needs more than passing unit tests; a patch must preserve behavior and improve resource use across workloads with enough signal to beat noise.

## Approach
- The authors build SWE-Pro from 102 expert-written optimization pull requests in `pandas`, `scikit-learn`, and `xarray`.
- Each task gives the model a real repository state, correctness tests, and parameterized performance tests that vary input size, data properties, and execution options.
- The benchmark measures runtime, peak memory, and Time-Weighted Memory Usage (TWMU), which captures sustained memory pressure over time.
- Measurements run in fresh Docker containers with calibration, warmup, adaptive sampling, and Signal-to-Noise Ratio filtering; only effects with SNR above 2 are counted.
- The evaluation tests six LLMs under oracle context and BM25 retrieval: GPT-5.2, Claude Sonnet 4.6, Kimi K2.5, Gemini 3.1 Flash-Lite, GLM-5.1, and MiniMax M2.7.

## Results
- Expert gold patches achieve 15.48× runtime speedup, 171.31× peak memory reduction, and 619.22× TWMU reduction on average.
- Gold patches show reproducible runtime improvements on 91.2% of tasks, peak memory gains on 65.7%, and TWMU gains on 52.0%; another dataset validation view reports detectable runtime effects on 93.1%, peak memory on 70.6%, and TWMU on 55.9%.
- Under oracle context, LLM patch application rates range from 30.4% to 97.1%, while correctness rates range from 18.6% to 79.4%, so many applicable patches still break behavior.
- Under oracle context, Gemini 3.1 Flash has the highest detectable runtime pass rate at 12.7% with 1.27× IF; Claude Sonnet 4.6 has a lower runtime pass rate at 2.0% but a higher 6.67× IF.
- GPT-5.2 regresses under oracle context with 0.69× runtime IF and 0.85× TWMU IF.
- Memory gains from LLMs are rare: Claude Sonnet 4.6 reaches 16.61× peak-memory IF and 28.82× TWMU IF under oracle context, and 3556.03× TWMU IF under BM25, but the paper says these gains come from one instance rather than broad task success.

## Link
- [https://arxiv.org/abs/2606.25530v1](https://arxiv.org/abs/2606.25530v1)
