---
source: arxiv
url: http://arxiv.org/abs/2604.02729v1
published_at: '2026-04-03T04:44:07'
authors:
- Puyu Zeng
- Zhaoxi Wang
- Zhixu Duan
- Liang Feng
- Shaobo Wang
- Cunxiang Wang
- Jinghang Wang
- Bing Zhao
- Hu Wei
- Linfeng Zhang
topics:
- code-generation-benchmark
- industrial-code
- multilingual-evaluation
- software-engineering
- llm-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# IndustryCode: A Benchmark for Industry Code Generation

## Summary
IndustryCode is a benchmark for testing code generation on real industrial tasks across domains and languages that common coding benchmarks miss. It measures both modular sub-tasks and full project-level problems, and current top models still fall short of reliable industrial performance.

## Problem
- Existing code benchmarks focus on general software tasks, single domains, or single languages, so they do not test the domain knowledge, numerical precision, and language diversity found in industrial work.
- Real industrial coding often uses specialized languages such as MATLAB and Stata and requires solving linked sub-modules inside larger projects.
- This matters because benchmark scores on consumer or internet-style coding tasks do not tell you whether a model can handle finance, automation, aerospace, or other production engineering settings.

## Approach
- The paper builds **IndustryCode**, a benchmark with **125 main industrial problems** decomposed into **579 sub-problems**.
- The tasks come from real production code used by industry practitioners, then are manually reconstructed and revised to reduce pretraining contamination and add harder math, algorithm, engineering, and architecture constraints.
- The benchmark spans **4 languages**: **Python, C++, MATLAB, and Stata**, covering about **20 sub-domains** such as finance, automation, aerospace, construction, semiconductors, and logistics.
- Evaluation uses a hierarchical setup: models solve sub-problems with cumulative context from the main task and prior generated code, then are also scored on full main problems.
- Scoring combines **execution-based numerical validation** with an **LLM judge** for cases where functional or structural equivalence is hard to check with fixed I/O tests alone.

## Results
- Dataset scale: **125 main problems**, **579 sub-problems**; split into **19 main / 80 sub** for development and **106 main / 499 sub** for test.
- Best overall model: **Claude 4.5 Opus** with **68.1% Pass@1** on **sub-problems** and **42.5%** on **main problems**.
- Other strong proprietary models: **Claude 4.5 Sonnet** reached **64.4% / 33.8%** overall; **Gemini-3-pro** reached **63.4% / 41.2%**; **GPT-5.2** reached **53.4% / 32.4%**.
- Strong open-model result: **Qwen3-Max** scored **70.4%** on **C++ sub-problems**, beating **GPT-5.2 (67.9%)** and **Gemini-3-pro (66.0%)** in that setting; its overall scores were **55.9% / 32.5%**.
- Error analysis says failures are led by **syntax errors (32.8%)**, **misunderstanding the question (30.2%)**, and **hallucination (19.6%)**; **reasoning failure** is lower at **8.4%**.
- Thinking mode helped some models by about **+4.70%** on sub-problems and **+7.65%** on main problems on average for models that benefited, but it also increased context confusion and syntax problems in other cases.

## Link
- [http://arxiv.org/abs/2604.02729v1](http://arxiv.org/abs/2604.02729v1)
