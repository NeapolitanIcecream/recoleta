---
source: arxiv
url: https://arxiv.org/abs/2606.25588v1
published_at: '2026-06-24T08:59:01'
authors:
- Yi Gao
- Ziyuan Zhang
- Xing Hu
- Xiaohu Yang
- Xin Xia
topics:
- test-migration
- code-intelligence
- multi-agent-systems
- software-testing
- llm-code-generation
- repository-graphs
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration

## Summary
IntentTester migrates unit tests across similar libraries by converting source tests into language-neutral test intent and generating executable tests for a target repository. It targets cases where API-signature mapping fails, including Java-Python migration.

## Problem
- Unit tests encode domain behavior, but similar libraries often rewrite tests manually, which wastes effort and leaves behavior gaps.
- API-signature and code-pattern mapping tools fail when libraries expose the same function through different APIs, coding styles, or programming languages.
- Runnable migrated tests need constructors, fixtures, return-value chains, and assertions; missing dependencies often cause runtime failures.

## Approach
- The system splits source tests into smaller sub-tests and converts each one into a Test Description Language record with test data, setup, focal method, and assertions.
- It builds a target repository graph with classes, methods, fields, tests, and typed edges such as calls, returns, field access, inheritance, and test-to-method links.
- It retrieves candidate target entities from TDL steps using MiniLM embeddings and FAISS k-NN search, then expands graph edges to collect needed dependencies.
- A planning agent checks whether the context has enough constructors, methods, and assertion targets; it expands once more or discards unsupported intents.
- An LLM generates the target test from the TDL, graph context, and reference tests, then a verification agent checks the output and sends feedback when needed.

## Results
- The evaluation covers 9 open-source projects across JSON, HTML, and Time libraries in Java and Python.
- From 2,058 source tests, the pipeline produced 5,536 sub-tests; 3,257 remained after filtering.
- IntentTester generated 2,776 syntactically correct tests with 85% correctness, compared with 51% for MUT and 43% for METALLICUS.
- 2,410 generated tests executed successfully in target repositories, giving a 74% effectiveness rate.
- The paper reports a 34 percentage-point correctness gain over MUT and a 42 percentage-point gain over METALLICUS.
- The generated tests exposed 25 real defects, including NanoJSON stack overflow on circular JSON references and a JFiveParse null dereference; the JFiveParse issue was patched by maintainers.

## Link
- [https://arxiv.org/abs/2606.25588v1](https://arxiv.org/abs/2606.25588v1)
