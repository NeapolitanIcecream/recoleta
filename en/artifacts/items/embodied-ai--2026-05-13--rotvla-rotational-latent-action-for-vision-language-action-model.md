---
source: arxiv
url: https://arxiv.org/abs/2605.13403v1
published_at: '2026-05-13T11:58:02'
authors:
- Qiwei Li
- Xicheng Gong
- Xinghang Li
- Peiyan Li
- Quanyun Zhou
- Hangjun Ye
- Jiahuan Zhou
- Yadong Mu
topics:
- vision-language-action
- latent-actions
- robot-foundation-model
- cross-embodiment-learning
- flow-matching
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# RotVLA: Rotational Latent Action for Vision-Language-Action Model

## Summary
RotVLA is a 1.7B-parameter vision-language-action model that uses continuous SO(n) latent actions instead of discrete latent action tokens. It reports top or near-top success rates on LIBERO and RoboTwin2.0 while training on more than 1700 hours of robot and human video.

## Problem
- VLA pretraining has to mix robot datasets with different embodiments and unlabeled human videos, where action labels do not share one native action space.
- Existing latent action models often quantize actions into discrete tokens, which can lose continuous motion detail and limit action composition.
- Reconstruction-based latent action training can learn shortcuts that encode the target frame instead of the motion between frames, which weakens transfer to robot control.

## Approach
- RotVLA encodes the transition between two frames as a continuous rotation matrix in SO(n), with n set to 16 in the experiments.
- The latent action model uses SoftVQ and then projects the predicted matrix to the nearest valid rotation matrix with SVD, giving a continuous codebook-based action representation.
- A triplet training loss uses frames t, t+1, and t+2: it learns two one-step latent actions, multiplies them to form a two-step latent action, and trains the decoder to reconstruct the third frame from the composed action.
- The VLA model uses InternVL3.5-1B plus a 24-layer DiT action head trained with flow matching to predict latent actions from vision and language.
- During robot fine-tuning, one flow-matching action head jointly denoises latent actions and robot actions; robot action tokens can attend to latent action tokens, so the latent action guides control.

## Results
- Pretraining uses more than 1700 hours of data from Open X-Embodiment, AGIBOT-beta, RoboMIND, RoboCOIN, and Ego4D; the full model has about 1.7B parameters.
- On LIBERO, RotVLA reports 98.2% average success: 98.2 Spatial, 99.6 Object, 98.4 Goal, and 96.4 Long. The table lists X-VLA at 98.1 average, OpenVLA-OFT at 97.1, GR00T-N1.6 at 97.0, and UniVLA at 95.4.
- On RoboTwin2.0, RotVLA reports 89.6% success in the clean setting and 88.5% in the randomized setting. The closest listed baselines are StarVLA at 88.2/88.3, Motus at 88.7/87.0, and LingBot-VLA at 88.6/86.7.
- On real ARX R5 tasks, the paper reports more than 90% success on two single-arm tasks and lower failure than pi_0.5 on dual-arm cup stacking, using 100 demonstrations per task.
- Inference latency is reported as 79 ms per step on an NVIDIA H20 server, compared with 61 ms per step for pi_0.5.
- The triplet latent action training shows a larger reconstruction-gap measure than recon-only training: Delta 0.0048 vs 0.0037 in Table 2, with next-frame MSE 0.0030 vs 0.0029 and imagined-frame MSE 0.0078 vs 0.0066.

## Link
- [https://arxiv.org/abs/2605.13403v1](https://arxiv.org/abs/2605.13403v1)
