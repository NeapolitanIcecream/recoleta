---
source: arxiv
url: http://arxiv.org/abs/2604.23892v1
published_at: '2026-04-26T21:34:51'
authors:
- Mohammad Zaeed
- Tanzima Z. Islam
- Vladimir Indic
topics:
- llm-code-optimization
- gpu-performance
- multi-agent-systems
- hpc
- performance-profiling
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization

## Summary
Optimas is an automated GPU code optimization system that feeds runtime performance evidence into an LLM, then compiles and validates the generated code. The paper’s main claim is that diagnostic-guided generation can turn profiler output into correct code edits that improve performance across many experiments.

## Problem
- GPU performance tuning is still manual because profilers show bottlenecks but do not produce code changes, and LLMs given only source code failed to find a single improving optimization in the authors’ preliminary test.
- Raw profiling data is too large and too noisy for direct LLM input; a single kernel can produce hundreds of megabytes of traces, and current models have context limits.
- Correctness and speedup both need execution-based validation, since code that compiles may still miss the real bottleneck or break output semantics.

## Approach
- Optimas builds a multi-agent pipeline with profiling, analysis, prompt construction, and evaluation agents. The system automates about 90% of the workflow and retries failed compilations up to three times.
- It selects the smallest set of hot kernels covering at least 80% of runtime, then compresses diagnostics into compact summaries from three sources: Roofline analysis, PC stall sampling, and hardware counter interaction analysis.
- For PC sampling, it keeps only dominant stall signals per source line. The paper gives one concrete reduction: a 41-line kernel’s raw PC trace shrank from 990 MB to 10 MB after aggregation and to a summary under 6 KB.
- For hardware counters, it uses a sparse feature-selection method based on ensemble orthogonal matching pursuit to pick about 5 counters that best explain runtime variation, then maps those counters to natural-language descriptions.
- Prompts include the code, the diagnostic summaries, and guardrails that restrict edits to implicated regions and require each edit to cite the evidence it targets. The framework then compiles, runs, checks bit-for-bit correctness, and measures performance. The paper also introduces EAR metrics to score evidence coverage, edit localization, and whether measured changes match the diagnosis.

## Results
- The abstract reports 3,410 real-world experiments on 10 benchmarks and 2 HPC mini-applications.
- The authors claim 100% correct code generation and performance improvement in more than 98.82% of those experiments.
- Reported average speedups on NVIDIA GPUs range from 8.02% to 79.09%.
- The paper states that a code-only baseline with no diagnostics produced 0% valid optimizations.
- In the visible results table for GPT-5, several per-benchmark gains are large: Accuracy reaches 79.09% with PC+Roofline, Sobol reaches 41.60% with PC, Dot reaches 36.73% under several settings, and Copy/Mul/Add/Triad are mostly in the low-to-high 30% range.
- The excerpted results table is truncated, so full benchmark-by-benchmark totals, all model comparisons, and full EAR metric values are not available in the provided text.

## Link
- [http://arxiv.org/abs/2604.23892v1](http://arxiv.org/abs/2604.23892v1)
