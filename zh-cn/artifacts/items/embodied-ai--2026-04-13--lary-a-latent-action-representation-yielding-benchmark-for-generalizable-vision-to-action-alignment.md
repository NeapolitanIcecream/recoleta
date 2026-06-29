---
source: arxiv
url: http://arxiv.org/abs/2604.11689v1
published_at: '2026-04-13T16:30:35'
authors:
- Dujun Nie
- Fengjiao Chen
- Qi Lv
- Jun Kuang
- Xiaoyu Li
- Xuezhi Cao
- Xunliang Cai
topics:
- vision-language-action
- latent-action-representation
- robot-benchmark
- generalist-robot-policy
- world-model
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment

## Summary
## 总结
LARYBench 是一个基准，用来测试从视频中学到的潜在动作表示是否真的有助于动作理解和机器人控制。论文的主要结论是，像 V-JEPA 2 和 DINOv3 这样的强通用视觉编码器，在语义动作解码和低层控制预测这两项任务上，都优于专门的潜在动作模型。

## 问题
- 视觉-语言-动作模型需要动作数据，但带标注的机器人动作数据集规模小、成本高，而人类视频很多，却没有标注。
- 许多论文把潜在动作当作从视频到控制的桥梁，但没有一个标准评估能直接衡量这些表示在语义动作和物理控制两方面的质量。
- 没有这种评估，就很难判断潜在动作模型到底学到了有用的动作结构，还是下游策略结果主要来自系统中的其他部分。

## 方法
- 论文提出 **LARYBench**，一个在两项任务上给表示打分的基准：语义动作分类，用来判断 **做什么**；轨迹回归，用来判断 **怎么做**。
- 它构建了一个大规模整理数据集，包含大约 **120 万段短视频 / 1000+ 小时**、**151 个动作类别**、**62 万对图像** 和 **59.5 万条运动轨迹**，覆盖人类和机器人数据、第一视角和第三视角、真实和仿真环境，以及 **11 种机器人本体**。
- 在语义评估中，基准用分类任务检验表示，对象包括 **28 个原子级机器人动作** 和 **145 个复合人类/机器人动作**。
- 在控制评估中，它训练一个简单的 MLP 回归器，把图像对中的潜在特征映射到机器人动作片段，并在 **CALVIN、VLABench、RoboCOIN 和 AgiBotWorld-Beta** 等数据集上报告 **MSE**。
- 它比较了 **11 个模型**，覆盖具身潜在动作模型、通用语义编码器、基于像素的生成式编码器，以及在冻结的通用视觉骨干上叠加 LAPA 风格训练得到的混合型“通用 LAM”模型。

## 结果
- 在语义动作分类上，**V-JEPA 2** 最好，平均准确率 **76.62%**，高于 **DINOv3 的 68.68%**，也高于所有通用 LAM 变体的约 **40.78% 到 49.36%**，以及 **LAPA 20.17%**、**UniVLA 17.99%**、**villa-X 20.90%** 等具身 LAM。
- 在三个分类子集上，**V-JEPA 2** 在 **Atomic Robot** 上得到 **79.09%**，在 **Composite Human** 上得到 **80.35%**，在 **Composite Robot** 上得到 **70.43%**。**DINOv3** 在同样任务上的结果是 **60.79% / 76.19% / 69.06%**。
- 论文指出，带通用骨干的混合模型在语义任务上可以大幅超过专门的具身 LAM。文中给出的结果是 **LAPA-DINOv2 平均达到 43.67%**，而 **UniVLA 为 17.99%**。
- 在低层控制回归上，**DINOv3** 在展示的模型中最好，平均 **MSE 为 0.19**；对比之下，**V-JEPA 2 为 0.25**，**Wan2.2 为 0.30**，**FLUX.2-dev 为 0.35**，**LAPA 为 0.97**。
- 按数据集看回归结果，**DINOv3** 在 **CALVIN** 上是 **0.22**，在 **VLABench** 上是 **0.06**，在 **RoboCOIN** 上是 **0.22**，在 **AgiBotWorld-Beta** 上是 **0.24**。**V-JEPA 2** 对应分别是 **0.27 / 0.07 / 0.32 / 0.33**。
- 主要实证结论是，现成的通用视觉表示已经包含与动作相关的信息，而且在这个基准上，**潜在特征空间比像素重建空间更适合机器人控制**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11689v1](http://arxiv.org/abs/2604.11689v1)
