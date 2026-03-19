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
- c-cpp
- benchmark
- retrieval-robustness
- semantic-retrieval
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# CLARC: C/C++ Benchmark for Robust Code Search

## Summary
CLARC is a robustness benchmark for C/C++ code retrieval that emphasizes real repositories, compilable code, and robust evaluation after removing lexical cues. The paper shows that current mainstream retrieval models degrade noticeably under identifier anonymization and low-level representations, indicating that they still rely heavily on superficial lexical features.

## Problem
- Existing code search benchmarks are mostly biased toward Python and rarely cover real-world C/C++ retrieval scenarios, leaving a clear evaluation gap for systems programming languages.
- Many datasets lack complete dependencies and compilable context, making it difficult to truly measure whether models understand code functionality and its contextual requirements.
- Existing evaluations rarely test perturbations such as variable renaming, identifier anonymization, and Assembly/Wasm systematically, so high scores may come only from lexical matching rather than semantic understanding; this matters for code search, RAG, and developer productivity.

## Approach
- Build an automated data pipeline: mine functions from 144 popular GitHub C/C++ repositories, keep compilable samples, and extract complete dependency context; the final dataset contains 6,717 query-code pairs, including 5,472 for training and 1,245 for evaluation.
- Divide samples into three groups by dependency complexity: relying only on the standard library, relying on custom-defined types, and relying on user-defined helper functions; Group 3 further distinguishes short/long context forms.
- Use an LLM to generate natural language queries, and validate whether their quality is comparable to or better than human-written descriptions through double-blind human scoring, bootstrap hypothesis testing, and agreement analysis.
- Design multiple robustness settings to strip away lexical cues: Neutralized, Randomized, Assembly, and WebAssembly, to test whether models truly rely on code semantics for retrieval.
- Evaluate 6 retrieval models on the benchmark, including BM25, CodeT5+, OASIS, Nomic-emb-code, OpenAI-text-embedding-large, and Voyage-code-3.

## Results
- Dataset scale and statistics: CLARC contains 6,717 sample pairs, including 1,245 in the evaluation set and 5,472 in the training set; in the evaluation set, the average query length is 84.8 tokens, the original code averages 244.2 tokens, 24.8 LOC, and cyclomatic complexity 3.4.
- LLM query quality validation: in double-blind evaluation with 125 samples per group, LLM descriptions were close to or better than human descriptions in Group 2 and Group 3 (Group 2: LLM 76.5 vs Human 72.0, p=76.32%; Group 3: 75.5 vs 71.5, p=84.92%); Group 1 was even higher (86.0 vs 60.0, p=99.99%). Krippendorff’s α was 65.51–74.77, indicating acceptable annotation agreement.
- Under the standard setting, the best model is already very strong on simple/moderate dependency samples: in Group 1, OASIS achieved NDCG 89.08, MRR 86.54, and R@1 79.85, far above BM25’s NDCG 10.50; in Group 2, Voyage achieved NDCG 94.06, MRR 92.10, and R@1 85.93, while Nomic also reached NDCG 93.61.
- The more complex Group 3 Short is clearly harder: the best model, Voyage, achieved only NDCG 66.66, MAP 50.93, and R@1 27.28; Nomic reached NDCG 65.39 and R@1 25.33; BM25 achieved only NDCG 10.50 and R@1 2.35, showing that helper-function dependencies significantly increase retrieval difficulty.
- The paper’s core conclusion is that after identifier anonymization, randomization, and compilation to Assembly/Wasm, retrieval performance of all six SOTA models “drops significantly”; the provided excerpt does not include the full numerical tables for these settings, but the authors explicitly interpret this as evidence that current models still mainly rely on lexical features rather than robust code semantic understanding.
- The authors also claim that even with conventional supervised fine-tuning, the performance gap between the standard setting and the anonymized setting still remains, indicating that naive fine-tuning is insufficient to solve the robustness problem; the excerpt does not provide the corresponding specific numbers.

## Link
- [http://arxiv.org/abs/2603.04484v1](http://arxiv.org/abs/2603.04484v1)
