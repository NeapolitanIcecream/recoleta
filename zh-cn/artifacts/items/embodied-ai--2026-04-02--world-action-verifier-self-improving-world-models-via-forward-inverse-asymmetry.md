---
source: arxiv
url: http://arxiv.org/abs/2604.01985v1
published_at: '2026-04-02T12:48:36'
authors:
- Yuejiang Liu
- Fan Feng
- Lingjing Kong
- Weifeng Lu
- Jinzhou Tang
- Kun Zhang
- Kevin Murphy
- Chelsea Finn
- Yilun Du
topics:
- world-models
- inverse-dynamics
- active-data-collection
- robot-learning
- simulated-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry

## Summary
## 摘要
WAV 是一种可自我改进的世界模型框架。它通过检查两件更简单的事，找出动作条件动力学模型可能出错的位置：未来状态是否看起来合理，以及该动作是否真的能产生这个状态。论文称，在探索不足的区域里，这种验证比直接预测下一状态更容易，因此能提高数据收集效率和下游策略学习效果。

## 问题
- 世界模型需要为大范围动作预测结果，包括糟糕或随机的动作，但带动作标签的机器人数据有限、成本高，而且有时采集不安全。
- 现有验证方法，如不确定性、集成分歧或学习进展，在最关键的地方往往失效：模型几乎没有先验支持的探索不足区域。
- 这很重要，因为验证差会导致数据选择差、世界模型更弱，以及策略评估、规划和优化效果更差。

## 方法
- WAV 将验证拆成两项检查：**状态合理性** 和 **动作可达性**。预测的下一状态既要看起来是一个有效未来状态，也要能够由给定动作到达。
- 对于合理性，WAV 在大规模无动作视频数据上训练一个子目标生成器，并从这个先验中采样合理的未来状态。
- 对于可达性，WAV 在带动作标签的数据上训练一个稀疏逆动力学模型，只根据与动作相关的状态特征来推断动作，使用学习得到的掩码，而不是完整观测。
- 然后它运行一个反向循环：当前状态 -> 采样得到的合理子目标 -> 推断动作 -> 世界模型 rollout。采样子目标与世界模型预测之间的差距被用作误差信号估计，用于探索和自我改进。
- 理论部分认为，当动作只依赖状态特征中的低维子集、环境随机性高且带标签数据有限时，稀疏逆向验证比稠密前向预测更容易。

## 结果
- 在 **MiniGrid、RoboMimic 和 ManiSkill** 上的 **9 个任务**中，WAV 报告称其世界模型学习的**样本效率提高了 2 倍**，相比现有方法更高。
- 论文报告称，与基线相比，**下游策略性能提升了 18%**。
- 在受控的 MiniGrid 研究中，鲁棒性评估将带标签数据规模从 **400 到 2000** 条转移变化，测试场景复杂度从 **6 到 14 个物体**变化，并加入 **0 到 4** 个噪声地板以增加随机性。
- MiniGrid 数据设置使用 **50k 交互序列**，其中 **200 个种子序列**作为带标签数据，**20k 无标签候选序列**用于采集；完整数据的一半用于训练无动作子目标生成器。
- 摘要说明，WAV 与 **Random、Uncertainty、Progress、Vanilla IDM 和 Oracle** 基线进行了比较，但所给文本没有包含各基准的详细指标表，也没有给出除 **2x** 和 **18%** 这两个核心结果之外的精确基线差距。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01985v1](http://arxiv.org/abs/2604.01985v1)
