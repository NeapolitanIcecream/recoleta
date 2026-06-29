---
source: arxiv
url: https://arxiv.org/abs/2605.26851v1
published_at: '2026-05-26T11:08:04'
authors:
- Qinghua Xu
- Guancheng Wang
- Lionel Briand
- Zhaoqiang Guo
- Kui Liu
topics:
- llm-test-generation
- java-unit-testing
- mockless-testing
- code-intelligence
- software-engineering-agents
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# LLM-based Mockless Unit Test Generation for Java

## Summary
MocklessTester generates Java unit tests without mocks by mining real dependency usage and repairing invalid tests under project-specific constraints. It reports higher coverage than PANTA on Defects4J and a new post-cutoff benchmark, Deps4J.

## Problem
- LLM-generated Java tests often fail when real dependencies must be constructed, imported, and called in valid order.
- Mock-based tests can miss bugs in dependency code because they replace real objects with simulated behavior.
- The paper frames the failure sources as missing project context and weak constraint compliance during repair.

## Approach
- A preparation step builds a Joern code property graph, a ClassIndex of visible classes and members, and a Markov typestate model for likely valid API call order.
- A planner selects uncovered paths in the class under test, then a generator writes tests using real construction and call examples mined from the project.
- A validator compiles and runs each generated JUnit test, then passes compile-time and runtime errors to the fixer.
- The fixer uses two repair stages: an initial fix from error feedback, then a constraint-checked fix using symbol rules, typestate rules, and memory of past successful or failed repairs.

## Results
- On Defects4J, average line coverage rises from 68.83% with PANTA to 88.82%, a +19.99 point gain.
- On Defects4J, branch coverage rises from 58.84% to 83.74%, and mutation score rises from 38.33% to 52.00%.
- On Deps4J, line coverage rises from 53.29% to 75.98%, and branch coverage rises from 42.34% to 58.12%.
- The abstract reports mutation-score gains of +13.67 points on Defects4J and +0.17 points on Deps4J.
- Dependency line coverage increases from 819 to 1197 on Defects4J and from 224 to 279 on Deps4J, meaning the generated tests execute more real dependency code.
- Reported cost averages 108.97 seconds and 26.59k tokens per method on Defects4J, and 69.85 seconds and 25.46k tokens per method on Deps4J.

## Link
- [https://arxiv.org/abs/2605.26851v1](https://arxiv.org/abs/2605.26851v1)
