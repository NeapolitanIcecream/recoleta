---
kind: ideas
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
run_id: 965aa45a-9904-41d6-8b72-237b0186a6e9
status: succeeded
topics:
- robot learning
- vision-language-action models
- reinforcement learning
- humanoid manipulation
- tactile sensing
- world models
- robot safety
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/world-models
- topic/robot-safety
language_code: en
pass_output_id: 325
pass_kind: trend_ideas
upstream_pass_output_id: 324
upstream_pass_kind: trend_synthesis
---

# Robot manipulation control and safety layers

## Summary
Robot VLA deployment work is getting more concrete around three operating needs: contact correction during manipulation, online adaptation after a policy misses a long-horizon task, and safety evaluation that records physical damage separately from task success. The most actionable changes are small control and evaluation layers around existing policies, with clear episode counts, perturbation tests, and simulator checks.

## Tactile residual correction for insertion, wiping, adjustment, and assembly tasks
Manipulation teams working on contact-heavy tasks can add a tactile correction loop around an existing VLA policy before retraining the whole policy. UniTacVLA gives a concrete version: encode current tactile state, predict near-future tactile latents, and let a lightweight Transformer add a bounded residual correction to the planned action at higher frequency than the VLA action chunks.

The cheap validation is a perturbed contact test on a few tasks where vision loses the contact point: USB insertion, wiping, alignment adjustment, or small assembly. UniTacVLA reports 64.0% clean success and 53.5% perturbed success across eight real-robot subtasks, while the reproduced pi0.5-TacVLA baseline reaches 45.25% clean and 16.25% perturbed. Its USB ablation also separates the contribution of tactile input, tactile chain-of-thought supervision, future tactile prediction, and the residual controller, which gives implementers a practical order for testing components.

### Sources
- [UniTacVLA: Unified Tactile Understanding and Prediction in Vision Language Action Models](../Inbox/2026-06-30--unitacvla-unified-tactile-understanding-and-prediction-in-vision-language-action-models.md): Describes UniTacVLA's tactile tokens, future tactile prediction, high-frequency correction controller, perturbation results, and USB insertion ablation.

## Prompt-level reinforcement learning for long-horizon VLA task recovery
A robot team with a capable base VLA can test online adaptation at the language-command layer. SARL treats prompts as semantic actions: a controller chooses a short language instruction, the VLA executes it, and reward updates a semantic Q-function over prompts. This is suited to long-horizon failures where the robot has useful primitive skills but the single task prompt leaves it stuck.

A practical pilot would seed three language-steered demonstrations for a task, run online episodes, and compare success under the fixed task prompt against learned prompt sequencing. SARL reports near-zero initial success under the task prompt and about 80% success after 60 to 100 online episodes on Libero-10 and four real WidowX long-horizon tasks. Z-1 adds a related simulation-side check for flow-based VLA policies: after supervised fine-tuning on public RoboCasa demonstrations, GRPO raises average success on 24 RoboCasa tasks from 67.4% to 80.6%.

### Sources
- [Adapting Generalist Robot Policies with Semantic Reinforcement Learning](../Inbox/2026-06-30--adapting-generalist-robot-policies-with-semantic-reinforcement-learning.md): Shows SARL's prompt-as-action adaptation loop, use of demonstrations, and online episode results on Libero-10 and WidowX tasks.
- [Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models](../Inbox/2026-06-30--z-1-efficient-reinforcement-learning-for-vision-language-action-models.md): Shows RL post-training for a flow-based VLA policy and the controlled 13.2-point gain over the authors' SFT initialization.

## Damage-aware simulation checks for household manipulation policies
Household robot evaluators can add a damage score alongside task success before moving a policy into real kitchens or living rooms. OopsieVerse gives a concrete template through DamageSim and OopsieBench: keep per-object and per-robot-link health on a 0 to 100 scale, reduce health when mechanical, thermal, or fluid damage evaluators fire, and report damage separately from completion.

This is most useful for tasks with unsafe shortcuts, such as pushing through fragile objects, contacting hot surfaces, spilling liquid, or overloading robot links. OopsieBench covers 32 task instances across OmniGibson and RoboCasa, and DamageSim is implemented across Nvidia Omniverse and MuJoCo-based stacks. The supplied evidence supports the evaluation workflow more than a policy improvement claim, so the first adoption step is a gate in simulation: pass the task and stay under a damage threshold.

### Sources
- [OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation](../Inbox/2026-06-30--oopsieverse-a-safety-benchmark-with-damage-aware-simulation-for-robot-manipulation.md): Defines DamageSim, OopsieBench, per-object health, damage classes, simulator coverage, and the benchmark scope.
- [OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation](../Inbox/2026-06-30--oopsieverse-a-safety-benchmark-with-damage-aware-simulation-for-robot-manipulation.md): Explains the gap in standard manipulation benchmarks that score completion without measuring damage caused during execution.
