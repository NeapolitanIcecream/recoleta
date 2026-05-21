---
source: arxiv
url: https://arxiv.org/abs/2604.24182v1
published_at: '2026-04-27T08:44:12'
authors:
- Siyao Xiao
- Yuhong Zhang
- Zhifang Liu
- Zihan Gao
- Jingye Zhang
- Sinwai Choo
- Dake Zhong
- Mengzhe Wang
- Xiao Lin
- Xianfeng Zhou
- Jia Jia
- Haoqian Wang
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-manipulation
- parameter-efficient-adaptation
- robot-generalization
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# $M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills

## Summary
$M^2$-VLA adapts a frozen vision-language model for robot manipulation with a layer-selection module and a memory-based meta-skill module. It reports higher LIBERO success rates than fine-tuned and frozen-VLM baselines while using 0.3B parameters.

## Problem
- Current VLA models often fine-tune the VLM backbone, which can erase language and visual reasoning needed for new instructions and objects.
- Robot control needs fine spatial and trajectory information, while VLM features are built for high-level image-text tasks.
- A small action head can lack capacity to learn many manipulation trajectories from limited robot data.

## Approach
- The model keeps the VLM frozen and separates perception from action generation, so the backbone retains its original vision-language ability.
- It encodes global and wrist camera images with DINOv2 and SigLIP, adds language tokens and learnable query tokens, and feeds them into the VLM.
- Mixture of Layers reads hidden states from VLM layers and filters them through separate attention paths for query/proprioception features, visual tokens, and action latents.
- The action head predicts actions through a denoising transformer.
- The Meta Skill Module stores perceptual-feature keys with successful future action chunks, retrieves the top 4 nearest skills by L1 distance, and injects them through cross-attention to refine the action latent.

## Results
- On synonymically rephrased LIBERO Spatial instructions, $M^2$-VLA reaches 66.2% success with a 29.4% performance drop, compared with OpenVLA at 20.0% and 64.7% drop, and VLA-Adapter at 52.8% and 45.4% drop.
- On a novel-object LIBERO pick-and-place test, $M^2$-VLA reaches 34.4% success with a 30.4% drop, compared with OpenVLA at 8.2% and 80.2% drop, and VLA-Adapter at 8.0% and 91.6% drop.
- On LIBERO simulation, $M^2$-VLA reports 97.8% Spatial, 99.0% Object, 97.2% Goal, 87.0% Long, and 95.3% average success over 500 tests per suite after 15,000 training steps.
- The best listed baseline average is VLA-Adapter Frozen at 89.4% with 0.5B parameters; SmolVLA reports 88.8% with 2.2B parameters, and FlowVLA reports 88.1% with 7.0B parameters.
- The paper reports training on 4 NVIDIA A800 GPUs and says the parameter-efficient design can train in 8 hours on one RTX 3090 GPU.
- Real-world setup uses an AgileX PiPer 6-DoF arm with a gripper, 2 RGB cameras, 50 teleoperated demonstrations per task, 5,000 training steps, and 20 rollouts per task; the provided excerpt is truncated before the full $M^2$-VLA real-world results table.

## Link
- [https://arxiv.org/abs/2604.24182v1](https://arxiv.org/abs/2604.24182v1)
