---
source: arxiv
url: http://arxiv.org/abs/2603.05764v1
published_at: '2026-03-05T23:48:41'
authors:
- Mykola Pinchuk
topics:
- benchmarking
- data-science-agents
- tabular-ml
- llm-agents
- reliability-evaluation
relevance_score: 0.91
run_id: materialize-outputs
---

# TML-Bench: Benchmark for Data Science Agents on Tabular ML Tasks

## Summary
TML-bench 是一个面向表格机器学习任务的数据科学智能体基准，重点评估模型在 Kaggle 风格端到端流程中的**正确性、可靠性和限时表现**。它不是只看一次最好成绩，而是通过重复运行、私有隐藏集评分和跨任务归一化，比较 10 个开源/开放权重 LLM 在真实 tabular ML 工作流中的稳定能力。

## Problem
- 现有很多基准只测局部编码或单次幸运表现，不能反映数据科学智能体是否真的能在**限定时间内完成端到端 tabular ML 工作流**。
- 不同 Kaggle 任务的指标不同（如 AUC、RMSE），直接横向比较困难；同时，单次结果也掩盖了**成功率和运行波动**。
- 这件事重要，因为实际使用中，用户需要的不只是“偶尔能做对”，而是**稳定地产生合法提交并拿到可复现分数**的智能体。

## Approach
- 作者提出 **TML-bench**：一个严格的 Kaggle 风格表格任务基准，覆盖 **4 个竞赛 × 3 个时间预算（240s、600s、1200s）**，并评测 **10 个模型**。
- 每个模型在每个任务和预算下**重复运行 5 次成功样本**；报告值取“最早 5 次成功运行”的**中位数**，而不是最好一次。
- 运行由 **Kilo Code** 统一 harness 执行：在干净工作区内限时运行，自动检查提交格式，并在**智能体不可见的私有隐藏标签**上评分，确保端到端正确性。
- 为了跨任务比较，作者先把不同指标统一成“越高越好”，再在每个任务/预算设置内做 **min-max 归一化**，主榜单采用“**每个竞赛取最佳预算，再对 4 个竞赛平均**”的聚合方式。
- 为降低污染风险，评测时**关闭互联网**，并只选择**知识截止时间早于竞赛发布时间**的模型。

## Results
- 在主聚合指标下，**MiniMax-M2.1-TEE** 在 **4/4 个竞赛**上的综合表现最好，是论文声称的总榜第一模型。
- 更长时间预算整体上有帮助，但提升并不总是平滑：在 **40 条 model×competition 扩展曲线**中，仅 **23/40 = 57.5%** 是单调不变差；按模型汇总的中位单调率为 **62.5%**，说明“给更多时间就更好”在当前重复次数下仍较噪声。
- 具体任务结果：在 **bank-customer-churn-ict-u-ai** 上，**1200s** 最强中位 **AUC = 0.928000**（GPT OSS 120B TEE），而 **240s** 最强为 **0.926671**（MiniMax-M2.1-TEE）；同任务中 Nemotron-3-Nano 在 1200s 仅 **0.813105**，差距明显。
- 在 **foot-traffic-wuerzburg-retail-forecasting-2-0** 上，**MiniMax-M2.1-TEE** 在三档预算都最优：**RMSE 0.066846 / 0.065770 / 0.065489**（240s/600s/1200s）。同时 **GLM 4.7 Flash** 在 1200s 的中位 **0.107502**，IQR 为 **0.070186..0.221725**，显示出显著不稳定性。
- 在 **playground-series-s5e10** 上，**1200s** 的结果高度接近，最佳为 **RMSE 0.056190**（GLM-4.6-FP8），且许多模型差距只有**几 1e-4**，说明该任务上头部模型已非常接近。
- 在 **playground-series-s6e1** 上，**MiniMax-M2.1-TEE** 在 **1200s** 取得最佳 **RMSE 8.699779**；而 **TNG-R1T2-Chimera** 在 **600s** 出现明显失败模式，中位 **10.199380**、IQR **9.088197..13.444163**。论文未给出统一数值化的总体榜单分数表，但明确强调了**性能、成功率与稳定性之间存在显著分化**。

## Link
- [http://arxiv.org/abs/2603.05764v1](http://arxiv.org/abs/2603.05764v1)
