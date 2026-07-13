---
source: arxiv
url: https://arxiv.org/abs/2607.09648v1
published_at: '2026-07-10T17:46:32'
authors:
- Xiaoshen Han
- Haoyu Xiong
- Haonan Chen
- Chaoqi Liu
- Antonio Torralba
- Yuke Zhu
- Yilun Du
topics:
- robot-policy
- fast-manipulation
- action-representation
- trajectory-smoothing
- imitation-learning
- temporal-rescaling
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations

## Summary
B-spline Policy replaces fixed discrete action chunks with continuous B-spline action curves that can be sampled at high frequency and executed at different speeds. Real-robot tests show shorter completion times with comparable or improved success rates, although excessive speedup can exceed controller limits.

## Problem
- Visuomotor policies often complete manipulation tasks much more slowly than humans; the paper cites roughly 60 seconds for robots versus roughly 10 seconds for humans folding a T-shirt.
- Fixed-length action chunks use the same temporal resolution throughout a task and can create discontinuities when consecutive chunks are joined.
- These issues become more damaging at high execution speeds, where sparse or discontinuous commands can cause tracking errors and task failure.

## Approach
- Fit cubic B-splines to demonstration trajectories, placing more knots in high-curvature regions and fewer knots in smooth regions.
- Train standard imitation-learning policies to predict local spline parameters, including control points and knots, instead of discrete action sequences.
- Sample each continuous curve at a high low-level control frequency and change execution speed with temporal rescaling, without retraining the policy for each speed.
- Align each new predicted spline segment with the last executed action by finding the point on the new curve with the smallest action mismatch.
- Integrate the representation with Diffusion Policy and ACT-style regression policies as a drop-in replacement for standard action chunking.

## Results
- In real-world Cube Picking, Diffusion+BSP at 4X achieved 20/20 success in 2.45 seconds, compared with 20/20 in 3.52 seconds for the 4X Diffusion baseline. Regression+BSP at 4X achieved 19/20 in 2.08 seconds, compared with 19/20 in 3.74 seconds for the baseline.
- In long-horizon Table Cleaning, Regression+BSP at 4X reduced average completion time from 23.57 seconds to 11.80 seconds, a 50% reduction, while success changed from 13/20 to 14/20.
- On Speed Stacking, Regression+BSP improved success from 8/20 to 16/20 at 1X and from 4/20 to 13/20 at 2X, with completion times of 17.61 and 10.98 seconds respectively.
- Across diffusion and regression comparisons, BSP matched or improved success rate in 14 of 18 settings and generally reduced completion time.
- At aggressive speedup, performance can collapse: Regression+BSP achieved 0/20 on Speed Stacking at 4X, which the paper attributes to low-level controller tracking limits.
- Simulation results on Push-T, RoboMimic, and RoboCasa show similar or higher success rates in the reported tasks; for example, Diffusion+BSP improved Turn off microwave from 77% to 89% and Close door from 27% to 46%.

## Link
- [https://arxiv.org/abs/2607.09648v1](https://arxiv.org/abs/2607.09648v1)
