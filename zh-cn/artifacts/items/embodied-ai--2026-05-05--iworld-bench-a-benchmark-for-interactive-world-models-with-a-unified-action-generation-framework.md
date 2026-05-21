---
source: arxiv
url: https://arxiv.org/abs/2605.03941v2
published_at: '2026-05-05T16:30:03'
authors:
- Jianjie Fang
- Yingshan Lei
- Qin Wan
- Ziyou Wang
- Yuchao Huang
- Yongyan Xu
- Baining Zhao
- Weichen Zhang
- Chen Gao
- Xinlei Chen
- Yong Li
topics:
- interactive-world-models
- world-model-benchmark
- action-control
- camera-trajectory
- robot-data-scaling
- embodied-ai
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework

## Summary
## 概要
iWorld-Bench 是一个用于测试交互式世界模型是否能遵循动作输入并保持场景记忆的基准和数据集。它在文本、one-hot 和相机参数控制之间标准化动作命令，使不同模型可以在相同任务上比较。

## 问题
- 现有世界模型基准的场景来源较窄，视角有限，对天气或光照的覆盖较少，这会削弱其对智能体训练场景的测试能力。
- 交互式模型接受不同控制方式，例如文本、类似键盘的 one-hot 输入和相机姿态，因此很难直接比较。
- 现有任务更多测试视觉生成，而不是动作响应、轨迹跟随，以及循环路径上的记忆能力。

## 方法
- 作者使用 12 个现有数据集和 4 个模拟器中的 18 个模拟器环境构建数据，然后统一视频格式、坐标系和相机参数。
- 他们创建了一个 Action Generation Framework，将每个动作映射为文本命令、one-hot 编码，以及相机内参/外参。
- 动作空间定义了 27 个平移 ID 和 27 个旋转 ID，共有 729 种可能组合；评估字典聚焦于当前模型支持的 81 个常见组合动作。
- 该基准定义了 6 类任务，覆盖动作控制难度 1-4 级、记忆能力和相机跟随。
- 它使用 9 个指标评估视觉生成、轨迹跟随和记忆。

## 结果
- 该数据集从 2780 万个多图像样本中过滤后包含 330,000 个视频片段；其中 2,100 个视频被选作评估数据。
- 该基准包含 4,900 个测试任务：动作控制难度 1、2、3、4 级各 1,000 个任务；200 个记忆任务；700 个相机跟随任务。
- 覆盖范围包括 4 种视角（UGV、UAV、人类、机器人）、9 种室外天气类型、5 种室内光照类型、18 个模拟器环境和数千个场景。
- 论文评估了 14 个世界模型：5 个文本控制模型、2 个 one-hot 控制模型和 7 个相机参数控制模型。
- 摘录未提供各模型的排行榜分数或指标值，因此文中最明确的结果是该基准的规模和覆盖范围，以及它的跨模态动作映射。
- 在表 1 中，iWorld-Bench 是唯一一个被标为支持多输入、交互式任务、相机控制、记忆能力、多场景、多视角和全天候评估的基准；它的 4,900 个样本超过 WorldBench（425）、MoveBench（1,018）、VMbench（1,050）、WorldEval（1,400）、EWMBench（2,100）和 WorldScore（3,000），但 WorldModelBench 的样本更多（67,000）。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03941v2](https://arxiv.org/abs/2605.03941v2)
