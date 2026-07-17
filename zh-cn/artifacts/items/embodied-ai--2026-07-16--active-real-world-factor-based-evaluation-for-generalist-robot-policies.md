---
source: arxiv
url: https://arxiv.org/abs/2607.14439v1
published_at: '2026-07-16T00:21:54'
authors:
- Andrew Liao
- Hanchen Cui
- Karthik Desingh
- Aryan Deshwal
topics:
- robot-policy-evaluation
- generalist-robot-policy
- active-learning
- real-world-robotics
- factor-based-testing
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Active Real-World Factor-Based Evaluation for Generalist Robot Policies

## Summary
## 摘要
该论文提出了一种主动式真实世界评估框架，用于估计通用机器人策略在任务因素变化下的表现，同时减少实体试验次数。在三项操作任务的 2,331 次评估中，与均匀随机测试相比，该方法通常可节省 20–40% 的试验次数。

## 问题
- 通用机器人策略可能因物体位置、桌面高度、相机视角及其他部署条件的变化而失效，但针对这些因素开展穷尽式真实硬件评估既缓慢又昂贵。
- 狭窄的测试套件和汇总成功率可能遗漏容易失败的区域，并歪曲策略的性能分布及其部署准备度。

## 方法
- 使用结构化任务因素表示每个评估配置，并对由此形成的设计空间中的策略连续性能得分进行建模。
- 使用概率代理模型，主要是带有 RBF 核和自动相关性判定的高斯过程，根据此前评估过的配置预测性能及不确定性。
- 使用贝叶斯主动测试采集函数，包括后验标准差、负积分后验方差、BALD 和 EPIG，选择信息量最大的下一个真实世界配置。
- 首先随机选择 30 次评估，然后依次评估所选配置并更新代理模型，直到试验预算用尽。

## 结果
- 该研究涵盖三项 UR5e 操作任务中的 2,331 个有效真实世界配置，涉及三个因素、11×11 的物体位置网格、三种桌面高度和三种场景相机视角。
- 研究报告称，每项任务均进行了 700 多次真实世界基准评估；每次评估耗时约一分钟。
- 在 100 次试验的评估预算下，与典型随机测试相比，主动测试通常可节省 20–40 次试验，即减少 20–40% 的工作量。
- 摘录未提供详细的代理模型预测误差数值或各方法的单独结果；其中最明确的具体结论是，与随机测试相比，主动测试能更高效地刻画策略的性能分布，并识别容易失败的区域。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14439v1](https://arxiv.org/abs/2607.14439v1)
