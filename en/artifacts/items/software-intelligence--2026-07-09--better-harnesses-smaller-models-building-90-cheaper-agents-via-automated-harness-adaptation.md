---
source: arxiv
url: https://arxiv.org/abs/2607.08938v1
published_at: '2026-07-09T21:08:01'
authors:
- Chenyang Yang
- Xinran Zhao
- Tongshuang Wu
- "Christian K\xE4stner"
topics:
- small-language-models
- agent-harnesses
- automated-harness-optimization
- software-agents
- inference-cost
- business-workflows
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation

## Summary
The paper shows that small language models can reach near-frontier-agent performance on routine business workflows when their agent harness is automatically adapted. The best adapted agent achieved 89.7% of LLM performance at 4% of the cost.

## Problem
- Frontier LLM agents are expensive and slow to deploy at scale, while small language models often fail when placed in harnesses designed for larger models.
- The problem matters because routine business workflows may need reliable execution, low inference cost, local deployment, and better privacy rather than open-ended generation.

## Approach
- The paper maps agent failures, including tool-use, instruction-following, knowledge, long-context, and planning failures, to three adaptation types: context, tools, and agent loops.
- A meta-agent automatically edits a software-agent harness by changing prompts, skills, tools, hooks, context management, and sub-agents.
- The optimizer evaluates candidate harnesses, inspects failure trajectories, proposes targeted edits, runs sanity checks, and keeps candidates that improve validation performance.
- The method shifts repeatable workflow knowledge and control logic from the language model into prompts, custom tools, filtered tool sets, and runtime safeguards.

## Results
- Across 7 business tasks, 3 SLM families, and 21 task-model pairs, optimized harnesses improved performance on 16 pairs and closed the SLM-LLM gap on 7 pairs.
- The best SLM agent recovered 89.7% of LLM-agent performance with a 96% cost reduction, or about 4% of the LLM cost.
- In the budget-approval example, Gemma-4-26B-A4B improved from 75.0% accuracy with the default harness to 98.3% with an adapted harness, compared with 97.3% for Gemini-3.1-Pro; the LLM cost was $0.22 per query.
- Successful adaptations addressed instruction-following and knowledge failures most often, each appearing in 81% of successful adaptations; adding context occurred in 86%, creating tools in 43%, and managing tools in 29%.
- Adaptation improved accuracy by 21.1 percentage points when task instances changed from the most diverse setting to the least diverse setting.
- Stronger SLMs gained more from adaptation, with reported improvements of 48.8% versus 15.5% for weaker models, showing that harness changes cannot replace missing core capabilities.

## Link
- [https://arxiv.org/abs/2607.08938v1](https://arxiv.org/abs/2607.08938v1)
