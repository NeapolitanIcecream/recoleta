---
source: arxiv
url: http://arxiv.org/abs/2604.11572v1
published_at: '2026-04-13T14:51:43'
authors:
- Siyuan Xu
- Tianshi Wang
- Fengling Li
- Lei Zhu
- Heng Tao Shen
topics:
- vision-language-action
- post-training-quantization
- robot-efficiency
- mixed-precision
- sequential-control
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# DA-PTQ: Drift-Aware Post-Training Quantization for Efficient Vision-Language-Action Models

## Summary
DA-PTQ is a post-training quantization method for vision-language-action models that targets a failure mode common in robot control: small quantization errors turn into trajectory drift over time. It adds interface-level compensation and drift-aware bit allocation so low-bit VLA models stay closer to full-precision behavior on resource-limited robots.

## Problem
- Vision-language-action models are large and expensive to run on onboard robot hardware, so quantization is useful for cutting memory and compute.
- Standard post-training quantization works poorly for VLAs because action errors compound across control steps; small perturbations at the vision-language-to-action interface can grow into kinematic drift.
- Existing VLA quantization methods mainly optimize static reconstruction or single-step sensitivity, which misses long-horizon error propagation in sequential control.

## Approach
- DA-PTQ treats quantization as a sequential control problem instead of a layer reconstruction problem. The target is to reduce trajectory drift caused by quantization noise.
- Its first part, Cross-Space Representation Compensation, measures how quantization shifts the conditioning activations at the vision-language-to-action interface, then applies per-channel affine correction plus a low-rank cross-channel transform to align quantized activations with full-precision statistics.
- These correction parameters are folded into the quantized weights after calibration, so the method claims no extra inference overhead.
- Its second part, Motion-Driven Mixed-Precision Allocation, builds a Jacobian-based proxy for how errors in each action dimension propagate into end-effector drift, then uses a drift-weighted loss and layer sensitivity scores to keep the most drift-sensitive layers in BF16 while quantizing others to low precision such as W4.
- The full pipeline is training-free and uses a small calibration dataset with forward passes and lightweight gradient accumulation.

## Results
- The excerpt does not provide quantitative tables or exact benchmark numbers.
- The paper claims DA-PTQ "significantly reduces kinematic drift" compared with conventional PTQ strategies on sequential robot control.
- It claims performance comparable to full-precision models under low-bit settings, with mixed precision using BF16 for sensitive layers and W4 for the rest.
- It claims the method enables practical deployment of diffusion-based VLA models on resource-limited robotic platforms without additional runtime cost after folding the compensation into model weights.
- The method uses a 7-dimensional action formulation and defines drift through accumulated Jacobian-weighted action error over a control horizon, but the excerpt gives no success-rate, latency, memory, or accuracy numbers against baselines such as AWQ, GPTQ, QuantVLA, QVLA, or SQAP-VLA.

## Link
- [http://arxiv.org/abs/2604.11572v1](http://arxiv.org/abs/2604.11572v1)
