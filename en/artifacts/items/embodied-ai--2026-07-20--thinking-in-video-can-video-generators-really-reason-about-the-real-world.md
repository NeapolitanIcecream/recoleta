---
source: arxiv
url: https://arxiv.org/abs/2607.17523v1
published_at: '2026-07-20T03:56:43'
authors:
- Yongheng Zhang
- Guang Yang
- Ruihan Hou
- Qiguang Chen
- Ziang Liu
- Xiaolong Liu
- Manman Zhang
- Yanchao Hao
- Zheng Wei
- Hao Wu
- Libo Qin
- Peishan Dai
- Yinghui Li
- Di Yin
- Xing Sun
topics:
- world-models
- video-generation
- causal-reasoning
- multimodal-evaluation
- physical-simulation
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Thinking in Video: Can Video Generators Really Reason About the Real World?

## Summary
The paper introduces Thinking in Video as a way to test whether video generators reason about causal real-world dynamics rather than only produce plausible-looking motion. Its Causal-Generative Dual-Judge framework finds a gap between models' ability to perceive causal structure and their ability to render the correct future.

## Problem
- Conventional video metrics such as Fréchet Video Distance measure visual quality but do not establish causal correctness.
- A generator may produce a realistic consequence through memorized visual patterns without understanding the conditions that caused it.
- This distinction matters for treating video generators as world models for open-world reasoning and decision-making.

## Approach
- CGDJ separates explicit causal perception from implicit generative prediction.
- For explicit perception, Flatten Temporal Video converts 70 sampled frames into a 7x10 spatial grid and rasterizes the question above it, creating a single 1280x720 image input.
- For implicit prediction, each of 600 videos is split at an expert-labeled causal inflection point; 7 pre-event keyframes condition generation of the post-event sequence.
- The benchmark uses 900 Video-MME videos for causal understanding and 600 videos balanced between 300 Natural Sciences and 300 Sociology & Humanities samples for causal action generation.
- Gemini-3-Pro judges causal correctness and generation quality using semantic alignment, reference consistency, and physical validity; Whisper-large-v2 transcribes generated audio for separate audio-visual analysis.

## Results
- The excerpt provides no numerical accuracy or quality scores, so direct metric comparisons against baselines cannot be reported here.
- Open-source models, including Wan-2.2-14B and HunyuanVideo-1.5, produce moderately plausible causal continuations but show near-zero explicit causal perception under the flattened-video protocol.
- Closed-source Sora-2 and Veo-3.1 show measurable explicit causal perception and stronger alignment between perception and prediction, but the alignment remains limited.
- Models often verbalize correct causal logic in audio more reliably than they render the corresponding visual outcome, revealing audio-visual misalignment.
- The findings support a Perception-Prediction Gap: plausible dynamics alone do not demonstrate robust causal reasoning or reliable world simulation.

## Link
- [https://arxiv.org/abs/2607.17523v1](https://arxiv.org/abs/2607.17523v1)
