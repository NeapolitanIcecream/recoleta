---
source: arxiv
url: http://arxiv.org/abs/2603.04484v1
published_at: '2026-03-04T18:57:37'
authors:
- Kaicheng Wang
- Liyan Huang
- Weike Fang
- Weihang Wang
topics:
- code-search
- benchmark
- c-cpp
- retrieval-robustness
- program-understanding
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# CLARC: C/C++ Benchmark for Robust Code Search

## Summary
CLARC is a robustness benchmark for C/C++ code retrieval that focuses on testing whether models truly understand code semantics rather than relying on superficial lexical cues such as variable names and function names. The paper also proposes an automated data construction pipeline and uses real GitHub projects, compilable code, anonymization, and low-level language transformations to systematically expose weaknesses in existing retrieval models.

## Problem
- Existing code search benchmarks are mostly biased toward Python and **lack real-world C/C++ text-to-code retrieval** evaluation, making it difficult to transfer research conclusions to systems programming scenarios.
- Many code snippets in existing datasets are **not compilable or have incomplete context**, failing to reflect the importance of dependent types, helper functions, and contextual understanding in real development.
- Existing benchmarks rarely test robustness under perturbations such as **variable renaming, identifier anonymization, and compilation to Assembly/Wasm**, so high scores may simply reflect lexical matching rather than genuine understanding of code semantics; this matters because real environments involve obfuscation, attacks, and retrieval across abstraction layers.

## Approach
- Built an automated pipeline that extracts functions from **144 real GitHub C/C++ repositories** while preserving their dependency context; only samples that are **compilable** in a predefined environment are kept.
- Divided samples into three groups by dependency complexity: **Group 1** depends only on the standard library, **Group 2** uses custom-defined types, and **Group 3** calls user-defined helper functions; **Group 3** is further split into **Short/Long** context forms.
- Used **LLMs (o3-mini, grok-4)** to automatically generate natural language queries, and verified whether query quality is comparable to human-written descriptions through **human double-blind scoring + bootstrap hypothesis testing**.
- To isolate the influence of lexical features, designed multiple robustness settings: **neutralized** (generic placeholder anonymization), **randomized** (random naming), **assembly**, and **webassembly**, progressively removing identifiers and high-level semantic cues from the source code.
- Evaluated **6 retrieval models** on the benchmark, including BM25, CodeT5+, OASIS, Nomic-emb-code, OpenAI text-embedding-large, and Voyage-code-3.

## Results
- CLARC contains **6,717 query-code pairs** in total, with **1,245** for evaluation and **5,472** for training; the evaluation set comes from **45 repositories**, and the training set from **99 repositories**.
- In query quality validation, LLM-generated descriptions were comparable to or better than human-written descriptions: for example, in **Group 1** the LLM score was **86.0** versus **60.0** for humans, with p-value **99.99%**; for **Group 2** it was **76.5 vs 72.0** (p-value **76.32%**); for **Group 3** it was **75.5 vs 71.5** (p-value **84.92%**).
- Under the standard setting, strong models performed very well: on **Group 2**, **Voyage** reached **NDCG 94.06 / MRR 92.10 / MAP 92.11 / R@1 85.93**, and **Nomic** reached **NDCG 93.61 / MRR 91.61**; by contrast, **BM25** achieved only **NDCG 17.83 / MRR 14.64**.
- In the standard setting for **Group 1**, the best results were close to saturation: **OASIS** achieved **NDCG 89.08 / MRR 86.54 / R@20 98.48**, and **Voyage** achieved **NDCG 88.99 / MRR 86.93**, both clearly outperforming **CodeT5+** with **NDCG 64.54**.
- For the more complex **Group 3 Short**, performance dropped significantly: the best model, **Voyage**, achieved only **NDCG 66.66 / MRR 80.53 / MAP 50.93 / R@1 27.28**, showing that helper-function dependencies and contextual complexity substantially increase retrieval difficulty.
- The paper explicitly claims that after **identifier anonymization** and compilation to **Assembly / Wasm**, all six SOTA models showed **significant declines** in retrieval effectiveness; the provided excerpt does not include the full numerical tables for these robustness settings, but the authors’ core conclusion is that current models still **rely heavily on lexical features rather than robust semantic understanding of code**.

## Link
- [http://arxiv.org/abs/2603.04484v1](http://arxiv.org/abs/2603.04484v1)
