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
WAV 是一个可自我改进的世界模型框架。它先检查两件更简单的事，来找出动作条件动力学模型可能出错的地方：未来状态看起来是否合理，以及这个动作是否真的能产生它。论文声称，在探索不足的区域里，这种验证比直接预测下一状态更容易，因此能提高数据收集效率和下游策略学习效果。

## 问题
- 世界模型需要预测一大范围动作的结果，包括差动作或随机动作，但带动作标注的机器人数据数量有限、采集成本高，有时还不安全。
- 现有的验证方法，比如不确定性、集成分歧或学习进展，在最需要它们的地方往往失效，也就是模型几乎没有先验支持的探索不足区域。
- 这会带来实际后果：验证做不好，就会选错数据，世界模型更弱，策略评估、规划和优化的效果也会变差。

## 方法
- WAV 把验证拆成两个检查：**状态合理性** 和 **动作可达性**。预测出的下一状态既要像一个合理的未来状态，也要能由给定动作到达。
- 为了判断合理性，WAV 在大量无动作视频数据上训练一个子目标生成器，并从这个先验中采样合理的未来状态。
- 为了判断可达性，WAV 在带动作标注的数据上训练一个稀疏逆动力学模型，只用与动作相关的状态特征来推断动作，并使用学习到的掩码，而不是完整观测。
- 然后它执行一个反向循环：当前状态 -> 采样到的合理子目标 -> 推断出的动作 -> 世界模型滚动预测。采样子目标和世界模型预测之间的差距，被用作探索和自我改进的误差信号。
- 理论部分指出，当动作只依赖状态特征的低维子集、环境随机性较高、且标注数据有限时，稀疏逆向验证比稠密前向预测更容易。

## 结果
- 在 **MiniGrid、RoboMimic 和 ManiSkill** 覆盖的 **9 个任务** 上，WAV 的世界模型学习样本效率比现有方法高 **2 倍**。
- 论文报告，下游策略性能比基线提升了 **18%**。
- 在受控的 MiniGrid 研究中，鲁棒性评估把带标签数据量从 **400** 到 **2000** 个 transition 做变化，把场景复杂度从 **6** 到 **14** 个对象做变化，并加入 **0 到 4** 个噪声地面来提高随机性。
- MiniGrid 的数据设置使用 **50k** 条交互序列，其中 **200** 条种子序列作为带标签数据，**20k** 条无标签候选序列用于采样；完整数据的一半用于训练无动作的子目标生成器。
- 摘要说明，WAV 与 **Random、Uncertainty、Progress、Vanilla IDM 和 Oracle** 基线做了比较，但提供的文本里没有给出各基准的详细指标表，也没有给出除标题里的 **2x** 和 **18%** 之外的精确差距。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01985v1](http://arxiv.org/abs/2604.01985v1)
