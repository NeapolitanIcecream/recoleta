---
source: arxiv
url: http://arxiv.org/abs/2604.02190v1
published_at: '2026-04-02T15:48:45'
authors:
- Yongkang Li
- Lijun Zhou
- Sixu Yan
- Bencheng Liao
- Tianyi Yan
- Kaixin Xiong
- Long Chen
- Hongwei Xie
- Bing Wang
- Guang Chen
- Hangjun Ye
- Wenyu Liu
- Haiyang Sun
- Xinggang Wang
topics:
- autonomous-driving
- vision-language-action
- mixture-of-transformers
- driving-planning
- 3d-perception
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving

## Summary
UniDriveVLA is a unified vision-language-action model for autonomous driving that separates understanding, perception, and planning into different transformer experts. The paper claims this avoids interference between spatial perception and language reasoning and reaches state-of-the-art results on nuScenes open-loop evaluation and Bench2Drive closed-loop evaluation.

## Problem
- Existing driving VLA models face a tradeoff: plain 2D vision-language models keep language reasoning but miss spatial structure needed for driving.
- Adding 3D or spatial tokens into shared model parameters can hurt the pre-trained vision-language model's reasoning ability through representation interference.
- This matters because autonomous driving needs both semantic understanding and precise spatial perception for safe planning.

## Approach
- The model uses a Mixture-of-Transformers design with three experts: a driving-understanding expert, a scene-perception expert, and an action-planning expert.
- Tokens for understanding, perception, and action go through separate expert-specific projections, so the three functions do not compete in the same parameter subspace.
- A masked joint attention layer allows controlled information flow: understanding tokens keep causal masking, perception tokens can read earlier understanding tokens, and action tokens can read both semantic and spatial context.
- The perception branch uses a sparse query-based decoder built from multi-scale 2D visual features instead of dense BEV or dense 3D grids; it predicts 3D detection, mapping, ego status, motion, and occupancy.
- Training happens in three stages: multimodal pretraining for semantic ability, joint training for language/perception/planning with LoRA and reduced VLM learning rate, then expert fine-tuning with the VLM frozen and an added motion objective.

## Results
- The paper claims state-of-the-art performance on **nuScenes** for open-loop evaluation and on **Bench2Drive** for closed-loop evaluation.
- Reported benchmark metrics shown in the excerpt include **Avg. L2** for open-loop planning and **Driving Score / Success Rate / Efficiency / Comfortness** for closed-loop evaluation, but the UniDriveVLA row is not visible in the provided text, so its exact numbers are not available here.
- The excerpt gives baseline closed-loop numbers on Bench2Drive for prior VLA methods: **AutoVLA** reaches **78.84 Driving Score** and **57.73% Success Rate**; **SimLingo** reaches **85.94 Driving Score** and **66.82% Success Rate**; **R2SE** reaches **86.28 Driving Score** and **69.54% Success Rate**.
- A non-VLA baseline, **AD-MLP**, shows **3.64 Avg. L2** on open-loop and **18.05 Driving Score** with **0.00% Success Rate** on closed-loop Bench2Drive.
- The paper also claims strong performance across **3D detection, online mapping, motion forecasting, and driving-oriented VQA**, plus evaluation on DriveBench and several general VQA benchmarks, but the excerpt does not provide those task-specific scores.
- Figure 2 reports a qualitative mechanism result: in a shared-weight decoder, cosine similarity between language and perception tokens rises toward **1**, while the MoT design keeps similarity low, which the authors use as evidence of reduced feature collapse and better task separation.

## Link
- [http://arxiv.org/abs/2604.02190v1](http://arxiv.org/abs/2604.02190v1)
