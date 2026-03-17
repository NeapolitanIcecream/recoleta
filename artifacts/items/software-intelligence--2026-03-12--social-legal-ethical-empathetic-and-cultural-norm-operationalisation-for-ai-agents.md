---
source: arxiv
url: http://arxiv.org/abs/2603.11864v1
published_at: '2026-03-12T12:37:39'
authors:
- Radu Calinescu
- Ana Cavalcanti
- Marsha Chechik
- Lina Marsso
- Beverley Townsend
topics:
- ai-governance
- ai-agents
- formal-verification
- requirements-engineering
- norm-alignment
relevance_score: 0.38
run_id: materialize-outputs
---

# Social, Legal, Ethical, Empathetic and Cultural Norm Operationalisation for AI Agents

## Summary
本文提出一套把社会、法律、伦理、共情与文化（SLEEC）高层规范，系统化转换为可验证 AI 代理要求的工程流程。它更像是一篇框架与议程论文，重点在于定义流程、工具链与未解决挑战，而非报告新的模型性能基准。

## Problem
- 论文要解决的问题是：如何把 OECD、UNESCO、法规与行业准则中的抽象规范，转化为具体、可实现、可验证的 AI 代理要求；这很重要，因为医疗、执法、护理机器人等高风险场景中的代理会做出影响生命、安全、隐私与自主性的决策。
- 传统需求工程方法不适合此任务，因为它们难以处理多方利益相关者、抽象价值原则、规范冲突，以及对“是否合规”的形式化保证。
- 如果不能把高层价值落实为明确规则并验证，AI 代理即使功能可用，也无法被证明与人类规范和价值一致。

## Approach
- 核心方法是一个 **5 阶段 SLEEC 规范操作化流程**：先定义代理能力，再从高层原则中抽取可执行规范要求，随后检查规则集是否良构，再把规则映射到训练与运行时机制，最后验证代理是否遵守这些规则。
- 在最简单的层面上，它把“应当尊重隐私/自主/安全”这类抽象话，变成类似“当发生 X 且条件 Y 成立时，代理必须在 T 时间内执行 Z；除非出现例外条件 D”这样的形式化规则。
- 论文采用 **SLEEC DSL** 表达规则，并用两类形式化分析互补检查：一类基于 process algebra / tock-CSP + FDR，检测冲突与冗余；另一类基于 FOL* + LEGOS，分析整个规则集的全局充分性与过度限制性。
- 在实现层面，已验证的规则会被下沉为可观测事件、测量变量、状态与动作，同时用于训练数据模式设计和部署时的 runtime guardrails，以约束代理决策并支持后续规范更新。
- 论文用 ALMI 护理机器人作为贯穿案例，展示如何从能力、规则到调试修正规范要求。

## Results
- 论文**没有提供标准机器学习基准上的定量性能结果**，也没有报告诸如准确率、F1、胜率或大规模对比实验数字。
- 明确的结构性结果是提出了一个 **5-stage** 操作化流程：能力规格、规范需求引出、良构性检查、SLEEC-aware 实现、合规验证；并声明任何阶段失败都应阻止部署。
- 论文给出 ALMI 机器人示例规则中的**时间约束数字**：如 `MealTime -> InformUser within 10 minutes`，`SmokeDetectorAlarm -> CallEmergencySupport within 2 minutes`，`HumanOnFloor -> CallEmergencySupport within 4 minutes`。
- 论文展示了一个具体冲突修复：原规则中对紧急呼叫的禁止窗口会与火警场景冲突，因此将相关 defeater 的禁止时长从 **3 分钟缩短到 1 分钟** 以解除冲突。
- 论文还展示了一个“过度限制”修复：为避免“无响应跌倒者无法同意而导致永远不能呼救”，引入新的 `userResponsive` 能力，并将禁止条件细化为“**not humanAssents 且 userResponsive**”时才阻止呼救。
- 最强的论文主张是：通过 DSL、FDR、LEGOS、SLEEC-TK、LLM-guided debugging 等工具组合，可以把抽象 SLEEC 原则转化为**可检查、可调试、可实现、可验证**的 AI 代理规范，并形成未来研究与政策议程。

## Link
- [http://arxiv.org/abs/2603.11864v1](http://arxiv.org/abs/2603.11864v1)
