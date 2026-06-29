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
## 总结
EmbodiedMidtrain 在 VLA 微调前先让视觉-语言模型适应机器人控制，方法是挑选那些与机器人数据最相似的 VLM 训练样本。论文表明，这一步中训练能在多个基准和骨干模型上提升下游操控表现，而且用到的模型规模和训练预算都更小。

## 问题
- VLA 通常从现成的 VLM 开始，这些模型训练于字幕生成、VQA 和文档理解等广泛任务；而机器人策略训练使用的是与物理交互相关的操控轨迹。
- 论文测量了这种不匹配，发现 VLA 数据形成紧凑簇，并且与更广泛的 VLM 分布分离，所以起始表示与动作学习的对齐较差。
- 这很重要，因为直接做 VLA 微调必须自己跨过这道差距，这会限制下游机器人性能。

## 方法
- 该方法在冻结的 VLM 特征上训练一个轻量二分类器，用来区分 VLA 样本和 VLM 样本。
- 分类器分数被当作接近度分数：分数更高的 VLM 样本被视为与机器人数据分布更相似。
- 它对一个大型 VLM 数据池逐样本排序，保留最符合 VLA 分布的前 K 个样本，并在 VLA 微调前先用这组筛选后的混合数据对 VLM 做中训练。
- 这个流程不改动 VLM 或 VLA 架构，只改变中间训练阶段使用的数据。
- 候选池同时包含通用 VLM 数据和面向具身的 VLM 数据，因此被选出的子集保留了一部分多样性，同时向空间和具身内容偏移。

## 结果
- 在 **Calvin ABC-D** 上，**InternVL3.5-1B** 在 EmbodiedMidtrain 后的平均序列长度从 **3.173** 提升到 **3.714**。它的 5 步完成分数从 **0.406** 提升到 **0.551**。
- 在 **SimplerEnv-Bridge** 上，同一个 **InternVL3.5-1B** 模型的成功率从 **36.5** 提升到 **56.3**。在 **Libero-10** 上，它从 **39.0** 提升到 **54.2**。
- 在 **Qwen3VL-2B** 上，EmbodiedMidtrain 让 **Calvin** 从 **3.205** 提升到 **3.584**，让 **SimplerEnv-Bridge** 从 **38.5** 提升到 **45.8**，让 **Libero-10** 从 **33.8** 提升到 **40.2**。
- 中训练后的 **InternVL3.5-1B** 在 **Calvin** 上超过了专家 VLA 基线：平均长度 **3.714**，高于 **π0** 的 **3.509** 和 **OpenVLA** 的 **2.548**。
- 这些提升对应的训练预算要小得多：中训练模型在 **Calvin / Simpler / Libero** 上分别只看了 **1.0M / 4.1M / 4.1M** 个样本，而复现的专家 VLA 和现成 VLM 基线用了 **7.7M / 25.6M / 25.6M** 个样本。
- 在 **InternVL3.5-1B** 的消融实验中，学习到的估计器优于随机选择和其他打分规则：**Calvin 3.714** 对 **随机选择 3.398**，**Simpler 56.3** 对 **43.8**，**Libero 54.2** 对 **48.4**。它也优于特征距离（**3.126 / 53.1 / 51.2**）、VLA 条件困惑度（**3.159 / 55.2 / 48.0**）和 delta 困惑度（**1.527 / 39.6 / 54.2**）。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20012v1](http://arxiv.org/abs/2604.20012v1)
