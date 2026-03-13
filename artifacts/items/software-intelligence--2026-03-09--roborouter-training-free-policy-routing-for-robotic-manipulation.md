---
source: arxiv
url: http://arxiv.org/abs/2603.07892v3
published_at: '2026-03-09T02:14:32'
authors:
- Yiteng Chen
- Zhe Cao
- Hongjia Ren
- Chenjie Yang
- Wenbo Li
- Shiyi Wang
- Yemin Wang
- Li Zhang
- Yanming Shao
- Zhenjun Zhao
- Huiping Zhuang
- Qingyao Wu
topics:
- robotic-manipulation
- policy-routing
- training-free
- multi-agent-system
- retrieval-augmented
relevance_score: 0.32
run_id: materialize-outputs
---

# RoboRouter: Training-Free Policy Routing for Robotic Manipulation

## Summary
RoboRouter提出一种**无需训练**的机器人操作策略路由框架：不再追求单一万能策略，而是在已有异构策略池中为每个任务自动挑选最合适的策略。它通过检索相似历史执行记录并结合结构化反馈持续更新，从而在仿真和真实机器人上稳定超过单一策略。

## Problem
- 机器人操作领域已有VLA、VA、代码组合等多类策略，但各自只在部分任务分布上表现强，跨任务与分布外泛化有限。
- 现实中不断有新策略出现，如果每次都重新训练一个总控路由器，成本高、适配慢，也不利于持续扩展。
- 因此关键问题是：**如何在不做额外训练、也不逐个试错执行所有候选策略的前提下，为当前任务选到最可能成功的策略**。

## Approach
- 构建一个由四个agent组成的训练免费框架：**Retriever、Router、Evaluator、Recorder**。
- 先把当前任务编码成多模态表示：结合语言指令、视觉观测，以及由视觉基础模型提取的任务元数据（如对象信息）。
- Retriever在历史执行数据库中检索相似任务记录，并重排候选；Router根据这些相似案例和各策略历史表现，直接预测当前该选哪个策略。
- Evaluator观看执行视频并结合规则指标（成功标志、时间、距离、接触/对齐等）生成结构化总结；Recorder把这些反馈写回数据库与路由上下文，形成在线改进闭环。
- 新策略接入时，只需在少量代表任务上做轻量评估并写入记忆，无需重新训练整个系统。

## Results
- **仿真（RoboTwin 2.0）**：在20个代表任务、每任务100次试验上，RoboRouter平均成功率达到 **79.85%**，优于所有单一基线：ACT **55.90%**、DP **51.05%**、DP3 **76.45%**、RDT **60.35%**、π0 **69.90%**、Code as Policies **54.45%**。
- 按论文摘要与正文表述，RoboRouter在仿真中的平均成功率相对最佳单一策略提升**超过3个百分点**；从表1看，相比最佳平均基线DP3（**76.45%**），提升约 **3.40 个百分点**。
- **真实世界**：在5个代表任务、每任务20次重复试验上，RoboRouter平均成功率为 **47%**，高于ACT **26%**、DP **18%**、RDT **33%**、π0 **34%**；相对最佳单一基线π0提升 **13 个百分点**。
- 真实任务细项中，RoboRouter在**Click Alarmclock**上达到 **10/20**，高于最佳基线 **8/20**；在**Open Laptop**上为 **9/20**，高于最佳基线 **8/20**；在**Place Container Plate**上与最佳基线持平，为 **12/20**。
- 论文还声称路由带来的额外时延较小、相对整体执行时间可忽略，但给定摘录中的时间表被截断，**未提供完整可核对的具体时延数字**。

## Link
- [http://arxiv.org/abs/2603.07892v3](http://arxiv.org/abs/2603.07892v3)
