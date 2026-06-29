---
source: arxiv
url: https://arxiv.org/abs/2606.23531v1
published_at: '2026-06-22T16:11:15'
authors:
- Jinsong Lin
- Chi kit Ng
- Zhiyong Xiong
- Zikang Pan
- Yihan Hu
- Tabassum Tamima
- Ziyi Hao
- Eddie Cheung
- Jiewen Lai
- Huxin Gao
- Hongliang Ren
topics:
- vision-language-action
- surgical-robotics
- endoscopic-navigation
- reinforcement-learning
- robot-policy
- medical-robotics
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation

## Summary
BiliVLA is a vision-language-action policy for autonomous ERCP endoscope navigation in a phantom model. It joins target recognition, bounding-box grounding, and 3-DoF motor commands, then improves the policy with supervised tuning and GRPO.

## Problem
- ERCP cannulation needs stable navigation in a narrow monocular view with glare, occlusion, tissue contact, and variable anatomy.
- Existing robotic or vision systems often split perception, planning, and control, which can fail when target appearance changes or the view degrades.
- Safer autonomous navigation matters because repeated cannulation attempts raise clinical risk, including post-ERCP pancreatitis.

## Approach
- The model takes an endoscopic image plus a stage-specific instruction and outputs three items: target category, normalized bounding box, and a discrete action.
- The robot action space has 11 motion primitives: 8 bending directions, forward, backward, and stop, mapped to 3 DoF actuation for tip bending and insertion or retraction.
- The authors build BiliVLA-Motion with 10k image-motion pairs from a phantom ERCP setup: 3k entry navigation, 2.6k lumen traversal, and 4.4k calculus localization.
- Scene-aware supervision ties each instruction to the target category and output schema, so the policy learns which structure to find in each ERCP stage.
- Safety-aware labels set wall-contact frames to a full-image box and a backward command, teaching the policy to retreat when the view shows unsafe proximity.
- Training has two stages: LoRA supervised fine-tuning of Qwen3-VL-8B with grounding and action labels, then GRPO using rewards for bounding-box IoU, correct action, and valid output format.

## Results
- In real-world phantom experiments across three ERCP subtasks, BiliVLA reports total mIoU 0.9625, action precision 91.96%, and success rate 84.85%.
- Against EndoVLA, total action precision rises from 84.44% to 91.96%, and success rate rises from 58.86% to 84.85%.
- Against Qwen3-VL, total success rate rises from 51.82% to 84.85%, with total mIoU rising from 0.8117 to 0.9625.
- GRPO improves the full model over BiliVLA without GRPO: success rate 84.85% versus 63.64%, action precision 91.96% versus 89.00%, and mIoU 0.9625 versus 0.9488.
- Per task, the full model reports entry navigation mIoU 0.9162, PR 90.82%, SR 72.73%; lumen traversal mIoU 0.9630, PR 91.46%, SR 100.00%; calculus localization mIoU 0.9816, PR 92.55%, SR 81.82%.

## Link
- [https://arxiv.org/abs/2606.23531v1](https://arxiv.org/abs/2606.23531v1)
