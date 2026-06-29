---
source: arxiv
url: https://arxiv.org/abs/2606.20135v1
published_at: '2026-06-18T11:58:30'
authors:
- Jianing Guo
- Fangzheng Chen
- Zihao Mao
- Wong Lik Hang Kenny
- Zhenhong Wu
- Yu Li
- Yishuai Cai
- Yuanpei Chen
- Yikun Ban
- Kai Chen
- Qi Dou
- Yaodong Yang
- Xianglong Liu
- Huijie Zhao
- Simin Li
topics:
- flow-matching
- frequency-domain-actions
- vision-language-action
- temporal-smoothness
- robot-action-generation
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Frequency-Aware Flow Matching for Continuous and Consistent Robotic Action Generation

## Summary
FAFM changes flow-matching robot policies to predict DCT frequency coefficients instead of fixed discrete action chunks, then reconstructs continuous actions at any control rate. It targets smoother, more stable robot actions without adding network parameters.

## Problem
- Fixed action chunks discard control-frequency information, which matters because robot datasets can mix demonstrations sampled at different rates, such as RT-1 at 3 Hz and ALOHA at 50 Hz in Open X-Embodiment.
- Step-indexed training can map the same index to different physical times, creating conflicting supervision for the same observation.
- Independent per-step action prediction can produce jitter between adjacent actions, which can hurt soft-body tasks such as pouring or surgical manipulation.

## Approach
- FAFM converts each demonstration chunk into DCT coefficients tied to physical time, so the target describes the trajectory shape instead of a fixed step index.
- Flow matching runs in coefficient space: the model learns a velocity field from noise to the target coefficient vector.
- The predicted coefficients decode into a continuous trajectory with a cosine basis, so the policy can output actions at arbitrary temporal resolution.
- A derivative loss supervises the analytic first-order time derivative of the decoded action. This penalizes high-frequency coefficient errors and reduces abrupt action changes.
- The method uses λ=1 for the derivative term and adds no extra networks or learnable parameters. The paper applies it to standalone flow-matching policies and VLA action heads.

## Results
- On obstacle avoidance, FAFM reports SR 61, LDLJ -5.60±1.08, and 12 trajectory modes. Baselines include FM at SR 48, LDLJ -8.62±0.69, M=14; DP at SR 35, LDLJ -9.16±0.77, M=8; SFP at SR 49, LDLJ -6.98±0.82, M=3; MPD at SR 16, LDLJ -6.78±0.47, M=2; and FreqPolicy at SR 39, LDLJ -9.02±1.11, M=10.
- On the synthetic two-mode sinusoidal benchmark, the paper claims FAFM is the only method that separates both modes while keeping trajectories smooth. The excerpt provides no numeric metric for this benchmark.
- On LapGym rope threading, the visible table reports FAFM at SR 97 and LDLJ -7.57±1.32. The strongest visible baseline SR is MPD at 94, while DP reports 92, SFP 72, FreqPolicy 89, and FM 89.
- On LapGym tasks, the paper states that FAFM has the highest success rate and smoothness across rope threading, grasp-lift-touch, bimanual tissue manipulation, and ligating loop, and converges faster than all listed baselines. The excerpt is truncated, so the full FAFM numbers for three tasks are not visible.
- The paper also claims gains on LIBERO with VLA backbones and on a real Franka robot, including smoother motion and better handling of mechanical bias and mixed-frequency input. The excerpt does not include the related quantitative table.

## Link
- [https://arxiv.org/abs/2606.20135v1](https://arxiv.org/abs/2606.20135v1)
