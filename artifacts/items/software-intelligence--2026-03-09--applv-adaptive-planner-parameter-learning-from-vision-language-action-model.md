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
---

# APPLV: Adaptive Planner Parameter Learning from Vision-Language-Action Model

## Summary
本文提出 APPLV，将视觉-语言基础模型从“直接输出机器人动作”改为“预测经典导航规划器参数”，以兼顾场景理解能力与经典规划器的安全性、精确控制和实时性。它面向狭窄、拥挤、低容错环境中的移动机器人导航，并在仿真与实体机器人上显示出比现有参数学习方法更好的性能与泛化。

## Problem
- 经典导航方法安全、可解释，但高度依赖人工调参；同一组静态参数难以适应不同环境甚至同一环境中的不同局部情况。
- 端到端学习和直接式 VLA 虽然绕开了调参，但在狭窄空间所需的厘米级精度、真实噪声鲁棒性和实时推理延迟方面表现不足。
- 现有 APPL 系列能学会在线调参，但在未见环境上的泛化仍有限，且整体导航性能在高约束场景中还有明显提升空间。

## Approach
- 核心思想：不让大模型直接控制机器人，而是让它根据当前图像、历史帧和机器人状态，输出经典局部规划器的参数（如速度上限、采样密度、代价权重），再由经典规划器生成动作。
- 模型结构：使用 **Qwen2.5-VL-3B** 提取当前自定义俯视图与文本提示的多层隐藏表示，结合一个历史编码器建模时序信息，再通过 **DPT 风格回归头** 融合特征并回归参数向量。
- 训练分两步：先做监督微调（applv-sl），从启发式专家规则和已有 applr 策略收集的导航轨迹中做行为克隆；再做强化学习微调（applv-rlft），用 **TD3** 进一步优化成功率、时间效率与避障表现。
- 该设计的简单理解是：大模型负责“看懂环境并决定该把规划器调成什么风格”，经典规划器负责“高速、安全地算出具体运动命令”。
- 方法可插拔到多种经典局部规划器上，文中验证了 **DWA、TEB、MPPI、DDP** 四类规划器。

## Results
- 在 **300 个测试 BARN 环境**（每个环境测试 3 次）上，**applv-rlft** 在四类规划器中都给出最强或接近最强结果：
  - **DWA**：成功率 **87.20%**，优于 applr **73.15%**、Heuristic **82.47%**、Transformer BC **83.03%**、Zero-Shot VLM **81.00%**；平均时间 **18.68s** 也优于这些基线（分别为 **27.38/25.83/27.58/31.27s**）。
  - **MPPI**：成功率 **89.70%**，高于 applr **78.53%**、Heuristic **84.48%**、Transformer BC **83.68%**、Zero-Shot VLM **85.24%**；平均分 **0.434** 也高于对应基线 **0.356/0.365/0.378/0.367**。
  - **DDP**：成功率 **94.34%**，高于 applr **85.35%**、Heuristic **89.50%**、Transformer BC **85.57%**、Zero-Shot VLM **92.50%**；平均分 **0.463** 也高于 **0.404/0.418/0.411/0.417**。
- 在 **TEB** 上，applv-rlft 的成功率 **90.30%**，略高于 Transformer BC **90.25%** 和 applv-sl **90.00%**，同时平均时间降至 **12.51s**，明显快于 Heuristic **19.11s**、Transformer BC **20.35s**、Zero-Shot VLM **16.64s**、applr **20.29s**；平均分 **0.441** 也为该组最佳。
- 相比仅做监督学习的 **applv-sl**，**RL fine-tuning** 在多数规划器上继续提升：DWA 成功率 **86.10% → 87.20%**，MPPI **88.93% → 89.70%**，TEB **90.00% → 90.30%**，DDP **92.68% → 94.34%**。
- 论文还声称在**未见环境泛化**和**实体机器人实验**中优于现有方法，但摘录中未提供更细的实体实验量化数字。

## Link
- [http://arxiv.org/abs/2603.08862v1](http://arxiv.org/abs/2603.08862v1)
