---
source: arxiv
url: http://arxiv.org/abs/2603.03800v1
published_at: '2026-03-04T07:23:54'
authors:
- Xingyao Wang
- Valerie Chen
- Heng Ji
- Graham Neubig
topics:
- code-agents
- reward-modeling
- process-supervision
- software-engineering
- human-in-the-loop
relevance_score: 0.94
run_id: materialize-outputs
---

# A Rubric-Supervised Critic from Sparse Real-World Outcomes

## Summary
本文提出一种从真实生产环境中稀疏、延迟且噪声很大的用户-代理结果信号中学习代码代理“critic”的方法。核心贡献是用24个可从交互轨迹直接观察到的行为rubrics，把大量无明确结果标签的真实轨迹转成可训练监督信号。

## Problem
- 论文解决的是：现实中的代码代理通常与人协作工作，但成功信号不像学术基准那样有清晰单步可验证奖励，而是**稀疏、延迟、噪声大**，导致难以评估、训练和做推理时选择。
- 这很重要，因为真实软件工程场景里，用户关心的不只是单测通过，还包括修改是否正确、可维护、可审查，以及是否真正减少了人的工作量。
- 只依赖 benchmark 训练出的评估器无法可靠迁移到生产环境；文中指出这类 critic 在真实结果上的 AUC 仅 **0.45–0.48**，接近随机。

## Approach
- 把真实多轮人机交互切成**segments**：每段从一次用户请求开始，到代理调用 finish 结束，作为最小监督与归因单位。
- 设计 **24 个 Critic Rubrics**，覆盖代理行为问题、用户后续反馈模式、基础设施问题等；这些标签只看轨迹本身，不看最终PR结果，从而避免结果泄漏。
- 用 LLM 对所有 segment 打 rubric 标注，再把少量真实结果代理信号一起用于训练：包括 **PR merge** 和更细粒度的 **code survival**。
- 训练一个**半监督多任务 critic**：一头预测 sparse success，另一头预测 dense rubrics。这样在 **151,837** 个真实 segments 中，虽然只有 **4%** 有 code-survival、**6%** 有 PR-merge 标签，但其余 **96%** 也能通过 rubrics 提供学习信号。
- 训练后的 critic 可直接用于三类用途：**best-of-N reranking、early stopping、训练数据筛选/数据整理**。

## Results
- 数据规模上，作者使用 **38,241** 个真实对话、**151,837** 个 segments；其中只有 **5,349 (4%)** 有 code survival 标签，**9,750 (6%)** 有 PR merge 标签，直接体现监督稀缺。
- rubric 有效性方面，在 **SWE-bench / SWE-Gym** 中，诸如 incomplete implementation、insufficient testing、insufficient debugging、insufficient analysis 等失败模式会使成功率下降 **15–21 个百分点**，且 **p < 0.001**（FDR校正后）。在真实数据中，效果更弱更噪声，但如 reversion request 对 code survival 仍有显著负效应，**Δ = -0.13, q < 0.001**。
- 真实监督必要性：仅用 benchmark 轨迹训练的 critics 在真实世界结果上表现接近随机，**AUC 0.45–0.48**，且还可能损害 SWE-bench 下游选择效果。
- 推理时重排序方面，critic 可提升 SWE-bench 上的 best-of-N 选择：在可重排轨迹子集上，**Best@8 相比 Random@8 提升 +15.9**。
- 早停方面，critic 支持更高效的推理计算分配：文中报告**+17.7** 的提升，同时**尝试次数减少 83%**。
- 作者还声称 critic 可用于训练时的数据筛选，利用 critic 选择真实轨迹做监督微调；给定节选中未提供更细的量化对比数值。

## Link
- [http://arxiv.org/abs/2603.03800v1](http://arxiv.org/abs/2603.03800v1)
