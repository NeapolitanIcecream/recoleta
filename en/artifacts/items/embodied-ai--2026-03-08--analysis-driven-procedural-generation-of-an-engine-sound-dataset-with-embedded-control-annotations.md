---
source: arxiv
url: http://arxiv.org/abs/2603.07584v1
published_at: '2026-03-08T11:05:10'
authors:
- Robin Doerfler
- Lonce Wyse
topics:
- audio-dataset
- procedural-generation
- engine-sound-synthesis
- signal-processing
- control-annotation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Analysis-Driven Procedural Generation of an Engine Sound Dataset with Embedded Control Annotations

## Summary
This paper proposes a procedural engine sound generation framework based on the analysis of real recordings, capable of synthesizing clean audio data with sample-accurate RPM/torque annotations. The authors also release a public dataset for research on engine timbre analysis, parameter estimation, and generative modeling.

## Problem
- Existing engine audio data is typically **hard to obtain, expensive, and heavily contaminated by noise**, and often lacks operating-state annotations that are strictly synchronized with the audio.
- Machine learning methods require **large-scale, standardized, precisely annotated** data; real-world collection often depends on proprietary equipment and struggles to cover a sufficiently broad range of operating conditions.
- Existing public datasets are mostly aimed at classification/detection, with **coarse or missing temporal annotations**, and are also difficult to systematically augment and modify under controlled conditions, which limits research on parameter estimation, synthesis, and benchmark evaluation.

## Approach
- Features are extracted from a small amount of real engine recordings: first, **RPM-based adaptive resampling** is used to stabilize the fundamental frequency; then an **FFT aligned with harmonics** is applied; finally, a **centroid method tracks** the position deviations and amplitude envelopes of each engine-order harmonic.
- The extracted information—"**how strong each harmonic should be and how much it should deviate under different RPM/torque conditions**"—is stored in lookup tables, which drive a **harmonic + noise + resonator** parametric synthesizer to generate audio.
- The synthesizer includes **128 sine oscillators**, and adds pink-noise modulation, burst noise, and parallel feedback-delay resonators to enhance realism and diversity.
- A **four-channel synchronized encoding** is used: the first two channels are stereo audio, while the latter two directly embed normalized RPM and torque, so the annotations can be recovered from within the audio itself at **sample-level precision**, without requiring separate metadata files.
- Timbre features are extracted from source recordings of **4 vehicles**, with **5–10 minutes per vehicle**, then combined with a **2.5-hour** control-trajectory pool for augmentation, while multiple dataset subsets are generated through variations in noise/resonance parameters.

## Results
- The **Procedural Engine Sounds Dataset** is generated and publicly released: **19.0 hours, 5,935 files, 24.5 GB** in total, covering **8 dataset subsets**.
- The dataset spans a broad range of operating conditions: RPM ranges from **0–7,007** (mean **3,171**, standard deviation **1,714**), and torque ranges from **-107–718 Nm** (mean **120**, standard deviation **201**).
- A **15–30×** expansion is achieved from relatively small amounts of source data; in Figure 1, the authors compare **90 minutes of real recordings** with **150 minutes of synthesized audio** generated from only **5 minutes of extracted material**, claiming that it preserves key engine-order structures and engine-specific signature characteristics across the full RPM-torque space.
- Sample-level annotations are embedded directly in the audio channels, with control variables encoded in 16-bit format, corresponding to roughly **0.3 RPM** and **0.03 Nm** resolution.
- In the baseline validation, the authors trained a **1.4M-parameter** differentiable harmonic + noise synthesis network to reconstruct audio using only RPM/torque as input, trained for **100 epochs** on dataset **A/B/C**, and report **stable convergence with only a very small train/validation gap**.
- The paper **does not provide explicit numerical performance metrics** (such as reconstruction error, percentage improvement over baselines, MOS scores, etc.); the strongest concrete claim is that the synthesized data preserves real harmonic structure, supports neural synthesis training, and enables the construction of large-scale, controllable, annotated corpora from limited real recordings.

## Link
- [http://arxiv.org/abs/2603.07584v1](http://arxiv.org/abs/2603.07584v1)
