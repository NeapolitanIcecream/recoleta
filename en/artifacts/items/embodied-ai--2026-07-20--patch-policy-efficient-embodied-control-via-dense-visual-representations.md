---
source: arxiv
url: https://arxiv.org/abs/2607.18236v1
published_at: '2026-07-20T17:59:41'
authors:
- Gaoyue Zhou
- Zichen Jeff Cui
- Ada Langford
- Bowen Tan
- Yann LeCun
- Lerrel Pinto
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Patch Policy: Efficient Embodied Control via Dense Visual Representations

## Summary
Patch Policy is a lightweight transformer policy that uses dense, pretrained Vision Transformer patch features for robot control instead of compressing each image into a global token or using a billion-parameter vision-language-action model. Across four simulated benchmarks and three real-world manipulation tasks, it reports higher control performance with substantially fewer parameters and low latency.

## Problem
- Global pooling and CLS tokens discard fine-grained spatial information needed for precise manipulation.
- Large vision-language-action models retain dense visual inputs but require costly training and inference, limiting their use in high-frequency control.
- The paper addresses whether frozen, Internet-pretrained dense visual features can improve standard visuomotor policies without the cost of a full VLM.

## Approach
- Patch Policy feeds all Vision Transformer patch embeddings from each observation directly into a transformer-based policy rather than pooling them into one vector.
- A block-causal attention mask allows full bidirectional attention among patches within the same frame while preserving causal attention across time.
- The architecture is compatible with standard action heads, including VQ-BeT and Diffusion Policy, and supports image or vector goals.
- The visual encoders remain frozen, so only the policy is trained; experiments use representations including DINOv2, DINOv3, WebSSL, V-JEPA 2, and SigLIP 2.

## Results
- Across Push-T, LIBERO Goal, BlockPush, and Cube, WebSSL patch features with Diffusion Policy score 0.80, 0.98, 1.65, and 1.73 respectively; the corresponding global-feature baselines score 0.79, 0.99, 1.34, and 0.21.
- On real-robot tasks with 20 trials, DINOv2 Patch Policy reaches final-stage success rates of 0.70 for Cable Insertion, 0.85 for Pen Collection, and 0.90 for Tool Hanging, exceeding the reported OpenVLA-OFT rates of 0.30, 0.60, and 0.65.
- The paper reports a 40% relative improvement over policies using state-of-the-art global-pooled representations and an 18% improvement over fine-tuned OpenVLA-OFT across its evaluation suites.
- DINOv2 VQ-BeT has 51.55M total parameters and 10.99 ms latency on an NVIDIA H200, compared with 7.61B parameters and 61.71 ms for OpenVLA-OFT; DINOv2 Patch Policy training uses 6.5 GPU-hours versus 16 GPU-hours for OpenVLA-OFT.
- On Push-T, retaining 256 patches scores 0.69, while compressing to 64, 16, 4, and 1 patch scores 0.52, 0.53, 0.51, and 0.48, supporting the claim that spatial compression harms precise control.
- The evidence covers four simulated environments and three tasks on one 7-DoF Franka setup; the excerpt does not establish performance across broader robot embodiments, datasets, or long-term deployment conditions.

## Link
- [https://arxiv.org/abs/2607.18236v1](https://arxiv.org/abs/2607.18236v1)
