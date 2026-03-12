---
source: hn
url: https://multipowerai-trust.vercel.app
published_at: '2026-03-06T23:24:31'
authors:
- rogergrubb
topics:
- ai-agents
- trust-infrastructure
- auditability
- agent-commerce
- human-in-the-loop
relevance_score: 0.88
run_id: materialize-outputs
---

# Show HN: MultiPowerAI – Trust and accountability infrastructure for AI agents

## Summary
MultiPowerAI提出一套面向AI代理的“信任与问责基础设施”，目标是在代理具备支付、调用工具、雇佣其他代理等真实执行能力时，为其补上身份、审计和风险控制层。它更像一个产品/平台方案而非学术论文，重点是让代理行为可验证、可追责、可中止。

## Problem
- 现有AI代理已经能花钱、发邮件、执行交易，但通常缺少**身份认证、授权边界和责任归属**，一旦出错很难证明“谁做了什么、是否被授权”。
- 多代理协作场景中，代理之间的调用、采购和委托缺少**统一账本、收据和审计链**，事后往往只能靠日志重建，可靠性差。
- 提示注入、恶意输入、模型漂移或账号滥用会让代理越权行动；若没有**实时监控、暂停开关和人工审批**，损失会迅速扩大。

## Approach
- 为每个代理分配**可验证的加密身份**、密钥、钱包和权限策略，形成基础身份层与授权边界。
- 所有代理动作和交易都进行**签名、时间戳记录和加密审计**，生成从首次调用到最终结果的完整可证明审计链。
- 引入**动态信任分数（0–100）**与行为画像，监测异常模式，如花费暴增、访问陌生端点、异常时段操作，并支持自动暂停。
- 对高风险操作提供**人工在环审批**、多签/法定人数批准，以及代理间交易的**托管结算**，降低高价值动作的执行风险。
- 提供**已验证技能市场**与多模型聚合查询接口，使代理在受控、可记录的环境中发现能力、购买服务并做更稳健决策。

## Results
- 文中给出的最明确量化能力是**商户验证延迟低于200ms**（sub-200ms merchant verification）。
- 平台宣称提供**动态信任分数0–100**，用于持续评估代理状态与可信度。
- 技能市场当前宣称有**12个在线技能**，覆盖finance、coding、research、security等类别。
- 多模型查询接口宣称可**一次调用并行查询5个模型**（Claude、GPT、Gemini、DeepSeek及一个综合结果流程），再生成加权综合答案。
- 商业分成上，平台称技能发布者可获得**80%销售收入**。
- 没有提供标准学术基准、对照实验或公开数据集结果；最强的具体主张是：提供低延迟验证、全链路加密审计、异常检测自动暂停，以及代理间托管与多签治理能力。

## Link
- [https://multipowerai-trust.vercel.app](https://multipowerai-trust.vercel.app)
