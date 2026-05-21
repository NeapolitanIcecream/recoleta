---
source: arxiv
url: https://arxiv.org/abs/2605.01950v1
published_at: '2026-05-03T16:19:45'
authors:
- Siyuan Duan
- Ke Zhang
- Xizhao Luo
topics:
- world-models
- backdoor-attacks
- trajectory-ranking
- reinforcement-learning-security
- visual-triggers
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# TRAP: Tail-aware Ranking Attack for World-Model Planning

## Summary
TRAP attacks world-model planners by changing how triggered observations rank imagined trajectories. It reports high attack success on DreamerV3 and TD-MPC2 with a deployment-time visual patch and no training-time poisoning or parameter changes.

## Problem
- World models choose actions by scoring many imagined futures, so shallow backdoor attacks on one-step predictions or policy outputs can be washed out by planning.
- A visual trigger that changes the ordering of top candidate trajectories can redirect long-horizon behavior while clean inputs remain mostly normal.
- This matters for robotics, autonomous driving, and other planned-control settings because a compromised planner can keep making bad decisions after a trigger appears.

## Approach
- The attacker uses white-box access to the target world model and optimizes a universal visual patch at inference time under a bounded perturbation budget.
- For each clean and triggered observation, the model imagines candidate trajectories and computes score changes between the two conditions.
- TRAP selects the high-score tail under clean planning because those trajectories drive action choice.
- A tail-aware ranking loss suppresses the scores of these selected trajectories, with a softmin aggregation across candidates to focus on hard-to-suppress trajectories.
- Two gates control optimization: a sign gate penalizes score increases, and a magnitude gate penalizes excessive suppression below a margin beta.

## Results
- With patch ratio 0.09 and epsilon 64, TRAP reaches 98.1 ± 0.8% ASR and 63.2 ± 0.9% mean return drop on DreamerV3 Crafter; the random patch baseline has 43.9 ± 8.4% ASR and -0.1 ± 3.5% mean drop.
- On DreamerV3 DMControl, TRAP reports 69.8 ± 0.7% drop and 100.0 ± 0.0% ASR on humanoid-walk, 22.8 ± 2.3% and 99.6 ± 0.5% on cheetah-run, 18.5 ± 1.5% and 100.0 ± 0.0% on walker-walk, and 9.8 ± 3.8% and 77.2 ± 3.7% on dog-run.
- On DreamerV3 Atari, TRAP reports 100.0 ± 0.0% ASR on seaquest, pong, breakout, and invaders, with mean return drops of 97.5 ± 0.8%, 164.5 ± 8.3%, 98.8 ± 0.7%, and 93.3 ± 1.8%.
- On TD-MPC2 DMControl, TRAP reports 100.0 ± 0.0% ASR on hopper-hop, cheetah-run, and walker-walk, with mean return drops of 99.8 ± 0.3%, 98.4 ± 0.4%, and 92.4 ± 0.9%.
- On TD-MPC2 walker-walk, TRAP improves over the random patch baseline from 1.9 ± 3.2% drop and 64.0 ± 2.5% ASR to 92.4 ± 0.9% drop and 100.0 ± 0.0% ASR.

## Link
- [https://arxiv.org/abs/2605.01950v1](https://arxiv.org/abs/2605.01950v1)
