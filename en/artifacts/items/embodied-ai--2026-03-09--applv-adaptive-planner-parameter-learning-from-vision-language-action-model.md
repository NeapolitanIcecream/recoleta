---
source: arxiv
url: http://arxiv.org/abs/2603.08862v1
published_at: '2026-03-09T19:23:09'
authors:
- Yuanjie Lu
- Beichen Wang
- Zhengqi Wu
- Yang Li
- Xiaomin Lin
- Chengzhi Mao
- Xuesu Xiao
topics:
- vision-language-action
- robot-navigation
- planner-parameter-learning
- classical-planning
- foundation-models
- sim2real
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# APPLV: Adaptive Planner Parameter Learning from Vision-Language-Action Model

## Summary
This paper proposes APPLV, a method that does not directly output robot actions, but instead uses a vision-language-action model to predict the parameters of a classical navigation planner for mobile robot navigation in narrow, crowded environments. It aims to combine the scene understanding capability of foundation models with the safety, precision, and low-latency control of classical planners.

## Problem
- Although classical navigation methods are safer and more interpretable, they are highly sensitive to parameters such as speed limits, cost weights, and sampling density, and typically require manual tuning for specific environments.
- End-to-end learning and direct-action VLA methods eliminate manual parameter tuning, but often struggle to achieve centimeter-level precise control in narrow spaces, have relatively high inference latency, and generalize poorly to unseen environments.
- Existing hybrid parameter-learning methods (such as the APPL series) can automate parameter tuning, but their generalization to unseen environments and overall navigation performance remain insufficient.

## Approach
- Core idea: **instead of letting the VLA directly control the robot, it predicts the parameters of a classical local planner**, and then classical planners such as DWA/TEB/MPPI/DDP generate the actual control commands.
- The input consists of the current custom bird's-eye-view image, historical frames, the robot's current velocity state, and the previous timestep's parameters; the image encodes key information such as obstacle laser scans, the global path, and robot pose.
- The vision-language backbone uses **Qwen2.5-VL-3B** to extract multi-layer hidden features, and applies **LoRA** for parameter-efficient fine-tuning; at the same time, a history encoder is used to model temporal context.
- These multi-layer features from the current frame and the historical features are fed into a **DPT-style regression head**, which outputs planner parameters such as speed limits, cost function weights, and planning horizons.
- Training is conducted in two stages: first, supervised learning on demonstration trajectories (applv-sl, minimizing parameter regression MSE), then reinforcement learning fine-tuning with **TD3** (applv-rlft) to directly optimize navigation rewards.

## Results
- Across **300 test BARN environments** and 4 types of local planners, **applv-rlft achieved the highest Avg. Score in every group**: DWA **0.374**, MPPI **0.434**, TEB **0.441**, and DDP **0.463**.
- On **DWA**, compared with applr, applv-rlft achieved a success rate of **87.20% vs 73.15%**, average time of **18.68s vs 27.38s**, and Avg. Score of **0.374 vs 0.296**; compared with the Heuristic Expert, its success rate improved by **4.73 percentage points** (**87.20% vs 82.47%**).
- On **MPPI**, applv-rlft reached a success rate of **89.70%**, average time of **16.75s**, and Avg. Score of **0.434**; this outperformed applv-sl's **0.415** and the Heuristic Expert's **0.365**, and was also higher than Zero-Shot VLM's **0.367**.
- On **TEB**, applv-rlft achieved an Avg. Score of **0.441**, higher than Zero-Shot VLM's **0.398**, Transformer BC's **0.383**, and the Heuristic Expert's **0.388**; its average time of **12.51s** was also the lowest in that group.
- On **DDP**, applv-rlft obtained one of the highest success rates in the full table at **94.34%** and an Avg. Score of **0.463**, outperforming Zero-Shot VLM's **92.50% / 0.417**, applv-sl's **92.68% / 0.440**, and applr's **85.35% / 0.404**.
- The paper also claims validation in **real Jackal robot experiments** and emphasizes **better generalization to unseen environments**; however, the excerpt does not provide specific quantitative results for the real-robot portion.

## Link
- [http://arxiv.org/abs/2603.08862v1](http://arxiv.org/abs/2603.08862v1)
