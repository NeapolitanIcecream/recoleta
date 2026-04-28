---
source: arxiv
url: http://arxiv.org/abs/2604.16646v1
published_at: '2026-04-17T19:02:54'
authors:
- Zeeshan Rasheed
- Abdul Malik Sami
- Muhammad Waseem
- Kai-Kristian Kemell
- Mika Saari
- Pekka Abrahamsson
topics:
- agentic-frameworks
- reasoning-benchmarks
- multi-agent-systems
- software-engineering
- llm-evaluation
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Agentic Frameworks for Reasoning Tasks: An Empirical Study

## Summary
This paper compares 22 open-source agentic frameworks on reasoning benchmarks under one test setup. The main finding is that framework choice matters more for orchestration quality, cost control, and failure handling than for claimed agent architecture.

## Problem
- Teams use agentic frameworks for reasoning-heavy work, but there is little broad, benchmark-based evidence on which frameworks are accurate, fast, affordable, and stable in practice.
- Prior comparisons usually test only a few frameworks or focus on architecture surveys, developer experience, or narrow tasks, which leaves framework selection under real constraints unclear.
- This matters for software engineering and other reasoning-intensive uses because bad orchestration can waste days of runtime, burn API budget, or fail to finish tasks even when the base model could answer them.

## Approach
- The authors collected 1,200 GitHub repositories from January 2023 to July 2025, applied selection criteria, and chose 22 widely used open-source agentic frameworks.
- They built a taxonomy of five architecture types: single-agent, role-based multi-agent, hierarchical, modular, and graph-based.
- They evaluated the frameworks in a unified setup on three reasoning benchmarks: BBH, GSM8K, and ARC.
- They measured four practical outcomes: reasoning accuracy, execution time, computational cost, and consistency across benchmarks.
- They also analyzed failure cases to separate reasoning limits from system failures such as memory growth, retry loops, quota exhaustion, and context handling problems.

## Results
- 19 of 22 frameworks completed all three benchmarks.
- 12 frameworks showed consistent performance, with mean accuracy of **74.6% to 75.9%**, execution time of **4 to 6 seconds per task**, and cost of **0.14 to 0.18 cents per task**.
- Mathematical reasoning stayed weak across all completed frameworks: mean accuracy on **GSM8K was 44.35%**, versus **89.80% on BBH** and **89.56% on ARC**.
- The paper says this math gap appears across architecture types, which suggests current agent frameworks inherit the base model's multi-step numerical weaknesses rather than fixing them.
- Several poor results came from system failures rather than wrong reasoning: **Camel** failed to complete BBH after **11 days** because context kept growing; **Upsonic** spent **$1,434 in one day** after extraction failures triggered retries and large prompts; **AutoGen** and **Mastra** exhausted API quotas through repeated agent interactions that increased prompt length without improving answers.
- The paper’s main practical claim is that framework selection for reasoning tasks should focus on memory discipline, retry policy, context control, and cost behavior more than architectural category alone.

## Link
- [http://arxiv.org/abs/2604.16646v1](http://arxiv.org/abs/2604.16646v1)
