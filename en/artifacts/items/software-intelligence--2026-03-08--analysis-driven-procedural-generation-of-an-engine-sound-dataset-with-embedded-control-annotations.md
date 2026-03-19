---
source: arxiv
url: http://arxiv.org/abs/2603.07584v1
published_at: '2026-03-08T11:05:10'
authors:
- Robin Doerfler
- Lonce Wyse
topics:
- procedural-audio
- engine-sound
- synthetic-dataset
- control-annotations
- harmonic-synthesis
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Analysis-Driven Procedural Generation of an Engine Sound Dataset with Embedded Control Annotations

## Summary
This paper proposes a procedural engine sound generation framework driven by analysis of real recordings, and releases a dataset with sample-level control annotations. Its goal is to generate clean, controllable, and machine-learning-suitable engine audio corpora at low cost.

## Problem
- Existing engine sound data is difficult to obtain: real-world collection is expensive, requires specialized equipment, and is often contaminated by environmental noise and mechanical noise.
- Many data-driven tasks require operating-condition labels that are strictly time-aligned with the audio (such as RPM and torque), but public datasets usually provide only coarse-grained annotations or none at all.
- Real recordings are difficult to systematically augment and modify under controlled conditions, limiting algorithm training, evaluation, and benchmark construction.

## Approach
- First, perform **analysis-driven feature extraction** on real engine recordings: using speed-adaptive resampling, frequency-aligned FFT, and centroid-based harmonic tracking to extract the amplitude and offset of each harmonic order, and model them as functions of RPM/torque.
- Then reconstruct the sound with an **extended harmonic-plus-noise parametric synthesizer**: 128 sinusoidal oscillators generate the main harmonics, with added pink noise, burst noise, and resonators to simulate combustion randomness, mechanical events, and exhaust resonance.
- Control variables are embedded directly into four-channel audio: the first two channels are stereo engine audio, and the last two channels encode RPM and torque, so sample-level ground truth can be recovered without external metadata.
- A small amount of source recordings is used to extract a "timbre fingerprint," which is then extended over richer control trajectories to achieve controllable, large-scale data augmentation.

## Results
- The **Procedural Engine Sounds Dataset** was generated and publicly released: a total of **19.0 hours, 5,935 files, 24.5 GB**, covering **8 data subsets**.
- The data comes from source recordings of **4 vehicles**, with each vehicle requiring only **5–10 minutes** of source material; combined with a **2.5-hour** control trajectory pool, this achieves **15–30×** data augmentation. Figure 1 also shows generating **150 minutes** of synthesized audio from **5 minutes** of extracted material and comparing it with **90 minutes** of real recordings; the authors claim the key order structures are preserved.
- The operating-condition coverage is clearly specified: RPM **0–7,007** (mean **3,171**, standard deviation **1,714**), torque **-107–718 Nm** (mean **120**, standard deviation **201**).
- Sample-level annotations are implemented through 48 kHz four-channel encoding; RPM and torque are encoded at 16-bit precision, corresponding to approximately **0.3 RPM** and **0.03 Nm** resolution.
- Baseline validation uses a **1.4M-parameter** differentiable harmonic-plus-noise synthesis network, taking only RPM/torque as input, trained for **100 epochs** on dataset **A/B/C**, and reports "stable convergence with a very small training/validation gap"; however, the excerpt **does not provide specific loss values or quantitative comparisons with other methods**.
- The paper's strongest claim is that the generated data preserves characteristic engine harmonic structures while being suitable for parameter estimation, conditional synthesis, and neural generative modeling tasks.

## Link
- [http://arxiv.org/abs/2603.07584v1](http://arxiv.org/abs/2603.07584v1)
