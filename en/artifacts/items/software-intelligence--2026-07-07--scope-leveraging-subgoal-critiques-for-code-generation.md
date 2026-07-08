---
source: arxiv
url: https://arxiv.org/abs/2607.05810v1
published_at: '2026-07-07T04:09:41'
authors:
- Yueke Zhang
- Yifan Zhang
- Zihan Fang
- Kevin Leach
- Wei Zhang
- Yu Huang
topics:
- code-generation
- code-intelligence
- llm-feedback
- program-repair
- formal-methods
- software-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# SCOPE: Leveraging Subgoal Critiques for Code Generation

## Summary
SCOPE improves code generation by using a prover-trained critic to spell out missing semantic requirements before the coder revises its program. It reports higher pass@1 than coder-only, Self-Refine, and Reflexion baselines on LiveCodeBench V6 and BigCodeBench Hard.

## Problem
- LLM-generated code can look correct while missing constraints in the prompt, such as edge cases, invariants, API limits, or input rules.
- Test feedback often says that a program failed, but it may not identify which semantic obligation the code violated.
- This matters because developers cannot write exhaustive tests for open-ended coding tasks, and weak feedback can lead models to make broad edits that miss the actual bug.

## Approach
- SCOPE uses two models: a frozen Qwen3-Coder-30B coder and a critic initialized from DeepSeek-Prover-V2-7B.
- The critic reads the problem and the draft code, then emits three parseable fields: subgoals, gap analysis, and a robustness checklist.
- Supervised fine-tuning trains the critic on 528 critique-guided tuples built from LiveCodeBench V1-V3, with DeepSeek-V3 used to create teacher critiques.
- Reinforcement learning uses GRPO with two rewards: a dense reward for critique quality and semantic alignment, and a sparse reward based on whether the critique improves execution score after the coder revises the draft.
- At inference time, the coder writes an initial solution, the critic identifies missing obligations, and the coder revises the solution using that critique.

## Results
- On LiveCodeBench V6, SCOPE reaches 39.4% pass@1, compared with 36.6% for Reflexion, 33.1% for Self-Refine, and 20.6% for coder-only generation.
- On BigCodeBench Hard, SCOPE reaches 42.6% pass@1, compared with 36.5% for Reflexion and 34.5% for coder-only generation.
- The paper reports that SCOPE rescues 19 failed solutions, compared with 16 for Reflexion.
- For bug-triggered localization, SCOPE has 42.1% localized wins within 20 lines, compared with 31.3% for Reflexion.
- SCOPE makes smaller repairs, with 28.0 median changed lines versus 35.0 for Reflexion.
- The reported gains are strongest on tasks with concrete semantic constraints, where explicit subgoals can point the coder to a specific missing condition.

## Link
- [https://arxiv.org/abs/2607.05810v1](https://arxiv.org/abs/2607.05810v1)
