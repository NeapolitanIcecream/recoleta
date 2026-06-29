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
AMCP 将软件重模块化看作凝聚力代理和稳定性代理之间的协商。只有当改动仍在架构师设定的稳定性预算内时，它才会改进代码划分。

## 问题
- 现有软件聚类工具常常只优化单一结构指标，比如 TurboMQ，因此它们可能推荐在版本之间变化过大的布局。
- 布局变化过大会让开发者重新学习系统结构，即使凝聚力提高了，维护成本也会上升。
- 加权求和的多目标方法需要手动设定系数，而且不能强制执行硬性的稳定性下限。

## 方法
- 论文把软件系统建模为有向依赖图，把分解建模为类到簇的划分。
- 凝聚力代理用 TurboMQ 除以簇数来给每个划分打分。稳定性代理用 1 - MoJo(D, D_prev) / n_common 来打分。
- AMCP 从上一次被接受的分解开始，在每一步枚举所有单类重分配。
- 它只保留那些同时提高凝聚力并满足 U_sta >= τ_sta 的移动，然后选择稳定性损失与凝聚力收益之比最小的移动。
- 论文声称已经给出有限终止、在闭实例条件下符合 Zeuthen 策略的有界让步，以及在单步邻域内局部满足帕累托最优的形式化证明。

## 结果
- 在 Xwork 1.0 到 1.1 上，实验使用了 113 个公共类，1.0 版有 10 个包，1.1 版有 156 个类。
- 当 τ_sta 从 0.60 到 0.90，且 τ_coh 固定为 0.5 时，AMCP 达到 U_coh = 0.5980、U_sta = 0.9167、社会福利 = 1.5146，并进行了 6 步协商。
- 在同一个 Xwork 图上，Bunch 报告的 U_coh = 0.5979、U_sta = 0.9167，所以在稳定性预算较宽松时，AMCP 与主要凝聚力结果一致。
- CC/G 报告的 U_coh = 0.5885、U_sta = 0.9167、社会福利 = 1.5052，低于宽松预算运行中的 AMCP 的 1.5146。
- 当 τ_sta 严格设为 0.95 时，AMCP 在 3 步后停止，U_coh = 0.5919、U_sta = 0.9583、社会福利 = 1.5502，说明它确实执行了所说的稳定性预算约束。
- 运行时间声明是：113 类的 Xwork 系统每步 1.24 秒，120 模块的 Apache Ant 子集每步 1.02 秒。十个系统的扩展评估和 NSGA-II 比较会放到后续论文中，所以这段摘要没有给出这些结果的数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04188v1](https://arxiv.org/abs/2605.04188v1)
