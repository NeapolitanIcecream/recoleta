---
source: arxiv
url: http://arxiv.org/abs/2604.07957v1
published_at: '2026-04-09T08:21:58'
authors:
- Hongjin Chen
- Shangyun Jiang
- Tonghua Su
- Chen Gao
- Xinlei Chen
- Yong Li
- Zhibo Chen
topics:
- vision-language-navigation
- world-models
- trajectory-prediction
- teacher-student-learning
- embodied-ai
relevance_score: 0.79
run_id: materialize-outputs
language_code: en
---

# WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models

## Summary
WorldMAP trains a navigation trajectory predictor by turning world-model-generated future views into pseudo-labeled paths. The paper argues that world models help more as supervision generators than as test-time planners for single-image vision-language navigation.

## Problem
- The task is to predict a grounded, traversable navigation trajectory from one egocentric image and a language instruction in unseen environments.
- Direct vision-language models often output unstable paths that miss geometry, obstacles, or the correct stopping point.
- World models can generate plausible future views, but those views do not directly give the structured target, obstacle, and path supervision needed to train a reliable predictor.

## Approach
- WorldMAP uses a teacher-student setup. The teacher uses generated future videos to build a semantic-spatial memory and a shared bird's-eye-view planning space.
- The teacher retrieves instruction-relevant views with CLIP, uses a VLM plus UniPixel to segment target regions and obstacles, projects them into BEV, and builds a cost map.
- It then runs Fast Marching Method planning on that cost map to produce trajectory pseudo-labels.
- A lightweight student VLM takes the original image and instruction and predicts waypoints directly, with a multi-hypothesis trajectory head and a best-match training loss.
- At inference time, only the student runs, so the expensive world-model and planning pipeline is used only for training.

## Results
- On Target-Bench, WorldMAP reports the best ADE and FDE among compared methods: **ADE 42.06**, **FDE 38.87**, **DTW 31.95**.
- Against the best competing baseline, **Gemini-3-Pro**, WorldMAP reduces **ADE from 51.27 to 42.06** for an **18.0%** improvement and **FDE from 67.19 to 38.87** for a **42.1%** improvement; DTW is close (**31.95 vs. 31.63**).
- WorldMAP uses a **Qwen3-VL-8B** student and outperforms direct open-source VLM prediction by a large margin. For example, direct **Qwen3-VL-8B** scores **ADE 183.93, FDE 339.58, DTW 177.33**.
- It also beats the world-model-augmented baseline **MindJourney**, which reports **ADE 152.41, FDE 250.17, DTW 84.84**.
- The paper’s main concrete claim is that generated futures work better as training supervision for grounded planning than as extra test-time evidence for direct reasoning.

## Link
- [http://arxiv.org/abs/2604.07957v1](http://arxiv.org/abs/2604.07957v1)
