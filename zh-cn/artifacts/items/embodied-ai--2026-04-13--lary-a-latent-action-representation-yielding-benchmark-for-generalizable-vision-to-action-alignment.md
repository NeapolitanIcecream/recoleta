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
## 摘要
LARYBench 是一个基准，用来测试从视频中学到的潜在动作表征是否真的有助于动作理解和机器人控制。论文的核心结论是，强大的通用视觉编码器，如 V-JEPA 2 和 DINOv3，在语义动作解码和底层控制预测这两项任务上都优于专门的潜在动作模型。

## 问题
- 视觉-语言-动作模型需要动作数据，但带标注的机器人动作数据集规模小、成本高，而人类视频数据规模大，却没有标注。
- 许多论文提出用潜在动作作为从视频到控制的桥梁，但目前没有统一的评测，能直接衡量这些表征在语义动作和物理控制两个层面的质量。
- 缺少这样的评测时，很难判断一个潜在动作模型究竟学到了有用的动作结构，还是下游策略的结果主要来自系统中的其他部分。

## 方法
- 论文提出了 **LARYBench**，这个基准从两项任务评估表征：语义动作分类评估 **做什么**，轨迹回归评估 **怎么做**。
- 它构建了一个经过整理的大型数据集，包含约 **120 万个短视频 / 1000+ 小时**、**151 个动作类别**、**62 万对图像** 和 **59.5 万条运动轨迹**，覆盖人类和机器人数据、第一视角和第三视角、真实与模拟环境，以及 **11 种机器人形态**。
- 在语义评测中，基准通过分类任务测试表征，涵盖 **28 个原子机器人动作基元** 和 **145 个复合人类/机器人动作**。
- 在控制评测中，它训练一个简单的 MLP 回归器，将图像对的潜在特征映射到机器人动作片段，并在 **CALVIN、VLABench、RoboCOIN 和 AgiBotWorld-Beta** 等数据集上报告 **MSE**。
- 论文比较了 **11 个模型**，包括具身潜在动作模型、通用语义编码器、基于像素的生成式编码器，以及一种混合的“general LAM”模型：在冻结的通用视觉骨干网络上叠加 LAPA 风格训练。

## 结果
- 在语义动作分类上，**V-JEPA 2** 最好，平均准确率为 **76.62%**；**DINOv3** 为 **68.68%**；所有 general LAM 变体约为 **40.78% 到 49.36%**；具身 LAM 如 **LAPA 20.17%**、**UniVLA 17.99%**、**villa-X 20.90%**。
- 在三个分类子集上，**V-JEPA 2** 在 **Atomic Robot** 上为 **79.09%**，在 **Composite Human** 上为 **80.35%**，在 **Composite Robot** 上为 **70.43%**。**DINOv3** 在相同任务上的结果为 **60.79% / 76.19% / 69.06%**。
- 使用通用骨干网络的混合模型在语义任务上可以大幅超过专门的具身 LAM。论文给出的结果是 **LAPA-DINOv2 平均达到 43.67%**，而 **UniVLA 为 17.99%**。
- 在底层控制回归上，展示的模型中 **DINOv3** 最好，平均 **MSE 为 0.19**；相比之下，**V-JEPA 2 为 0.25**、**Wan2.2 为 0.30**、**FLUX.2-dev 为 0.35**、**LAPA 为 0.97**。
- 分数据集看回归结果，**DINOv3** 在 **CALVIN** 上为 **0.22**，在 **VLABench** 上为 **0.06**，在 **RoboCOIN** 上为 **0.22**，在 **AgiBotWorld-Beta** 上为 **0.24**。**V-JEPA 2** 的结果为 **0.27 / 0.07 / 0.32 / 0.33**。
- 主要的实验结论是，现成的通用视觉表征已经包含与动作相关的信息，并且在这个基准中，**潜在特征空间与机器人控制的对齐效果优于像素重建空间**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11689v1](http://arxiv.org/abs/2604.11689v1)
