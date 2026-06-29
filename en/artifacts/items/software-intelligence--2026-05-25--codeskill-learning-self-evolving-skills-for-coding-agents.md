---
source: arxiv
url: https://arxiv.org/abs/2605.25430v1
published_at: '2026-05-25T05:12:49'
authors:
- Yanzhou Li
- Yiran Zhang
- Xiaoyu Zhang
- Xiaoxia Liu
- Yang Liu
topics:
- coding-agents
- skill-learning
- procedural-memory
- reinforcement-learning
- software-engineering-agents
- swe-bench
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# CODESKILL: Learning Self-Evolving Skills for Coding Agents

## Summary
CODESKILL trains a small LLM to turn coding-agent trajectories into reusable skills and keep a compact skill bank. The claimed gain is higher pass rate for frozen coding agents without changing the coding agent itself.

## Problem
- Coding agents leave long action traces while fixing repositories or working in terminals, but raw traces are too large and task-specific to reuse directly.
- Existing skill and memory methods often use fixed prompts or hand-written update rules, so they can keep weak, redundant, or over-specific knowledge.
- This matters because a better skill bank can improve future software-engineering tasks while leaving the main coding model frozen.

## Approach
- CODESKILL learns a skill-management policy from trajectories. It outputs operations that generate a new skill, revise an existing skill, add a candidate, merge it with another skill, or drop it.
- Each skill is a markdown instruction with a title, trigger condition, and actionable steps for the coding agent.
- The skill bank has task-level skills for broad repair workflows and event-driven skills for local events such as command failures, test errors, or repeated failure modes.
- Training starts with supervised targets from teacher models, then uses GRPO reinforcement learning.
- The RL reward combines rubric-based skill quality, verifier-based execution improvement, and an alignment score that checks whether the coding agent actually used the skill.

## Results
- With Qwen3.5-35B-A3B as the frozen coding policy, CODESKILL reached 39.26 average success across EnvBench-Python, EnvBench-Java, SWE-Bench Verified, and Terminal-Bench 2, compared with 29.57 for no-skill and 35.25 for the strongest prompt or memory baseline.
- The same setting reduced average solved-instance steps to 35.15, compared with 44.12 for no-skill and 36.99 for the strongest prompt or memory baseline.
- Per-benchmark success with Qwen3.5-35B-A3B was 18.60 on EnvBench-Python versus 6.98 no-skill, 38.32 on EnvBench-Java versus 27.10, 66.00 on SWE-Bench Verified versus 57.33, and 34.12 on Terminal-Bench 2 versus 25.88.
- With GPT-5.4-mini as the frozen coding policy, CODESKILL reached 30.73 average success, compared with 21.80 for no-skill and 27.86 for the strongest prompt or memory baseline.
- The abstract reports an average pass-rate gain of 9.69 points over no-skill and 4.01 points over the strongest prompt-based or memory baseline, equal to about 33% and 11% relative gains.
- In the lifecycle ablation, the full system kept 676 skills, compared with 1252 skills for extraction-only and extraction-plus-evolution variants, while preserving 39.26 average success in the Qwen3.5-35B-A3B setting.

## Link
- [https://arxiv.org/abs/2605.25430v1](https://arxiv.org/abs/2605.25430v1)
