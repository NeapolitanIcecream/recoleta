---
source: arxiv
url: https://arxiv.org/abs/2606.26095v1
published_at: '2026-06-24T17:59:56'
authors:
- Dong Jing
- Tianqi Zhang
- Jiaqi Liu
- Jinman Zhao
- Zelong Sun
- Li Erran Li
- Zhiwu Lu
- Mingyu Ding
topics:
- vision-language-action
- cross-embodiment
- action-priors
- robot-manipulation
- flow-matching
- history-compression
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Action Priors for Cross-embodiment Robot Manipulation

## Summary
## 摘要
论文提出在视觉-语言-动作（VLA）训练之前，先用只包含动作的机器人轨迹预训练 VLA 动作模块。目标是让策略获得运动先验，使跨本体 VLA 训练从一个已经能建模机器人时间运动的动作头开始。

## 问题
- 标准 VLA 模型从 VLM 继承视觉和语言先验，而动作模块通常从随机权重或无关模态的权重开始训练。
- VLA 训练早期必须同时学习动作动态，以及视觉-语言到动作的对齐，这会降低收敛速度并造成梯度不稳定。
- 跨本体训练增加了难度，因为不同机器人有不同的动作空间、控制约定和运动分布。

## 方法
- 阶段 1 只使用状态-动作轨迹训练一个 Transformer 编码器-解码器动作模块，不使用图像或语言。
- 编码器将交错的状态-动作序列压缩为一个归一化的潜在动作嵌入。
- 解码器用 flow-matching 损失从该潜变量重建动作块，学习机器人运动上的连续动作分布。
- 阶段 2 将预训练解码器复用为 VLA 动作头，并训练 VLM 根据视觉、语言、数据集提示和一个查询 token 预测动作潜变量。
- VLA 训练早期加入来自阶段 1 编码器的逐步衰减潜变量蒸馏损失，同一个编码器也可以把过去的状态-动作历史压缩为一个上下文 token。

## 结果
- 评估覆盖 13 个跨本体操作任务，包含 2 个仿真基准 LIBERO 和 RoboCasa，以及 1 个真实世界 Franka 平台。
- 论文称，相比不使用动作先验的 VLA 训练，该方法成功率更高、收敛更快，但摘录没有给出具体成功率或收敛步数。
- 作者报告称，在数据稀缺的真实世界任务上收益更大，尤其是演示很少的长尾任务，但摘录没有给出各任务的数值结果。
- 阶段 1 中增加只含动作的数据量据称可以提升下游 VLA 性能，但摘录没有给出缩放曲线或数据集规模数字。
- 论文称，历史压缩通过加入单个历史 token 帮助长时程任务，且额外成本可忽略，但摘录没有包含 token 数、延迟或成功率的量化数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26095v1](https://arxiv.org/abs/2606.26095v1)
