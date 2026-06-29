---
source: arxiv
url: https://arxiv.org/abs/2606.04708v1
published_at: '2026-06-03T10:38:45'
authors:
- Siyuan Yang
- Linzheng Guo
- Ouyang Lu
- Zhaxizhuoma
- Daoran Zhang
- Xinmiao Wang
- Ting Xiao
- Fangzheng Yan
- Zhijun Chen
- Yan Ding
- Chao Yu
- Chenjia Bai
- Xuelong Li
topics:
- vision-language-action
- robot-data-scaling
- umi-data
- fisheye-perception
- trajectory-validation
- robot-foundation-model
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training

## Summary
VISTA adapts UMI handheld demonstration data for VLA training by addressing two failure sources: fisheye wrist-camera perception and robot-infeasible action traces. It pairs an 8M-sample fisheye VQA dataset with trajectory validation and two-stage VLA training.

## Problem
- UMI and FastUMI make real-world robot data collection cheaper and less tied to one robot, but their wrist-mounted fisheye views differ from the standard images used to pretrain VLM backbones.
- Human-collected UMI trajectories can violate target-robot joint limits, collide with the robot body, or require controller motion that the robot cannot track.
- These issues matter because a VLA trained on raw UMI data may learn visual features that do not parse its own wrist-camera input and actions that fail during deployment.

## Approach
- VISTA builds UMI-VQA, an 8M-sample VQA dataset for wrist-mounted fisheye observations: 3M real UMI VQA pairs and 5M fisheye-style spatial-diversity samples adapted from RefSpatial.
- The real UMI-VQA split covers object grounding, scene understanding, captioning, interaction grounding, and spatial reasoning under gripper-centric distortion and occlusion.
- A physical-validation pipeline checks trajectory completeness, then scores valid trajectories for continuity, self-collision risk, and execution fidelity before training.
- Training uses two stages: joint autoregressive learning on UMI-VQA plus validated action tokens, followed by continuous action refinement with a flow-matching action expert.
- The pretraining set includes 100K real-world UMI trajectories that pass validation plus the 8M UMI-VQA samples.

## Results
- The excerpt claims VISTA beats pi-0.5, LingBot-VLA, and Wall-X on UMI-style simulation benchmarks and 20 real-world manipulation tasks, but it does not provide success rates or table values.
- Evaluation covers two simulation benchmarks, RoboTwin-UMI and LIBERO-UMI, plus 20 real-world tasks.
- UMI-VQA contains 8M samples: 3M real wrist-fisheye VQA pairs and a 5M spatial-diversity supplement.
- The 3M real UMI-VQA portion is reported as Object Grounding 842K, 27.5%; Scene Understanding 406K, 13.2%; Captioning 103K, 3.3%; Interaction Grounding 894K, 29.1%; Spatial Reasoning 824K, 26.9%.
- The hardware uses about a 180-degree fisheye field of view, weighs about 600 g, and reports about 3 mm fused pose accuracy.
- The paper reports that UMI-VQA improves downstream policy performance and that higher physical-validation scores predict better deployment outcomes, but the excerpt gives no numeric correlation or ablation scores.

## Link
- [https://arxiv.org/abs/2606.04708v1](https://arxiv.org/abs/2606.04708v1)
