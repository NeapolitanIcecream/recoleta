---
source: arxiv
url: https://arxiv.org/abs/2607.08837v1
published_at: '2026-07-09T18:00:24'
authors:
- Sunshine Jiang
- John Marangola
- David Zhang
- Raghuram Kowdeed
- Ruiyang Luo
- Nitish Dashora
- Richard Li
- Pulkit Agrawal
- Zhang-Wei Hong
topics:
- robot-foundation-model
- vision-language-action
- prompt-exploration
- sparse-reward-rl
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Prompt-Driven Exploration

## Summary
Prompt-Driven Exploration (PDE) explores robot behavior by changing the language prompt instead of adding only action noise. A vision-language model rewrites prompts from rollout videos, helping reinforcement learning find successful behaviors when the initial policy has near-zero reward.

## Problem
- Sparse binary rewards leave weak vision-language-action policies with no successful trajectories to reinforce, especially on difficult manipulation tasks.
- Action-space noise changes individual actions locally, so it rarely escapes a policy that follows the wrong strategy across an entire episode.
- The problem matters for fine-tuning generalist robot policies from limited demonstrations, where initial success can be close to 0%.

## Approach
- PDE samples alternative prompts for the same task and keeps the prompt fixed during each rollout, creating globally different behavior modes.
- A vision-language model watches rollout videos, diagnoses failures, and proposes revised prompts without updating model weights during prompt search.
- The method treats the prompt sampler as an implicit posterior over useful policy behaviors and updates it with task outcomes and trajectory history.
- Proximal Policy Optimization trains on exploratory and canonical prompts through mixture sampling and mixed backpropagation, transferring useful behavior back to the canonical task prompt.

## Results
- In a microwave-closing case study, prompt search found 10-12 successful prompt variants within 85 cumulative rollouts; the best prompts reached below 40% success before policy training.
- PDE increased success on the original canonical prompt from 0% to approximately 98% by training step 100, while standard action-noise PPO stayed near zero.
- On LIBERO-PRO, PDE outperformed all tested baselines across hard, medium, and easy tiers, with a 60% relative improvement on the hard tier of 47 tasks.
- The benchmark covered 120 LIBERO-PRO tasks and evaluated success over 250 environments per task; PDE also improved learning over action noise with GR00T and Pi0 backbones.
- The paper reports broader gains on ManiSkill manipulation tasks and challenging LLM coding tasks, supporting use beyond one robot benchmark.

## Link
- [https://arxiv.org/abs/2607.08837v1](https://arxiv.org/abs/2607.08837v1)
