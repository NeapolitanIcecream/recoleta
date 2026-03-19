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
relevance_score: 0.44
run_id: materialize-outputs
language_code: zh-CN
---

# Can Adjusting Hyperparameters Lead to Green Deep Learning: An Empirical Study on Correlations between Hyperparameters and Energy Consumption of Deep Learning Models

## Summary
本文研究深度学习训练中的超参数调整是否会影响能耗，并检验是否能在不损伤性能的情况下实现更“绿色”的训练。结论是：许多超参数与能耗存在相关性，且并行训练时这种敏感性更强。

## Problem
- 现有深度学习越来越依赖更大数据和更复杂模型，训练能耗与成本持续上升，也带来更高碳排放。
- 过去研究多关注超参数对精度等性能的影响，但“超参数如何影响能耗”这一问题缺少系统实证证据。
- 这很重要，因为如果只通过调参就能降低训练能耗而不降性能，就能以很低工程成本提升绿色 AI 实践。

## Approach
- 作者把“调参”建模为一种**超参数变异**过程：围绕原始默认配置，随机改变 epochs、learning rate，以及每个模型特有的第三类超参数（weight decay、gamma 或 threshold）。
- 在 5 个真实开源深度学习模型、3 个常用数据集上，分别训练原始模型和变异模型，记录 package、RAM、GPU 能耗，以及训练时间和准确率等性能指标。
- 采用 `perf` 和 `nvidia-smi` 收集能耗数据，并在**单模型训练**与**双模型并行训练**两种场景下进行对比分析。
- 用 Spearman 相关分析研究“超参数—能耗/性能”的关系；用 Wilcoxon signed-rank test 与 Cliff’s delta 比较变异模型和原始模型的能耗-性能权衡，判断是否出现更绿色的配置。
- 实验共构造了 **375 个变异模型**（5 models × 3 hyperparameters × 5 mutations × 5 runs）；文中另称研究覆盖“五个模型”，贡献部分一处写“六个模型”，存在表述不一致。

## Results
- 单模型场景下，**epochs 与能耗相关性最稳定**：表 4 中 epochs 在 package/ram/gpu 三类能耗上均为 **0/0/0/0/6**，total 为 **0/0/0/0/18**，表示作者统计的 6 个相关检验均为同一方向的显著相关。
- 单模型场景下，**learning rate 的影响更复杂但更广泛**：表 4 的 total 为 **0/4/13/1/0**；对应性能与时间（表 5）total 为 **0/5/6/1/0**，说明学习率同时影响能耗、时间和性能。
- 并行场景下，相关性明显增强：表 6 中 epochs 的 total 为 **0/0/0/0/30**，learning rate 的 total 为 **1/5/23/1/0**，weight decay 为 **0/3/13/2/0**，比单模型场景覆盖更多显著关系，支持“并行训练时能耗对超参数更敏感”的结论。
- 论文给出一个具体例子：在 Siamese network 上降低 learning rate 时，**平均 GPU 能耗约减少 1.6 kJ**，同时**平均准确率基本不变**，说明调参可以在保持性能的同时降低训练能耗。
- 作者声称在五个真实模型和三类数据集上都观察到：部分变异配置比默认配置**更绿色**，即**能耗更低且性能相当或更好**；但在所给摘录中，RQ2 并未提供每个模型对应的完整显著性数值、具体能耗降幅或统一基线提升百分比。

## Link
- [http://arxiv.org/abs/2603.06195v1](http://arxiv.org/abs/2603.06195v1)
