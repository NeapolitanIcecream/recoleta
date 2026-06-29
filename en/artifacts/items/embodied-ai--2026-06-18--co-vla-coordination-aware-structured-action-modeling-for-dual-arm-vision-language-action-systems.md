---
source: arxiv
url: https://arxiv.org/abs/2606.20285v1
published_at: '2026-06-18T14:28:37'
authors:
- Yandong Wang
- Jiaqian Yu
- Xiongfeng Peng
- Lu Xu
- Yamin Mao
- Weiming Li
- Jaewook Yoo
- Dongwook Lee
- Daehyun Ji
- Mingbo Zhao
- Chao Zhang
topics:
- vision-language-action
- dual-arm-manipulation
- robot-foundation-model
- structured-action-modeling
- bimanual-coordination
- robot-control
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Co-VLA: Coordination-Aware Structured Action Modeling for Dual-Arm Vision-Language-Action Systems

## Summary
Co-VLA adds explicit dual-arm coordination structure to a VLA action head and uses that structure during execution. It reports the largest gains on tightly coupled bimanual tasks, with smaller gains under heavy simulation randomization.

## Problem
- Standard VLA policies often output one concatenated dual-arm action vector, so timing, role split, and safety-related motion smoothing are learned implicitly.
- This matters for bimanual manipulation because tasks such as handover, lifting, and joint transport need synchronized motion and asymmetric arm roles.
- Implicit coordination is hard to inspect or adjust at deployment time when actions jitter, desynchronize, or collide.

## Approach
- Co-VLA keeps a pretrained VLA backbone, based on $\pi_0$ in the excerpt, and replaces the monolithic action head with a Structured Action Expert.
- The Structured Action Expert predicts one shared latent for task-level coordination and two residual latents for left-arm and right-arm adjustments.
- Final 7-DoF joint velocity commands for each arm are the sum of shared and residual action components.
- Task-adaptive auxiliary losses shape the decomposition: sparse residual loss for near-symmetric motion, shared mean velocity loss for asymmetric roles, and temporal synchronization loss for coupled timing. The auxiliary weight is $\lambda=0.001$.
- A Latent-Aware Controller reads shared and residual action energies at deployment, then low-pass filters joint commands with adaptive stiffness to preserve coordinated micro-adjustments and suppress jitter. It does not require force sensing or impedance control.

## Results
- On RoboTwin 2.0 Easy settings across 8 selected bimanual tasks, average success increased to 82% for Co-VLA, compared with 76% for $\pi_0$ and 73% for $\pi_{0.5}$.
- On RoboTwin 2.0 Hard settings, average success was 22% for Co-VLA, compared with 21% for $\pi_0$ and 21.9% for $\pi_{0.5}$, so the hard-setting aggregate gain is small.
- On Handover Block Easy, Co-VLA reached 91% success, compared with 64% for $\pi_0$ and 44% for $\pi_{0.5}$, a +27 point gain over $\pi_0$.
- The abstract reports a 27% success-rate gain in tight-coordination tasks and more than 2x OOD real-world improvement, from 13% to 27%.
- The abstract reports task completion time reductions of up to 25%.
- The training setup used 1,000 successful demonstrations per simulated task, 100 evaluation rollouts per setting, 1,000 SAE warm-up steps, 30,000 full fine-tuning steps, batch size 32, and 4 GPUs with FSDP.

## Link
- [https://arxiv.org/abs/2606.20285v1](https://arxiv.org/abs/2606.20285v1)
