---
source: arxiv
url: https://arxiv.org/abs/2607.06101v1
published_at: '2026-07-07T10:14:44'
authors:
- Rohit Mehra
- Samdyuti Suri
- Prithviraj K Tagadinamani
- Kapil Singi
- Vikrant Kaulgud
- Adam P. Burden
topics:
- ai-coding-agents
- software-engineering-education
- developer-tools
- human-ai-interaction
- multi-agent-systems
- knowledge-debt
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Agents That Teach: Towards Designing Incidental Learning Back into AI-Assisted Software Development

## Summary
## 摘要
论文认为，AI 编码代理可能减少开发者的偶然学习；当代理完成的代码变更无法被开发者解释时，会形成 Knowledge Debt。论文提出 SHIELD，这是一个基于 VSCode 的多代理原型，可把代理的推理轨迹转化为有选择的学习提示和短课程。

## 问题
- AI 编码代理为开发者解决更多编码工作，可能拿走过去在日常工作中训练开发者的代码阅读、调试和设计推理过程。
- 论文把由此产生的缺口称为 Knowledge Debt：代理完成的变更不断积累，但开发者的理解没有同步增长，这可能影响后续调试、适配和维护。
- 论文的动机包括：据报告，目前提交代码中有 42% 由 AI 生成，预计到 2027 年将达到 65%；论文还引用了一项对照研究，其中使用 AI 辅助的开发者在后续理解测试中的得分低 17%。

## 方法
- 论文提出 6 条设计原则，用于在开发者与代理协作中加入偶然学习：上下文相关、基于实际内容、环境式、有选择、可适应、闭环。
- SHIELD 观察编码代理的遥测数据：代码变更、理由、考虑过的替代方案和置信度。
- Teachability Triage Agent 会把候选概念与每位开发者的 Concept Map 进行比较，并结合复杂度、新颖性和可迁移性等信号。
- Probe Generator 在 IDE 中提出异步问题，用来检查开发者是否已经理解该概念。
- 如果存在理解缺口，Microlearning Generator 会生成一段与实际代码变更绑定的短课程，随后 Knowledge Assessor 检查理解情况并更新 Concept Map。

## 结果
- 论文没有报告实证评估结果、用户研究指标或基准测试分数；论文称评估是未来工作。
- SHIELD 作为 VSCode 扩展实现，使用 CrewAI、Azure 后端服务、Neo4j 作为 Concept Map、GPT-5.1 承担代理角色，并接入 Claude Code instrumentation。
- 原型包括 5 个具名代理角色或组件：Telemetry Observer Agent、Learning Orchestrator、Teachability Triage Agent、Probe Generator Agent、Microlearning Generator Agent，另有 Knowledge Assessor Agent。
- 演示流程展示了 1 个具体任务：支付 API webhook 重试问题，Claude Code 将固定重试逻辑改为带抖动的指数退避，SHIELD 将该变更转化为探测问题、微学习条目和理解检查。
- 论文称早期利益相关方演示获得了正面反馈，但没有给出人数、研究设计或效应量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06101v1](https://arxiv.org/abs/2607.06101v1)
