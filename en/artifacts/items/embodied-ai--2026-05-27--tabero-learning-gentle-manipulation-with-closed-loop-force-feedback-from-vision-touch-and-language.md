---
source: arxiv
url: https://arxiv.org/abs/2605.27886v1
published_at: '2026-05-27T03:08:21'
authors:
- Qiwei Wu
- Rui Zhang
- Xin Xiang
- Tao Li
- Weihua Zhang
- Junjie Lai
- Renjing Xu
topics:
- vision-language-action
- tactile-sensing
- force-control
- gentle-manipulation
- robot-data-scaling
- robot-benchmark
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language

## Summary
Tabero adds touch and closed-loop force control to VLA-style robot policies for gentle manipulation. It claims over 70% lower average grip force under gentle instructions while preserving high task success on its benchmark.

## Problem
- VLA policies usually use images and language but lack tactile feedback, so they can complete a task while squeezing, striking, or damaging objects.
- Aligned vision-touch-language robot data is scarce because real tactile data collection needs specialized hardware and slow maintenance.
- Standard robot benchmarks measure success rate and miss contact quality, such as peak grip force and applied force.

## Approach
- Tabero replays open-source manipulation trajectories, including LIBERO-style tasks, inside Isaac Lab with a tactile gripper to generate synchronized vision, touch, force, proprioception, action, and language data.
- The simulator records wrist and third-person RGB-D views, simulated GelSight tactile images at 320 × 240, an 11 × 9 marker displacement grid, and fingertip contact forces at 20 Hz.
- The data pipeline varies gripper stiffness and damping, such as Kp = 2000, 500, 200 N/m and Kd = 100, 25, 10 N·s/m, then pairs low-force trials with words such as “gently” and high-force trials with words such as “firmly.”
- Tabero-VTLA encodes tactile marker motion or tactile images as tokens, predicts both pose and force targets, and sends them to a fixed hybrid controller.
- The controller separates grip force from applied object force, then uses force feedback to adjust gripper width and end-effector position during execution.

## Results
- The abstract reports over 70% lower average grip force under gentle instructions while maintaining high task success; the excerpt does not provide the exact success rate for that comparison.
- Cross-platform replay keeps average task success close to the source setup: MuJoCo averages 0.85 across four LIBERO subtasks, while Isaac replay with the same robot setup averages 0.76.
- With the tactile-equipped Franka gripper, average data retention drops as force is reduced: 0.60 at T-100, 0.50 at T-25, and 0.36 at T-10.
- Spatial tasks show the largest force sensitivity in Table 1: success falls from 0.83 in Isaac replay to 0.42 at T-100, 0.24 at T-25, and 0.07 at T-10.
- Object tasks remain more stable under reduced force: 0.77 in Isaac replay, 0.84 at T-100, 0.87 at T-25, and 0.73 at T-10.
- The benchmark evaluates contact quality with four force metrics: maximum transient grip force, average grip force, maximum transient applied force, and average applied force.

## Link
- [https://arxiv.org/abs/2605.27886v1](https://arxiv.org/abs/2605.27886v1)
