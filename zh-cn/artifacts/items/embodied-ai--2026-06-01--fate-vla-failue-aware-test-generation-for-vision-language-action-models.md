---
source: arxiv
url: https://arxiv.org/abs/2606.02307v1
published_at: '2026-06-01T14:27:13'
authors:
- Arusa Kanwal
- Pablo Valle
- Shaukat Ali
- Aitor Arrieta
topics:
- vision-language-action
- robot-evaluation
- failure-discovery
- adaptive-testing
- surrogate-guided-testing
- embodied-ai
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# FATE-VLA:Failue-aware test generation for vision-language-action models

## Summary
## 概要
FATE-VLA 是一个面向 Vision-Language-Action 机器人策略的自适应测试生成器，用来寻找更容易出错、且彼此不同的操作场景。它在 SimplerEnv 的四个 VLA 模型上，比随机采样和只强调多样性的自适应随机测试发现了更多失败。

## 问题
- 它解决的是 VLA 评估不够有力的问题：固定或随机抽样的任务场景，可能漏掉高维机器人场景空间里那些少见且成簇出现的失败。
- 这很重要，因为机器人策略在静态基准上看起来安全，但在特定的物体、位置、朝向或指令条件下仍可能失败。
- 论文还会测量发现的失败在轨迹和物体上是否多样，而不只是失败数量。

## 方法
- 核心方法是生成候选操作场景，在 VLA 策略上执行一个场景，记录成功或失败，再用不断增长的日志指导下一次测试。
- 一个变体把 FSCS-ART 的多样性选择和一个代理分类器结合起来，用它预测候选场景是否会失败。
- 另一个变体用随机森林估计失败概率，并用 `score = alpha * p_fail + (1 - alpha) * normalized_distance` 给每个候选项打分。
- 测试空间包括物体选择、位置和朝向。实验使用 7 个物体，以及 SimplerEnv 的工作空间范围 `x = [-0.5, -0.05]` 和 `y = [0.0, 0.4]`。
- 评估的 VLA 模型是 OpenVLA、pi0、GR00T-N1.6 和 EO-1，使用的是 SimplerEnv 的拾取任务，每种配置运行 10 次。

## 结果
- 在没有天花板效应的 VLA 模型上，这些方法比随机测试将失败率提高了 14 到 30 个百分点，比 FSCS-ART 提高了 13 到 29 个百分点。
- 在 GR00T-N1.6 上，最佳方法把失败率从随机测试的 35.6% 和 FSCS-ART 的 36.5% 提高到 Sorting_RF 的 65.3%。论文也把这一结果写成成功率从 64.4% 降到 34.7%。
- 在 EO-1 上，失败率从随机测试的 36.7% 和 FSCS-ART 的 38.0% 提高到 Sorting_RF 的 60.0%，分别提升了 +23.3 和 +22.0 个百分点。
- 在 EO-1 上，轨迹覆盖率从随机测试的 82.8% 和 FSCS-ART 的 81.5% 提高到 Sorting_DT 的 84.0%。
- 在 GR00T-N1.6 上，失败条件下的轨迹覆盖率从随机测试的 78.2% 和 FSCS-ART 的 79.9% 提高到 Sorting_RF 的 83.0%。
- EO-1 上的失败物体覆盖率在 Weighted_RF 下达到 98.6%，高于随机测试的 96.1%，也与 FSCS-ART 的 98.6% 持平。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02307v1](https://arxiv.org/abs/2606.02307v1)
