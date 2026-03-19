---
source: arxiv
url: http://arxiv.org/abs/2603.09497v1
published_at: '2026-03-10T10:58:59'
authors:
- Maximilian Harnot
- Sebastian Komarnicki
- Michal Polok
- Timo Oksanen
topics:
- rag
- llm-testing
- embedded-c
- unit-test-generation
- software-verification
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# EmbC-Test: How to Speed Up Embedded Software Testing Using LLMs and RAG

## Summary
This paper proposes EmbC-Test: a RAG+LLM pipeline for embedded C unit test generation that uses in-project code, documentation, and historical tests to provide context to a large language model, enabling it to generate executable tests more quickly. Industrial evaluation shows that this method significantly outperforms random retrieval and no-retrieval baselines in correctness, usability, and efficiency.

## Problem
- Target problem: automatically generate tests for embedded C software, reducing the high cost and poor scalability of manual test writing and preventing verification from becoming a bottleneck in the release process.
- Why it matters: in safety-related embedded development, tests must not only be fast, but also traceable, reproducible, and consistent with project APIs/specifications; naïve zero-shot LLMs are prone to hallucinations, misuse internal interfaces, and write incorrect assertions, creating “false confidence.”
- Existing gap: prior AI/automated testing work has mostly focused on high-level languages, with limited coverage of embedded C, and has rarely incorporated project documentation, source code, and legacy tests together into the generation process.

## Approach
- Core idea: first split project artifacts (C header files, source code, legacy Python tests, requirements documents) and build a searchable knowledge base, then let the LLM “look up references” before generating tests, using the retrieved context to assist generation.
- To improve retrieval quality, the authors compare code chunking methods such as fixed-size, brace-aware, and AST-based splitting, as well as splitting historical tests by individual test unit; they then build a vector index using local embeddings.
- The retrieval stage uses hybrid retrieval: combining dense vector retrieval with BM25 lexical retrieval, then merging them with Reciprocal Rank Fusion, weighting both equally, and sending the top-5 chunks into the prompt.
- The prompt consists of a system prompt and a user prompt; in the user prompt, retrieved code/test snippets come first, followed by environment and project constraints, and finally software requirements, so the model sees context before writing tests.
- The evaluation covers 5 dimensions: coverage, test correctness (syntax/imports/runtime), retrieval quality, system latency and throughput, and subjective human expert review, with comparisons against random retrieval and non-RAG baselines.

## Results
- Correctness: RAG-generated tests achieve **100.0%** syntax correctness and **84.5%** runtime validation pass rate; random retrieval achieves **100.0% / 62.4%**, and no retrieval achieves **96.8% / 50.5%**. This indicates that RAG mainly and substantially improves the proportion of tests that “run correctly.”
- Coverage: under single-pass generation without iterative optimization, RAG reaches up to **43% branch coverage** and **67% line coverage**; the manual test baseline reaches **76% branch** and **93% line**, but the latter was achieved after months of iterative refinement.
- Human evaluation: the best RAG configuration scores **4.33** (relevance), **4.61** (assertion correctness), **4.06** (edge-case completeness), and **4.83** (readability) on a 5-point scale, with a test usability rate of **94.4%**.
- Acceptance: under the highest human-rated configuration, **38.9%** of tests can be accepted directly, **55.6%** require modification, and **5.6%** require rewriting; the authors state that RAG outperforms random retrieval and no retrieval across all human evaluation categories.
- Efficiency: system throughput is about **270 tests/hour**, while humans under this framework produce about **1 test/hour**. For **57** software requirements, the estimated total workload can be reduced from **57 hours** to **19.2 hours**, saving **66%** of the time.
- Industrial adoption: the paper states that the tool has been deployed into the Hydac Software workflow as part of an AI-assisted testing ecosystem, helping shift test engineers from repetitive test writing toward review, boundary-condition supplementation, and oracle improvement.

## Link
- [http://arxiv.org/abs/2603.09497v1](http://arxiv.org/abs/2603.09497v1)
