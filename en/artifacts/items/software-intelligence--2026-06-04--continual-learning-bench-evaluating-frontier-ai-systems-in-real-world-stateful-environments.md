---
source: arxiv
url: https://arxiv.org/abs/2606.05661v1
published_at: '2026-06-04T03:43:28'
authors:
- Parth Asawa
- Christopher M. Glaze
- Gabriel Orlanski
- Ramya Ramakrishnan
- Benji Xu
- Asim Biswal
- Vincent Sunn Chen
- Frederic Sala
- Matei Zaharia
- Joseph E. Gonzalez
topics:
- continual-learning
- llm-agents
- agent-memory
- benchmarking
- software-engineering
- stateful-evaluation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments

## Summary
CL-Bench tests whether LLM agents improve during a sequence of related real-world tasks, rather than only perform well on isolated prompts. Its main finding is that full-context in-context learning beats several memory systems on average.

## Problem
- Current memory, long-context, and test-time adaptation evaluations often test recall, context compaction, or static task accuracy; they do not measure whether an agent learns hidden environment-specific structure over time.
- This matters for software agents, forecasting agents, and decision-support agents that must reuse lessons from prior interactions and adapt after concept drift.

## Approach
- CL-Bench contains six domains: software engineering, signal processing, disease outbreak forecasting, database querying, strategic game-playing, and demand forecasting.
- Each task is a sequence of instances with shared hidden structure, such as codebase layout, schema conventions, disease dynamics, or opponent strategy.
- The benchmark compares stateful runs that keep prior experience against stateless runs that start fresh on each instance.
- The main metric is gain: per-instance stateful reward minus stateless reward for the same system on the same instance. Normalized gain scales this by the system's remaining headroom.
- Tasks were reviewed by at least two authors and validated by 2 to 3 domain experts on realism, reusable knowledge, and measurable learning improvement.

## Results
- The best aggregate system was full-context ICL with Claude Sonnet 4.6: 22.3% ± 4.1 normalized reward, 25.4% ± 3.6 normalized gain, and $30.4 mean rollout cost.
- Full-context ICL with GPT-5.4 ranked second by normalized reward: 20.1% ± 9.1 reward and 20.1% ± 9.1 gain at $18.4 cost.
- Claude Code with Sonnet 4.6 ranked third by reward and second-tier by gain: 19.0% ± 7.1 reward, 23.9% ± 5.7 gain, and $38.6 cost.
- Dedicated memory systems lagged: Mem0 with GPT-5.4 reached 15.1% ± 6.4 reward and 20.2% ± 5.9 gain; ACE with GPT-5.4 reached 4.6% ± 2.7 reward and 8.6% ± 2.5 gain while costing $62.8.
- ICL with Gemini 3 Flash had the lowest listed cost at $7.6 and still reached 16.4% ± 3.8 normalized gain.
- Per-task curves showed clearer learning in Sales Prediction and Blind Spectrum Monitoring, weak learning in Cohort Studies, and Database Exploration gains driven by stateful runs avoiding frequent stateless failures.

## Link
- [https://arxiv.org/abs/2606.05661v1](https://arxiv.org/abs/2606.05661v1)
