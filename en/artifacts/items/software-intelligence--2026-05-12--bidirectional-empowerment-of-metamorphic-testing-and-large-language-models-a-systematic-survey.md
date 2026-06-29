---
source: arxiv
url: https://arxiv.org/abs/2605.13898v1
published_at: '2026-05-12T13:47:26'
authors:
- Zheng Zheng
- Zenghui Zhou
- Yinwang Xu
- Daixu Ren
- Tsong Yueh Chen
topics:
- metamorphic-testing
- llm-testing
- software-quality-assurance
- code-intelligence
- test-automation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey

## Summary
This survey maps how metamorphic testing can test LLM systems and how LLMs can automate parts of metamorphic testing. It reviews 93 primary studies and organizes the area into two main directions.

## Problem
- LLM outputs are probabilistic, open-ended, and often lack a single correct answer, so exact test oracles work poorly for tasks such as QA, dialogue, code generation, RAG, and agents.
- Metamorphic testing checks relations between related inputs and outputs, which fits cases where correctness is semantic or comparative.
- Metamorphic testing still needs human effort to find metamorphic relations, build input transformations, and implement executable tests.

## Approach
- The survey follows Kitchenham-style systematic review methods and searches ACM Digital Library, IEEE Xplore, SpringerLink, ScienceDirect, arXiv, plus Google Scholar supplementation.
- It uses a metadata search query combining metamorphic-testing terms with LLM, GPT, Claude, Gemini, DeepSeek, code model, RAG, and agent terms.
- It includes studies that use metamorphic testing for LLMs or use LLMs to support metamorphic testing, while excluding unrelated uses of “MR” and general ML testing without LLM involvement.
- It organizes the literature into 2 directions: MT for LLMs and LLMs for MT.
- MT for LLMs covers hallucination, fairness, robustness, code reliability, RAG, dialogue, and autonomous agents; LLMs for MT covers relation discovery, input transformation, test implementation, and closed-loop testing.

## Results
- The paper reviews 93 primary studies selected from literature available up to April 30, 2026.
- The covered publication period mainly spans January 2019 to April 2026, with faster growth after ChatGPT’s release in late 2022 and stronger growth after 2024.
- The search used 5 main scholarly sources and inspected the first 250 Google Scholar results per query for supplementary coverage.
- The main claimed contribution is a 2-part taxonomy: MT for LLMs and LLMs for MT.
- The survey reports no benchmark-style model-performance gains such as accuracy, pass rate, or defect-detection improvement over a baseline; its quantitative claims are corpus size, search scope, time window, and category counts described in the survey figures.

## Link
- [https://arxiv.org/abs/2605.13898v1](https://arxiv.org/abs/2605.13898v1)
