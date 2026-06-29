---
source: arxiv
url: https://arxiv.org/abs/2606.13677v1
published_at: '2026-06-11T17:59:49'
authors:
- Zhao-Heng Yin
- Guanya Shi
- Pieter Abbeel
- C. Karen Liu
topics:
- dexterous-manipulation
- sim-to-real
- articulated-tools
- robot-policy-learning
- trajectory-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Mana: Dexterous Manipulation of Articulated Tools

## Summary
Mana solves dexterous manipulation of thin articulated tools by turning data generation into a coarse-to-fine animation pipeline, then training a visuomotor policy on the simulated trajectories. It matters because the paper targets tabletop grasping and in-hand actuation for tools like tongs, pliers, clothespins, and syringes, which are hard to control with teleoperation or end-to-end RL.

## Problem
- Articulated tools need stable grasping and forceful actuation at the same time, often with millimeter-scale contact sensitivity and 3-7 N actuation forces.
- Position-based teleoperation cannot reliably create the contact forces needed for thin tools, and RL from scratch has trouble finding the right contact points and force directions.
- The task includes both acquisition from the table and in-hand manipulation, so the policy must handle long-horizon behavior, not just a fixed in-hand grasp.

## Approach
- Users click functional affordance regions on each tool mesh in under 1 minute per tool.
- The system generates grasp keyframes first, then connects them with motion planning for free-space moves and short-horizon reinforcement learning for contact-rich phases.
- It splits episodes into pre-grasping, grasping, and in-hand actuation, which keeps RL focused on the hard force-control parts.
- It trains a point-cloud-conditioned diffusion policy on the simulated trajectories, using segmented RGB-D point clouds plus robot proprioception to output wrist and finger actions.
- It adds point-cloud noise and part masking during training to improve transfer from simulation to the real robot.

## Results
- The paper reports zero-shot sim-to-real transfer on 4 articulated tool types: tongs, pliers, clothespins, and syringes.
- On 2 instances per tool type, the full method reaches about 0.6-0.8 success per 10 trials across grasping, opening, closing, and use, for example 0.8 on tongs grasp/open, 0.7 on pliers grasp/open/close, and 0.6-0.8 on clothespins tasks.
- Teleoperation with GeoRT performs much worse, often at 0.0-0.3 success; on tongs grasp/open/close it is 0.3/0.1/0.3 for one instance and 0.3/0.2/0.3 for the other.
- The open-loop baseline is also lower, usually around 0.1-0.7 depending on the task, and drops to 0.0-0.3 on the syringe tasks.
- For composed end-to-end tool-use tasks, the paper reports 7/10 tong pick, 5/10 plier cut, 6/10 clothespin use, and 5/10 syringe inject.
- The ablation claims performance improves with more trajectories, more grasp keyframes, and stronger force/action randomization, but it does not give exact ablation numbers in the excerpt.

## Link
- [https://arxiv.org/abs/2606.13677v1](https://arxiv.org/abs/2606.13677v1)
