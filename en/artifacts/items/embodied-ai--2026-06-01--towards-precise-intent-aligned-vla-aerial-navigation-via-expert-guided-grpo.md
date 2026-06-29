---
source: arxiv
url: https://arxiv.org/abs/2606.02313v1
published_at: '2026-06-01T14:31:35'
authors:
- Tianyang Chen
- Wenjun Li
- Xin zhou
- Yuze Wu
- Fei Gao
topics:
- vision-language-action
- uav-navigation
- reinforcement-fine-tuning
- grpo
- sim2real
- intent-alignment
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO

## Summary
EG-GRPO trains a VLA UAV policy to follow fine-grained flight instructions by mixing online rollouts with one expert trajectory per GRPO group. The paper reports higher task success and intent alignment than SFT baselines, plus faster rollouts through parallel simulation and inference.

## Problem
- Supervised fine-tuning needs costly UAV trajectory data and gives weak supervision for detailed instructions such as S-shaped bypassing, orbiting, or over/under passing.
- Online RL for 3D aerial navigation has sparse rewards and a large continuous action space, so random exploration rarely finds useful trajectories for complex flight skills.
- Rollout collection is slow because physics simulation on RT-core GPUs and VLA inference on compute GPUs can leave hardware idle in a serial loop.

## Approach
- The policy starts from OpenVLA-OFT, with actions constrained to 4-DoF UAV commands: Δx, Δy, Δz, and Δψ.
- EG-GRPO forms each trajectory group with G-1 online rollouts and exactly 1 rule-based expert trajectory, using ρ = 1/G. The expert sample keeps the group reward variance usable for relative advantage estimates.
- A trajectory-level reward model scores each full flight path against the language instruction. The evaluator is an LLM, and the paper says it was checked on 10K rollout trajectories by certified drone pilots, but the excerpt gives no agreement percentage.
- The system uses Isaac Lab vectorized simulation with high-fidelity scenes, collision meshes, and a UAV kinematic model.
- A double-buffer pipeline runs simulation on an NVIDIA L20 workstation and VLA inference on an NVIDIA A100 server in parallel through Ray and SSH tunneling.

## Results
- Overall, OpenVLA-OFT SFT improves from 26.1% SR and 4.50 IAS to 55.6% SR and 7.24 IAS with EG-GRPO. This is a 2.13× success-rate increase and a 60.9% IAS increase over the SFT baseline.
- On easy tasks, OpenVLA-OFT rises from 33.5% SR and 5.19 IAS to 68.2% SR and 8.28 IAS, a +34.7 point SR gain and +3.09 IAS gain.
- On difficult tasks, OpenVLA-OFT rises from 18.7% SR and 3.81 IAS to 43.1% SR and 6.20 IAS, a +24.4 point SR gain and +2.39 IAS gain.
- Against π0 overall, the method reports 55.6% SR and 7.24 IAS versus 32.0% SR and 5.31 IAS.
- In the difficult-task ablation, GRPO without expert injection reaches 26.4% SR and 4.66 IAS. EG-GRPO reaches 43.1% SR and 6.20 IAS, adding +16.7 points SR and +1.54 IAS over GRPO.
- The parallel rollout pipeline reduces per-step rollout time from 904.67 s to 511.01 s, a 43.5% reduction.

## Link
- [https://arxiv.org/abs/2606.02313v1](https://arxiv.org/abs/2606.02313v1)
