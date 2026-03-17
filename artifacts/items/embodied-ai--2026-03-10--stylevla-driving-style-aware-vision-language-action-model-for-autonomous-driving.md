---
source: arxiv
url: http://arxiv.org/abs/2603.09482v1
published_at: '2026-03-10T10:33:58'
authors:
- Yuan Gao
- Dengyuan Hua
- Mattia Piccinini
- "Finn Rasmus Sch\xE4fer"
- Korbinian Moller
- Lin Li
- Johannes Betz
topics:
- vision-language-action
- autonomous-driving
- style-conditioned-policy
- physics-informed-learning
- trajectory-generation
relevance_score: 0.74
run_id: materialize-outputs
---

# StyleVLA: Driving Style-Aware Vision Language Action Model for Autonomous Driving

## Summary
本文提出面向自动驾驶的风格感知视觉-语言-动作模型 StyleVLA，并同时构建了带有五种驾驶风格标注的数据集。核心结论是：通过物理约束监督微调一个轻量级 4B 多模态模型，可以在风格一致性与轨迹可行性上超过通用闭源大模型。

## Problem
- 现有自动驾驶 VLA/VLM 通常只学到单一驾驶策略，难以按用户要求生成如舒适、运动或安全等不同风格的轨迹。
- 公开自动驾驶数据集虽然有丰富感知信息，但缺少明确的多风格轨迹监督，导致“可控个性化驾驶”训练基础不足。
- 许多方法把轨迹当作离散 token 预测，缺少显式车辆运动学约束，容易产生不够物理可行的输出。

## Approach
- 构建 **StyleVLA dataset**：基于 CommonRoad + Frenetix 运动规划器，从 **1,484** 个场景生成五种风格轨迹，并经统计过滤后得到 **1,216** 个场景、**76,030** 个 BEV 样本和 **42,084** 个 FPV 样本。
- 五种风格分别为 **Default / Balanced / Comfort / Sporty / Safety**；通过调整规划代价函数中速度、jerk、障碍距离、可见性等权重，生成不同风格的“真值”轨迹。
- 将任务转成多模态指令学习：输入图像、历史自车状态、目标点和风格指令，输出未来 **3s 或 5s** 的结构化轨迹 JSON。
- 以 **Qwen3-VL-4B** 为底座，采用 **QLoRA 4-bit** 微调，并在标准交叉熵损失外加入一个 **MLP 回归头**，直接回归连续轨迹状态，减少离散 token 带来的量化误差。
- 再加入 **physics-informed kinematic consistency loss (PIKC)**，用简单运动学方程约束相邻时刻的位置、速度、朝向、加速度关系，提升物理一致性与可执行性。

## Results
- 数据集过滤后的风格统计显示差异明确：**Sporty** 平均速度最高 **7.32 m/s**、路径最长 **25.13 m**；**Safety** 平均速度最低 **6.39 m/s**、路径最短 **21.44 m**；**Comfort** 的 RMS jerk 最低 **0.727 m/s^3**。
- BEV 消融实验表明，数据越多越好：从 **4.5k** 到 **50k** 训练样本，**ADE 2.08→1.17 m**，**FDE 5.43→3.06 m**，**PSR 20.60%→33.19%**，**Heading MAE 0.073→0.035 rad**。
- 损失函数消融表明物理监督有效：在 **50k** 数据上，**CE** 到 **CE+REG** 使 **FDE 3.82→3.17 m**、**PSR 29.00%→32.08%**；再加 **PIKC** 后达到 **ADE 1.17 m、FDE 3.06 m、PSR 33.19%、Heading MAE 0.035 rad**，优于仅 CE 的 **ADE 1.47 m、FDE 3.82 m、PSR 29.00%、0.043 rad**。
- 文中称基础开源模型在零样本下 **0% success**，说明通用预训练模型并不天然具备驾驶物理与风格控制能力。
- BEV 基准中，微调后的 **Qwen3-VL-4B** 成功率达到 **39.47%**，明显高于最佳闭源基线 **16.38%**；同时推理时间约 **1.92 s**，而部分专有模型单次推理需 **70 s+**。
- 论文开头给出的综合风格驾驶得分上，**StyleVLA** 达到 **0.55 (BEV)** 和 **0.51 (FPV)**，相比 **Gemini-3-Pro** 的 **0.32** 和 **0.35** 更高，表明专用、轻量、物理约束驱动的模型在该领域任务上可超过闭源通用模型。

## Link
- [http://arxiv.org/abs/2603.09482v1](http://arxiv.org/abs/2603.09482v1)
