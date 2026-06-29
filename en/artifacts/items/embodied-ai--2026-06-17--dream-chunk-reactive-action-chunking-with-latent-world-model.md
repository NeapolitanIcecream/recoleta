---
source: arxiv
url: https://arxiv.org/abs/2606.18589v1
published_at: '2026-06-17T01:28:07'
authors:
- Wenxi Chen
- Kaidi Zhang
- Chi Lin
- Zhiyuan Zhang
- Yu She
- Yuejiang Liu
- Raymond A. Yeh
- Shaoshuai Mou
- Yan Gu
topics:
- vision-language-action
- action-chunking
- latent-world-model
- test-time-scaling
- robot-manipulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DREAM-Chunk: Reactive Action Chunking with Latent World Model

## Summary
DREAM-Chunk improves action-chunking VLA policies by sampling multiple action chunks at test time and using a latent world model to choose the chunk whose predicted state best matches the real robot state. It targets stochastic dynamics, hardware errors, partial observability, and perturbations without fine-tuning the base policy.

## Problem
- Action-chunking policies execute several actions after one VLA inference call, so later actions can become stale when the robot or environment deviates during execution.
- This matters for long-horizon manipulation because execution noise, moving objects, and external perturbations can make open-loop chunks miss grasps, ports, or insertion targets.
- Existing fixes often replan more often, change the policy, or add test-time optimization; DREAM-Chunk keeps the base VLA fixed and uses extra inference-time sampling plus a small world model.

## Approach
- At each replanning step, the method samples N candidate action chunks from the frozen chunking policy.
- A lightweight encoder maps each observation to a latent state, and a latent dynamics model predicts the future latent states caused by each candidate chunk.
- During execution, the robot encodes the current observation and compares it with the phase-aligned predicted latent states.
- It executes the action from the candidate chunk with the closest predicted latent state, so it can switch chunks when the realized rollout shifts.
- The method depends on the policy having useful corrective behaviors in its sampled action distribution; it selects among sampled behaviors rather than creating new ones.

## Results
- In Kinetix, the paper reports higher solve rates under action noise as N increases, with results averaged over 12 environments; the excerpt does not provide exact solve-rate values from the figure.
- Under Kinetix action noise σ=0.3, DREAM-Chunk gains more from larger sample counts when demonstrations come from experts trained with higher action noise; low-noise expert data such as σ=0.1 gives smaller gains.
- In Kinetix ablations at σ=0.2 with N=20, RSSM-style R2-Dreamer and LEWM latent models work better than EB-JEPA and a frozen policy-encoder variant; the excerpt gives no exact numeric scores for these curves.
- On hardware, the paper tests 4 manipulation tasks across SO-101 and Franka Panda using SmolVLA and π0.5, with about 50 to 100 teleoperated demonstrations per task.
- On a precise insertion task under external perturbation, DREAM-Chunk raises open-loop π0.5 success from 10% to 65%.
- The auxiliary model is much smaller and faster than the VLA: a JEPA world model can have 15M parameters, SmolVLA has about 450M, π0.5 has more than 2B, VLA inference takes more than 100 ms, and world-model encoding plus prediction takes less than 10 ms.

## Link
- [https://arxiv.org/abs/2606.18589v1](https://arxiv.org/abs/2606.18589v1)
