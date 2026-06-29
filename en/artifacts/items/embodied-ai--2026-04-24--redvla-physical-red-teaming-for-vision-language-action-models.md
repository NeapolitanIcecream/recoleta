---
source: arxiv
url: http://arxiv.org/abs/2604.22591v1
published_at: '2026-04-24T14:18:23'
authors:
- Yuhao Zhang
- Borong Zhang
- Jiaming Fan
- Jiachen Shen
- Yishuai Cai
- Yaodong Yang
- Jiaming Ji
topics:
- vision-language-action
- robot-safety
- physical-red-teaming
- embodied-ai
- simulated-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# RedVLA: Physical Red Teaming for Vision-Language-Action Models

## Summary
RedVLA is a physical red-teaming method for vision-language-action models. It places and refines risk objects in robot scenes to trigger unsafe behavior before deployment, and it reports high attack success across six VLA models.

## Problem
- VLA models can cause physical harm during execution, but current red-teaming methods focus on language or image attacks rather than risks that arise through robot-environment interaction.
- Safety testing for robots needs to find unsafe behavior while keeping the original task and scene mostly valid; otherwise failures can come from broken setups instead of real safety weaknesses.
- This matters for real deployment in manipulation and other physical domains because unsafe actions can be irreversible and costly.

## Approach
- RedVLA fixes the task instruction and perturbs only the initial physical scene by adding one risk object.
- Stage 1, Risk Scenario Synthesis, uses benign robot trajectories to find critical interaction regions such as transit, grasping, and vibration zones, then places a risk object where the robot is likely to contact it.
- Each test case targets a specific safety violation under a taxonomy with three cost types: state-level, cumulative-level, and conditional-level. The hazards include resource damage, dangerous item misuse, robot damage, and environmental harm.
- Stage 2, Risk Amplification, runs the policy, reads the executed trajectory, picks a spatial anchor near collision or grasp events, and moves the risk object toward that anchor with gradient-free optimization until the target unsafe behavior appears.
- The paper also proposes SimpleVLA-Guard, a lightweight detector built from RedVLA-generated data that monitors internal VLA features and intervenes online.

## Results
- Across six VLA models on LIBERO-based risk scenarios, RedVLA reaches average attack success rates from 64.9% to 95.5%; the best result is 95.5% on pi_0.5, and the paper states this is achieved within 10 optimization iterations.
- Average ASR by safety type is above 95% for state-level scenarios, 88.9% for cumulative-level scenarios, and 66.1% for conditional-level scenarios.
- In the full model comparison table, average ASR/SR is: OpenVLA 64.9% / 39.1%, OpenVLA-OFT 90.5% / 44.7%, VLA-Adapter 89.9% / 48.4%, VLA-Adapter-Pro 91.6% / 45.3%, pi_0 93.2% / 54.6%, pi_0.5 95.5% / 62.1%.
- Several individual scenario ASRs are near or at 100%. Examples: cumulative dangerous item misuse reaches 100.0% ASR on all six models; pi_0.5 reaches 98.5% on cumulative resource damage and 98.0% on conditional environmental harm.
- Stronger base models also show higher vulnerability in this evaluation. OpenVLA-OFT improves benign success rate over OpenVLA by 20.6 points and ASR by 25.6 points; pi_0.5 improves benign success rate over pi_0 by 2.6 points and ASR by 2.3 points.
- Under language and visual perturbations, the excerpt reports RedVLA still keeps high ASR, with average ASR 88.2% for language perturbations and 85.5% for visual perturbations, while benign perturbations alone keep ASR at or below 5.2%. The paper also claims SimpleVLA-Guard cuts online ASR by 59.5% with small impact on task performance.

## Link
- [http://arxiv.org/abs/2604.22591v1](http://arxiv.org/abs/2604.22591v1)
