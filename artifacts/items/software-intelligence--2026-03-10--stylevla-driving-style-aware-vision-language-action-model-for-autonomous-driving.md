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
- autonomous-driving
- vision-language-action
- driving-style-control
- physics-informed-learning
- trajectory-generation
relevance_score: 0.18
run_id: materialize-outputs
---

# StyleVLA: Driving Style-Aware Vision Language Action Model for Autonomous Driving

## Summary
StyleVLA提出了一个面向自动驾驶的“驾驶风格可控”视觉-语言-动作模型，并同时构建了支持五种驾驶风格的数据集。其核心结论是：结合物理约束监督的轻量级专用模型，在风格感知轨迹生成上可显著超过通用闭源VLM/VLA基线。

## Problem
- 现有自动驾驶数据集通常缺少**显式驾驶风格标注**，导致模型难以学习如Comfort、Sporty、Safety等差异化行为。
- 现有VLA模型大多只学习**单一通用驾驶策略**，无法根据用户指定风格生成可控轨迹，这影响个性化体验、舒适性与用户接受度。
- 许多方法将轨迹生成视为**纯token预测**，缺乏对车辆运动学约束的显式建模，容易产生物理上不合理的输出。

## Approach
- 构建**StyleVLA数据集**：基于CommonRoad与Frenetix规划器，从1,484个场景中为五种风格（Default、Balanced、Comfort、Sporty、Safety）生成风格轨迹，并经统计过滤后得到**1,216个场景、76,030个BEV样本、42,084个FPV样本**。
- 通过**风格特定代价函数**生成监督信号：简单说，就是给“速度、加速度抖动、与障碍物距离、风险/可见性”等项设置不同权重，让同一场景下规划器自动产出不同驾驶风格的轨迹。
- 在模型上，采用**Qwen3-VL-4B**为基础模型，用**QLoRA**低成本微调，并把轨迹输出组织为结构化JSON，预测未来3秒或5秒的完整运动学状态。
- 在训练目标上，使用**混合损失**：标准交叉熵负责生成离散轨迹token，额外的MLP回归头负责连续状态回归，再加入**物理信息驱动的运动学一致性损失（PIKC）**，约束相邻时刻位置与速度/加速度/航向之间满足基本车辆运动规律。

## Results
- 数据集规模方面，论文声称StyleVLA包含**1,216个场景**，**76,030个BEV样本**和**42,084个FPV样本**；五种风格在统计上可区分，例如**Sporty平均速度7.32 m/s**最高，**Safety平均速度6.39 m/s**最低，**Comfort RMS jerk 0.727 m/s³**最低。
- 在BEV消融实验中，训练数据从**4.5k→50k**持续提升性能：ADE从**2.08 m降到1.17 m**，FDE从**5.43 m降到3.06 m**，PSR从**20.60%升到33.19%**，Heading MAE从**0.073降到0.035 rad**。
- 在损失函数消融中，基于50k训练集，**CE**到**CE+REG**可将FDE从**3.82 m降到3.17 m**、PSR从**29.00%升到32.08%**；再加入**PIKC**后，ADE进一步从**1.21 m降到1.17 m**，FDE从**3.17 m降到3.06 m**，PSR升到**33.19%**，Heading MAE从**0.036降到0.035 rad**。
- 在BEV基准对比中，作者称微调后的**Qwen3-VL-4B**在2,000个测试样本上达到**39.47% success rate**，而最佳闭源基线仅**16.38%**；同时推理时间约**1.92 s**，而某些专有模型单次推理需**70 s以上**。
- 论文摘要片段给出的综合风格驾驶评分显示，**StyleVLA达到0.55（BEV）和0.51（FPV）**，显著高于**Gemini-3-Pro的0.32（BEV）和0.35（FPV）**。该综合分数同时考虑成功率、物理可行性和对用户指定风格的遵循度。
- 作者据此声称，一个**专用、轻量、物理感知**的模型能够在领域特定任务上超过通用闭源模型；这是论文最核心的突破性结论。

## Link
- [http://arxiv.org/abs/2603.09482v1](http://arxiv.org/abs/2603.09482v1)
