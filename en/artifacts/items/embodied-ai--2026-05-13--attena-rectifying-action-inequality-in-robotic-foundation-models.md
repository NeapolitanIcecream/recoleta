---
source: arxiv
url: https://arxiv.org/abs/2605.13548v1
published_at: '2026-05-13T13:55:37'
authors:
- Daojie Peng
- Fulong Ma
- Jiahang Cao
- Qiang Zhang
- Xupeng Xie
- Jian Guo
- Ping Luo
- Andrew F. Luo
- Boyu Zhou
- Jun Ma
topics:
- vision-language-action
- robot-foundation-models
- world-action-models
- manipulation-policy
- loss-weighting
- robot-data-scaling
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# AttenA+: Rectifying Action Inequality in Robotic Foundation Models

## Summary
AttenA+ improves robot foundation model training by giving higher loss weight to slow, precision-heavy action steps. It reports small but consistent success-rate gains on Libero and RoboTwin 2.0 without changing model backbones.

## Problem
- VLA and WAM models usually give every action timestep the same loss weight, although grasping, aligning, and placing are more error-sensitive than fast approach motions.
- This matters because last-centimeter errors can fail long-horizon manipulation tasks, even when most of the trajectory is correct.

## Approach
- Compute instantaneous velocity magnitude from the ground-truth action. On Libero, the method uses continuous motion dimensions and omits the binary gripper state.
- Convert velocity into a training weight: low velocity gets a larger weight, and high velocity gets a lower weight.
- Test four velocity-to-weight mappings: inverse, inverse squared, exponential decay, and logarithmic.
- Apply the weights to the existing training loss, such as weighted L1 loss for OpenVLA-OFT and weighted flow-matching loss for pi-style generative policies.
- Clip and optionally normalize weights so near-static steps do not control the gradient and the average loss scale stays close to the baseline.

## Results
- On Libero, AttenA+OFT reaches 98.60% average success rate versus 97.10% for OpenVLA-OFT, a +1.50 point gain. Average error rate drops from 2.90% to 1.40%.
- Libero task scores for AttenA+OFT are 99.0% ± 0.16 on Spatial, 100.0% ± 0.00 on Object, 98.8% ± 0.28 on Goal, and 96.6% ± 0.30 on the 10-task long-horizon split.
- Against OpenVLA-OFT on Libero, gains are +1.4 points on Spatial, +1.6 on Object, +0.9 on Goal, and +2.1 on long-horizon tasks.
- With the generative pi-0.5 backbone on Libero, AttenA+pi-0.5 reaches 97.95% average success rate versus 96.85%, a +1.10 point gain. Average error rate drops from 3.15% to 2.05%.
- On RoboTwin 2.0, AttenA+WAM reaches 92.46% average success rate versus 91.80% for Fast-WAM and 92.20% for LingBot-VA. It reports 93.06% on Clean and 91.86% on Randomized.
- The paper also claims real-world validation on a Franka manipulator and cross-task generalization, but the excerpt gives no concrete real-world success-rate numbers.

## Link
- [https://arxiv.org/abs/2605.13548v1](https://arxiv.org/abs/2605.13548v1)
