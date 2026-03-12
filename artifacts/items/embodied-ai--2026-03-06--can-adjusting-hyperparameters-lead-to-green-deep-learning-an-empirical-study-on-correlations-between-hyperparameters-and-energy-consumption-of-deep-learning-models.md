---
source: arxiv
url: http://arxiv.org/abs/2603.06195v1
published_at: '2026-03-06T12:07:14'
authors:
- Taoran Wang
- Yanhui Li
- Mingliang Ma
- Lin Chen
- Yuming Zhou
topics:
- green-deep-learning
- hyperparameter-tuning
- energy-efficiency
- empirical-study
- parallel-training
relevance_score: 0.04
run_id: materialize-outputs
---

# Can Adjusting Hyperparameters Lead to Green Deep Learning: An Empirical Study on Correlations between Hyperparameters and Energy Consumption of Deep Learning Models

## Summary
本文研究一个很实际但常被忽视的问题：调超参数不仅会影响模型效果，也会影响训练能耗。作者通过对真实深度学习模型做“超参数变异”实验，发现不少超参数与能耗存在相关性，而且有时可以在不伤害性能的前提下降低能耗。

## Problem
- 论文要解决的问题是：**超参数如何影响深度学习训练能耗，以及是否能通过调参让模型更“绿色”**。
- 这很重要，因为更大的数据和更复杂的模型正在显著推高计算资源、用电和碳排放，也增加训练与维护成本。
- 以往工作更多研究框架或性能优化，**超参数与能耗之间的系统性关系**仍缺少实证分析，尤其是在并行训练场景下。

## Approach
- 核心方法很简单：把常见“调参”过程视为一种**超参数变异**。作者从原始模型出发，围绕默认值随机改动 epochs、learning rate，以及各模型支持的第三个超参数（weight decay / gamma / threshold）。
- 他们在 **5 个真实开源模型**、**3 个数据集**（MNIST、CIFAR-10、Market-1501）上分别训练原模型和变异模型，并收集 **CPU package、RAM、GPU 能耗**、训练时间和准确率。
- 变异范围围绕默认值设置，例如 epochs 为 **[0.75d, 1.25d]**，learning rate 为 **[0.1d, d]** 或 **[d, 10d]**；每个模型对 3 个超参数各做 **5 次变异**，每个设置再运行 **5 次**，共构造 **375 个变异模型**。
- 分析上使用 **Spearman 相关分析**看超参数与能耗/性能的关系，用 **Wilcoxon signed-rank test** 和 **Cliff’s delta** 做与原模型的 trade-off 比较，判断是否存在更绿色的设置。
- 他们还额外研究**并行训练**：一次让两个模型并行训练，比较单模型训练与并行训练下结论是否变化。

## Results
- 论文声称：**许多超参数与能耗存在正相关或负相关**。在单训练场景下，表 4/5 汇总显示，epochs 对能耗相关性最稳定：在 energy 指标上累计出现 **18 次**一致相关信号；learning rate 在 energy 上累计 **18 次**、在 time/performance 上累计 **12 次**相关信号。
- 在并行场景下，能耗对超参数更敏感。表 6 显示并行训练中 energy 相关信号总数为 **60 次**（其中 learning rate **30 次**、epochs **30 次**），明显高于单训练表 4 的 **54 次**总相关信号；作者据此认为并行环境下能耗更容易随超参数变化。
- 论文给出一个具体例子：对 Siamese network 调低 learning rate 时，**平均 GPU 能耗约减少 1.6 kJ**，同时**平均准确率基本不受影响**，作为“调参可让训练更绿色”的直观证据。
- 作者明确宣称存在一些变异设置能做到**更低能耗且性能相当甚至更好**，即实现 greener DL；但在给定摘录中，**没有提供统一的精确百分比提升、完整基线数值或每个模型上的详细显著性结果**。
- 数据与规模方面，实验覆盖 **5 个模型、3 个数据集、375 个变异模型**，并同时测量 **pkg / ram / gpu / time / accuracy**，说明结论基于较系统的实证而非单一案例。

## Link
- [http://arxiv.org/abs/2603.06195v1](http://arxiv.org/abs/2603.06195v1)
