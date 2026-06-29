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
## 摘要
iWorld-Bench 是一个用于测试交互式世界模型是否遵循动作输入并保持场景记忆的基准和数据集。它把文本、one-hot 和相机参数控制下的动作命令统一起来，方便在同一组任务上比较不同模型。

## 问题
- 现有世界模型基准的场景来源较窄、视角有限，对天气和光照的覆盖也少，这削弱了它们在智能体训练场景中的测试能力。
- 交互式模型接受的控制方式不同，例如文本、类似键盘的 one-hot 输入和相机位姿，直接比较很困难。
- 现有任务更偏向视觉生成，对动作响应、轨迹跟随，以及沿循环路径的记忆测试较少。

## 方法
- 作者从 12 个现有数据集和 4 个模拟器中的 18 个模拟环境构建数据，然后统一视频格式、坐标系统和相机参数。
- 他们创建了一个动作生成框架，把每个动作映射到文本命令、one-hot 编码，以及相机内参和外参。
- 动作空间定义了 27 个平移 ID 和 27 个旋转 ID，共有 729 种可能组合；评估字典聚焦于当前模型支持的 81 个常见组合动作。
- 该基准定义了 6 类任务，覆盖动作控制难度 1-4、记忆能力和相机跟随。
- 它用 9 个指标评估视觉生成、轨迹跟随和记忆。

## 结果
- 数据集在过滤掉 2,780 万个多图像样本后，包含 330,000 个视频片段；其中 2,100 个视频被选作评估样本。
- 该基准包含 4,900 个测试任务：动作控制难度 1、2、3、4 各 1,000 个任务；200 个记忆任务；以及 700 个相机跟随任务。
- 覆盖范围包括 4 种视角（UGV、UAV、人类、机器人）、9 种室外天气类型、5 种室内光照类型、18 个模拟环境和数千个场景。
- 论文评估了 14 个世界模型：5 个文本控制模型、2 个 one-hot 控制模型和 7 个相机参数控制模型。
- 这段摘录没有提供各模型的排行榜分数或指标数值，所以最强的已报告结果是该基准的规模、覆盖范围，以及跨模态动作映射。
- 在表 1 中，iWorld-Bench 是唯一被标记为支持多输入、交互任务、相机控制、记忆能力、多场景、多视角和全天候评估的基准；它的 4,900 个样本超过了 WorldBench（425）、MoveBench（1,018）、VMbench（1,050）、WorldEval（1,400）、EWMBench（2,100）和 WorldScore（3,000），而 WorldModelBench 的样本更多（67,000）。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03941v2](https://arxiv.org/abs/2605.03941v2)
