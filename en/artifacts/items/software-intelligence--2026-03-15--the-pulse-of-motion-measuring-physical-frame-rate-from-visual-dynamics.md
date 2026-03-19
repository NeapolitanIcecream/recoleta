---
source: arxiv
url: http://arxiv.org/abs/2603.14375v1
published_at: '2026-03-15T13:29:31'
authors:
- Xiangbo Gao
- Mingyang Wu
- Siyuan Yang
- Jiongze Yu
- Pardis Taghavi
- Fangzhou Lin
- Zhengzhong Tu
topics:
- video-generation
- temporal-grounding
- physical-simulation
- benchmarking
- motion-analysis
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# The Pulse of Motion: Measuring Physical Frame Rate from Visual Dynamics

## Summary
This paper proposes **Visual Chronometer**, a method for estimating the true physical frame rate (PhyFPS) using only motion cues in a video, thereby measuring and correcting “temporal scale hallucinations” in generated videos. The authors also build two benchmarks showing that current mainstream video generation models generally suffer from misaligned and unstable physical time scales.

## Problem
- Existing video generation models typically produce motion that merely “looks smooth,” but they lack a stable, controllable time scale that matches the real world.
- Training data treats slow motion, timelapse, and normal videos uniformly at standardized frame rates, causing models to fail to learn “how much real time each frame corresponds to.”
- This leads to what the authors define as **chronometric hallucination**: the motion speed in generated videos is ambiguous, unstable, and difficult to control. This matters for using video models as world models, because physical simulation must be correct not only in space but also in time.

## Approach
- The core mechanism is simple: train a regressor called **Visual Chronometer** that takes a video clip as input and directly predicts the true physical frame rate **PhyFPS** implied by its motion, rather than relying on unreliable metadata FPS.
- To obtain supervision, the authors collect high-fidelity videos from data sources with reliable temporal annotations, first upsample them to 240 FPS, and then synthesize different PhyFPS values through three physically inspired temporal resampling methods: **sharp capture**, **motion blur**, and **rolling shutter**.
- Architecturally, the method uses **VideoVAE+** as the video encoder, followed by an attention-based query pooling head, and finally regresses `log(PhyFPS)`; training uses MSE in log space to more stably cover the range from 2 to 240 FPS.
- The authors construct two evaluation sets: **PhyFPS-Bench-Real** for validating prediction accuracy on real videos, and **PhyFPS-Bench-Gen** for auditing alignment between generated models’ meta FPS and actual PhyFPS, as well as temporal stability within and across videos.
- The predicted PhyFPS is also used as a post-processing signal to retime generated videos globally or locally, testing whether this can improve perceived naturalness for human viewers.

## Results
- The training set covers **18 target PhyFPS** values (2, 5, 10, ... , 240), with **465,535** video clips in total, each standardized to **128 frames**; training uses windows of up to **32 frames**.
- On **PhyFPS-Bench-Gen**, mainstream generation models generally show severe misalignment. For example, **LTX-Video** has a meta FPS of **24**, but a predicted PhyFPS of **46.52**, with an average error of **23.67 FPS** and a percentage error of **99%**; **InfinityStar (10s)** has a meta FPS of **16**, a PhyFPS of **36.15**, an average error of **20.19 FPS**, and a percentage error of **126%**.
- Even relatively better alignment still shows clear error: among open-source models, **Wan2.1-T2V-1.3B** has an average error of **7.54 FPS** and a percentage error of **31%**; among closed-source models, **Sora-2** has an average error of **8.40 FPS** and a percentage error of **28%**; **Seedance-1.0-Lite** has **8.31 FPS / 35%**.
- In terms of temporal stability, models’ **Intra CV** is roughly **0.10–0.17**, and **Inter CV** is roughly **0.25–0.52**, indicating noticeable temporal jitter both within the same video and across different videos; for example, **CogVideoX-5B** has an Inter CV of **0.52**, while **Seedance-1.5-Pro** has an Inter CV of **0.25**.
- The user study collected **1,490** pairwise comparisons from more than **15** participants. The preference score for original videos was **19.0%**, while global correction based on average PhyFPS (**Pred**) reached **44.2%**, and local dynamic correction (**Pred Dyn**) reached **36.9%**, showing that PhyFPS-based post-processing significantly improves human-perceived temporal naturalness.
- The paper also explicitly claims that powerful general-purpose **VLMs** are “highly unreliable” as PhyFPS judges, but the provided excerpt does not include their specific quantitative scores.

## Link
- [http://arxiv.org/abs/2603.14375v1](http://arxiv.org/abs/2603.14375v1)
