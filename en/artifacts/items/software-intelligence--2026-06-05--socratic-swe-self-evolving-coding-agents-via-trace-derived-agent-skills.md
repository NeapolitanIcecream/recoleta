---
source: arxiv
url: https://arxiv.org/abs/2606.07412v1
published_at: '2026-06-05T16:00:17'
authors:
- Chuan Xiao
- Zhengbo Jiao
- Shaobo Wang
- Wei Wang
- Bing Zhao
- Hu Wei
- Linfeng Zhang
- Lin Qu
topics:
- software-engineering-agents
- code-intelligence
- self-evolving-agents
- synthetic-training-data
- reinforcement-learning
- swe-bench
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills

## Summary
Socratic-SWE trains coding agents by turning their past repository-solving traces into skills that guide the next batch of synthetic repair tasks. The paper reports higher pass rates than self-evolving baselines on SWE-bench and Terminal-Bench under the same 36k-task training budget.

## Problem
- High-quality software engineering training tasks are scarce, and static bug-injection pipelines do not track the agent's current failure modes.
- SWE agents produce rich traces with searches, edits, commands, tests, failures, and fixes, yet many training methods reduce these traces to rewards and discard the rest.
- This matters because fixed task pools give less useful signal as the solver improves, which can slow or stop training gains.

## Approach
- The system collects successful and failed solver traces from real repository tasks.
- A distillation model converts repeated failure modes and useful repair patterns into structured skills with a name, description, applicability conditions, and ordered operations.
- A generator uses those skills to create targeted repair tasks in real repositories, with tests or commands as verifiers.
- Each task must pass format, repository-grounding, execution-stability, and semantic checks before training use.
- The generator is rewarded when a task's solver update aligns with gradients from a held-out validation set; the solver trains with GDPO using full-pass, partial-repair, and regression-avoidance rewards.

## Results
- After 3 iterations and 36k validated training instances, Socratic-SWE reaches 50.40% on SWE-bench Verified, 36.67% on SWE-bench Lite, 22.85% on SWE-bench Pro, and 14.61% on Terminal-Bench 2.0.
- Compared with the Qwen3.5-9B base agent, it gains +7.80 points on SWE-bench Verified, +7.00 on Lite, +5.61 on Pro, and +4.50 on Terminal-Bench 2.0.
- The mean score across the four benchmarks is 31.13%, up from 24.91% for the base agent, a +6.22 point gain.
- On SWE-bench Verified, the strongest baseline SSR reaches a +4.40 point gain after 3 iterations, while Socratic-SWE reaches +7.80.
- In 5-iteration scaling on SWE-bench Verified, Socratic-SWE reaches 52.00% and SSR reaches 48.00%.
- Ablations on SWE-bench Verified at iteration 3 show drops to 48.00% without trace distillation and 48.60% when replacing GDPO with GRPO, versus 50.40% for the full system.

## Link
- [https://arxiv.org/abs/2606.07412v1](https://arxiv.org/abs/2606.07412v1)
