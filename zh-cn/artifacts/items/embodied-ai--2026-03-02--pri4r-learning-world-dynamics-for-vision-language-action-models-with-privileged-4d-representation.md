---
source: arxiv
url: http://arxiv.org/abs/2603.01549v2
published_at: '2026-03-02T07:23:53'
authors:
- Jisoo Kim
- Jungbin Cho
- Sanghyeok Chu
- Ananya Bal
- Jinhyung Kim
- Gunhee Lee
- Sihaeng Lee
- Seung Hwan Kim
- Bohyung Han
- Hyunmin Lee
- Laszlo A. Jeni
- Seungryong Kim
topics:
- vision-language-action
- world-model
- robot-manipulation
- 3d-point-tracking
- privileged-learning
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation

## Summary
Pri4R让视觉-语言-动作（VLA）模型在训练时额外学习“动作会如何改变3D世界”，从而提升机器人操控的物理感知与控制精度。它用特权4D表示（3D点轨迹随时间变化）做辅助监督，但测试时不增加任何输入、输出或计算开销。

## Problem
- 现有VLA主要用动作标签训练，学到的是“怎么动”，但往往学不到“动了之后世界会怎样变化”。
- 这会导致策略虽然语义上合理，却缺乏对几何约束、接触和物体运动规律的理解，在门把手、抽屉、旋钮等交互中容易失败。
- 以语言、图像、特征或目标观测作为辅助预测信号，通常与机器人控制所处的时空度量空间不直接对齐，且常带来额外推理开销。

## Approach
- 核心方法是在训练阶段给VLA加一个轻量级point track head，让它根据当前观测和骨干网络内部特征，预测未来一段时间的**3D点位移轨迹**。
- 这些3D点轨迹是“特权监督”：仿真中由真实场景网格生成，真实数据中由现成3D点跟踪器伪标注；训练完成后该分支被丢弃。
- 通过把VLA用于动作预测的内部嵌入注入到点轨迹头，点轨迹损失的梯度会反向塑造共享表征，使其编码场景几何如何随动作演化。
- 作者选择**3D点轨迹**而不是图像、语言或深度图，因为它同时具备时间稠密、几何度量化、空间稀疏且与动作空间更对齐的优点。
- 该设计可兼容两类主流VLA：backbone-centric（如OpenVLA-OFT）和expert-style（如π系列），只需很小结构改动，且推理时恢复原始VLA架构不变。

## Results
- **LIBERO**：OpenVLA-OFT平均成功率从 **92.7%** 提升到 **96.3%**（+3.6）；其中 **LIBERO-Long** 从 **85.5%** 提升到 **95.3%**（+9.8，约可视为+10%）。
- **LIBERO**：π0.5 从 **92.6%** 提升到 **94.0%**（+1.4）；**LIBERO-Long** 从 **90.5%** 提升到 **94.3%**（+3.8）。π0 从 **87.4%** 提升到 **90.6%**（+3.2）。
- **RoboCasa**：OpenVLA-OFT平均成功率从 **33.1%** 提升到 **46.3%**（+13.2，约相对提升 **40%**）；分项上如 turning levers **36.0→66.7**（+30.7）、pressing buttons **56.0→79.3**（+23.3）、open/close drawers **59.0→80.0**（+21.0）。
- **RoboCasa**：π0.5 平均 **52.9→57.0**（+4.1），π0 平均 **38.8→42.2**（+3.4），说明收益跨不同VLA架构都存在。
- 论文还声称在**真实世界实验**中同样有提升，并通过消融验证3D点轨迹是学习action-world dynamics的更有效监督目标；但给定摘录未提供真实机器人部分的具体数值。

## Link
- [http://arxiv.org/abs/2603.01549v2](http://arxiv.org/abs/2603.01549v2)
