---
source: arxiv
url: https://arxiv.org/abs/2607.11270v1
published_at: '2026-07-13T08:53:34'
authors:
- Peijun Tang
- Shangjin Xie
- Baifu Huang
- Binyan Sun
- Haotian Yang
- Kuncheng Luo
- Weiqi Jin
- Shilin Fang
- Jianan Wang
topics:
- robot-foundation-model
- world-model
- vision-language-action
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Towards Predictive, Aligned, and Scalable Robot Learning

## Summary
## 摘要
Lumo-2 是一种潜在世界-动作模型，会先预测与动作相关的未来动态，再生成机器人动作。它通过三阶段模态对齐，改善时间推理、物理理解、扩展能力和灵巧操作。

## 问题
- 机器人策略通常会根据单次观测直接映射动作。当同一视角出现在倒水等任务的不同阶段时，这种做法容易产生歧义。
- 以重建为重点的动作标记化可能生成准确的动作编码，但这些编码与视觉上下文、语言及下游控制的对齐仍然较弱。
- 时间对齐和跨模态对齐不足，会限制模型对长时程任务、物理过程复杂的任务以及跨本体任务的泛化能力。

## 方法
- Lumo-2 首先根据视觉观测、语言、本体感知信息和短期历史缓冲区，推断物理基础明确的世界动态紧凑潜在表示，然后以该表示为条件生成动作。
- 第一阶段使用向量量化架构，联合训练视觉世界动态和动作自编码。视觉动态用于指导动作重建，动作则用于约束动态表示。
- 第二阶段加入语义动作标记，并通过动作重建、行为描述、视觉语言引导的动作生成、跨模态预测和对比学习目标，使动作标记与视觉和语言对齐。
- 第三阶段联合训练视觉语言理解、未来投影和动作生成，使模型在生成动作块之前先投影潜在的未来动态。
- 训练使用 Qwen3.5-4B、来自多个平台的多样化机器人数据、第一视角视频和时间上下文缓冲区，以减少部分可观测性导致的误差。

## 结果
- 摘要片段没有提供任务成功率、基准测试分数、数据集总量或相对基线的具体差距。
- Lumo-2 声称在 3 类真实世界任务中持续优于较强的 VLA 和 WAM 基线：时间推理、物理理解以及高控制复杂度操作。
- 摘要声称，模型在需要未来状态预测和物理推理的长时程任务及灵巧操作任务上取得了最明显的改进。
- 训练方案包含 3 个渐进式对齐阶段，并在 64 张 NVIDIA H100 GPU 上训练 30,000 步；这些属于训练细节，不是性能结果。
- 根据摘要片段，模型可以使用第一视角人类视频和 VisionPro 数据进行微调。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11270v1](https://arxiv.org/abs/2607.11270v1)
