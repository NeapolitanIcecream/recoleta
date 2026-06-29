---
source: arxiv
url: https://arxiv.org/abs/2605.29605v1
published_at: '2026-05-28T08:42:12'
authors:
- Dehao Huang
- Aoxiang Gu
- Chengjie Zhang
- Bolin Zou
- Wenlong Dong
- Zilang Cen
- Yue Wang
- Hong Zhang
topics:
- vision-language-action
- robot-confidence
- uncertainty-calibration
- failure-detection
- manipulation
- libero
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# VLAConf: Calibrated Task-Success Confidence for Vision-Language-Action Models

## Summary
VLAConf estimates task-success confidence for VLA robot policies with a success-only confidence head trained on frozen VLA features. It targets faster confidence queries and support for both discrete-action and continuous-action VLA backbones.

## Problem
- Robots need an online estimate of whether the current manipulation rollout will succeed, so they can stop, recover, roll back, or ask for help before a failure completes.
- Existing VLA confidence methods often use prompt ensembles or action-token probabilities, which add repeated inference cost and fit discrete-action models better than continuous-action models.
- Failure rollouts are costly and unsafe to collect, so the paper focuses on learning the confidence signal mainly from successful demonstrations.

## Approach
- VLAConf freezes the pretrained VLA and pools its visual and language hidden states, then fuses them with proprioceptive state through small MLPs.
- A Coin-Flip Network head is trained on successful rollout steps only. Its output norm becomes an anomaly score: familiar successful states tend to get lower scores, and unusual states tend to get higher scores.
- The anomaly head is conditioned on rollout step using a learned step embedding plus a normalized progress value, with FiLM-style modulation and a residual gate.
- Step scores are aggregated over the observed prefix, then Platt scaling maps the scalar score to a task-success probability using a small set of completed rollouts with binary outcomes.

## Results
- On standard LIBERO with OpenVLA-OFT, VLAConf reaches pre-execution ECE 0.0340, Brier 0.1614, and NLL 0.4991, compared with ConfidenceVLA at ECE 0.0363, Brier 0.1702, and NLL 0.5295.
- For OpenVLA-OFT online execution, VLAConf reports Brier 0.1073 and NLL 0.3335, better than ConfidenceVLA at Brier 0.1647 and NLL 0.5041, while its ECE is worse at 0.1188 versus 0.0276.
- VLAConf is much faster than ConfidenceVLA on OpenVLA-OFT: 64.9 ms average inference time versus 712.9 ms, about 11x faster.
- On the continuous-action π^0.5 backbone, ConfidenceVLA is not reported because it depends on action-token probabilities; VLAConf reports pre-execution ECE 0.0370, Brier 0.0821, and NLL 0.3141.
- On π^0.5 online execution, VLAConf reports ECE 0.0515, Brier 0.0668, and NLL 0.2501, compared with VLAConf-NoStep at ECE 0.0448, Brier 0.0884, and NLL 0.3261.
- Reported policy success rates are 78.2% for OpenVLA-OFT with VLAConf and 91.3% for π^0.5 with VLAConf on the averaged standard LIBERO suites.

## Link
- [https://arxiv.org/abs/2605.29605v1](https://arxiv.org/abs/2605.29605v1)
