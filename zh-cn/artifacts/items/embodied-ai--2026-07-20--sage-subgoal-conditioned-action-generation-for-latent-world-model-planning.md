---
source: arxiv
url: https://arxiv.org/abs/2607.17973v1
published_at: '2026-07-20T14:10:56'
authors:
- Letian Cheng
- Qi Zhang
- Yisen Wang
topics:
- latent-world-model
- long-horizon-planning
- subgoal-generation
- action-proposals
- robot-manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# SAGE: Subgoal-Conditioned Action Generation for Latent World Model Planning

## Summary
## 总结
SAGE 通过使用预测的潜在子目标引导冻结潜在世界模型的动作提议，提升了长时域目标条件规划的性能。在 PushT 和 OGBench Cube 上，它显著提高了远距离目标下的成功率，同时保持了较强的短时域性能。

## 问题
- 潜在世界模型规划器会评估想象出的动作序列，但随着规划时域延长，随机或通用的提议只能覆盖动作空间中很小的一部分。
- 远距离目标提供的局部引导较弱，因此在固定候选数量下，规划器很难找到可达且质量较高的动作序列。
- 这对长时域机器人控制具有实际影响：即使预测世界模型保持不变，动作提议的质量也可能限制性能。

## 方法
- 一个可变时长的 Transformer 子目标生成器根据观测历史、当前状态、远距离目标、剩余时域和指定时长，预测未来 15、20 或 25 步对应的可达潜在状态。
- 第二个 Transformer 以预测的子目标和远距离目标为条件，生成轨迹级高斯混合动作选项，用结构化提议取代通用的随机初始化。
- 冻结的 LeWM 潜在世界模型评估所提议的未来，并通过交叉熵方法（CEM）进行细化，在执行前选择并改进动作序列。
- 规划器执行每个选定的局部选项，观测环境，预测新的子目标，并在多个时间阶段之间重新规划。

## 结果
- 在时域 150 下，完整的 SAGE 将 PushT 成功率从 LeWM 的 12.7% 提高到 64.7%，将 OGBench Cube 成功率从 26.7% 提高到 67.3%；评估使用相同的冻结 LeWM、300 个候选序列和 30 轮 CEM。
- 在 PushT 上，SAGE 在时域 25 和 50 下的成功率分别达到 94.0% 和 81.3%；在论文报告的相应时域下，LeWM 的成功率分别为 56.0% 和 12.7%，PRISM 则分别为 54.7% 和 17.3%。
- 在 OGBench Cube 上，SAGE 在时域 25 和 100 下的成功率分别达到 98.7% 和 85.3%；LeWM 的相应成功率为 66.7% 和 57.3%。
- 仅使用生成器的消融版本在时域 150 下于 PushT 和 Cube 上分别达到 58.7% 和 51.3%，而完整 SAGE 分别达到 64.7% 和 67.3%，表明子目标条件动作提议还能带来额外收益。
- 移除 LeWM 排序和 CEM 细化后，PushT 在时域 150 下的成功率从 64.7% 降至 16.0%，说明学习得到的提议仍需要世界模型引导的选择与细化。
- 结果来自 PushT 和 OGBench Cube 的留出轨迹查询，每个评估清单包含 50 个起点—目标对，共使用三个评估清单；该摘录无法证明模型在这些基准之外，或在实体机器人和仿真到现实设置中的性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.17973v1](https://arxiv.org/abs/2607.17973v1)
