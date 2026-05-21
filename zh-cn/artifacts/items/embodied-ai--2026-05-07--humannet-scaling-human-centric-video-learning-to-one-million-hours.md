---
source: arxiv
url: https://arxiv.org/abs/2605.06747v1
published_at: '2026-05-07T15:21:58'
authors:
- Yufan Deng
- Daquan Zhou
topics:
- human-centric-video
- robot-data-scaling
- vision-language-action
- embodied-foundation-model
- human-to-robot-transfer
- egocentric-video
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# HumanNet: Scaling Human-centric Video Learning to One Million Hours

## Summary
## 摘要
HumanNet 是一个面向具身学习的 1,000,000 小时以人为中心的视频语料库，包含第一人称和第三人称片段、字幕、运动描述以及手部/身体信号。论文称，在受控 VLA 验证中，使用 1,000 小时第一人称 HumanNet 视频进行预训练，可以达到或略高于使用 100 小时真实机器人数据进行预训练的效果。

## 问题
- 机器人和具身策略需要大量交互数据，但真实机器人数据集成本高、规模较小，并且常绑定到某一种机器人平台或任务集。
- 与遥操作机器人日志相比，人类视频以更大规模包含操作、工具使用、导航、全身运动和长流程任务。
- 关键问题是如何把广泛的互联网视频和采集到的人类视频转化为支持机器人相关预训练的数据，而不是只用于通用视频识别。

## 方法
- HumanNet 收集并筛选以人类活动为核心的人类中心视频，包括物体操作、工具使用、移动、装配、家电使用、运输和多步骤任务。
- 数据集保留第一人称和第三人称视角：第一人称片段捕捉手与物体的接触和行为者意图，第三人称片段捕捉全身运动和场景上下文。
- 流水线使用关键词发现、网页和平台检索、开源数据集以及自采录制内容，然后进行去重、归一化、内容过滤、质量过滤、场景切分和片段生成。
- 标注包括 3D 手部/身体姿态、适用于部分第一人称片段的单目 SLAM、运动重定向、视频字幕、运动描述和活动类别。
- 当运动重定向误差低于 15 mm 且有效帧覆盖率超过 60% 时，片段可以进入面向机器人的子集。

## 结果
- HumanNet 报告包含 1,000,000 小时以人为中心的视频，覆盖第一人称和第三人称视角；论文将其与 EgoScale 的 20,854 小时、Ego4D 的约 3,670 小时、Ego-Exo4D 的 1,286 小时、OpenEgo 的 1,107 小时以及 EPIC-KITCHENS-100 的约 100 小时进行比较。
- 受控 VLA 验证使用相同的 LingBot-VLA 架构和相同的下游机器人语料：34 小时、100 个任务、每个任务 20 个 episode。
- 比较测试了四种初始化：Qwen VLM、使用 100 小时真实机器人 CoBot 数据适配的 Qwen、使用 1,000 小时第一人称 HumanNet 视频适配的 Qwen，以及使用 20,000 小时真实机器人数据训练的 LingBot。
- 在五个留出的任务组中，据报告，1,000 小时第一人称 HumanNet 初始化达到并在若干任务组上略高于 100 小时真实机器人 CoBot 初始化。
- 摘录未提供确切的验证损失值，因此最强的量化结论是数据效率比较：在固定的 34 小时下游设置下，1,000 小时人类第一人称视频的表现与 100 小时机器人视频相当或更好，同时缩小了与使用 20,000 小时机器人数据训练的 LingBot 基线之间的差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06747v1](https://arxiv.org/abs/2605.06747v1)
