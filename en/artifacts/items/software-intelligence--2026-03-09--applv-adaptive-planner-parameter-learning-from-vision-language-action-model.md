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
- robot-navigation
- vision-language-models
- planner-parameter-learning
- classical-planning
- reinforcement-learning
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# APPLV: Adaptive Planner Parameter Learning from Vision-Language-Action Model

## Summary
This paper proposes APPLV, which shifts vision-language foundation models from “directly outputting robot actions” to “predicting classical navigation planner parameters,” in order to combine scene understanding with the safety, precise control, and real-time performance of classical planners. It targets mobile robot navigation in narrow, crowded, low-fault-tolerance environments, and shows better performance and generalization than existing parameter-learning methods in both simulation and real-robot experiments.

## Problem
- Classical navigation methods are safe and interpretable, but rely heavily on manual parameter tuning; a single static parameter set is hard to adapt to different environments or even different local situations within the same environment.
- End-to-end learning and direct VLA methods avoid manual tuning, but fall short in the centimeter-level precision required in narrow spaces, robustness to real-world noise, and real-time inference latency.
- Existing APPL-family methods can learn online parameter tuning, but still have limited generalization to unseen environments, and there is substantial room to improve overall navigation performance in highly constrained scenarios.

## Approach
- Core idea: instead of letting a large model directly control the robot, it uses the current image, historical frames, and robot state to output parameters for a classical local planner (such as speed limits, sampling density, and cost weights), after which the classical planner generates the actions.
- Model architecture: **Qwen2.5-VL-3B** is used to extract multi-layer hidden representations from the current custom bird’s-eye-view image and text prompt, combined with a history encoder to model temporal information, and then a **DPT-style regression head** fuses the features and regresses a parameter vector.
- Training is done in two stages: first, supervised fine-tuning (**applv-sl**) performs behavior cloning from navigation trajectories collected using heuristic expert rules and an existing **applr** policy; then reinforcement-learning fine-tuning (**applv-rlft**) uses **TD3** to further optimize success rate, time efficiency, and obstacle avoidance.
- A simple way to understand the design is: the large model is responsible for “understanding the environment and deciding what style the planner should be tuned to,” while the classical planner is responsible for “computing specific motion commands quickly and safely.”
- The method can be plugged into multiple classical local planners; the paper validates it on four planner types: **DWA, TEB, MPPI, DDP**.

## Results
- On **300 test BARN environments** (each tested 3 times), **applv-rlft** delivers the best or near-best results across all four planner types:
  - **DWA**: success rate **87.20%**, outperforming **applr 73.15%**, **Heuristic 82.47%**, **Transformer BC 83.03%**, and **Zero-Shot VLM 81.00%**; average time **18.68s**, also better than these baselines (**27.38/25.83/27.58/31.27s**, respectively).
  - **MPPI**: success rate **89.70%**, higher than **applr 78.53%**, **Heuristic 84.48%**, **Transformer BC 83.68%**, and **Zero-Shot VLM 85.24%**; average score **0.434**, also above the corresponding baselines **0.356/0.365/0.378/0.367**.
  - **DDP**: success rate **94.34%**, higher than **applr 85.35%**, **Heuristic 89.50%**, **Transformer BC 85.57%**, and **Zero-Shot VLM 92.50%**; average score **0.463**, also above **0.404/0.418/0.411/0.417**.
- On **TEB**, **applv-rlft** achieves a success rate of **90.30%**, slightly above **Transformer BC 90.25%** and **applv-sl 90.00%**, while reducing average time to **12.51s**, significantly faster than **Heuristic 19.11s**, **Transformer BC 20.35s**, **Zero-Shot VLM 16.64s**, and **applr 20.29s**; its average score **0.441** is also the best in this group.
- Compared with supervised-only **applv-sl**, **RL fine-tuning** further improves results on most planners: DWA success rate **86.10% → 87.20%**, MPPI **88.93% → 89.70%**, TEB **90.00% → 90.30%**, DDP **92.68% → 94.34%**.
- The paper also claims better **generalization to unseen environments** and better performance in **physical robot experiments** than existing methods, but the excerpt does not provide more detailed quantitative results for the physical experiments.

## Link
- [http://arxiv.org/abs/2603.08862v1](http://arxiv.org/abs/2603.08862v1)
