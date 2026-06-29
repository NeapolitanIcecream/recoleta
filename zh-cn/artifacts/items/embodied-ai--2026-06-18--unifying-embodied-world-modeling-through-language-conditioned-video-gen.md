---
source: hn
url: https://arxiv.org/abs/2606.17030
published_at: '2026-06-18T23:28:34'
authors:
- gmays
topics:
- embodied-world-model
- language-conditioned-video
- robot-data-scaling
- generalist-robot-policy
- vision-language-action
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Unifying Embodied World Modeling Through Language-Conditioned Video Gen

## Summary
## 摘要
Qwen-RobotWorld 是一个以语言为条件的视频世界模型，可为具身智能体在操作、驾驶、导航和人到机器人迁移场景中预测未来视觉轨迹。它的价值在于，同一个模型可以生成合成机器人数据，支持策略评估，并为控制提供规划信号。

## 问题
- 具身智能体需要能预测动作后场景如何变化的世界模型，但机器人数据分散在不同实体形态、任务和动作格式中。
- 许多机器人策略难以直接使用来自驾驶、导航、操作和人类演示的数据，因为动作空间不同。
- 更好的预测式视频模型可以降低数据采集成本，并在真实机器人运行策略之前改进测试。

## 方法
- 论文使用自然语言作为共享动作接口：模型接收当前观测和用语言描述的动作，然后生成未来视频轨迹。
- 核心模型是一个 60 层双流扩散 Transformer，通过逐层联合注意力将冻结的 Qwen2.5-VL 语义特征与 video-VAE 潜变量连接起来。
- 训练使用 Embodied World Knowledge，这是一个包含 860 万个视频-文本样本、2 亿多帧、20 多种实体形态和 500 多个动作类别的语料库。
- 训练课程分为两个阶段：先学习通用视觉先验，再在相同的语言-动作格式下针对具身数据进行专门训练。

## 结果
- 摘录没有给出原始基准分数，但报告了排名和对比结果。
- Qwen-RobotWorld 在 EWMBench 和 DreamGen Bench 上总体排名第 1。
- 根据摘要，它在 WorldModelBench 和 PBench 上优于所有开源模型。
- RoboTwin-IF 上的零样本测试被报告为支持泛化能力和多视角一致性，但摘录中没有包含数值分数。
- 论文声称的训练规模是 860 万个视频-文本样本、2 亿多帧，覆盖 20 多种实体形态和 500 多个动作类别。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17030](https://arxiv.org/abs/2606.17030)
