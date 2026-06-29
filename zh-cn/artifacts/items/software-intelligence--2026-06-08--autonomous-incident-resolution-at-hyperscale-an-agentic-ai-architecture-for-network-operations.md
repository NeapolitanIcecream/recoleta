---
source: arxiv
url: https://arxiv.org/abs/2606.09122v1
published_at: '2026-06-08T07:15:53'
authors:
- Arun Malik
topics:
- multi-agent-systems
- autonomous-remediation
- network-operations
- incident-response
- ai-safety
- agentic-ops
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Autonomous Incident Resolution at Hyperscale: An Agentic AI Architecture for Network Operations

## Summary
## 摘要
这篇论文介绍了一个用于处理超大规模云网络事件的生产级多智能体 AI 系统。它声称，对常见事件类型的自主处置率超过 90%，MTTR 从小时降到分钟。

## 问题
- 人工值班响应无法跟上拥有数百万设备、分布在数百个数据中心的云网络规模。
- 网络故障可能在几秒内级联，而人工诊断和修复通常需要几分钟到几小时。
- 运行知识往往掌握在资深工程师手里，这会拖慢响应，也让事件处理不一致。

## 方法
- 该系统把事件处理拆成四个智能体：接入、规划、执行和验证。
- 智能体使用从真实人工处置中整理出的结构化操作手册，包含明确的前置条件、步骤、成功检查和中止规则。
- 运维动作以类型化技能的形式暴露出来，带有明确的权限、schema、幂等性行为和审计日志。
- 安全控制在执行前后检查授权、影响范围、冗余、速率限制、回滚路径和动作后的健康状态。
- 自主性按 0 到 4 级提升，从建议模式到自我改进行为；当失败率上升时，会降级并触发断路器。

## 结果
- 在一家大型云服务商的生产环境中，该系统声称，对理解较清楚的事件类别，自主处置率超过 90%。
- 对于由系统自主处理的事件，MTTR 相比人工响应提升了两个数量级，从小时降到分钟。
- 报告中的误报修复率低于 5%，这些情况没有带来客户可见影响。
- 论文报告没有因自主动作引发的严重事件，并称没有任何动作超出其预测的影响范围。
- 自动回滚出现在少量执行尝试中，而且都在定义的时间范围内恢复。
- 摘要没有提供原始事件数量、数据集细节、置信区间，或按类别划分的评估表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09122v1](https://arxiv.org/abs/2606.09122v1)
