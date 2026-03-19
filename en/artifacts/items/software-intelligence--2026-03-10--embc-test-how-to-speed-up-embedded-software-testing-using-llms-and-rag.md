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
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# EmbC-Test: How to Speed Up Embedded Software Testing Using LLMs and RAG

## Summary
This paper proposes EmbC-Test: a RAG+LLM pipeline for embedded C unit test generation that constrains outputs using in-project code, documentation, and historical tests. Its goal is not to fully replace humans, but to shift test engineers from writing tests by hand to efficient review and revision, thereby significantly accelerating industrial verification workflows.

## Problem
- Automated testing for embedded C still relies heavily on manual writing, which is time-consuming and struggles to keep up with faster software release cycles, making verification a development bottleneck.
- Direct zero-shot LLM-based test generation is unreliable: it can easily hallucinate nonexistent APIs, types, or assertions, and even when tests run, they may encode incorrect expectations, which is especially risky in safety-related scenarios.
- Existing AI/automated testing research focuses more on high-level languages, and less often uses project-specific documentation, legacy tests, and code structure systematically for embedded C test generation.

## Approach
- Build a project knowledge base: collect C header files, source code, and historical Python tests, and chunk them using fixed-length, brace-aware, AST-based, and test-unit methods.
- Perform local embedding and indexing over the knowledge chunks; at runtime, use requirement text as the query, apply hybrid retrieval from vector search and BM25 lexical search, fuse results with RRF, and take the top-5 context.
- Feed the retrieved code snippets, test templates, project environment descriptions, and software requirements into the prompt so the cloud LLM can generate tests aligned with project conventions.
- Provide accompanying quality evaluation and assurance: compare RAG, random retrieval, and a no-retrieval baseline, and validate across syntax, runtime correctness, coverage, retrieval quality, performance, and human review.

## Results
- In the industrial evaluation, RAG-generated tests achieved **100.0%** syntactic correctness and **84.5%** runtime validation pass rate; compared with random retrieval at **100.0% / 62.4%** and no retrieval at **96.8% / 50.5%**, RAG was clearly stronger in runtime correctness.
- In terms of coverage, the best RAG configuration achieved **43% branch coverage** and **67% line coverage**; the existing human-written test suite reached **76% branch** and **93% line**, but the latter was the result of months of iteration, whereas the RAG results came from a single generation pass with no feedback-based optimization.
- In human evaluation, the best RAG configuration achieved the following on a 5-point scale: **4.33** (relevance), **4.61** (assertion correctness), **4.06** (edge-case completeness), **4.83** (readability).
- The best configuration achieved a test usability rate of **94.4%**; among these, **38.9%** were directly acceptable, **55.6%** required minor edits, and only **5.6%** needed rewriting.
- Generation efficiency was about **270 tests/hour**, while humans under this framework produced about **1 test/hour**.
- In a case study involving **57** software requirements, the total testing effort could be reduced from **57 hours** to **19.2 hours**, claiming a **66%** time savings.

## Link
- [http://arxiv.org/abs/2603.09497v1](http://arxiv.org/abs/2603.09497v1)
