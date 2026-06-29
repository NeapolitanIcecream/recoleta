---
source: hn
url: https://martinfowler.com/articles/what-is-code.html
published_at: '2026-05-31T21:40:11'
authors:
- wapasta
topics:
- llm-assisted-coding
- code-intelligence
- domain-driven-design
- software-design
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# What Is Code

## Summary
Code generation by LLMs makes typed instructions cheaper, so the durable value of code is the shared conceptual model it encodes. The article argues that teams should treat coding as vocabulary building for humans, tools, and LLMs.

## Problem
- LLMs can generate executable code from high-level prompts, which reduces the value of merely typing implementation details.
- Teams still need shared domain meaning: names, boundaries, invariants, workflows, and rules that people and tools can reason about.
- Fast generation can create cognitive debt when code contains familiar patterns that the team does not understand or cannot maintain.

## Approach
- The article splits code into 2 roles: machine instructions and a human-readable model of the problem domain.
- It explains coding as translation between domain vocabulary and technical vocabulary, such as mapping retail concepts like catalog, order, payment, and shipment into web and data structures.
- It uses Domain-Driven Design ideas such as bounded contexts and ubiquitous language to explain why local abstractions must be discovered with domain experts and users.
- It argues that TDD, refactoring, and active coding help teams discover names, boundaries, and invariants through feedback.
- It applies the same view to LLMs: precise code vocabulary, stable abstractions, and tests give the model better context than vague prompts alone.

## Results
- Quantitative results: 0 reported. The article has no datasets, benchmark metrics, baselines, user-study counts, or measured productivity gains.
- It claims 2 main roles for code: instructions for machines and a conceptual model for humans, tools, and LLMs.
- It identifies 1 main LLM risk: cognitive debt caused by generated vocabulary and structure that developers do not understand.
- It gives 3 concrete design aids for LLM-assisted work: stable abstractions, clear semantics, and tests embedded in the codebase.
- It claims well-structured code can reduce prompt sensitivity and model dependence, but gives no accuracy, defect-rate, or latency numbers.

## Link
- [https://martinfowler.com/articles/what-is-code.html](https://martinfowler.com/articles/what-is-code.html)
