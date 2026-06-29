---
source: arxiv
url: https://arxiv.org/abs/2606.12320v1
published_at: '2026-06-10T16:54:47'
authors:
- Krti Tallam
topics:
- ai-agent-governance
- runtime-policy
- multi-agent-security
- capability-attenuation
- enterprise-ai
- auditability
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents

## Summary
## 摘要
论文提出了一种五平面运行时架构，用于治理通过企业工具和连接器执行操作的生产环境 AI 代理。它针对的是委托动作风险：单个被授权的步骤可以组合成未经授权的业务流程。

## 问题
- 企业安全工具主要检查数据流动或单次请求，而生产环境代理会生成会改变系统记录的多步计划。
- 标准策略引擎评估的是原子主体和布尔型允许/拒绝决策；代理系统需要对委托链和会话历史做有状态检查。
- 这一点很重要，因为被攻破或被误导的代理可以按顺序使用被允许的工具，导致数据外泄、越权，或修改业务流程。

## 方法
- 该架构把治理分成 5 个平面：1 个推理平面负责判断意图，外加 4 个执行平面，分别对应网络、身份、终端和数据。
- 推理平面会在动作到达基础设施前，检查代理计划、复合主体、委托链、能力集合和会话状态。
- Stop-anywhere mediation 在代理执行循环的 7 个位置插入检查，并支持 6 种中断原语：pause、escalate、narrow、modify、defer 和 rollback。
- 复合主体把委托链与衰减后的能力绑定起来；有效权限是链上所有未过期能力集合的交集。
- 审计记录采用结构化且可防篡改的形式，因此事件响应人员可以重建已做出的决定，以及每个平面如何执行。

## 结果
- 论文声称，在一个典型工作流和 4 个额外用例中，已经阻断了 7 类生产代理威胁，这些用例分别是金融服务、医疗、软件工程和客户运营。
- 论文提出了 4 条正确性不变式：组合权限、调解覆盖、受限的复合权限和证据充分性；这些内容从结构上进行了论证，摘录中没有给出形式化证明。
- 策略引擎核心的参考实现报告称，在每次试验中都满足了衰减正确性和证据可重建性；摘录没有给出试验次数。
- 报告称，裁决在策略引擎核心中的运行时间是个位数微秒。
- 报告称，审计底座的防篡改证据在参考实现中按设计工作。
- 论文没有报告在真实代理基准上的完整系统得分；它把这项评估列为后续工作。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12320v1](https://arxiv.org/abs/2606.12320v1)
