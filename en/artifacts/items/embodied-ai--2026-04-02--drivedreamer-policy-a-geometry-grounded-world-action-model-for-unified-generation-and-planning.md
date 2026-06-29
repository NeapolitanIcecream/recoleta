---
source: arxiv
url: http://arxiv.org/abs/2604.01765v1
published_at: '2026-04-02T08:33:18'
authors:
- Yang Zhou
- Xiaofeng Wang
- Hao Shao
- Letian Wang
- Guosheng Zhao
- Jiangnan Shao
- Jiagang Zhu
- Tingdong Yu
- Zheng Zhu
- Guan Huang
- Steven L. Waslander
topics:
- world-action-model
- autonomous-driving
- geometry-grounding
- video-prediction
- motion-planning
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning

## Summary
DriveDreamer-Policy is a driving world-action model that predicts depth, future video, and driving actions in one system. Its main claim is that explicit geometry helps both imagination and planning, and it reports state-of-the-art planning scores on Navsim with better video and depth generation.

## Problem
- Existing driving VLA and world-action models often predict actions or future images without explicit 3D geometry, which weakens occlusion reasoning, distance estimation, and safety-related planning.
- A visually plausible future is not always useful for control if the representation does not encode free space, layout, and physical structure.
- This matters for autonomous driving because planning depends on how the 3D scene will evolve over time, especially in rare or safety-critical cases.

## Approach
- The model uses a multimodal LLM backbone, Qwen3-VL-2B, to read language instructions, multi-view RGB images, and current action context, then outputs compact query embeddings.
- It attaches three lightweight generators to those embeddings: a pixel-space depth generator, a latent video generator, and a diffusion-based action generator for trajectories.
- The query groups follow a fixed causal order: depth queries feed video queries, and both feed action queries. In simple terms, the model predicts geometry first, then future appearance, then driving actions.
- Depth is generated explicitly as a monocular depth map and used as a geometric scaffold for future video prediction and planning.
- The system is modular: it can run planning only, planning with imagination, or full world generation for simulation and data synthesis.

## Results
- On Navsim v1, DriveDreamer-Policy reaches **89.2 PDMS**, beating PWM at **88.1**, WoTE at **88.3**, DriveVLA-W0 at **88.4**, and AutoVLA at **89.1**.
- On Navsim v2, it reaches **88.7 EPDMS**, which the paper states is **+2.6** over the previous method; the table shows DriveVLA-W0 at **86.1**.
- On video generation, it improves **FVD** from **85.95** (PWM) to **53.59**, a drop of **32.36**. It also improves **LPIPS** from **0.23** to **0.20**, while **PSNR** is **21.05** vs **21.57** for PWM.
- On depth generation, it reports **AbsRel 8.1**, **δ1 92.8**, **δ2 98.6**, **δ3 99.5**. A fine-tuned PPD baseline gets **AbsRel 9.3**, **δ1 91.4**, **δ2 98.3**, **δ3 99.5**.
- The paper claims ablations show explicit depth gives complementary gains to video imagination and improves planning robustness, though the excerpt does not include the ablation tables.

## Link
- [http://arxiv.org/abs/2604.01765v1](http://arxiv.org/abs/2604.01765v1)
