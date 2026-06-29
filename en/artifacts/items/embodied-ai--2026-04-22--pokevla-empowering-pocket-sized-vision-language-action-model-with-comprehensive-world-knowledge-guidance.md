---
source: arxiv
url: http://arxiv.org/abs/2604.20834v2
published_at: '2026-04-22T17:58:19'
authors:
- Yupeng Zheng
- Xiang Li
- Songen Gu
- Yuhang Zheng
- Shuai Tian
- Weize Li
- Linbo Wang
- Senyu Fei
- Pengfei Li
- Yinfeng Gao
- Zebin Xing
- Yilun Chen
- Qichao Zhang
- Haoran Li
- Wenchao Ding
topics:
- vision-language-action
- robot-manipulation
- embodied-foundation-model
- spatial-reasoning
- multi-view-learning
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# PokeVLA: Empowering Pocket-Sized Vision-Language-Action Model with Comprehensive World Knowledge Guidance

## Summary
PokeVLA is a small vision-language-action model for robot manipulation that adds embodied world knowledge before action training. It targets better spatial understanding, target awareness, and robustness than lightweight VLA baselines.

## Problem
- Existing VLA models often pass generic vision-language features into an action head with weak alignment to robot manipulation, which can make learning inefficient and costly.
- Pre-trained VLM knowledge does not match robot tasks well enough, especially for spatial relations, multi-view consistency, and target-focused guidance.
- These gaps matter because robot manipulation needs accurate object grounding, spatial reasoning, and stable behavior under scene changes and perturbations.

## Approach
- The method has two stages. First, it pre-trains a compact vision-language model called PokeVLM on about 2.4M to 2.5M multimodal samples covering general VQA, spatial grounding, affordance learning, and embodied reasoning.
- PokeVLM uses a Qwen2.5-0.5B language model with SigLIP and DINOv2 visual encoders, so the base model stays small while adding embodied visual-language knowledge.
- During VLA post-training, the model learns a special `<SEG>` token that predicts manipulation-target segmentation masks from both base and wrist camera views. This gives the policy a shared representation of the target across views.
- It aligns visual hidden states with features from the 3D geometry model VGGT during training, so the model learns scene structure without needing the geometry model at inference time.
- An action head with learnable action queries gathers language, vision, segmentation, geometry, and robot-state features and feeds them into the action expert for action prediction.

## Results
- On LIBERO-Plus, when trained on the LIBERO-Plus dataset, PokeVLA beats OpenVLA-OFT by **4.0%** and VLA-Adapter by **2.5%** in total success rate.
- In a transfer setting trained only on original LIBERO and tested on LIBERO-Plus variations and perturbations, PokeVLA exceeds OpenVLA-OFT by **9.7%** and VLA-Adapter by **20.2%** in average success rate.
- In real-world tasks with spatial and color references, it reports a **12.5%** success-rate gain over similar-scale baselines.
- Under real-world perturbations, the reported gain grows to **20.0%**, which the paper presents as evidence of stronger robustness.
- The pre-training corpus contains roughly **2.4M to 2.5M** samples, including **665K** general, **694K** grounding, **553K** affordance, and **511K** reasoning examples.

## Link
- [http://arxiv.org/abs/2604.20834v2](http://arxiv.org/abs/2604.20834v2)
