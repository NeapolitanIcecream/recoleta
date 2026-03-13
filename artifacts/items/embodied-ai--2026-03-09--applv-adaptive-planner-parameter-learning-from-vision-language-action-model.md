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
---

# APPLV: Adaptive Planner Parameter Learning from Vision-Language-Action Model

## Summary
本文提出 APPLV，一种不直接输出机器人动作、而是让视觉-语言-动作模型预测经典导航规划器参数的方法，用于狭窄拥挤环境中的移动机器人导航。它试图结合基础模型的场景理解能力与经典规划器的安全性、精确性和低延迟控制。

## Problem
- 经典导航方法虽然更安全、可解释，但对速度上限、代价权重、采样密度等参数高度敏感，通常需要针对具体环境手工调参。
- 端到端学习和直接动作式 VLA 省去了手工调参，但在狭窄空间中往往难以实现厘米级精确控制，且推理延迟较高，泛化到未见环境也较弱。
- 现有混合式参数学习方法（如 APPL 系列）能自动调参，但在未见环境中的泛化和整体导航表现仍不足。

## Approach
- 核心思想：**不让 VLA 直接控制机器人，而是让它预测经典局部规划器的参数**，再由 DWA/TEB/MPPI/DDP 等经典规划器生成实际控制命令。
- 输入由当前自定义俯视图图像、历史帧、机器人当前速度状态以及上一时刻参数组成；图像中编码了障碍激光、全局路径和机器人位姿等关键信息。
- 视觉语言骨干使用 **Qwen2.5-VL-3B** 提取多层隐藏特征，并通过 **LoRA** 做参数高效微调；同时用一个历史编码器建模时间上下文。
- 这些当前帧多层特征与历史特征被送入 **DPT 风格回归头**，输出规划器参数，如速度限制、代价函数权重、规划时域等。
- 训练分两阶段：先用示范轨迹做监督学习（applv-sl，最小化参数回归 MSE），再用 **TD3** 做强化学习微调（applv-rlft），直接优化导航奖励。

## Results
- 在 **300 个测试 BARN 环境**、4 类局部规划器上，**applv-rlft 均取得各组最高 Avg. Score**：DWA **0.374**、MPPI **0.434**、TEB **0.441**、DDP **0.463**。
- **DWA** 上，applv-rlft 相比 applr：成功率 **87.20% vs 73.15%**，平均时间 **18.68s vs 27.38s**，Avg. Score **0.374 vs 0.296**；相比 Heuristic Expert，成功率提升 **4.73 个百分点**（87.20% vs 82.47%）。
- **MPPI** 上，applv-rlft 达到成功率 **89.70%**、平均时间 **16.75s**、Avg. Score **0.434**；优于 applv-sl 的 **0.415** 和 Heuristic Expert 的 **0.365**，也高于 Zero-Shot VLM 的 **0.367**。
- **TEB** 上，applv-rlft 的 Avg. Score 为 **0.441**，高于 Zero-Shot VLM 的 **0.398**、Transformer BC 的 **0.383** 和 Heuristic Expert 的 **0.388**；其平均时间 **12.51s** 也是该组最低。
- **DDP** 上，applv-rlft 取得全表最高成功率之一 **94.34%** 与 Avg. Score **0.463**，优于 Zero-Shot VLM 的 **92.50% / 0.417**、applv-sl 的 **92.68% / 0.440**、applr 的 **85.35% / 0.404**。
- 论文还声称在**真实 Jackal 机器人实验**中验证了方法，并强调对**未见环境的更好泛化**；但摘录中未给出真实机器人部分的具体数值。

## Link
- [http://arxiv.org/abs/2603.08862v1](http://arxiv.org/abs/2603.08862v1)
