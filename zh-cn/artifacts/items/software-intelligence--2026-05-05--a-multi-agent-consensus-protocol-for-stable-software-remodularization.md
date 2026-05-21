---
source: arxiv
url: https://arxiv.org/abs/2605.04188v1
published_at: '2026-05-05T18:27:02'
authors:
- Ahmed F. Ibrahim
topics:
- software-remodularization
- multi-agent-negotiation
- code-intelligence
- architecture-recovery
- software-clustering
- stability-constraints
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# A Multi-Agent Consensus Protocol for Stable Software Remodularization

## Summary
## 摘要
AMCP 将软件重模块化视为内聚代理和稳定性代理之间的协商。只有当变更保持在架构师设定的稳定性预算内时，它才会改进代码分区。

## 问题
- 现有软件聚类工具通常优化单一结构指标，例如 TurboMQ，因此可能推荐在版本之间变化过大的布局。
- 大幅布局变化会让开发者重新学习系统结构，即使内聚性提高，也会增加维护成本。
- 加权和多目标方法需要手动设定系数，并且不会强制执行硬性稳定性下限。

## 方法
- 论文将软件系统建模为有向依赖图，将分解建模为把类划分到簇中的分区。
- Cohesion Agent 用 TurboMQ 除以簇数量来为每个分区评分。Stability Agent 将其评分为 1 - MoJo(D, D_prev) / n_common。
- AMCP 从上一次接受的分解开始，并在每一步枚举所有单个类的重新分配。
- 它只保留能提高内聚性且满足 U_sta >= τ_sta 的移动，然后选择每单位内聚性增益带来稳定性损失最小的移动。
- 论文声称给出了有限终止、闭实例条件下符合 Zeuthen 风格的有界让步，以及在单步移动邻域内局部 Pareto 可满足性的形式化证明。

## 结果
- 在 Xwork 1.0 到 1.1 上，实验使用 113 个共有类、版本 1.0 中的 10 个包，以及版本 1.1 中的 156 个类。
- 当 τ_sta 从 0.60 到 0.90 且 τ_coh 固定为 0.5 时，AMCP 达到 U_coh = 0.5980、U_sta = 0.9167、social welfare = 1.5146，并进行了 6 个协商步骤。
- 同一 Xwork 图上的 Bunch 报告 U_coh = 0.5979、U_sta = 0.9167，因此在稳定性预算宽松时，AMCP 与主要内聚性结果相当。
- CC/G 报告 U_coh = 0.5885、U_sta = 0.9167、social welfare = 1.5052，低于宽松预算运行中 AMCP 的 1.5146。
- 当采用严格的 τ_sta = 0.95 时，AMCP 在 3 步后停止，结果为 U_coh = 0.5919、U_sta = 0.9583、social welfare = 1.5502，显示了论文所称的稳定性预算执行效果。
- 运行时间声称为：113 类 Xwork 系统每步 1.24 秒，120 模块 Apache Ant 子集每步 1.02 秒。十个系统的扩展评估和 NSGA-II 比较推迟到后续论文，因此该摘录没有给出这些主张的数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04188v1](https://arxiv.org/abs/2605.04188v1)
