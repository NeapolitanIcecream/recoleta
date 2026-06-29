---
source: arxiv
url: http://arxiv.org/abs/2604.05323v1
published_at: '2026-04-07T01:52:42'
authors:
- Chuhang Liu
- Yayun He
- Zuheng Kang
- Xiaoyang Qu
- Jianzong Wang
topics:
- vision-language-action
- inference-acceleration
- token-pruning
- kv-cache
- robot-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# VLA-InfoEntropy: A Training-Free Vision-Attention Information Entropy Approach for Vision-Language-Action Models Inference Acceleration and Success

## Summary
VLA-InfoEntropy is a training-free inference method for vision-language-action models that keeps more useful visual tokens and reuses less useful ones through KV cache. It aims to make OpenVLA faster at test time while keeping or improving task success on LIBERO.

## Problem
- VLA models process many visual tokens at every step, and many of those tokens carry little task-relevant information. This raises latency and compute cost, which hurts real-time robotics use.
- Prior acceleration methods often prune by only one signal, such as visual redundancy or attention, and can miss instruction-critical regions or fail to adapt over a rollout.
- The paper targets faster inference without retraining the model, which matters when deploying large robot policies on limited hardware.

## Approach
- The method computes **visual entropy** for each image token from its grayscale histogram. High-entropy tokens come from textured or edge-rich regions and are treated as more informative.
- It also computes **attention entropy** from text-to-vision cross-attention. If a visual token gets concentrated attention from task text, its attention entropy is low, so its normalized information score is high.
- A timestep schedule shifts token selection over the rollout: earlier steps keep more globally informative visual tokens, and later steps keep more instruction-relevant tokens.
- The selected important tokens are excluded from the reusable static set, while lower-value static tokens reuse cached KV states using the VLA-Cache mechanism.
- The full selection rule is the union of top visual-entropy tokens and top attention-information tokens, with counts controlled by timestep-dependent hyperparameters.

## Results
- On **LIBERO**, the method reports **76.4% average success** versus **75.0%** for **OpenVLA** baseline, **74.7%** for **VLA-Cache**, **74.9%** for **SP-VLA**, and **75.0%** for **Spec-VLA**.
- Per-suite success rates for **VLA-InfoEntropy** are **86.4** on **LIBERO-Spatial**, **87.6** on **LIBERO-Object**, **79.4** on **LIBERO-Goal**, and **52.2** on **LIBERO-Long**. It leads on Spatial, Object, Goal, and average score, but not on Long, where **Spec-VLA** reports **55.0**.
- Efficiency numbers against **OpenVLA**: **latency 31.25 vs 51.91**, **FLOPs 1.214 vs 1.864**, and **speedup 1.53x vs 1.00x**. The paper also states **34.9% fewer FLOPs** and **39.8% lower CUDA latency**.
- In the ablation, average success is **69.8** with visual entropy only, **73.9** with attention entropy only, **75.8** with a static visual+attention combination, and **76.4** with the full timestep-aware method. Latency improves from **33.82** and **33.24** to **32.26**, then **31.25**.
- With different token budgets, **100 tokens** gives **76.4%** success at **31.25** latency and **1.205 FLOPs**. Using **60 tokens** drops success to **71.6%**, while **140 tokens** raises latency to **36.64** for **76.8%** success.

## Link
- [http://arxiv.org/abs/2604.05323v1](http://arxiv.org/abs/2604.05323v1)
