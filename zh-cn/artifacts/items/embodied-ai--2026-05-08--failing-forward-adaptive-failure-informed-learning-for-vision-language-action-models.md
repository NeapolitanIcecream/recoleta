---
source: arxiv
url: https://arxiv.org/abs/2605.08434v2
published_at: '2026-05-08T19:57:11'
authors:
- Meng Zheng
- Samhita Marri
- Anwesa Choudhuri
- Benjamin Planche
- Zhongpai Gao
- Van Nguyen Nguyen
- Terrence Chen
- Girish Chowdhary
- Ziyan Wu
topics:
- vision-language-action
- robot-policy-learning
- failure-informed-learning
- diffusion-policy
- flow-matching
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Failing Forward: Adaptive Failure-Informed Learning for Vision-Language-Action Models

## Summary
## 摘要
AFIL 是一种面向基于扩散和流的视觉-语言-动作机器人策略的失败感知训练与采样方法。它把失败 rollout 用作负向引导，使策略避开与不良结果相关的动作区域。

## 问题
- 只使用成功样本的行为克隆不会为 VLA 策略提供小执行错误后的恢复训练信号。
- 手工设计的失败类别和人工纠正难以扩展到新的操作任务或机器人形态。
- 这个问题很重要，因为部署中的错误会把机器人推到演示数据之外的状态，导致长时程任务失败。

## 方法
- 预训练 VLA 在线生成失败 rollout，因此该方法从策略自身行为中收集失败数据，而不是依赖人工定义的失败模式。
- 模型使用 2 个动作生成器：一个用成功轨迹训练，另一个用失败轨迹训练。
- 2 个动作生成器共享 1 个视觉-语言主干，因此相比训练独立的完整 VLA 模型，额外参数成本更低。
- 在扩散或流采样期间，失败生成器把动作推离容易失败的方向，成功生成器把动作拉向成功行为。
- 引导权重是自适应的：它使用成功预测和失败预测之间的余弦距离，尺度为 α(1 - cos)，因此当两者预测一致时引导较弱，当两者分歧较大时引导较强。

## 结果
- 给定摘录报告了域内和域外操作任务实验，包括短时程和长时程设置，但没有提供任务成功率百分比、数据集规模或表格数值。
- 论文的主要结果主张是，在测试的操作任务中，任务成功率高于现有 VLA 基线。
- 论文称，通过使用在线生成的失败轨迹作为训练数据和负向采样引导，该方法能更好地从失败状态中恢复。
- 该方法适用于摘录中点名的 2 类 VLA 生成器：基于扩散的策略和基于流的策略。
- 具体的架构主张是，AFIL 增加 1 个失败动作生成器，同时与成功生成器共享 VLM 主干。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08434v2](https://arxiv.org/abs/2605.08434v2)
