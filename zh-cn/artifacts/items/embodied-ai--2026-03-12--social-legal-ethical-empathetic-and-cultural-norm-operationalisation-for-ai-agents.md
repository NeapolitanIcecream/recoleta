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
- normative-reasoning
- formal-verification
- requirements-engineering
- responsible-ai
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Social, Legal, Ethical, Empathetic and Cultural Norm Operationalisation for AI Agents

## Summary
本文提出一个将社会、法律、伦理、共情与文化（SLEEC）高层规范系统化落地到 AI 代理中的工程流程。核心贡献是把抽象原则转成可验证的规则、实现约束与验证步骤，并梳理现有工具与未解挑战。

## Problem
- 高风险 AI 代理（如医疗、执法、护理机器人）需要遵守社会、法律、伦理、共情与文化规范，但现有框架多停留在“应当公平/尊重隐私”等抽象层面。
- 抽象原则难以直接转化为**具体、无歧义、可实现、可验证**的系统需求，因此难以证明代理真的符合人类规范与价值。
- 传统需求工程不足以处理多利益相关方参与、规范冲突、上下文依赖以及形式化合规保证等问题。

## Approach
- 提出一个 **5 阶段 SLEEC-norm operationalisation process**：能力规格定义、规范需求 elicitation、规则良构性检查、SLEEC-aware 实现、合规验证；任一阶段失败都应阻止部署。
- 用利益相关方参与的方法，把高层原则映射为可操作的“代理指标/proxies”，再绑定到代理能力上，最终写成 SLEEC DSL 规则：`when trigger [and guard] then response [within time]`，并支持 `unless` defeater 表达例外。
- 对规则集做形式化检查：一条路线将规则映射到 tock-CSP 并用 FDR / SLEEC-TK 检查冲突与冗余；另一条路线把整体规则集编码到 FOL* 并用 LEGOS / LEGOS-SLEEC 分析冲突、冗余、**insufficiency** 与 **over-restrictiveness**。
- 在实现阶段，将经验证规则映射到可观测事件、监测量、内部状态和可控动作；同时进入训练数据模式与运行时 guardrails，使代理在学习时和部署时都受规范约束，并支持后续规范更新。

## Results
- 这篇论文主要是**框架/流程与综述性贡献**，给出的摘录中**没有标准机器学习基准上的定量实验指标**，也没有准确的总体性能数字。
- 文中给出一个辅助护理机器人 ALMI/TIAGo 的具体示例规则：如 `MealTime -> InformUser within 10 minutes`，`SmokeDetectorAlarm -> CallEmergencySupport within 2 minutes`，`HumanOnFloor -> CallEmergencySupport within 4 minutes`。
- 通过形式化检查，作者展示了一个**时间冲突**示例：当跌倒后因未获同意而禁止求助，与烟雾报警后需在 **2 分钟**内呼叫急救的规则发生冲突；一种修复方式是把禁止呼叫的持续窗口从 **3 分钟**缩短到 **1 分钟**。
- 通过全局规则分析，作者还发现一个**过度约束**问题：若用户失去响应能力，则“未同意”条件可能阻止必要求助；修复后规则要求同时满足“未同意且用户有响应”时才禁止在 **1 分钟**内呼叫，从而保留对无响应跌倒用户的求助能力。
- 论文的最强主张是：该流程能把高层治理原则系统性地转成**可追踪、可实现、可验证**的代理规范，并利用现有工具在部署前发现冲突、冗余、规则不足和过度限制等问题。

## Link
- [http://arxiv.org/abs/2603.11864v1](http://arxiv.org/abs/2603.11864v1)
