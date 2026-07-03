---
source: arxiv
url: https://arxiv.org/abs/2607.01410v1
published_at: '2026-07-01T19:15:17'
authors:
- Yunfu Deng
- Josiah P. Hanna
topics:
- sim2real
- robot-policy
- latent-representation
- bisimulation
- visual-navigation
- cross-domain-transfer
relevance_score: 0.79
run_id: materialize-outputs
language_code: zh-CN
---

# BIFROST: Bridging Invariant Feature Representation for Observation-space Sim2Real Transfer

## Summary
## 摘要
BIFROST 训练一个共享的潜在历史编码器，使在仿真中训练的机器人策略无需在线适配即可在目标域运行。所给摘录显示，在视觉和动力学差距下，BIFROST 在 sim2sim 中有明确收益；文中声称有 sim2real 结果，但所给文本未展示具体数值。

## 问题
- Sim2real 机器人策略常常失败，因为仿真图像不同于相机图像，仿真物理也不同于真实接触、摩擦和执行器行为。
- 现有方法通常用独立模块分别处理感知差距和动力学差距；当两类差距同时出现时，这种组合可能失效。
- 这个问题重要，因为真实机器人数据采集成本高且有风险，而仿真数据的成本低到足以用于策略训练。

## 方法
- BIFROST 通过在匹配的可观测配置下，在仿真中重放目标域动作序列，收集成对的目标-源轨迹片段。
- 一个 GRU 历史编码器将两个域的观测-动作历史映射到同一个潜在状态空间。
- 训练使用三项损失：目标奖励预测、潜在下一状态预测，以及跨域后继对齐。
- 对齐损失近似预测潜在后继分布之间的 Wasserstein-1 距离，遵循跨域双模拟思想：奖励和未来行为相似的历史应映射到彼此接近的位置。
- 编码器训练完成后会被冻结；SAC 在仿真的潜在状态上训练策略，随后同一个编码器和策略在目标域运行，不再进行适配。

## 结果
- 在俯视 sim2sim 导航中，BIFROST 在 10 个种子上的成功率达到 0.68 ± 0.08；相比之下，Direct Transfer 为 0.19 ± 0.04，Target-Only 为 0.46 ± 0.09，BDA 为 0.67 ± 0.05，Co-Training BC 为 0.59 ± 0.08，Co-Training Offline RL 为 0.63 ± 0.08。
- 在自我中心视角 sim2sim 导航中，BIFROST 的成功率达到 0.50 ± 0.08；相比之下，Direct Transfer 为 0.03 ± 0.02，Target-Only 为 0.16 ± 0.07，BDA 为 0.34 ± 0.05，Co-Training BC 为 0.37 ± 0.07，Co-Training Offline RL 为 0.17 ± 0.14。
- 导航任务的目标域数据预算为 200 条轨迹，约 4,600 个成对片段，平均长度为 32。
- 摘录声称在接触丰富的操作任务和视觉伺服任务上有 sim2real 证据，但所给文本不包含定量的 sim2real 表格或指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01410v1](https://arxiv.org/abs/2607.01410v1)
