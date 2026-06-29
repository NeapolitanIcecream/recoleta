---
source: arxiv
url: https://arxiv.org/abs/2606.13672v1
published_at: '2026-06-11T17:59:15'
authors:
- Arnav Kumar Jain
- Yilin Wu
- Jesse Farebrother
- Gokul Swamy
- Andrea Bajcsy
topics:
- world-model
- robot-manipulation
- multiview-vision
- latent-dynamics
- test-time-planning
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation

## Summary
## 摘要
WEAVER 是一个用于机器人操作的世界模型。它从多视角输入和动作片段预测未来潜在状态、奖励和解码后的观测。它面向三种用途：策略评估、策略改进和测试时规划。

## 问题
- 机器人世界模型需要准确，在长时间跨度内保持一致，还要足够快，才能用于规划。
- 操作任务还带来多视角遮挡、接触丰富的运动，以及需要基于预测轨迹判断任意视觉-运动策略。
- 以往模型在保真度、一致性和速度之间要做取舍，不能同时支持这三种下游用途。

## 方法
- 用预训练编码器把多视角图像和本体感觉编码为潜变量。
- 用 flow-matching 目标预测未来潜在轨迹，并加入 diffusion forcing 来保证长时程一致性。
- 使用稀疏记忆和短期历史，让模型同时跟踪最近运动和更长上下文。
- 增加潜在奖励头和 critic 头，让模型可以给想象轨迹打分，而不必先把图像解码给外部评判器。
- 用 rectified flow 对模型做蒸馏，并使用 KV caching 和 token dropping 降低推理成本。

## 结果
- 在 DROID 验证集上，WEAVER 在外视角、16 NFE 下得到 FID 10.20、FVD 27.83；Ctrl-World 分别是 FID 26.09、FVD 78.73。在腕部视角上，WEAVER 得到 FID 21.50、FVD 90.72；Ctrl-World 分别是 33.83 和 195.37。
- 在分布外任务集上，WEAVER 在外视角、16 NFE 下得到 FID 23.95、FVD 88.27；Ctrl-World 分别是 36.16 和 139.54。
- 报告的 10 秒轨迹推理时间中，WEAVER 在 16 NFE 下为 4.78 秒，Ctrl-World 为 14.65 秒；在 50 NFE 下分别为 14.25 秒和 42.33 秒。
- 在五个真实机器人操作任务的策略评估中，WEAVER 报告与真实世界成功率的相关系数 rho = 0.870。
- 在策略改进上，它把 pi_0.5 机器人基础模型的真实世界成功率提高了 38%，且不需要真实世界交互。
- 在测试时规划上，它把真实世界成功率提高了 14%，运行速度比 Ctrl-World 快 5-10 倍。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13672v1](https://arxiv.org/abs/2606.13672v1)
