---
source: arxiv
url: http://arxiv.org/abs/2604.23581v1
published_at: '2026-04-26T07:38:47'
authors:
- Dongxin Guo
- Jikun Wu
- Siu Ming Yiu
topics:
- agent-evaluation
- workflow-debugging
- root-cause-analysis
- llm-as-judge
- software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking

## Summary
## 摘要
AgentEval 通过在 DAG 中给多步 AI agent 工作流的每一步打分，并追踪更早的错误如何导致后续失败，来评估这类系统。它面向生产调试和回归测试，因为端到端检查会漏掉大多数可操作的失败。

## 问题
- 多步 agent 会在规划、工具选择、参数生成、执行和综合这些中间步骤出错，但端到端评估只能看到最终输出。
- 在真实工作流里，很多失败都由更早的步骤传导而来，所以团队需要知道错误从哪里开始，而不只是知道最终答案不好。
- 生产团队还需要在 CI/CD 中持续做回归检测，而临时性的轨迹检查无法规模化提供这种能力。

## 方法
- 论文把每次 agent 运行建模成一个评估 DAG，其中节点是工作流步骤，边表示步骤之间的依赖关系。
- 每种步骤都有自己的质量指标：计划、工具选择、参数生成、执行和综合。经过校准的 GPT-4o 判定器使用局部上下文和可选参考，对每一步按 1–5 量表评分。
- 如果某一步失败，AgentEval 会根据一个 3 层、21 个子类的分类法给出失败标签，这个分类法基于 523 条独立 agent 轨迹构建。
- 根因归因使用一条简单规则：如果失败步骤依赖于更早失败的父节点，就把得分最低的父节点当作来源；否则把该步骤标记为根因。
- 系统支持由 schema 定义和从轨迹推断出来的 DAG，能通过循环展开和基于时间戳的分支解析处理大多数非 DAG 轨迹，并且可以接入 CI/CD 做回归测试。

## 结果
- 在 150 个人工标注测试样例上，AgentEval 的失败检测召回率达到 0.89，端到端评估为 0.41，扁平的步骤级评估为 0.67。相较端到端评估，召回率高 2.17 倍；相较扁平步骤级评估，高 22 个百分点。
- 在同一设置下，人工一致性达到 Cohen’s kappa = 0.84，扁平步骤级评估为 0.71，端到端评估为 0.52。
- 根因准确率为 0.72，而扁平步骤级评估为 0.38，人工上限为 0.81。在消融实验中，去掉 DAG 结构后，根因准确率下降 34 个百分点，失败检测召回率下降 22 个百分点。
- 在全部 450 个测试样例中，63% 的步骤级失败来自上游错误传导。非 DAG 轨迹约占 12%；在这些样例上，AgentEval 仍然给出 0.82 的失败检测召回率和 0.58 的根因准确率。
- 在不改分类法或评分规则的跨系统测试中，失败检测召回率在 -bench retail 和 airline 上分别为 0.83 和 0.79，在 SWE-bench 代码编辑上为 0.78。根因准确率在这些设置下分别降到 0.61、0.55 和 0.52。
- 在一个为期 4 个月、18 名工程师参与的试点中，系统检测到 23 个发布前回归， median 根因定位时间从 4.2 小时降到 22 分钟，回归检测器在 18 组模拟场景-工作流组合上的精度为 88%，召回率为 94%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23581v1](http://arxiv.org/abs/2604.23581v1)
