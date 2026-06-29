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
Pelican-Unified 1.0 训练一个具身模型，让它从同一个潜在状态里进行语言推理、预测未来视频，并输出机器人动作片段。它针对感知型 VLM、视频世界模型和可执行机器人策略之间的缺口。

## 问题
- 机器人系统常把感知、推理、未来预测和控制拆成多个模型，这在长任务中会造成状态不一致。
- RT-2、OpenVLA 和 π0 这类 VLA 策略把观测映射到动作，但摘录说它们通常缺少显式的未来视频预测。
- 视频世界模型可以预测视觉未来，但任务推理和低层机器人动作可能仍然脱节。

## 方法
- 基于 Qwen3-VL 4B 的 VLM 读取观测、动作历史和语言指令，然后写出面向任务和动作的思维链。
- 这段推理轨迹的最后隐藏状态被投影到一个稠密潜在状态 `z`，并以此同时条件化未来视频生成和动作预测。
- 基于 Wan2.2-5B 的扩散 Transformer 在同一个过程中去噪未来视频潜变量和连续动作片段，并为每种模态设置独立的输入和输出头。
- 训练结合文本损失、视频流匹配损失和动作 SmoothL1 损失，这三种损失都会更新共享潜在状态。

## 结果
- 在 8 个 VLM 基准上，Pelican-Unified 的平均分是 64.7；Qwen3-VL-4B-Instruct 为 58.2，MolmoAct 为 27.5。
- 在具身 VLM 基准上，它在 Where2Place 上比 Qwen3-VL-4B-Instruct 高 28.2 分，在 PhyX 上高 20.6 分。
- 在 RoboTwin 50 任务双臂操作上，它的平均成功率达到 93.5%，其中干净设置下为 93.6%，随机化条件下为 93.3%。
- 在 RoboTwin 上，它超过了 π0 的 62.2%、π0.5 的 79.8%、starVLA 的 88.3%、LingBot-VA 的 92.3% 和 AIM 的 93.1%；摘录说它在对比的动作方法中排名第二。
- 在 RoboTwin 上，50 个任务里有 31 个任务的成功率至少达到 95%，39 个任务至少达到 90%，15 个任务达到 100%。
- 在 WorldArena 上，它报告的 EWM Score 为 66.03，并在摘录所比较的世界模型方法中排名第一。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15153v1](https://arxiv.org/abs/2605.15153v1)
