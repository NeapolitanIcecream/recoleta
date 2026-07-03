---
source: arxiv
url: https://arxiv.org/abs/2607.01421v1
published_at: '2026-07-01T19:31:02'
authors:
- Laxmipriya Ganesh Iyer
topics:
- agentic-ai-governance
- engineering-management
- software-risk
- multi-agent-software-engineering
- human-ai-interaction
- ai-native-teams
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Risk Architecture for AI-Native Engineering Teams: An Organizational Framework for Agentic System Governance

## Summary
## 摘要
论文认为，工程经理需要一个团队层面的风险模型来管理智能体式 AI 系统，因为标准的软件所有权、测试和升级规则会漏掉由概率性自主智能体引发的故障。

## 问题
- 传统软件风险管理假设行为是确定性的、部署是离散的、组件所有权是清晰的；智能体式 AI 系统同时打破这三项假设。
- 现有 AI 治理工作覆盖 NIST AI RMF 和 ISO/IEC 42001 等政策规则，OWASP 智能体式 AI 指南等技术目录覆盖威胁；它们没有告诉工程经理谁负责检测、回滚或升级。
- 论文将跨团队边界视为关键风险点，尤其是在确定性的下游系统把概率性 AI 输出当作精确结果使用时。

## 方法
- 论文定义了一个 7 维团队画像：输出确定性、动作自主性、验证模型、风险所有权、升级触发器、数据表面和变更速度。
- 论文比较了 3 类团队：纯软件工程团队、混合团队和 AI 原生团队。
- 论文构建了一个 6 簇故障分类法：安全、隐私、自主性、变更引发的故障、所有权/问责，以及依赖边界确定性不匹配。
- 论文通过评分来综合评估风险覆盖：判断每种团队画像能否检测、控制并升级一个已定义场景集，其中包括一个双团队生产者-消费者边界案例。
- 论文用公开事件为场景簇提供依据，包括 Microsoft 365 Copilot EchoLeak、OpenAI 2023 年 3 月的聊天标题和支付数据漏洞、Replit 被报告的生产数据库删除事件、Air Canada 聊天机器人案例，以及澳大利亚 Robodebt 案例。

## 结果
- 摘录没有给出检测、控制或升级覆盖率的具体分数；论文称其结论来自综合充分性测试，而非对团队行为的观察。
- 论文称，团队从 3 种画像迁移时，覆盖率会下降：纯软件工程、混合、AI 原生运营。
- 论文声称的主要缺口出现在 AI 原生阶段：只有在这一阶段才会出现未覆盖的高后果故障，组织边界处的覆盖最差。
- 论文识别了 6 个簇中的 20 个场景，其中 5 个场景属于依赖边界确定性不匹配。
- 公开依据包括 EchoLeak，Microsoft CNA 给出的 CVSS 为 9.3，NVD 给出的 CVSS 为 7.5；OpenAI 2023 年 3 月的暴露事件影响约 1.2% 的 Plus 订阅用户；Robodebt 追缴了约 17.6 亿美元的非法债务。
- 具体的管理产出是一个最小风险分配模型：为工具契约、因果动作链和跨团队边界指定负责人；添加语义升级触发器；并赋予团队执行非对称回滚和对账的权限。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01421v1](https://arxiv.org/abs/2607.01421v1)
