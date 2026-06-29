---
source: arxiv
url: https://arxiv.org/abs/2606.19998v1
published_at: '2026-06-18T09:34:22'
authors:
- Jinghan Yang
- Yunchao Zhang
- Wang Yuan
- Haolun Wan
- Jiaming Zhang
- Zhengyang Hu
- Yanchao Yang
topics:
- vision-language-action
- failure-prediction
- robot-safety
- information-theory
- sim2real
- generalist-robot-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Tri-Info: Generalizable, Interpretable Failure Prediction for VLA Models via Information Theory

## Summary
## 摘要
Tri-Info 使用近期状态和动作嵌入上计算的熵与互信息，预测 VLA 机器人 rollout 中的失败。它的目标是在不重新训练的情况下跨模型迁移，并完成 sim-to-real 迁移，同时给出触发警报的具体原因。

## 问题
- VLA 策略在遇到新物体、光照、任务、模型或物理环境时可能失败，而机器人失败可能在人类反应前损坏物体或造成安全风险。
- 现有失败检测器常依赖某一个模型的内部嵌入空间，因此在 VLA 架构变化时需要重新训练。
- 有用的检测器必须提前预警，并说明策略是在冻结、漂移，还是在与观测状态不同步地行动。

## 方法
- 论文将 VLA 控制视为由状态嵌入、动作嵌入、下一状态和下一动作组成的闭环序列。
- 它推导出八个熵和互信息信号，然后将其缩减为三个 Tri-Info 信号：动作熵 H(A_t)、时间动作互信息 I(A_t; A_t+1)，以及状态转移/动作互信息 I(S_t, S_t+1; A_t)。
- 这三个信号对应简单的失败线索：动作多样性过低或过高、动作随时间的一致性较弱，以及动作与状态变化之间的耦合较弱。
- 该方法用滑动窗口和 k-NN 互信息、熵估计器估计每个信号，然后对数值做 z 归一化。
- 它为每个信号训练一个 GRU，平均三个失败概率，并使用函数型保形预测设置随时间变化的警报阈值。

## 结果
- 评估覆盖六个 VLA 模型和三个基准设置：LIBERO-10、CALVIN 和 ALOHA，包括仿真任务和真实机器人任务。
- 摘要称，在 sim-to-real 迁移下，Tri-Info 在真实任务上达到 83% 准确率，而此前的检测器降至随机水平。
- 单指标逻辑回归显示，这些信息论信号带有直接的失败信号：所有八个指标的域内合并 AUC 至少为 0.701，I(A_t; A_t+1) 达到 0.895 的合并 AUC。
- 加入时间 GRU 建模后，八个指标的合并单指标 AUC 提升到 0.973-0.982；H(A_t) 达到 0.982 的合并 AUC，I(A_t; A_t+1) 达到 0.976。
- 在域内 LIBERO 上，Tri-Info 报告 PI0 在轨迹中段时的平衡准确率为 0.91，PI0.5 在进度达到 10% 时为 0.85，且 PI0.5 的峰值为 0.92。
- 基线对比称，Tri-Info 与最强的域内基线相当，并且无需重新训练即可跨架构、环境和 sim-to-real 迁移；SAFE 在 PI0 上峰值为 0.96，在 PI0.5 上为 0.91，而 STAC 在 rollout 后期达到 0.89 和 0.93。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.19998v1](https://arxiv.org/abs/2606.19998v1)
