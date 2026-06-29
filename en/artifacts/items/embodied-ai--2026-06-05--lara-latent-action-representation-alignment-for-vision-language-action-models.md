---
source: arxiv
url: https://arxiv.org/abs/2606.07100v1
published_at: '2026-06-05T09:51:25'
authors:
- Mengya Liu
- Baoxiong Jia
- Jiangyong Huang
- Jingze Zhang
- Siyuan Huang
topics:
- vision-language-action
- latent-action-models
- robot-data-scaling
- diffusion-policy
- representation-alignment
- robot-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# LARA: Latent Action Representation Alignment for Vision-Language-Action Models

## Summary
LARA jointly trains a Latent Action Model and a diffusion-based Vision-Language-Action policy by aligning their internal action representations. The paper targets the robot action data bottleneck by using unlabeled video dynamics without freezing the latent action model during policy learning.

## Problem
- VLA policies need large action-labeled robot datasets, but real robot demonstrations are expensive and scarce.
- Latent Action Models can learn motion representations from unlabeled human or robot videos, but prior pipelines usually train the LAM separately and then freeze it.
- A frozen LAM can encode visual changes that do not matter for control, while the VLA policy can produce plausible-looking action trajectories that do not cause the intended state change.

## Approach
- LARA starts with a LAM that maps a current frame and a future frame into a continuous latent action, quantizes it with a VQ-style codebook, and reconstructs the future frame with a forward dynamics model.
- The VLA side uses a flow-matching diffusion policy with a DiT backbone to generate action chunks from vision-language features, proprioception, and noise.
- During joint training, LARA aligns the LAM latent action with an intermediate DiT feature using a cosine-similarity loss and a learned projection head.
- The full objective combines action flow matching, the LARA alignment loss, and the LAM reconstruction loss, so both the LAM and the VLA policy update together.
- The method can be used for VLA pre-training, post-training an existing VLA model, or refining LAM latent action tokens used as pseudo-labels.

## Results
- The abstract claims average gains of about 10% for full VLA training, about 5% for post-training enhancement, and about 15% for LAM refinement across 3 simulation benchmarks and 1 real-world manipulation benchmark.
- In the OXE-constrained LIBERO comparison, LARA full reaches 88.6 average success, compared with OpenVLA at 76.5, Octo at 75.1, LAPA at 65.7, and LARA DiT-only at 84.4.
- On LIBERO Long, LARA full reaches 86.0, compared with OpenVLA at 53.7 and LARA DiT-only at 76.5.
- In the OXE-constrained SIMPLER-ENV comparison, LARA full reaches 65.2 average success, compared with Moto-GPT at 61.4, OpenVLA at 32.7, Octo at 14.6, and LARA DiT-only at 55.8.
- As a post-training add-on to GR00T-N1.6, GR00T-N1.6-LARA reports 95.6 average on LIBERO versus 95.0 for GR00T-N1.6, and 79.9 average on SIMPLER-ENV versus 78.9.
- The table also shows that LARA full is not the top unconstrained model on all reported benchmarks: for example, GR00T-N1.6-LARA reports 79.9 on SIMPLER-ENV, while villa-X reports 77.7 and GR00T-N1.6 reports 78.9; on LIBERO, UniVLA reports 95.2 and GR00T-N1.6-LARA reports 95.6.

## Link
- [https://arxiv.org/abs/2606.07100v1](https://arxiv.org/abs/2606.07100v1)
