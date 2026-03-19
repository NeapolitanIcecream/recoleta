---
source: arxiv
url: http://arxiv.org/abs/2603.06987v1
published_at: '2026-03-07T02:11:29'
authors:
- Isaac R. Ward
- Michelle Ho
- Houjun Liu
- Aaron Feldman
- Joseph Vincent
- Liam Kruse
- Sean Cheong
- Duncan Eddy
- Mykel J. Kochenderfer
- Mac Schwager
topics:
- world-model
- failure-detection
- bimanual-manipulation
- conformal-prediction
- robot-anomaly-detection
- foundation-vision-model
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Foundational World Models Accurately Detect Bimanual Manipulator Failures

## Summary
本文提出一种用于双臂机器人运行时失效检测的方法：在预训练视觉基础模型的压缩潜空间里训练概率世界模型，并用其不确定性做异常分数。核心价值在于无需显式枚举高维失败模式，就能更可靠地发现即将发生或正在发生的操纵失败。

## Problem
- 论文解决的是**双臂视觉运动机器人在部署中如何实时检测异常失败**的问题；这很重要，因为失败可能导致性能下降、设备损坏，甚至危及人身安全。
- 这类机器人状态空间极大，包含多视角图像、动作和本体感觉信号，**手工定义所有失败模式几乎不可行**。
- 传统统计或简单重构式异常检测方法难以处理**高维、多模态、时序相关**的机器人行为数据。

## Approach
- 用预训练视觉基础模型 **NVIDIA Cosmos Tokenizer** 先把多视角图像压缩到潜空间，再结合动作和本体感觉历史，训练一个**历史条件概率世界模型**预测下一步状态。
- 世界模型采用 **VAE 风格**输出未来潜变量分布；其**预测方差/标准差**可直接当作“我对当前行为有多不确定”的分数。简单说：模型只学“正常行为”，遇到不像训练分布的行为时，不确定性会上升。
- 论文设计了两种失效分数：**(1) 世界模型不确定性**；**(2) 世界模型预测误差**（预测与真实下一状态在潜空间中的差异）。
- 用**保形预测（conformal prediction）**在仅使用正常轨迹的校准集上自动设定阈值，从而把连续分数转成运行时“正常/异常”判断，并控制误报率。
- 还引入了一个新的真实数据集 **Bimanual Cable Manipulation**，包含多相机、动作/本体感觉信号，以及标注的失败轨迹，用于评测真实双臂电缆操作中的掉线缆等失败。

## Results
- 在 **Bimanual Cable Manipulation** 上，作者方法 **WM uncertainty** 取得最佳总体分类准确率：**92.0±6.4%**，其中正常轨迹 **87.9±17.0%**、失败轨迹 **95.1±5.5%**；对应阈值为 **85% conformal prediction threshold**。
- 同一数据集上，**WM prediction error** 达到 **87.9±6.4%** 总体准确率；优于多种基线，但低于 WM uncertainty 的 **92.0±6.4%**。
- 与学习型基线相比，最佳作者方法比次优学习方法 **logpZO** 的总体准确率 **89.3±6.8%** 高 **约2.7 个百分点**；论文摘要还声称其**failure detection rate 高 3.8%**。
- 与其他基线相比：**AE reconstruction error 61.0±4.2%**、**AE sim 66.4±6.1%**、**SPARC 42.6±6.8%**、**PCA K-means 48.6±12.6%**、**Random 38.7±6.4%**；说明该方法明显优于统计技术和若干常见异常检测方法。
- 参数效率上，作者世界模型只有 **569.7k** 可训练参数，而次优学习型方法约 **10M**；即**约 1/20 参数量**仍取得更好效果。
- 在 **Push-T** 仿真中，方法在 **1028** 条正常训练轨迹、**128** 条验证轨迹、**512** 条正常测试轨迹和 **2048** 条失败轨迹（**4** 种失败模式，各 **512** 条）上展示出能区分**视觉异常**（改颜色）和**动力学异常**（改摩擦）的能力，但文中摘录未给出该实验的完整量化指标。

## Link
- [http://arxiv.org/abs/2603.06987v1](http://arxiv.org/abs/2603.06987v1)
