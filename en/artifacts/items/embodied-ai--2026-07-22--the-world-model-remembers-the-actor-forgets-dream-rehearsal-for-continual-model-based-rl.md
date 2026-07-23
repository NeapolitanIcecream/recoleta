---
source: arxiv
url: https://arxiv.org/abs/2607.19749v1
published_at: '2026-07-22T04:46:49'
authors:
- Gurp Nijjer
topics:
- continual-reinforcement-learning
- model-based-reinforcement-learning
- world-models
- policy-rehearsal
- imagination-based-learning
- catastrophic-forgetting
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# The World Model Remembers, the Actor Forgets: Dream Rehearsal for Continual Model-Based RL

## Summary
The paper argues that, in DreamerV3-style continual model-based reinforcement learning, replay preserves the world model while the actor forgets how to use it. It introduces graded dream rehearsal, which trains the actor by behavior-cloning high-scoring imagined trajectories and retains skills without task labels, new parameters, or additional environment interaction during rehearsal.

## Problem
- DreamerV3 agents can catastrophically forget earlier tasks during sequential training, even with an unbounded replay buffer.
- Standard return-based evaluation cannot show whether forgetting comes from degraded world-model knowledge, representations, or actor behavior.
- The problem matters because protecting replayed experience and world-model accuracy does not necessarily preserve executable skills.

## Approach
- Probe DreamerV3 components on MiniGrid task chains using three seeds, comparing retained reward discrimination, value estimates, termination predictions, representations, and actor behavior.
- Isolate the recovery channel by freezing the world model and training the actor either with standard imagination-based reinforcement learning or supervised self-imitation.
- Use graded dream rehearsal: start imagined rollouts from buffered states, score them with the world model's reward, continuation, and value heads, and behavior-clone the top 25% with one shared actor.
- Apply a realized-first, termination-aware grading rule so achieved rewards outrank critic-only promises and post-terminal model predictions do not contaminate selection.

## Results
- Under never-clear replay, reward discrimination for the forgotten task had retention ratios of 0.99, 1.06, and 1.01; critic values rose from 0.84 to 0.91, and termination discrimination remained 0.95–1.0, while actor behavior still collapsed.
- With the world model frozen and identical imagined data, standard RL-in-imagination recovered the lost skill in 0/3 seeds; supervised self-imitation recovered it in 3/3 seeds after 2,000–7,500 updates with zero new environment steps.
- On four-task MiniGrid chains, dream rehearsal passed all tasks in 3/3 seeds versus 0/3 for plain replay; the historically weakest task averaged 0.824 retention, compared with 0.62 ± 0.13 for the stored-policy isolation reference.
- Dream rehearsal outperformed matched competent-filtered real-episode cloning on the weakest task: mean retention 0.815 versus 0.684, paired difference +0.131, bootstrap 95% CI [0.073, 0.238], with 3/3 all-task passes for both methods.
- The corrected grading rule achieved selection AUC 1.0 and top-quartile purity 1.0 on both tested task profiles, and the eight-task chain retained all tasks in 3/3 seeds; the study uses a 17M-parameter agent on MiniGrid, so larger-domain generalization remains untested.

## Link
- [https://arxiv.org/abs/2607.19749v1](https://arxiv.org/abs/2607.19749v1)
