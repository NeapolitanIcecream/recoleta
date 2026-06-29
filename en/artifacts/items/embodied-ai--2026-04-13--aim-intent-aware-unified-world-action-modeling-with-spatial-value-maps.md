---
source: arxiv
url: http://arxiv.org/abs/2604.11135v1
published_at: '2026-04-13T07:48:58'
authors:
- Liaoyuan Fan
- Zetian Xu
- Chen Cao
- Wenyao Zhang
- Mingqi Yuan
- Jiayu Chen
topics:
- vision-language-action
- world-model
- robot-manipulation
- spatial-value-map
- generalist-robot-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps

## Summary
AIM is a unified world-action model for robot manipulation that adds an explicit spatial value map between future video prediction and action generation. The paper claims this makes action decoding more reliable than reading actions directly from future visual features.

## Problem
- Existing world-action models can predict future visual scenes, but they still need substantial robot-specific training to produce reliable actions.
- Future RGB features describe scene appearance and motion, but control also needs spatial intent: where the robot should act and why that region matters for the task.
- This gap matters most in cluttered, long-horizon, and contact-sensitive manipulation, where action-relevant cues are sparse.

## Approach
- AIM predicts future RGB frames and aligned spatial value maps together, then predicts actions conditioned on the value maps instead of raw future RGB latents.
- The value map is an image-aligned interaction prior. It marks task-relevant regions in the future scene and gives the action head a simpler control signal.
- The model uses a shared mixture-of-transformers design built on the pretrained video model Wan2.2-TI2V-5B. RGB, value-map, and action streams share masked self-attention but keep separate feed-forward layers.
- An intent-causal attention mask blocks the action branch from reading future RGB tokens directly. Future information reaches the action branch through the predicted value-map tokens.
- After supervised pretraining, a self-distillation RL stage freezes the video and value branches and updates only the action head with GRPO, using sparse task rewards plus dense rewards from projected value-map responses.

## Results
- The paper builds a simulation dataset with **30K manipulation trajectories** with synchronized multi-view observations, actions, and value-map annotations.
- On the **RoboTwin 2.0** benchmark, AIM reports **94.0% average success** on **Easy** and **92.1%** on **Hard**.
- The abstract states AIM significantly outperforms prior unified world-action baselines, with larger gains on long-horizon and contact-sensitive tasks.
- In the provided table, AIM often matches or exceeds strong baselines and the supervised-only ablation (**Stage1**). Examples: **Move Can Pot** reaches **100% / 98%** vs Stage1 **99% / 97%**; **Pick Diverse Bottles** reaches **100% / 98%** vs Stage1 **99% / 97%**; **Scan Object** reaches **100% / 98%** vs Stage1 **98% / 97%**.
- Several tasks show near-ceiling performance for AIM, including **Open Laptop 100% / 100%**, **Place Bread Skillet 100% / 100%**, **Place Object Stand 100% / 100%**, and **Rotate QRcode 100% / 98%**.
- Some tasks remain weak, which shows the method does not solve all manipulation cases. Examples in the table include **Hanging Mug 43% / 42%**, **Blocks Ranking Size 47% / 43%**, and **Place Phone Stand 82% / 80%**.

## Link
- [http://arxiv.org/abs/2604.11135v1](http://arxiv.org/abs/2604.11135v1)
