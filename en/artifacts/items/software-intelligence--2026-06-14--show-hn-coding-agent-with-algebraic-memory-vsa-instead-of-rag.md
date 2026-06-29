---
source: hn
url: https://github.com/vitaliyfedotovpro-art/raidho
published_at: '2026-06-14T23:44:56'
authors:
- astrumverum
topics:
- coding-agent
- memory
- vsa
- multi-model
- cost-benchmark
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Show HN: Coding agent with algebraic memory (VSA) instead of RAG

## Summary
Raidho is a coding agent that splits reasoning, execution, and memory across separate components. It matters because it claims lower cost and persistent project memory compared with a single-model tool loop.

## Problem
- Most coding agents use one model for planning and tool use, which makes expensive reasoning pay for every iteration.
- Plain chat history does not preserve reusable facts well across runs, so the agent repeats work.
- The paper targets local coding workflows where provider choice, cost, and persistence matter.

## Approach
- It uses one model for reasoning in text mode and a second model for code execution in a tool loop.
- It adds durable memory that stores subject-relation-object facts on disk per project and reloads them on the next run.
- The memory uses a Vector Symbolic Architecture (VSA) instead of RAG, with algebraic fact composition and bit-packed similarity ranking.
- It also offers a council mode where two providers debate a question and a neutral pass distills agreement, disagreements, and a recommendation.
- An opt-in auto-distillation mode turns repeated successful read-only task loops into deterministic procedures for later reuse.

## Results
- The excerpt gives one explicit benchmark: on the same task with the same model, a deterministic procedure cost $0.05, the context-first hybrid cost $0.116, and the pure tool loop cost $0.301.
- On that benchmark, the hybrid matched the tool loop's report quality at 2.6x lower cost.
- In a repeated multi-step task over small data, auto-distillation reduced cost by 9.6x over 5 runs, which is a 70% drop.
- For a data-heavy audit, auto-distillation saved about nothing because the cost came from file contents, not loop overhead.
- The excerpt says the system was tested end-to-end against DeepSeek and Claude through official SDKs, but it does not provide broader benchmark tables in the text shown.

## Link
- [https://github.com/vitaliyfedotovpro-art/raidho](https://github.com/vitaliyfedotovpro-art/raidho)
