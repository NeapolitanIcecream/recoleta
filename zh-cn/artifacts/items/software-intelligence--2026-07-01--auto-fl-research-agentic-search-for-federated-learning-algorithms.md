---
source: arxiv
url: https://arxiv.org/abs/2607.01366v1
published_at: '2026-07-01T18:28:09'
authors:
- Holger R. Roth
- Ziyue Xu
- Chester Chen
- Daguang Xu
- Peter Cnudde
- Andrew Feng
topics:
- federated-learning
- coding-agents
- automated-research
- fl-optimization
- nvflare
- benchmark-evaluation
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Auto-FL-Research: Agentic Search for Federated Learning Algorithms

## Summary
## 摘要
Auto-FL-Research 是一种受约束的编码代理工作流，用于搜索联邦学习训练配方，同时固定数据、预算、通信和评分。它把代理编辑记录为候选方案，然后用多个种子重新运行选出的优胜方案，以区分可重复收益和搜索偶然结果。

## 问题
- 联邦学习性能取决于许多相互关联的选择：本地优化器、服务器聚合、调度、正则化、客户端更新和模型架构。
- 手动搜索成本高，不受约束的编码代理可能改变指标、数据划分、评估路径或计算预算，从而使基准测试胜出结果无效。
- 这个问题对跨机构医疗联邦学习很重要，因为各站点不能汇集原始数据，而训练协议的小改动可能改变最终模型质量。

## 方法
- AFR 使用 NVFlare 任务配置文件锁定数据集、指标、客户端设置、轮次、模型预算、允许编辑的文件和最终全局模型评估路径。
- 代理在该编辑范围内提出并实现候选方案，包括聚合规则、客户端调度、本地损失、优化器、正则化和注册模型变体。
- 静态检查和冒烟测试验证联邦学习约定：严格模型加载、DIFF 类型客户端更新、本地步数元数据，以及用于评分的同一个最终全局服务器模型。
- 每个活动记录 100 个候选方案，包括分数、运行时间、状态、编辑文件、产物、崩溃和文献事件。
- 选出的候选方案用五个种子重新运行，并与匹配基线和相同预算的标量 HPO 对照比较。

## 结果
- 在 FLamby 上，AFR 在 5 个医疗任务中的 4 个显示出可重复收益：Heart Disease 准确率从 0.721±0.001 提高到 0.794±0.005（+0.074），IXI Dice 从 0.7914±0.0005 提高到 0.9895±0.0000（+0.1981），ISIC2019 平衡准确率从 0.494±0.032 提高到 0.640±0.023（+0.146），Camelyon16 ROC AUC 从 0.5861±0.0310 提高到 0.7494±0.0182（+0.1634）。
- TCGA-BRCA 没有显示出有意义的可重复收益：C-index 从 0.807±0.009 到 0.808±0.025（+0.001），因此论文将该活动的胜出结果视为对种子敏感。
- IXI 比选定的 FedCompass 校准目标高 +0.0015 Dice，Camelyon16 比选定的 FENS 校准目标高 +0.0344 ROC AUC；ISIC2019 仍比其选定的外部目标低 0.110。
- 在分组客户端 LEAF 配置文件上，摘录报告 6 个任务中有 5 个显示出可重复收益。可见表格数值包括：FEMNIST 准确率从 0.834±0.002 提高到 0.873±0.004（+0.038），Shakespeare 下一字符准确率从 0.462±0.004 提高到 0.575±0.001（+0.113），Synthetic 准确率从 0.955±0.001 提高到 0.989±0.001（+0.033）。
- CelebA 是一个报告的失败案例：活动优胜方案没有超过重复基线均值，后续 top-k 检查只发现一个很小的替代收益，且不确定区间跨过零。
- 活动成本有明确记录：每个主搜索都使用 100 个候选方案上限；报告的墙钟时间从 FLamby TCGA 的 1.5 小时到 FLamby IXI 的 71.3 小时不等，每个任务发生 0 到 3 次崩溃。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01366v1](https://arxiv.org/abs/2607.01366v1)
