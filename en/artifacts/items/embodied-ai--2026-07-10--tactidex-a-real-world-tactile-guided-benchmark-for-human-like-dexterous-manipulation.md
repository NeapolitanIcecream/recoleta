---
source: arxiv
url: https://arxiv.org/abs/2607.09190v1
published_at: '2026-07-10T08:32:19'
authors:
- Suting Ni
- Hanbing Zhang
- Zhenyu Wei
- Guo Chen
- Chixuan Zhang
- Ye Shi
- Jingya Wang
topics:
- dexterous-manipulation
- tactile-sensing
- robot-data-scaling
- sim2real
- human-to-robot-transfer
- robot-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# TactiDex: A Real-World Tactile-Guided Benchmark for Human-Like Dexterous Manipulation

## Summary
TactiDex is a real-world benchmark for transferring human dexterous manipulation to robots with tactile supervision, rather than relying only on motion trajectories. TactiSkill uses synchronized human pressure data to train robotic hands to form contacts and regulate forces more like humans.

## Problem
- Human-to-robot dexterous transfer often matches hand and object motion while ignoring contact timing, force distribution, and grasp stability.
- Existing hand-object interaction datasets rarely combine real tactile measurements with precise hand and object motion, which limits physically grounded policy learning.
- This gap matters because trajectory matching can produce unstable grasps, excessive force, or physically implausible interaction during contact-rich tasks.

## Approach
- TactiDex records whole-hand pressure maps, articulated hand kinematics, wrist and object 6D poses, task phases, and text descriptions in synchronized real-world demonstrations.
- The dataset contains 5.1 million frames from 757 single-hand and bimanual sequences involving 49 calibrated objects and 10 subjects.
- TactiSkill starts with a frozen kinematic imitation policy and learns a residual policy that adjusts joint commands to regulate contact forces.
- Its tactile reward combines contact-event guidance, alignment with human finger-force patterns, and penalties for forces above a human-derived safety limit.
- An asymmetric Actor-Critic setup gives the critic simulated contact forces during training while the actor uses the human tactile reference available for deployment; the resulting policy is tested through sim-to-real transfer.

## Results
- The benchmark provides whole-hand tactile sensing through 162 pressure elements, with force resolution up to 0.01 N and a sampling rate of 17 Hz, synchronized with 120 Hz motion and pose streams.
- TactiDex combines real-world tactile data, high-precision kinematics, text annotations, and long-horizon bimanual manipulation; the comparison table lists 5.1M frames, 49 objects, and 757 sequences for the dataset.
- The paper claims higher manipulation success, contact fidelity, physical realism, geometric robustness, and interaction stability than kinematic-only transfer methods across single-hand and bimanual tasks.
- The provided excerpt does not include the experiment table's numerical success rates, metric values, dataset splits, or baseline comparisons, so it does not support a quantified performance improvement.
- The authors report real-world deployment on dexterous robotic hardware, including stable contact-rich manipulation and zero-shot sim-to-real transfer, but the excerpt gives no numerical hardware success rate.

## Link
- [https://arxiv.org/abs/2607.09190v1](https://arxiv.org/abs/2607.09190v1)
