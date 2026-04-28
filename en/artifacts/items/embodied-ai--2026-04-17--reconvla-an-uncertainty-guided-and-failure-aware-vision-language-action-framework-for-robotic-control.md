---
source: arxiv
url: http://arxiv.org/abs/2604.16677v1
published_at: '2026-04-17T20:20:43'
authors:
- Lingling Chen
- Zongyao Lyu
- William J. Beksi
topics:
- vision-language-action
- robot-reliability
- uncertainty-estimation
- conformal-prediction
- failure-detection
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control

## Summary
ReconVLA adds calibrated uncertainty estimates and runtime failure checks to a frozen vision-language-action policy. It aims to make robot control safer by scoring action reliability and flagging unsafe states before execution fails.

## Problem
- Vision-language-action models can generate robot actions from images and language, but they usually do not report calibrated confidence for those actions.
- This matters in real robot control because distribution shift, ambiguous observations, and stochastic action generation can lead to failures with no warning signal.
- The paper targets two uncertainty sources: input uncertainty that pushes the robot into unfamiliar states, and noise uncertainty from stochastic generative action sampling.

## Approach
- The method wraps a pretrained, frozen VLA policy instead of retraining it or changing its weights.
- For action uncertainty, it samples multiple candidate actions from the generative policy under different noise draws and applies conformal quantile regression to the action tokens to build calibrated prediction intervals.
- It uses those intervals as a confidence signal and selects the action candidate with lower predicted uncertainty for execution.
- For state failure detection, it tracks the robot's state in a learned feature space and measures deviation from training-time safe-state statistics with a Mahalanobis-distance-based detector.
- If the runtime state exceeds a safety threshold, the system flags a likely out-of-distribution or unsafe condition and can trigger a halt or fallback.

## Results
- The abstract claims the method was tested in both simulation and real-robot manipulation experiments across diverse tasks.
- It claims calibrated uncertainty estimates on action predictions that correlate with execution quality and task success.
- It claims better failure anticipation, fewer catastrophic errors, and improved reliability during deployment versus the underlying VLA without uncertainty guidance.
- The provided excerpt does not include quantitative tables or exact numbers for success rate, calibration error, datasets, or baseline margins, so no verified numeric improvement can be reported from this text alone.
- It also claims these gains come without retraining or modifying the base VLA policy.

## Link
- [http://arxiv.org/abs/2604.16677v1](http://arxiv.org/abs/2604.16677v1)
