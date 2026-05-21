---
source: arxiv
url: https://arxiv.org/abs/2605.15153v1
published_at: '2026-05-14T17:50:42'
authors:
- Yi Zhang
- Yinda Chen
- Che Liu
- Zeyuan Ding
- Jin Xu
- Shilong Zou
- Junwei Liao
- Jiayu Hu
- Xiancong Ren
- Xiaopeng Zhang
- Yechi Liu
- Haoyuan Shi
- Zecong Tang
- Haosong Sun
- Renwen Cui
- Kuishu Wu
- Wenhai Liu
- Yang Xu
- Yingji Zhang
- Yidong Wang
- Senkang Hu
- Jinpeng Lu
- Nga Teng Chan
- Yechen Wu
- Yong Dai
- Jian Tang
- Xiaozhu Ju
topics:
- embodied-foundation-model
- vision-language-action
- robot-world-model
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action

## Summary
## 摘要
Pelican-Unified 1.0 训练一个具身模型，让它从同一个潜在状态出发，用语言推理、预测未来视频，并输出机器人动作片段。它面向的问题是：偏重感知的 VLM、视频世界模型和可执行机器人策略之间存在脱节。

## 问题
- 机器人系统常把感知、推理、未来预测和控制拆成不同模型，这会在长任务中造成状态不匹配。
- RT-2、OpenVLA 和 π0 等 VLA 策略把观测映射为动作，但摘录称它们通常缺少显式的未来视频预测。
- 视频世界模型可以预测视觉未来，但任务推理和低层机器人动作可能仍然相互断开。

## 方法
- 一个基于 Qwen3-VL 4B 的 VLM 读取观测、动作历史和语言指令，然后写出面向任务和动作的思维链。
- 该推理轨迹的最终隐藏状态被投影为稠密潜在状态 `z`，同时作为未来视频生成和动作预测的条件。
- 一个基于 Wan2.2-5B 的扩散 transformer 在同一过程中对未来视频潜变量和连续动作片段去噪，并为每种模态使用单独的输入头和输出头。
- 训练结合文本损失、视频 flow-matching 损失和动作 SmoothL1 损失，三种损失都会更新共享潜在状态。

## 结果
- 在 8 个 VLM 基准上，Pelican-Unified 平均得分为 64.7；相比之下，Qwen3-VL-4B-Instruct 为 58.2，MolmoAct 为 27.5。
- 在具身 VLM 基准上，它相较 Qwen3-VL-4B-Instruct 在 Where2Place 上提高 +28.2 分，在 PhyX 上提高 +20.6 分。
- 在 RoboTwin 50 任务双臂操作中，它达到 93.5% 的平均成功率，其中干净设置下为 93.6%，随机化条件下为 93.3%。
- 在 RoboTwin 上，它超过 π0 的 62.2%、π0.5 的 79.8%、starVLA 的 88.3%、LingBot-VA 的 92.3% 和 AIM 的 93.1%；摘录称它在比较的动作方法中排名第二。
- 在 RoboTwin 上，50 个任务中有 31 个达到至少 95% 成功率，39 个达到至少 90%，15 个达到 100%。
- 在 WorldArena 上，它报告的 EWM Score 为 66.03，并在摘录比较的世界模型方法中排名第一。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15153v1](https://arxiv.org/abs/2605.15153v1)
