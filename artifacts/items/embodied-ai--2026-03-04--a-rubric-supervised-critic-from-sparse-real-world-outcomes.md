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
- reward-modeling
- process-supervision
- coding-agents
- human-in-the-loop
- trajectory-ranking
relevance_score: 0.16
run_id: materialize-outputs
---

# A Rubric-Supervised Critic from Sparse Real-World Outcomes

## Summary
本文提出一种从真实生产环境中稀疏、噪声化结果信号学习“critic”模型的方法，用于评估编码代理的交互轨迹。核心在于把多轮人机交互切成 segment，并用 24 个可从轨迹直接观察的 rubric 提供密集监督，从而让极少量真实结果标签也能训练出可部署的评分器。

## Problem
- 论文要解决的是：现实中的编码代理通常与人协作，成功信号不是单纯的单元测试通过，而是**稀疏、延迟、带噪声**的，如 PR merge、代码是否最终保留；这使得评估、训练和选择最佳轨迹都很困难。
- 这很重要，因为如果没有可靠评价器，就很难对真实世界 coding agent 做 A/B 测试、RL 训练、数据筛选或 inference-time reranking。
- 仅靠学术 benchmark 的可验证奖励并不能代表真实部署；作者指出只在 benchmark 上训练的 critic 在真实数据上几乎接近随机（AUC 0.45–0.48）。

## Approach
- 把多轮人机交互表示成 **segments**：每个 segment 从一次用户请求开始，到 agent 调用 finish 结束，作为最小可归因工作单元。
- 设计 **Critic Rubrics**：24 个行为特征，覆盖 agent 失误、用户后续反馈、基础设施问题；这些标签只依赖交互轨迹本身，不泄露最终结果。
- 用 LLM 对所有 segment 自动标注 rubrics，再结合极少量真实 outcome proxy 共同训练 critic；训练目标是**联合预测 rubric + success**，属于半监督、多任务学习。
- 真实结果信号来自两类 proxy：PR merge（粗粒度二分类）和 **code survival**（某个 segment 贡献的代码最终保留比例），其中 code survival 更细粒度但更稀疏。
- 学到的 critic 可直接用于三类下游：best-of-N reranking、early stopping、以及训练时的数据筛选/轨迹挑选。

## Results
- 数据规模上，作者使用 **38,241** 个对话、**151,837** 个 segments；其中只有 **5,349 (4%)** 有 code-survival 标签，**9,750 (6%)** 有 PR-merge 标签，但 rubrics 可覆盖全部 segment。
- 在 benchmark 中，rubric 所刻画的典型失败模式与失败强相关：如 incomplete implementation、insufficient testing、insufficient debugging、insufficient analysis 会使成功率下降 **15–21 个百分点**（SWE-bench/SWE-Gym，**p < 0.001**，FDR 校正后）。
- 真实世界监督是必要的：仅用 benchmark 训练的 critic 在真实 outcome 上几乎无效，AUC 仅 **0.45–0.48**，甚至会伤害 SWE-bench 上的下游选择表现。
- 在 inference-time reranking 上，critic 可把 SWE-bench 的 **Best@8 相对 Random@8 提升 +15.9**（在可 rerank 的轨迹子集上）。
- 在 early stopping 上，critic 实现 **+17.7** 的提升，同时将尝试次数减少 **83%**；说明它不仅能选更好轨迹，还能更早停掉差轨迹以节省计算。
- 论文还声称 code survival 虽然更稀疏，但比 PR merge 更适合作为训练信号；此外，带 rubric 的 critic 比 success-only critic 更能跨不同 LLM backbone 泛化，用作共享评分函数。

## Link
- [http://arxiv.org/abs/2603.03800v1](http://arxiv.org/abs/2603.03800v1)
