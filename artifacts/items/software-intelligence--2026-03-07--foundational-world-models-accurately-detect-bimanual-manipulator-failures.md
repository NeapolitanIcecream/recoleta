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
- robot-failure-detection
- world-models
- bimanual-manipulation
- conformal-prediction
- vision-foundation-models
relevance_score: 0.28
run_id: materialize-outputs
---

# Foundational World Models Accurately Detect Bimanual Manipulator Failures

## Summary
本文提出一种在视觉基础模型压缩潜空间中训练的概率世界模型，用于实时检测双臂机械臂的异常失败。核心思想是：只学习“正常行为”的时序动态，并把模型预测时的不确定性当作失败信号。

## Problem
- 双臂机械臂部署在高风险场景时，失败可能导致性能下降、设备损坏或人员安全风险，因此需要可靠的在线失败检测。
- 机器人状态空间由多视角图像、动作和本体感觉组成，维度极高，无法手工枚举或定义所有失败模式。
- 现有统计或简单重构式异常检测方法难以捕捉高维、时序、多模态机器人行为中的异常偏离。

## Approach
- 使用预训练视觉基础模型 **NVIDIA Cosmos Tokenizer** 将多视角图像压缩到潜空间，在此基础上训练一个**历史条件概率世界模型**，输入过去一段时间的图像、本体感觉和动作，预测下一时刻状态分布。
- 世界模型采用 **VAE 风格** 机制，不只给出预测，还输出潜变量分布的标准差；这个标准差的均值被当作**世界模型不确定性分数**。
- 同时还定义第二种分数：**世界模型预测误差**，即预测的下一步潜表示与真实观测潜表示之间的差异。
- 只用**正常轨迹**训练模型，并用**保形预测（conformal prediction）**在留出的正常数据上校准阈值；运行时若轨迹统计量超过阈值，则判为异常/失败。
- 该方法与多种基线比较，包括 normalizing flow、自动编码器重构误差、最近邻安全集相似度、SPARC、PCA+K-means 和随机基线；并引入新的 **Bimanual Cable Manipulation** 数据集。

## Results
- 在 **Bimanual Cable Manipulation** 数据集上，使用 **85% conformal threshold** 时，**WM uncertainty** 达到 **92.0% ± 6.4** 加权总分类准确率，包含 **87.9% ± 17.0** 的 nominal 准确率和 **95.1% ± 5.5** 的 failure 准确率，为表中最佳。
- 同一数据集上，**WM prediction error** 为 **87.9% ± 6.4** 加权准确率；次优学习基线 **logpZO** 为 **89.3% ± 6.8**，而 **AE reconstruction** 仅 **61.0% ± 4.2**，**AE sim** 为 **66.4% ± 6.1**。
- 相比统计方法，优势明显：**SPARC 42.6% ± 6.8**、**PCA K-means 48.6% ± 12.6**、**Random 38.7% ± 6.4**，说明世界模型方法在该任务上显著更强。
- 论文声称该方法仅有 **569.7k** 可训练参数，而“下一好的学习式方法”约为 **10M** 参数，即约 **1/20** 参数规模；同时其失败检测率仍**高出 3.8 个百分点**。
- 在 **Push-T** 仿真中，作者构造了 **4** 种失败模式（改色两种、降低摩擦、去除摩擦），共使用 **1028** 条训练 nominal、**128** 条验证 nominal、**512** 条测试 nominal 和 **2048** 条失败轨迹；结果显示世界模型不确定性能把视觉异常和动力学异常与正常轨迹分开，但摘录中未给出该实验的完整量化指标。
- 新引入的 **Bimanual Cable Manipulation** 数据集包含 **83** 条 nominal 训练/验证轨迹、**7** 条 nominal 校准、**7** 条 nominal 测试、**9** 条 failure 测试；任务为数据中心维护中的双臂插接电缆，主要失败模式是**电缆脱手**。

## Link
- [http://arxiv.org/abs/2603.06987v1](http://arxiv.org/abs/2603.06987v1)
