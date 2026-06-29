---
source: arxiv
url: https://arxiv.org/abs/2605.22812v1
published_at: '2026-05-21T17:57:44'
authors:
- Wenxuan Guo
- Ziyuan Li
- Meng Zhang
- Yichen Liu
- Yimeng Dong
- Chuxi Xu
- Yunfei Wei
- Ze Chen
- Erjin Zhou
- Jianjiang Feng
topics:
- vision-language-action
- gesture-grounding
- robot-manipulation
- robot-data-scaling
- sim2real
- flow-matching
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations

## Summary
GesVLA is a gesture-aware vision-language-action model for robot manipulation in cluttered scenes. It uses pointing gestures with language to identify the intended target and generate robot actions.

## Problem
- Text-only VLA models can fail when several similar objects are present and the user gives an instruction such as pick this up or put it there.
- Gesture-grounded robot data is scarce because real pointing videos are costly to collect and hard to label with exact target locations.
- The problem matters because target grounding errors lead directly to wrong grasps, wrong placements, and slower human-robot interaction.

## Approach
- GesVLA extracts hand keypoints with MediaPipe, selects keyframes where the pointing hand pauses, and projects wrist and index-finger keypoints into latent gesture tokens.
- A dual-VLM design separates gesture-language intent reasoning from online scene perception while passing cached latent states through cross-attention.
- The action expert uses flow matching to denoise a sampled action trajectory into continuous robot actions conditioned on the VLM states and robot state.
- The data engine renders synthetic hand motions on real RGB-D scene images, using GroundingDINO object boxes and depth-based 3D target points for exact pointing labels.
- Training has 2 stages: train the intent VLM on about 16k semi-synthetic gesture samples, then freeze it and train the perception VLM plus action expert on real robot demonstrations.

## Results
- On real-robot manipulation, GesVLA reaches 83.3% average success across 3 tasks, compared with 31.7% for text-only VLA, 31.7% for MLLM + VLA, 41.7% for geometric pipeline + VLA, and 61.7% for decoupled GesVLA.
- Pick-and-Place Block success is 95.0% for GesVLA versus 45.0% for text-only VLA, with 9/10 success on the hard subset compared with 3/10.
- Select Jelly success is 75.0% for GesVLA versus 35.0% for text-only VLA, with 6/10 success on the hard subset compared with 3/10.
- Select Fruit and Vegetable success is 80.0% for GesVLA versus 15.0% for text-only VLA, with 8/10 success on the hard subset compared with 1/10.
- On an 88-sample real-world intent reasoning test set, GesVLA's intent VLM reaches 94.3% accuracy and 97.2% progress score, compared with 38.6% and 61.4% for prompted Qwen3.5-plus, and 59.1% and 78.4% for a geometric pipeline.
- The intent model is trained on semi-synthetic data built from 300 RGB-D scenes and evaluated directly on real scenes with at least 7 objects, which supports the paper's sim-to-real claim for gesture grounding.

## Link
- [https://arxiv.org/abs/2605.22812v1](https://arxiv.org/abs/2605.22812v1)
