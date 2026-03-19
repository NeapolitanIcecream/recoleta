---
source: arxiv
url: http://arxiv.org/abs/2603.05764v1
published_at: '2026-03-05T23:48:41'
authors:
- Mykola Pinchuk
topics:
- benchmark
- data-science-agents
- tabular-ml
- llm-agents
- kaggle-style-evaluation
relevance_score: 0.04
run_id: materialize-outputs
language_code: zh-CN
---

# TML-Bench: Benchmark for Data Science Agents on Tabular ML Tasks

## Summary
TML-bench 是一个面向表格机器学习任务的数据科学代理基准，重点衡量模型在 Kaggle 风格端到端流程中的**性能、可靠性和时间受限下的稳定性**。论文用统一协议评测了 10 个开源 LLM，在 4 个竞赛、3 个时间预算下重复运行并用私有留出集打分。

## Problem
- 现有很多代理评测只看局部编码能力，难以反映真实数据科学工作流中的关键失败模式：读数据、特征处理、训练、迭代、生成合法提交文件。
- 单次“幸运跑通”不能代表实用价值；实际使用更关心**是否稳定地在时限内产出有效提交并取得不错分数**。
- 不同任务指标不同（如 AUC、RMSE），且时间预算受限，导致跨任务、跨模型比较不容易公平和可复现，这对实际选型很重要。

## Approach
- 提出 **TML-bench**：一个严格的 Kaggle 风格表格 ML 基准，使用 4 个竞赛、3 个时间预算（240s、600s、1200s），统一代理指令模板与单一执行 harness（Kilo Code）。
- 每个 `(competition, model, budget)` 组合取**最早 5 次成功运行**，用其中位数作为该设置的最终分数；成功的定义是：生成**格式合法的提交**，并在**代理不可见的私有留出标签**上得到有效分数。
- 为解决不同任务指标不可比问题，先把分数转成统一“越高越好”方向，再在每个 `(competition, budget)` 内做 **min-max 归一化**，构建总排行榜。
- 主排行榜采用“**每个竞赛取该模型最佳预算**，再在 4 个竞赛上平均”的聚合方式；同时报告成功率、IQR 稳定性、跨竞赛一致性和随时间预算变化的 scaling。
- 为降低污染风险，运行时关闭互联网，并只选择**知识截止时间早于竞赛开始时间**的模型。

## Results
- 论文共评测 **10 个 OSS LLM**，覆盖 **4 个竞赛 × 3 个时间预算 = 12** 个设置；每个设置要求 **5 次成功运行**，因此每个入选模型需完成完整覆盖。
- **MiniMax-M2.1-TEE** 在论文的主聚合指标下取得**四个竞赛上的最佳总体表现**；摘要和结果部分未给出其单一总分数值，但明确称其为 aggregate leader。
- 更长时间通常更好，但并不总是单调：在 **40 个 model×competition scaling 曲线**中，仅 **23/40 = 57.5%** 满足从 **240s→600s→1200s** 不变差；按模型中位数看，单调竞赛占比为 **62.5%**。
- 具体任务上，`bank-customer-churn-ict-u-ai`：1200s 最强中位 **AUC = 0.928000**（GPT OSS 120B TEE），240s 最强中位 **AUC = 0.926671**（MiniMax-M2.1-TEE）；同任务下某弱设置仅 **0.813105**（NVIDIA-Nemotron-3-Nano, 1200s）。
- `foot-traffic-wuerzburg-retail-forecasting-2-0`：MiniMax-M2.1-TEE 在三档预算都最好，**RMSE = 0.066846 / 0.065770 / 0.065489**（240s/600s/1200s）；GLM 4.7 Flash 在 1200s 出现明显不稳定，**median 0.107502，IQR 0.070186..0.221725**。
- `playground-series-s5e10`：1200s 时结果非常接近，最佳 **RMSE = 0.056190**（GLM-4.6-FP8）。`playground-series-s6e1`：MiniMax-M2.1-TEE 在 1200s 领先，**RMSE = 8.699779**；TNG-R1T2-Chimera 在 600s 出现异常，**median 10.199380，IQR 9.088197..13.444163**。

## Link
- [http://arxiv.org/abs/2603.05764v1](http://arxiv.org/abs/2603.05764v1)
