---
source: arxiv
url: http://arxiv.org/abs/2603.03018v1
published_at: '2026-03-03T14:13:39'
authors:
- Yuvraj Agrawal
topics:
- agentic-ai
- enterprise-telemetry
- mcp-tools
- deterministic-grounding
- registry-driven-architecture
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# REGAL: A Registry-Driven Architecture for Deterministic Grounding of Agentic AI in Enterprise Telemetry

## Summary
REGAL提出一种面向企业遥测的代理式AI落地架构：先用确定性数据管道把原始遥测压缩成可复现的语义化指标，再让LLM只通过注册表编译出的受控工具访问这些结果。其核心价值不在新学习算法，而在于把“语义定义、工具接口、治理策略”统一为可版本化的架构约束。

## Problem
- 企业工程遥测来自版本控制、CI/CD、缺陷跟踪和可观测平台，数据量大、异构且持续演化，直接把原始事件交给LLM会造成**上下文超载和高token成本**。
- 组织内部语义（如“P1”“回归”“候选发布”）是本地定义的；若仅靠概率式检索或RAG，模型容易**误解语义并产生幻觉**。
- 手写工具/API会随着schema和指标定义变化而**发生tool drift**，导致接口说明、实际执行与治理策略不一致，影响审计与合规。

## Approach
- 采用**确定性—概率性分离**：所有遥测先经可重放、幂等、版本化的Medallion ELT流程，从Bronze/Silver加工为面向AI消费的Gold语义工件；LLM只能消费这些工件，不能反向改变计算逻辑。
- 引入**metrics registry**作为单一事实源：在注册表中声明指标标识、语义说明、检索逻辑、平台范围、ACL与缓存策略。
- 通过**registry-driven compilation**自动把声明式指标定义编译成MCP工具，包括工具schema、描述、访问控制和缓存行为，从而把“interface-as-code”落到运行时。
- 通过**bounded action space**限制代理只能调用有限的、预编译的语义工具，而不是生成任意SQL或访问原始日志，以降低幻觉面和治理复杂度。
- 支持**pull + push**双路径：历史分析通过工具按时间窗拉取Gold指标；实时监控通过Gold层变更流触发告警和代理工作流，二者共享同一语义边界。

## Results
- 论文明确说明这是一项**系统架构与原型验证工作**，**没有报告标准基准数据集上的精确量化对比结果**，也**不提出新的学习算法**。
- 原型与案例研究声称验证了该架构在**可行性、延迟、token效率和治理性**上的价值；文中最具体的数字性表述是：在Gold工件**可放入内存**且**中等并发负载**下，聚合指标检索可保持**sub-second（亚秒级）**，命中缓存时响应**几乎即时**。
- 文中进一步声称，在上述原型场景中，**模型推理延迟而非数据检索延迟**成为端到端交互的主导部分，支持其“先确定性计算、后概率推理”的设计主张。
- 主要突破性主张不是SOTA指标，而是架构层面的：将**注册表作为单一事实源**、将**编译步骤作为工具一致性与治理执行机制**、并把**确定性Gold工件**作为LLM唯一输入边界，以缓解context overload、local semantics和tool drift三类企业落地痛点。

## Link
- [http://arxiv.org/abs/2603.03018v1](http://arxiv.org/abs/2603.03018v1)
