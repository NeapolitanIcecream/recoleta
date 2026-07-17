---
source: arxiv
url: https://arxiv.org/abs/2607.14609v1
published_at: '2026-07-16T06:12:05'
authors:
- Ruilin Chen
- Jingkai Jia
- Tong Yang
- Xinyu Zhou
- Qiao Sun
- Jiangwei Zhong
- Shizeng Zhang
- Nuo Chen
- Bailin He
- Wei Li
- Wenqiang Zhang
topics:
- robot-foundation-model
- vision-language-action
- tactile-grounding
- contact-rich-manipulation
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Representation-Aligned Tactile Grounding for Contact-Rich Robotic Manipulation

## Summary
The paper shows that future tactile prediction improves contact-rich robot manipulation most when it supervises an intermediate action-expert representation. Its Latent Tactile Predictor (LTP) raises average real-world success to 74% without adding inference-time computation.

## Problem
- Vision cannot reliably observe contact states such as pressure, slip, resistance, and insertion alignment, which limits VLA policies on tasks including insertion, wiping, unscrewing, and deformable grasping.
- Future tactile prediction can provide supervision about action-induced contact dynamics, but it is unclear which internal VLA representation should receive that supervision.
- Applying the loss to perceptual VLM features or final motor features can create representation-mismatched supervision, while raw tactile targets can emphasize sensor noise and calibration artifacts.

## Approach
- The authors freeze the VLA policy and train linear probes at different points in its action pathway to predict future tactile measurements, using probe error to identify where future contact information is most accessible.
- Intermediate action-expert features are selected because they are action-conditioned but not yet compressed into representations specialized for immediate motor decoding.
- LTP predicts compact future tactile embeddings from this intermediate representation using learnable queries, rather than predicting noisy raw tactile signals directly.
- The latent tactile loss is combined with the native action loss during training; the LTP branch is removed at inference, so the deployment pathway and inference cost remain unchanged.

## Results
- On five real-world contact-rich tasks with an ARX R5 robot, PaXini tactile sensors, 50 demonstrations per task, and 20 evaluation trials per task, intermediate grounding achieved 74% average success with the SmolVLA backbone.
- The 74% result exceeded VLM-side future tactile prediction at 58% by 16 percentage points and final-action-state prediction at 62% by 12 points.
- With the \(\pi_{0}\) backbone, standard, tactile-conditioned, VLM-side prediction, and final-action prediction policies achieved 40%, 54%, 58%, and 59% average success, respectively; representation-aligned grounding achieved 73%.
- The method was best on four of five SmolVLA tasks and tied for best on Deformable Object Grasping; its task-level average was 74%, versus 41% for tactile input without future tactile prediction and 38%, 48%, and 60% for three multi-interface grounding variants.
- Replacing latent tactile targets with raw tactile prediction reduced Plug Insertion success from 80% to 55%.
- The evidence is limited to the reported real-world task suite and two VLA backbones; the excerpt does not establish performance across broader robots, datasets, or longer-term deployment conditions.

## Link
- [https://arxiv.org/abs/2607.14609v1](https://arxiv.org/abs/2607.14609v1)
