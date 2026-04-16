---
source: arxiv
url: http://arxiv.org/abs/2604.05014v1
published_at: '2026-04-06T17:59:21'
authors:
- StarVLA Community
topics:
- vision-language-action
- robot-foundation-model
- world-model
- generalist-robot-policy
- benchmarking
- open-source-codebase
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing

## Summary
StarVLA is an open-source codebase that puts several vision-language-action and world-model robot policy designs under one modular interface. Its main contribution is a shared backbone-plus-action-head setup, common training recipes, and a unified evaluation stack across major robot benchmarks.

## Problem
- VLA research is split across incompatible architectures, codebases, and benchmark protocols, which makes comparison and reproduction hard.
- Existing systems often bind the backbone, action decoder, data pipeline, and evaluation setup together, so swapping one part usually requires rewriting the rest.
- This matters because progress on generalist robot policies depends on fair ablations, reusable baselines, and easier transfer across embodiments and benchmarks.

## Approach
- StarVLA defines a common policy view: map observations plus language to an action chunk, with training loss written as action loss plus optional auxiliary loss.
- The codebase separates each method into a vision-language backbone and a pluggable action head. Either part can be swapped without changing the training loop or evaluation interface.
- It implements four action-decoding variants under this shared design: autoregressive action tokenization (StarVLA-FAST), parallel regression (StarVLA-OFT), flow-matching denoising (StarVLA-π), and dual-system reasoning with a DiT action module (StarVLA-GR00T).
- It supports both VLM backbones such as Qwen-VL/Qwen3-VL and world-model backbones such as Cosmos/Cosmos-Predict2, plus shared recipes for multimodal co-training and cross-embodiment training.
- It unifies evaluation and deployment across LIBERO, SimplerEnv, RoboTwin 2.0, RoboCasa-GR1, and BEHAVIOR-1K, with the same interface for simulation and real-robot use.

## Results
- Table 1 claims StarVLA supports 7 integrated benchmarks, compared with 1 to 6 for the listed open-source baselines: OpenPI (2), Isaac-GR00T (6), OpenVLA-OFT (1), Dexbotic (5), and X-VLA (5).
- Table 1 also claims StarVLA is the only listed framework with all of these at once: modular action heads, swappable VLM backbones, swappable world-model backbones, mixture dataloading, open multimodal co-training, open cross-embodiment co-training, and multi-benchmark co-training.
- The abstract says its simple single-benchmark recipes match or surpass prior methods on multiple benchmarks with both VLM and world-model backbones.
- The excerpt does not provide benchmark scores, success rates, or exact gains over named baselines, so the quantitative performance evidence is incomplete here.

## Link
- [http://arxiv.org/abs/2604.05014v1](http://arxiv.org/abs/2604.05014v1)
