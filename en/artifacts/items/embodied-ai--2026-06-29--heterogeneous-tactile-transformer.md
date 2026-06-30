---
source: arxiv
url: https://arxiv.org/abs/2606.29948v1
published_at: '2026-06-29T08:24:38'
authors:
- Jianxin Bi
- Qiang Wang
- Jayaram Reddy
- Kelvin Lin
- Soibkhon Khajikhanov
- Ruihan Gao
- Harold Soh
topics:
- tactile-representation-learning
- heterogeneous-tactile-sensors
- self-supervised-pretraining
- robot-manipulation
- contact-rich-control
- robot-data-scaling
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Heterogeneous Tactile Transformer

## Summary
HTT trains one tactile backbone across optical and array tactile sensors using paired self-supervised data. It targets contact-rich perception and manipulation where sensor-specific tactile models fail to transfer across hardware.

## Problem
- Tactile sensors output different data types: images for GelSight Mini and 9DTact, and time-series taxel signals for Xela and TAC-02, so a model trained on one sensor cannot directly read another.
- This limits scaling tactile data across hardware and hurts robot policies that need force, slip, and spatial contact cues.
- Existing tactile pretraining mostly targets optical tactile sensors and can miss force-sensitive cues from array sensors.

## Approach
- The HPT dataset contains 1.6M synchronized paired tactile frames from GelSight Mini, 9DTact, Xela, and TAC-02, collected with a UMI setup across press, twist, and slide interactions.
- HTT uses sensor-specific encoders: ViT-style spatial patches for optical tactile images and temporal patches for array tactile time series.
- A shared transformer trunk maps all sensor embeddings into one latent space, while sensor-specific decoders reconstruct masked input patches.
- Cross-sensor predictors learn to predict masked embeddings of one sensor from its paired sensor and visible target tokens, using stop-gradient targets and an alignment weight ramped to 0.1.
- After pretraining, the decoders and predictors are dropped; downstream tasks use the relevant sensor encoder and the shared trunk.

## Results
- On 20-class object classification, HTT reaches 66.20% overall top-1 accuracy versus 47.54% for Scratch and 65.38% for MAE-only pretraining. On optical sensors, HTT reaches 94.84% on 9DTact and 91.35% on GSMini, compared with SITR at 81.34% and 74.31%.
- For force estimation, HTT reports 0.636 N overall 3D MAE, lower than Scratch at 1.111 N and MAE-only at 0.664 N.
- For slip detection, HTT reports 56.35% overall macro-F1, above Scratch at 31.14% and MAE-only at 51.62%. The largest listed alignment gain is on TAC-02: 45.45% macro-F1 for HTT versus 33.45% for MAE-only.
- In real-world camera-free manipulation with unseen Sharpa fingertip sensors, HTT reaches 95% success on toy screw and 55% on grasp tofu. qpos-only gets 5% on both tasks, while wrench input gets 50% on screw and 35% on tofu.
- In ManiFeel simulation, HTT(FF) reaches 0.48 success on Peg Insertion versus 0.21 for tacRGB, 0.23 for T3, and 0.35 for SITR. On Bulb Installation, HTT(RGB) reaches 0.77, matching SITR at 0.77 and above tacRGB at 0.72 and T3 at 0.73.

## Link
- [https://arxiv.org/abs/2606.29948v1](https://arxiv.org/abs/2606.29948v1)
