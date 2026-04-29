---
source: arxiv
url: http://arxiv.org/abs/2604.20012v1
published_at: '2026-04-21T21:40:58'
authors:
- Yiyang Du
- Zhanqiu Guo
- Xin Ye
- Liu Ren
- Chenyan Xiong
topics:
- vision-language-action
- robot-foundation-model
- mid-training
- data-selection
- embodied-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training

## Summary
## 摘要
EmbodiedMidtrain 在 VLA 微调之前，先通过挑选与机器人数据最相似的 VLM 训练样本，把视觉语言模型适配到机器人控制。论文表明，这一步中期训练能在多个基准和不同骨干模型上提升下游操作性能，同时所用模型规模和训练预算都小得多。

## 问题
- VLA 通常从现成的 VLM 出发，这些模型在图像描述、VQA 和文档理解等广泛任务上训练；而机器人策略训练使用的是与物理交互绑定的操作轨迹数据。
- 论文对这种错配进行了测量，发现 VLA 数据形成了紧凑簇，并且与更广泛的 VLM 分布相分离，因此初始表征与动作学习的对齐较差。
- 这很重要，因为普通的 VLA 微调必须独自跨过这道鸿沟，从而限制下游机器人性能。

## 方法
- 该方法在冻结的 VLM 特征上训练一个轻量的二分类器，用来区分 VLA 样本和 VLM 样本。
- 分类器分数被当作接近度分数：分数越高的 VLM 样本，被视为与机器人数据分布越相似。
- 它对大规模 VLM 数据池逐样本排序，保留 top-K 个与 VLA 最对齐的样本，并在 VLA 微调之前，先用这组筛选后的混合数据对 VLM 做中期训练。
- 这条流程不改变 VLM 或 VLA 的架构；它改变的是中间训练阶段使用的数据。
- 候选池同时包含通用 VLM 数据和面向具身任务的 VLM 数据，因此选出的子集在保留一定多样性的同时，会向空间和具身内容偏移。

## 结果
- 在 **Calvin ABC-D** 上，**InternVL3.5-1B** 在 EmbodiedMidtrain 后的平均序列长度从 **3.173** 提升到 **3.714**。其 5 步完成分数从 **0.406** 升至 **0.551**。
- 在 **SimplerEnv-Bridge** 上，同一个 **InternVL3.5-1B** 模型的成功率从 **36.5** 提升到 **56.3**。在 **Libero-10** 上，它从 **39.0** 提升到 **54.2**。
- 对 **Qwen3VL-2B**，EmbodiedMidtrain 将 **Calvin** 从 **3.205** 提升到 **3.584**，将 **SimplerEnv-Bridge** 从 **38.5** 提升到 **45.8**，将 **Libero-10** 从 **33.8** 提升到 **40.2**。
- 经过中期训练的 **InternVL3.5-1B** 在 **Calvin** 上超过了专家 VLA 基线：平均长度 **3.714**，而 **π0** 为 **3.509**，**OpenVLA** 为 **2.548**。
- 这些提升对应的训练预算小得多：中期训练模型在 **Calvin / Simpler / Libero** 上看到的样本数分别是 **1.0M / 4.1M / 4.1M**，而复现实验中的专家 VLA 和现成 VLM 基线分别为 **7.7M / 25.6M / 25.6M**。
- 在 **InternVL3.5-1B** 的消融实验中，学习得到的估计器优于随机选择和其他打分规则：**Calvin 3.714**，随机选择为 **3.398**；**Simpler 56.3**，随机选择为 **43.8**；**Libero 54.2**，随机选择为 **48.4**。它也优于特征距离（**3.126 / 53.1 / 51.2**）、VLA 条件困惑度（**3.159 / 55.2 / 48.0**）和 delta perplexity（**1.527 / 39.6 / 54.2**）。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20012v1](http://arxiv.org/abs/2604.20012v1)
