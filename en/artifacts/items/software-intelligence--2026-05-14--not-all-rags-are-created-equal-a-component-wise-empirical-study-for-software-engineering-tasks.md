---
source: arxiv
url: https://arxiv.org/abs/2605.14503v1
published_at: '2026-05-14T07:47:44'
authors:
- Qiang Ke
- Yanjie Zhao
- Hongjin Leng
- Shengming Zhao
- Haoyu Wang
topics:
- retrieval-augmented-generation
- code-intelligence
- software-engineering
- empirical-study
- rag-optimization
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks

## Summary
This paper tests which parts of a RAG pipeline matter most for Python software engineering tasks. Its main claim is that retrieval choices, especially the retriever, often affect final quality more than the generator.

## Problem
- RAG systems for software tasks require choices about query processing, retrieval, context refinement, and generation, but practitioners lack task-specific evidence for those choices.
- Prior work mainly studied code generation or one retrieval component, leaving weaker guidance for code summarization and code repair.
- Poor component choices can feed irrelevant code or documentation into an LLM and increase trial-and-error cost.

## Approach
- The authors build a modular Code RAG testbed that separates query processing, retrieval, context refinement, and generation so each part can be tested alone.
- They evaluate 3 tasks: code generation, code summarization, and code repair.
- They compare 4 query processing techniques, 7 retrieval models across sparse, dense, and hybrid retrieval, 4 context refinement methods, and 6 generators.
- The retrieval corpus combines Stack Overflow, Python API docs, LeetCode, CodeSearchNet, and Code-Contests, with exact-match test-solution decontamination.
- They also build an LLM-driven adaptive configuration system that maps task features to component choices using rules derived from the experiments.

## Results
- The excerpt provides no final W-Pass@1, CodeBLEU, or embedding-similarity scores, so the claimed performance gains cannot be checked numerically from the supplied text.
- The study covers over 21 models and methods: 4 query processing techniques, 7 retrieval models, 4 context refinement methods, and 6 generator models.
- The evaluation uses 4 datasets or dataset variants: a 300-problem APPS subset, 100 long CodeXGLUE Python snippets, an obfuscated CodeXGLUE variant, and a 300-sample DebugBench subset.
- The retrieval corpus contains 232,633 documents: 164,085 from Stack Overflow, 38,352 from Python API docs, 3,174 from LeetCode, 13,590 from CodeSearchNet, and 13,432 from Code-Contests.
- The main empirical claim is that retriever-side components influence final RAG performance more than generator choice in many settings, and BM25 performs well across the tested software tasks.
- The compression setup reports average context sizes of 1,533.47 tokens for 10 chunks, 3,578.81 for 20 chunks, 7,818.43 for 40 chunks, and 17,105.42 for 80 chunks.

## Link
- [https://arxiv.org/abs/2605.14503v1](https://arxiv.org/abs/2605.14503v1)
