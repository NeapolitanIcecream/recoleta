---
kind: trend
trend_doc_id: 161
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
topics:
- coding-agents
- software-engineering
- compiler-feedback
- software-architecture
- agent-control
run_id: materialize-outputs
aliases:
- recoleta-trend-161
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/compiler-feedback
- topic/software-architecture
- topic/agent-control
language_code: zh-CN
---

# 围绕控制闭环、编译器和架构检查的软件 agent 证据正在变得更扎实

## Overview
这一天的研究中，证据最扎实的是那些能被显式控制检查的软件 agent。依据最充分的工作把模型接到编译器、工单状态、验证器门控或经过基准测试的设计产物上。这让我们更清楚地看到 agent 现在能做什么，也看到可靠性仍会在哪里出问题，尤其是在架构理解上。

## Clusters

### Agent 工作正通过控制规则和架构约束来明确规定
面向生产的 agent 工作正在更明确地规定控制面。最有力的证据是一个由 Jira 支撑的闭环，它把 AI 限定在固定状态转换、置信度阈值、隔离 worktree 和验证器门控之内。在初始时间窗口中，该系统报告了 152 次运行，终态成功率为 100%，随后又积累了超过 795 个运行产物。另一篇架构论文提出了互补的一点：提示词措辞现在会改变系统本身的形态。在其案例研究中，同一个聊天机器人任务在提示词加入结构化输出和工具访问后，从 141 行代码和 2 个文件增长到 827 行代码和 6 个文件。共同点很直接：agent 能力正在与工作流规则、审查节点和架构意识一起打包，因为这些选择会影响最终构建出的内容以及系统运行的安全性。

#### Evidence
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): 确定性控制闭环、边界明确的自动化，以及已报告的生产结果。
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): 提示词措辞会改变架构规模和组件。

### 以编译器为依据的编码系统正在拿出更强的领域结果
编译器反馈正在成为让代码 agent 在更窄领域里变得实用的一种方法。ACCLAIM 把语言模型改写与常规编译器 pass 结合起来，覆盖 C 源码、LLVM IR 和汇编，并报告相对 clang -O3 平均 1.25× 的加速。在 COBOL 上，这一点更具体。COBOL-Coder 在 COBOLEval 上达到 73.95% 的编译成功率和 49.33 的 Pass@1，在论文报告的设定中明显高于 GPT-4o。随后，COBOLAssist 展示了生成之后修复闭环能带来的提升：当把编译器错误反馈给修订过程后，GPT-4o 的编译成功率从 41.8% 提升到 95.89%。实际结论是，面向特定领域的代码生成在模型接上编译器、测试和迭代修复时会表现更好，而不是只提示一次。

#### Evidence
- [Agentic Code Optimization via Compiler-LLM Cooperation](../Inbox/2026-04-05--agentic-code-optimization-via-compiler-llm-cooperation.md): 编译器与 LLM 协作进行优化，并报告了相对 clang -O3 的加速结果。
- [COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation](../Inbox/2026-04-05--cobol-coder-domain-adapted-large-language-models-for-cobol-code-generation-and-translation.md): 面向特定领域适配的 COBOL 模型在代码生成和翻译上取得了较强结果。
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): 编译器引导的修复闭环大幅提高了 COBOL 编译成功率。

### 架构推理仍弱于代码阶段辅助
设计阶段的理解仍然是多模态软件工具的弱点。SADU 在 154 张软件架构图和 2,431 个问答任务上测试视觉语言模型。报告中的最佳总体准确率是 70.18%，而一些常用模型要低得多，包括该基准中 gpt-4o-mini 的 17.77%。随着图变得更复杂，准确率还会继续下降，尤其是在行为图和关系密集的检索问题上。这一点很重要，因为 agent 系统已经在生成过程中做架构选择，但它们读取图示证据的能力仍然有限。这组语料指向了代码阶段辅助与设计阶段理解之间的缺口。

#### Evidence
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): 基准测试证据显示 VLM 在软件架构图上的能力较弱。
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): 架构决策已经出现在 coding-agent 工作流中。
