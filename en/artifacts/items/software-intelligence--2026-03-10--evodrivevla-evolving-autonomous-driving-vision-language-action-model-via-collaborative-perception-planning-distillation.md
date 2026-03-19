---
source: arxiv
url: http://arxiv.org/abs/2603.09465v1
published_at: '2026-03-10T10:19:07'
authors:
- Jiajun Cao
- Xiaoan Zhang
- Xiaobao Wei
- Liyuqiu Huang
- Wang Zijian
- Hanzhen Zhang
- Zhengyu Jia
- Wei Mao
- Hao Wang
- Xianming Liu
- Shuchang Zhou Liu
- Yang Wang
- Shanghang Zhang
topics:
- autonomous-driving
- vision-language-action
- knowledge-distillation
- trajectory-planning
- multimodal-learning
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# EvoDriveVLA: Evolving Autonomous Driving Vision-Language-Action Model via Collaborative Perception-Planning Distillation

## Summary
EvoDriveVLA is a vision-language-action distillation framework for autonomous driving, designed to simultaneously address perception degradation after visual encoder fine-tuning and instability in long-horizon planning. It combines “preserving original visual capabilities” with “using a stronger teacher to teach trajectory planning,” achieving leading results in both open-loop and closed-loop evaluations.

## Problem
- Existing autonomous driving VLA models tend to lose the robust visual representations acquired during pretraining after the visual encoder is unfrozen, leading to degraded perception.
- Long-horizon trajectory planning is prone to instability and error accumulation; if the teacher and student are trained under the same conditions, the teacher is not inherently better at planning than the student, limiting the value of distillation.
- Existing multi-trajectory distillation methods often rely on predefined planning vocabularies, and trajectory diversity and scene adaptability remain constrained, affecting generalization and safety in real dynamic driving scenarios.

## Approach
- Proposes the collaborative perception-planning distillation framework EvoDriveVLA, consisting of two parts: self-anchored visual distillation and oracle-guided trajectory distillation.
- On the perception side, it first copies the student’s visual encoder as a “self-anchor teacher,” which constrains the student during fine-tuning from drifting away from the original visual representations; at the same time, it uses AnchorFormer based on ground-truth future trajectories to assign higher constraint weights to key visual tokens.
- On the planning side, it constructs an “oracle teacher”: during training, it additionally sees future images and future ego states, giving it stronger future awareness and trajectory prediction ability than the student.
- The oracle teacher first generates a coarse trajectory, then feeds that coarse trajectory back into the model for coarse-to-fine refinement, producing more accurate and smoother candidate trajectories.
- It then uses MC-Dropout to sample hidden states 10 times (dropout rate 0.1) to expand the candidate set, selects the best trajectory with the minimum cross-entropy to the ground truth, and distills it to the student at both the hidden-state and output-distribution levels.

## Results
- **nuScenes open-loop**: EvoDriveVLA reaches **Avg L2 = 0.26 m** and **Avg Collision = 0.06%** under the **ST-P3** setting; compared with **DiMA** at **0.27 m / 0.08%**, this is an improvement of **0.01 m** and **0.02 percentage points**, respectively.
- **nuScenes open-loop**: On 3-second L2 / Collision under **ST-P3**, EvoDriveVLA achieves **0.43 m / 0.12%**, outperforming **OpenDriveVLA** at **0.55 m / 0.22%**, reducing them by **0.12 m** and **0.10 percentage points**, respectively.
- **nuScenes open-loop**: Under the **UniAD** setting, EvoDriveVLA achieves **Avg L2 = 0.52 m**, outperforming **DiMA** at **0.57 m** and **OpenDriveVLA** at **0.67 m**.
- **nuScenes open-loop**: Under the **UniAD** setting, EvoDriveVLA has **Avg Collision = 0.12%**; this is lower than **OpenDriveVLA** at **0.30%**, but higher than **DiMA** at **0.07%**, indicating that not every open-loop submetric is absolutely best.
- **NAVSIM closed-loop**: EvoDriveVLA achieves **PDMS = 85.3**, higher than **PARA-Drive** at **84.0**, **UniAD** at **83.4**, and **QwenVL2.5-8B** at **83.3**, making it the best in the table.
- **NAVSIM closed-loop**: EvoDriveVLA also achieves **NC 98.0**, **DAC 93.3**, **TTC 93.1**, **EP 81.1**, and **Comfort 100**; among these, **EP 81.1** is higher than **PARA-Drive 79.3** and **UniAD 78.8**, showing a significant improvement in closed-loop driving quality.

## Link
- [http://arxiv.org/abs/2603.09465v1](http://arxiv.org/abs/2603.09465v1)
