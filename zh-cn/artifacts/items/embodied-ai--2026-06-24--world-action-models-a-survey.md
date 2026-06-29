---
source: hn
url: https://arxiv.org/abs/2606.20781
published_at: '2026-06-24T23:41:19'
authors:
- simonpure
topics:
- world-action-models
- robot-world-models
- vision-language-action
- embodied-ai
- robot-policy
- survey
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# World Action Models: A Survey

## Summary
## 概要
这篇综述将世界动作模型（World Action Models，WAMs）定义为具身预测-动作模型：它们把对未来的预测提供给控制过程使用。文章把 WAMs 与视频生成器、世界模型和视觉-语言-动作策略进行对照，并解释影响当前系统的设计权衡。

## 问题
- WAM 研究分散在视频生成模型、基于语言的动作模型和视觉-语言机器人策略之间，方法之间难以比较。
- 这个问题很关键，因为机器人控制需要对动作有用的预测，同时受到计算、内存、延迟和动作标签成本的限制。
- 论文关注模型为了控制必须预测什么，而不是把每一种未来预测模型都视为同一类机器人模型。

## 方法
- 综述先区分广义世界模型、视频生成模型、基于动作的视频世界模型、视觉-语言-动作策略和 WAMs。
- 它按生成内容来组织方法：渲染后的未来、潜在空间中的未来，或不依赖视频生成的动作推理。
- 它还沿 4 个轴分解方法：预测基底、骨干模型、动作耦合和部署方式。
- 文章用这些轴比较可交互性、因果性、持久性、物理合理性、泛化能力、数据需求、评估方式和开放挑战。

## 结果
- 摘录没有报告基准分数、数据集指标或定量比较。
- 它提出一种双视角分类法：生成目标和模型结构。
- 它识别出 WAMs 的 3 种输出方式：渲染后的未来、潜在空间中的未来，以及不依赖视频生成的动作推理。
- 它列出 4 个主要设计轴：预测基底、骨干模型、动作耦合和部署方式。
- 它的主要观点是，WAMs 需要在未来细节的丰富程度与计算、内存、延迟和动作标签成本之间权衡；当前研究正在减少需要预测的未来内容，同时保留与控制相关的信息。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20781](https://arxiv.org/abs/2606.20781)
