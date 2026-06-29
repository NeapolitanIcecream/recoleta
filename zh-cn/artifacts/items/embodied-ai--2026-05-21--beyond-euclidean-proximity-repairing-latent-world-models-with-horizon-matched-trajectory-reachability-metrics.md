---
source: arxiv
url: https://arxiv.org/abs/2605.22164v1
published_at: '2026-05-21T08:34:57'
authors:
- Liangyu Li
- Shengzhi Wang
- Qingwen Liu
topics:
- latent-world-models
- model-predictive-control
- reachability-metrics
- trajectory-data
- robot-planning
- continuous-manipulation
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics

## Summary
## 摘要
TRM 是一种后置终端代价，适用于固定的潜在世界模型 MPC。它用学到的轨迹可达性来给候选终点排序，而不是用原始潜在 MSE。论文声称，在困难的 TwoRoom 上它能带来很大提升，因为潜在状态里包含位置，但规划器的欧氏代价给这个信号的权重太低。

## 问题
- 潜在 MPC 常用预测得到的终端潜在状态和目标潜在状态之间的欧氏距离来给动作候选打分，这会把被阻挡或不可达的终点排在可行路线前面。
- 这会影响控制，因为世界模型可能已经编码了所需状态，但规划器还是会因为终端度量不好而选错动作。
- TwoRoom 里能看到这个失败：LeWM 的潜在表示可以用线性探针恢复 XY 位置，R² = 0.998，但原始潜在 MSE 在困难的 n100 manifest 上只有 7.0% 的平均成功率。

## 方法
- TRM 在从日志轨迹中编码得到的配对样本上训练一个小的 pairwise head m_phi(z_i, z_j)。
- 训练目标是同一 episode 内的时间间隔 |t_i - t_j|，把它当作简单的可达性代理：一条有效轨迹上时间接近的状态，应该更容易连通。
- 采样方式与预测时长对齐：head 看到的是覆盖整段 episode、分布均衡的时间间隔，这样训练分布就和长时程终端候选排序问题一致。
- 在规划时，编码器、动力学模型、CEM 采样器、优化器和评估 manifest 都保持不变，只改终端代价。
- 这个学到的度量可以在可达性占主导的任务里替代原始潜在 MSE，也可以在连续操作任务里和标准化的原始潜在代价组合成混合代价。

## 结果
- 在带 LeWM 的困难 n100 TwoRoom 上，原始潜在 MSE 的平均成功率是 7.0%，完整时长的 TRM 达到 97.0%；同样架构和数据量的打乱标签 head 只有 0.0%。
- 在同样困难的 n100 manifest 上，PLDM 的原始潜在 MSE 平均成功率是 32.7%，完整时长的 TRM 达到 84.0%；打乱标签 head 仍然是 0.0%。
- 时长匹配很重要：覆盖整段 episode 的随机采样达到 90.0%，整段 episode 的均衡配对达到 97.5%，而最大 Δ = 50 的短时长 TRM 在相同的 100,000 对预算下只有 35.0%。
- 对 LeWM seed 3072 的同候选选择审计显示，geodesic Spearman 从原始潜在 MSE 的 0.018 升到真实标签 TRM 的 0.729；oracle 最优候选的排名百分位从 31.71 变到 3.86。
- XY-probe rowspace 在终端目标潜在 MSE 中占比不到 1%，但携带了大部分候选质量信号，这支持了原始潜在距离低估控制相关变量的说法。
- 在 PushT go50/go75 上，摘录只说明 TRM 风格的任务状态度量在 SCSA 排名和选中的最终距离上更好，但给出的文本里没有提供具体的 PushT 成功率或 SCSA 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22164v1](https://arxiv.org/abs/2605.22164v1)
