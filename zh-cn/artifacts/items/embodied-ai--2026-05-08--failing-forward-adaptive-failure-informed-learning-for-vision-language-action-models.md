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
AFIL 是一种面向基于扩散和流的视觉-语言-行动机器人策略的、能识别失败的训练和采样方法。它把失败轨迹当作负向引导，让策略避开与坏结果相关的动作区域。

## 问题
- 只用成功样本做行为克隆，会让 VLA 策略在出现轻微执行错误后没有恢复训练信号。
- 手工设计失败类别和人工纠正，面对新的操作任务或新的机器人形态时扩展性很差。
- 这个问题很重要，因为部署中的错误会把机器人推到演示数据覆盖不到的状态，导致长时程任务失败。

## 方法
- 预训练的 VLA 会在线生成失败轨迹，因此该方法收集的是策略自身行为产生的失败数据，而不是人工定义的失败模式。
- 模型使用 2 个动作生成器：1 个训练成功轨迹，1 个训练失败轨迹。
- 两个动作生成器共享 1 个视觉-语言骨干网络，因此比训练两个完整分开的 VLA 模型增加的参数更少。
- 在扩散或流式采样过程中，失败生成器把动作推离更容易失败的方向，成功生成器把动作拉向成功行为。
- 引导权重是自适应的：它使用成功和失败预测之间的余弦距离，按 α(1 - cos) 缩放，因此当两者一致时引导更弱，分歧更大时引导更强。

## 结果
- 给出的摘录报告了领域内和领域外的操作任务实验，包括短时程和长时程设置，但没有提供任务成功率、数据集规模或表格数值。
- 主要结论是，在测试的操作任务上，任务成功率高于现有的 VLA 基线。
- 论文声称，使用在线生成的失败轨迹作为训练数据和负采样引导，可以更好地从失败状态恢复。
- 该方法适用于摘录中提到的 2 类 VLA 生成器：基于扩散的策略和基于流的策略。
- 具体的架构主张是，AFIL 在与成功生成器共享 VLM 骨干的同时，增加了 1 个失败动作生成器。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08434v2](https://arxiv.org/abs/2605.08434v2)
