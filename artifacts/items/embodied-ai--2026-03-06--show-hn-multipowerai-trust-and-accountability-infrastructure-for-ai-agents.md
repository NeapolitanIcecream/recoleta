---
source: hn
url: https://multipowerai-trust.vercel.app
published_at: '2026-03-06T23:24:31'
authors:
- rogergrubb
topics:
- ai-agents
- agent-trust
- audit-trail
- access-control
- agent-commerce
relevance_score: 0.08
run_id: materialize-outputs
---

# Show HN: MultiPowerAI – Trust and accountability infrastructure for AI agents

## Summary
这不是一篇学术论文，而是一份面向市场的产品/基础设施说明，提出为 AI agents 提供“信任与问责层”。其核心主张是：在代理具备支付、采购和跨代理协作能力后，必须补上身份、权限、审计与风控基础设施。

## Problem
- 解决的问题：当前 AI agents 已能执行真实世界高风险操作（花钱、发邮件、采购、雇佣其他代理），但通常**没有可验证身份、授权证明、完整审计链和事故追责机制**。
- 这很重要，因为一旦出现提示注入、权限滥用、账户被盗用或多代理协作失控，部署方往往**无法证明发生了什么、是否被授权、由哪个 agent 导致**，进而带来安全、合规与商业责任风险。
- 多代理系统（如 LangGraph、CrewAI、AutoGen）进一步放大问题：缺少统一账本、收据和责任边界，使跨 agent 交易与协作难以在企业环境中可信落地。

## Approach
- 核心方法很简单：给每个 agent 加上一层**“数字身份 + 权限控制 + 交易账本 + 风险监控”**，让 agent 的每个动作都能被验证、限制和追踪。
- 为每个 agent 分配**加密身份**、信任分数（0–100）和可配置权限边界，例如可花多少钱、允许执行哪些动作、哪些动作永远禁止。
- 所有交易和动作都进行**签名、时间戳记录和不可篡改日志存证**，形成从首次调用到最终结果的完整审计链；还支持 agent-to-agent 调用、托管/结算与可验证“收据”。
- 加入**实时行为监控与熔断机制**：检测异常支出、异常 endpoint、异常时间模式；发现越界、可疑或被攻陷迹象时自动暂停并告警。
- 对高风险操作提供**人工审批、多签/仲裁和技能市场验证**等机制，并通过聚合多模型输出来辅助高风险决策。

## Results
- 文本**没有提供正式实验、公开数据集评测、统计显著性分析或与基线方法的严格对比结果**，因此没有可核验的学术量化突破。
- 最明确的产品级数字声明包括：**商户验证延迟低于 200ms**、agent **动态信任分数为 0–100**、技能市场当前有 **12 个 live skills**、创作者可获得 **80%** 销售分成。
- 提供了价格层级：**Free $0、Pro $49/mo、Enterprise Custom**；示例代码中展示了给 agent 充值 **5000（即 $50.00）** 并执行一次已记录的交易。
- 强具体功能性主张包括：每个动作都可**加密签名、时间戳记录、不可变审计**；支持**自动暂停异常 agent**、**高风险动作人工确认**、**agent 间托管支付**、**多签批准**与**跨模型聚合决策**。
- 如果按“创新突破”而非“实验结果”理解，最大卖点是把支付/权限/身份/审计/风控/市场整合到同一 agent 基础设施层，但这仍是**产品宣称**，而非论文实证结论。

## Link
- [https://multipowerai-trust.vercel.app](https://multipowerai-trust.vercel.app)
