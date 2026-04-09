---
source: arxiv
url: http://arxiv.org/abs/2604.02241v1
published_at: '2026-04-02T16:33:38'
authors:
- Qiyao Zhang
- Shuhua Zheng
- Jianli Sun
- Chengxiang Li
- Xianke Wu
- Zihan Song
- Zhiyong Cui
- Yisheng Lv
- Yonglin Tian
topics:
- vision-language-action
- uav-tracking
- embodied-visual-tracking
- simulator-benchmark
- temporal-modeling
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# UAV-Track VLA: Embodied Aerial Tracking via Vision-Language-Action Models

## Summary
UAV-Track VLA targets instruction-following aerial visual tracking with an end-to-end vision-language-action model and a new UAV tracking benchmark. The paper adds temporal modeling and spatial grounding to a \$\pi_{0.5}\$-based policy and reports better tracking success and lower inference latency in CARLA.

## Problem
- The paper addresses embodied UAV tracking where a drone must follow a target from visual input, language instructions, and its own state while producing continuous flight actions.
- This matters because current UAV tracking often depends on manual control or vision-only active tracking, which cannot handle natural-language task specifications in urban scenes with pedestrians, vehicles, occlusion, and fast motion.
- Existing VLA models for tracking have two stated gaps: weak use of multi-frame temporal information and weak spatial geometric priors for precise continuous control.

## Approach
- The authors build **UAV-Track**, a CARLA-based benchmark and dataset with **892,756 frames**, **176 tasks**, and **85 objects**, covering urban scenes, weather variation, target speed variation, and language instructions.
- The model starts from **\$\pi_{0.5}\$** and takes **4 RGB frames** (current plus 3 history frames), a language instruction, and UAV proprioception as input.
- A **temporal compression net** reduces token count for the 3 historical frames, then combines them with the current-frame tokens so the model can keep motion history without a large compute increase.
- A **dual-branch decoder** splits outputs into: (1) a spatial grounding head that predicts the target's relative 3D position and yaw as auxiliary supervision, and (2) a **flow-matching action expert** that predicts a **25-step** continuous displacement sequence for UAV control.
- Training uses a mixed loss with a position loss for the grounding branch and a flow-matching loss for the action branch, so the shared encoder learns geometry useful for control.

## Results
- On challenging **long-distance pedestrian tracking**, UAV-Track VLA reports **61.76% success rate** and **269.65 average tracking frames**.
- The abstract states these results **significantly outperform existing baselines**, but the provided excerpt does not include the full comparison table values needed to quantify the margin over each baseline.
- The model reduces single-step inference latency by **33.4%**, reaching **0.0571 s** per step relative to the original **\$\pi_{0.5}\$**.
- The benchmark contains **892,756 frames**, with about **200K** expert-demonstration frames and **690K** automatically collected frames.
- The paper claims **zero-shot generalization in unseen environments**, but the provided excerpt does not include the corresponding quantitative scores.

## Link
- [http://arxiv.org/abs/2604.02241v1](http://arxiv.org/abs/2604.02241v1)
