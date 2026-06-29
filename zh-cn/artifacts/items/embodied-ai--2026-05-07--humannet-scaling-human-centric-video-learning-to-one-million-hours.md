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
## 总结
HumanNet 是一个面向具身学习的 1,000,000 小时以人为中心的视频语料库，包含第一人称和第三人称片段，以及字幕、动作描述和手部/身体信号。论文声称，在受控的 VLA 验证中，用 1,000 小时来自 HumanNet 的第一人称视频继续预训练，效果可以达到，甚至在一些情况下略好于，用 100 小时真实机器人数据继续预训练。

## 问题
- 机器人和具身策略需要大量交互数据，但真实机器人数据集成本高、规模小，而且常常只对应单一机器人平台或任务集合。
- 人类视频包含操作、工具使用、导航、全身运动和长时程流程，规模远大于遥操作机器人日志。
- 核心问题是把大范围的互联网视频和采集到的人类视频转成能支持机器人相关预训练的数据，而不是只用于通用视频识别。

## 方法
- HumanNet 收集并筛选以人类活动为中心的视频，内容包括物体操作、工具使用、移动、装配、电器使用、搬运和多步骤任务。
- 数据集同时保留第一人称和第三人称视角：第一人称片段记录手和物体的接触以及执行者意图，第三人称片段记录全身运动和场景上下文。
- 流水线使用关键词发现、网络和平台检索、开源数据集以及自采视频，然后进行去重、标准化、内容过滤、质量过滤、场景切分和片段生成。
- 标注包含 3D 手部/身体姿态、适合的第一人称片段上的单目 SLAM、动作重定向、视频字幕、动作描述和活动类别。
- 当动作重定向误差低于 15 mm 且有效帧覆盖率超过 60% 时，一个片段可以进入面向机器人训练的子集。

## 结果
- HumanNet 报告了 1,000,000 小时的人类中心视频，包含第一人称和第三人称视角；论文将其与 EgoScale 的 20,854 小时、Ego4D 的约 3,670 小时、Ego-Exo4D 的 1,286 小时、OpenEgo 的 1,107 小时，以及 EPIC-KITCHENS-100 的约 100 小时进行比较。
- 受控的 VLA 验证使用相同的 LingBot-VLA 架构和相同的下游机器人语料库：34 小时、100 个任务、每个任务 20 个 episode。
- 比较测试了四种初始化：Qwen VLM、用 100 小时真实机器人 CoBot 数据适配后的 Qwen、用 1,000 小时 HumanNet 第一人称视频适配后的 Qwen，以及用 20,000 小时真实机器人数据训练的 LingBot。
- 在五个保留任务组上，1,000 小时第一人称 HumanNet 初始化据称与 100 小时真实机器人 CoBot 初始化持平，并在其中几个组上略有超过。
- 摘要没有给出精确的验证损失数值，因此最强的定量结论是数据效率对比：在固定的 34 小时下游设置下，1,000 小时人类第一人称视频的表现与 100 小时机器人视频相当或更好，同时与 20,000 小时机器人训练的 LingBot 基线相比，缩小了差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06747v1](https://arxiv.org/abs/2605.06747v1)
