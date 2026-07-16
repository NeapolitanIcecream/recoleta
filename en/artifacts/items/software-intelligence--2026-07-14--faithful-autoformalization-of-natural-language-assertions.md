---
source: arxiv
url: https://arxiv.org/abs/2607.13303v1
published_at: '2026-07-14T22:12:14'
authors:
- Hongyi Liu
- Madhusudan Parthasarathy
- Adithya Murali
topics:
- code-intelligence
- automated-software-production
- software-foundation-model
- generative-engineering
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Faithful Autoformalization of Natural Language Assertions

## Summary
Monty improves the reliability of translating natural-language method assertions into executable JML specifications by combining LLM generation, testing, clausal-conformance scoring, and user-guided disambiguation. On 541 tasks across 22 Java collection-like classes, it increased precision by as much as 20 percentage points over naive LLM translation while retaining high recall.

## Problem
- Writing formal contracts for software testing and verification is labor-intensive, yet incorrect translations can either flag correct code or allow buggy code to pass.
- Natural-language assertions are ambiguous, and existing autoformalization methods often assume that the assertion should be valid for the implementation, which is unsuitable for testing code or validating AI-generated code.

## Approach
- Monty prompts an LLM to generate multiple candidate JML assertions from a natural-language assertion and a Java class or method context.
- It filters candidates with syntax checks, fuzz-safety checks, and fuzz-semantic tests generated with Randoop, while retaining both likely test-valid and test-invalid interpretations.
- Its clausal coverage metric has an LLM describe each formal assertion in natural language and score bidirectional clause matching against the original assertion; candidates below a 0.6 conformance threshold are removed in the experiments.
- When valid and invalid candidates remain, active learning produces a distinguishing program valuation for the programmer or an oracle to resolve the ambiguity.

## Results
- The evaluation covers 541 natural-language/formal-specification pairs from 22 Java classes representing collection-like data structures, including both valid and invalid assertions.
- With Qwen2.5-Coder, a 32B-parameter model, Monty increased precision from 75% to 91.6% on one dataset and from 64% to 85% on another.
- These gains amount to improvements of 16.6 and 21 percentage points, respectively, while the paper reports that recall remained high.
- Ablation studies found clausal coverage more effective for conformance checking than the evaluated baseline approaches, and showed that precision gains were more pronounced with smaller models.
- The excerpt does not provide exact recall values, full baseline configurations, or confidence intervals, so the reported improvement is bounded to the supplied benchmark and experimental settings.

## Link
- [https://arxiv.org/abs/2607.13303v1](https://arxiv.org/abs/2607.13303v1)
