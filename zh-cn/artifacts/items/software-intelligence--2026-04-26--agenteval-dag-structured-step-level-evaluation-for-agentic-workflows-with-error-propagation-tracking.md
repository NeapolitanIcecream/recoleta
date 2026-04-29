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
## 概要
AgentEval 通过对 DAG 中的每一步打分，并追踪前序错误如何导致后续失败，来评估多步骤 AI agent 工作流。它面向生产环境中的调试和回归测试，因为端到端检查会漏掉大多数可处理的失败。

## 问题
- 多步骤 agent 会在中间的规划、工具选择、参数生成、执行和综合步骤中出错，但端到端评估只能看到最终输出。
- 在真实工作流中，很多失败是由更早的步骤传播而来，因此团队需要知道错误从哪里开始，而不只是知道最终答案不好。
- 生产团队还需要在 CI/CD 中持续检测回归，而临时的轨迹检查无法扩展到这一需求。

## 方法
- 论文将每次 agent 运行建模为一个评估 DAG，其中节点是工作流步骤，边表示步骤之间的依赖关系。
- 每种步骤类型都有各自的质量指标：规划、工具选择、参数生成、执行和综合。经过校准的 GPT-4o 评审器使用局部上下文和可选参考，按照 15 的评分标准对每一步打分。
- 如果某一步失败，AgentEval 会根据一个 3 层、21 个子类的分类体系分配失败标签，该体系基于 523 条独立的 agent 轨迹构建。
- 根因归因使用一条简单规则：如果某个失败步骤依赖于更早失败的父节点，则将得分最低的父节点视为来源；否则将该步骤标记为根因。
- 该系统支持按 schema 定义和从轨迹推断的 DAG，通过循环展开和基于时间戳的分支解析处理大多数非 DAG 轨迹，并可接入 CI/CD 用于回归测试。

## 结果
- 在 150 个由人工标注的测试用例上，AgentEval 的失败检测召回率达到 0.89，而端到端评估为 0.41，平面步骤评估为 0.67。这比端到端高 2.17 倍，比平面步骤评估高 22 个百分点。
- 在相同设置下，与人工的一致性达到 Cohens kappa = 0.84，平面步骤评估为 0.71，端到端评估为 0.52。
- 根因准确率为 0.72，平面步骤评估为 0.38，人工上限为 0.81。在消融实验中，移除 DAG 结构会使根因准确率下降 34 个百分点，失败检测召回率下降 22 个百分点。
- 在全部 450 个测试用例中，63% 的步骤级失败是由上游错误传播造成的。非 DAG 轨迹约占 12%；在这些用例上，AgentEval 的失败检测召回率仍有 0.82，根因准确率为 0.58。
- 在不修改分类体系和评分标准的跨系统测试中，失败检测召回率在 -bench 零售和航空场景上分别保持在 0.83 和 0.79，在 SWE-bench 代码编辑上为 0.78。对应设置下的根因准确率分别降至 0.61、0.55 和 0.52。
- 在一项为期 4 个月、18 名工程师参与的试点中，该系统检测出 23 个发布前回归，将根因识别时间中位数从 4.2 小时缩短到 22 分钟，并且回归检测器在 18 组模拟场景-工作流组合上的精确率达到 88%，召回率达到 94%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23581v1](http://arxiv.org/abs/2604.23581v1)
