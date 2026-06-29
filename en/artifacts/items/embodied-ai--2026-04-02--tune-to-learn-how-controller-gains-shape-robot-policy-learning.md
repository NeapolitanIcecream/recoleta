---
source: arxiv
url: http://arxiv.org/abs/2604.02523v1
published_at: '2026-04-02T21:23:08'
authors:
- Antonia Bronars
- Younghyo Park
- Pulkit Agrawal
topics:
- robot-learning
- controller-gains
- behavior-cloning
- reinforcement-learning
- sim2real
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# Tune to Learn: How Controller Gains Shape Robot Policy Learning

## Summary
This paper studies how low-level PD controller gains change robot policy learning. Its main claim is that gains should be chosen for learnability within a training setup, not by assuming they directly set task compliance.

## Problem
- Learned manipulation policies often run through position controllers, but gain selection is still treated as a classical control choice based on stiffness or compliance.
- That view misses how reactive policies work: the policy and controller together create the closed-loop behavior, so gains mainly change how easy the policy is to train and transfer.
- This matters for behavior cloning, reinforcement learning, and sim-to-real transfer because the same gain setting can help one pipeline and hurt another.

## Approach
- The paper reframes controller gains as an interface parameter and tests their effect across three settings: behavior cloning, RL from scratch, and zero-shot sim-to-real transfer.
- For behavior cloning, it builds controlled datasets with **Torque-to-Position Retargeting (TPR)** so trajectories stay close across gain settings while the position-command labels change with the gains.
- TPR converts torque demonstrations into position targets using the PD control equation, then replays them at policy rate to isolate the effect of gain-dependent action labels.
- For RL, it re-tunes action-space and training hyperparameters for each gain setting so poor results are less likely to come from mismatched hyperparameters.
- For sim-to-real, it performs gain-specific system identification, trains RL policies in the matched simulator, and evaluates zero-shot transfer on a real Franka robot, with domain-randomization and control-frequency ablations.

## Results
- **Behavior cloning:** Across several manipulation tasks and embodiments, the best closed-loop success concentrates in the **compliant, overdamped** gain regime; stiff or weakly damped gains reduce success. The excerpt does not provide exact per-task success numbers from the heatmaps.
- **TPR fidelity:** Retargeted trajectories keep **>=90% success** and **joint-position MSE < 1e-3** across gain settings up to **25x decimation (20 Hz)**.
- **Teleoperation study:** The user study includes **12 users**, **1-hour sessions**, and **1,297 total trials** on a box-pushing task. The excerpt states that results are reported later, but it does not include the numeric outcome table here.
- **Reinforcement learning:** The paper claims RL can reach successful policies in **all tested gain regimes** when hyperparameters are tuned to match the gain setting, across manipulation and locomotion tasks. The excerpt does not include final success percentages or reward numbers.
- **Sim-to-real:** The paper claims **stiff and overdamped** gains worsen motor-level sim-to-real transfer, while transfer is evaluated over **30 real-world rollouts** per gain setting using state-trajectory MSE. The excerpt does not include the final MSE values.
- **Data practice observation:** By analyzing DROID and Open X-Embodiment datasets, the authors report that existing datasets appear to use **stiff tracking behavior** as a default, based on command-following curves rather than published gain values.

## Link
- [http://arxiv.org/abs/2604.02523v1](http://arxiv.org/abs/2604.02523v1)
