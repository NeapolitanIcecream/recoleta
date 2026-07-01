---
source: arxiv
url: https://arxiv.org/abs/2606.31958v1
published_at: '2026-06-30T17:00:33'
authors:
- Jagdeep Singh Bhatia
- Andrew Wagenmaker
- William Chen
- Sergey Levine
topics:
- vision-language-action
- generalist-robot-policy
- robot-rl
- prompt-optimization
- robot-data-scaling
- long-horizon-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Adapting Generalist Robot Policies with Semantic Reinforcement Learning

## Summary
SARL adapts VLA robot policies by training an RL policy over language prompts instead of robot motor actions. This matters because long-horizon tasks can fail under one zero-shot prompt even when the VLA already has the needed low-level skills.

## Problem
- Generalist robot policies often fail on complex, long-horizon tasks outside their pretraining distribution.
- Standard RL methods update or steer low-level robot actions, so they need the base policy action distribution to start near a good solution.
- VLM prompt selection can propose reasonable subcommands, but it does not know which prompts cause useful physical behavior on a given robot.

## Approach
- SARL treats each VLA language prompt as a semantic action.
- At each step, SARL selects a prompt, the VLA converts that prompt and the current observation into robot actions, and the environment returns reward and the next state.
- SARL learns a semantic Q-function with temporal-difference backups to score prompts by expected task progress.
- A VLM narrows the prompt search by proposing candidate semantic actions from the current image and the high-level task.
- Real-world interaction grounds each prompt in the behavior it induces, so the learned controller can sequence simple skills into a longer task.

## Results
- On Libero-10 and 4 real-world WidowX long-horizon tasks, SARL raises the base VLA from near 0% initial success under the task prompt to about 80% success after 60-100 online episodes.
- In Libero-10, SARL adapts successfully on 5 tasks, matches performance on 1 task that was already close to solved, and leaves 4 tasks unsolved by any tested method.
- The Libero-10 curves use 64 evaluations per plotted point and report standard error over 3 seeds.
- The real-world WidowX curves use 10 evaluations per plotted point.
- Compared baselines include DSRL, Residual RL, and an in-context-learning VLM prompt-selection method; the paper reports that SARL outperforms them on the tested long-horizon adaptation tasks.
- Real-world training uses 3 language-steered demonstrations per task seeded into SARL and Residual RL replay buffers; DSRL is evaluated without those demonstrations because its latent-noise action space cannot ingest them directly.

## Link
- [https://arxiv.org/abs/2606.31958v1](https://arxiv.org/abs/2606.31958v1)
