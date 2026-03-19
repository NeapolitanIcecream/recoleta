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
- robot-manipulation
- policy-routing
- training-free
- vision-language-action
- multi-agent-systems
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# RoboRouter: Training-Free Policy Routing for Robotic Manipulation

## Summary
RoboRouter提出一种**免训练**的机器人策略路由框架，不再追求单一通用策略，而是为每个操作任务从现有异构策略池中选择更合适的策略。其核心思想是利用历史执行经验、相似任务检索和执行后反馈，在仿真与真实机器人上稳定超过单个策略。

## Problem
- 机器人操作领域已有VLA、VA、代码式组合等多类策略，但**各自在特定任务上强、跨任务泛化弱**，没有单一方法能全面胜出。
- 如果每次都运行所有候选策略再试错，代价太高；而为路由器再训练一个新模型，又会带来**数据、训练和持续集成新策略**的成本。
- 这个问题重要，因为机器人系统正在快速积累大量现成策略；若不能高效组合这些“专家”，系统能力和可扩展性都会受限。

## Approach
- 维护一个**异构策略池**和一个**历史执行数据库**；面对新任务时，不重新训练，而是先构建任务的多模态表示（指令、图像、视觉模型抽取的元数据）。
- 通过向量检索找到**相似历史任务**，再由LLM式Router根据这些记录和各策略的总体表现，直接预测当前最可能成功的策略。
- 执行后，VLM式Evaluator读取视频帧与规则化指标（成功标志、耗时、距离、接触/对齐等），生成结构化反馈；Recorder把这些信息写回数据库和路由上下文，形成**在线闭环改进**。
- 新策略接入时，只需在少量代表性任务上做**轻量评估**并写入记忆，无需额外训练；任务聚类进一步减少了评测开销。

## Results
- **仿真（RoboTwin 2.0）**：在20个代表任务、每任务100次试验上，RoboRouter平均成功率**79.85%**，高于所有单一基线：ACT **55.90%**、DP **51.05%**、DP3 **76.45%**、RDT **60.35%**、\(\pi_0\) **69.90%**、Code as Policies **54.45%**。
- 按论文摘要，RoboRouter相对单一策略在仿真中平均成功率提升**超过3%**；从表1看，相对最强单一平均基线DP3（**76.45%**），提升约**3.40个百分点**。
- **真实机器人**：5个任务、每任务20次试验，RoboRouter平均成功率**47%**，高于ACT **26%**、DP **18%**、RDT **33%**、\(\pi_0\) **34%**。
- 按论文摘要，真实环境平均成功率提升**超过13%**；从表2看，相对最强单一平均基线\(\pi_0\)（**34%**），提升约**13个百分点**。
- 具体真实任务示例：Click Alarmclock上RoboRouter **10/20**，优于RDT **8/20** 和 \(\pi_0\) **8/20**；Open Laptop上RoboRouter **9/20**，优于最佳单一基线 **8/20**；Place Container Plate上RoboRouter **12/20**，与最佳基线持平。
- 论文还声称路由带来的额外时延较小、执行效率基本保持，但给定摘录中的时间表格被截断，**未提供完整可核对的具体数值**。

## Link
- [http://arxiv.org/abs/2603.07892v3](http://arxiv.org/abs/2603.07892v3)
