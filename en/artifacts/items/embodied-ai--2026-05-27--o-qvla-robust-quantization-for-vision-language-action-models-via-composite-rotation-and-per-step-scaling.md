---
source: arxiv
url: https://arxiv.org/abs/2605.28803v1
published_at: '2026-05-27T17:55:01'
authors:
- Xinyu Wang
- Mingze Li
- Sicheng Lyu
- Dongxiu Liu
- Kaicheng Yang
- Ziyu Zhao
- Yufei Cui
- Xiao-Wen Chang
- Peng Lu
topics:
- vision-language-action
- vla-quantization
- robot-policy-compression
- diffusion-action-head
- post-training-quantization
- bimanual-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling

## Summary
Ω-QVLA is a training-free post-training quantization method for VLA robot policies. It quantizes both the language backbone and DiT action head to uniform W4A4 while keeping LIBERO success rates near FP16.

## Problem
- VLA models such as Pi 0.5 and GR00T N1.5 use billion-parameter backbones plus diffusion action heads, which makes robot-side deployment expensive in memory and compute.
- Existing PTQ methods often leave DiT attention or the action head at higher precision because action errors affect continuous robot control.
- Uniform W4A4 quantization matters because equal 4-bit weights and activations can reduce memory and support lower-precision compute without mixed-precision handling.

## Approach
- Applies orthogonal rotations before quantization so each linear layer can be computed as `(X R)(R^T W)`, then quantizes the rotated tensors.
- Uses SVD rotation to reduce weight channel energy imbalance; the paper reports weight row-norm spread dropping from 26× to 6× in an example layer.
- Adds a Hadamard rotation after SVD to spread activation outliers; the same example reports activation spread dropping from 20× to 1.6×.
- Uses block-wise SVD-Hadamard rotation with block size 64 plus zigzag channel permutation by weight norm to control cost.
- Calibrates DiT activation scales per layer, denoising step, and channel over 10 unlabeled trajectories and 8 Euler denoising steps.

## Results
- On LIBERO, Ω-QVLA W4A4 reaches 98.0% average success on Pi 0.5 versus 97.1% FP16; task scores are Goal 100.0, Spatial 99.0, Object 97.0, Long 96.0.
- On LIBERO, Ω-QVLA W4A4 reaches 87.8% average success on GR00T N1.5 versus 87.0% FP16; task scores are Goal 91.0, Spatial 86.0, Object 92.0, Long 82.0.
- Compared with W4A4 full QuantVLA on Pi 0.5, average success rises from 82.0% to 98.0%, and Long rises from 56.0% to 96.0%.
- Compared with W4A4 full baselines on GR00T N1.5, Ω-QVLA scores 87.8% average versus SmoothQuant 84.0%, DuQuant 70.0%, and QuantVLA 69.8%.
- The method reports a 71.3% static memory-footprint reduction.
- In real-world Pi 0.5 W4A4 tests on an ARX R5 dual-arm robot, Ω-QVLA scores 51.0 average progress across 5 tasks versus 49.6 for FP16 Pi-0.5 Base and 25.0 for QuantVLA.

## Link
- [https://arxiv.org/abs/2605.28803v1](https://arxiv.org/abs/2605.28803v1)
