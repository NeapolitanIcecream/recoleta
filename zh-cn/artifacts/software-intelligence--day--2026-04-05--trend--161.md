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

# Software-agent evidence is getting tighter around control loops, compilers, and architecture checks

## 概览
这一天的研究最强的部分，是那些可以用明确控制来检查的软件代理。证据最扎实的工作把模型接到编译器、工单状态、校验器门控或经过基准测试的设计工件上。这让我们更清楚地看到代理现在能做什么，以及可靠性还会在哪些地方失效，尤其是在架构理解上。

## 研究发现

### Agent work is being specified through control rules and architecture constraints
面向生产的代理工作越来越明确地围绕控制面展开。最有力的证据来自一个基于 Jira 的闭环，它把 AI 限定在固定的状态转换、置信阈值、隔离工作树和校验器门控之内。系统在初始窗口报告了 152 次运行，终态成功率为 100%，之后又积累了 795 以上的运行产物。另一篇架构论文给出互补结论：提示词措辞现在会直接改变系统形态。在它的案例研究里，同一个聊天机器人任务在提示加入结构化输出和工具访问后，从 141 行、2 个文件增长到 827 行、6 个文件。共同点很直接：代理能力正在和工作流规则、审查点以及架构感知一起打包，因为这些选择会影响构建出来的东西，以及它运行得有多安全。

#### 资料来源
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): Deterministic control loop, bounded automation, and reported production results.
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): Prompt wording changes architecture size and components.

### Compiler-grounded coding systems are posting stronger domain results
编译器反馈正在成为让代码代理在更窄领域里发挥作用的一种实用方式。ACCLAIM 把语言模型重写和常规编译器 pass 结合起来，覆盖 C 源码、LLVM IR 和汇编，并报告相较 clang -O3 的平均 1.25× 加速。在 COBOL 里，这种取向更具体。COBOL-Coder 在 COBOLEval 上取得 73.95% 的编译成功率和 49.33 的 Pass@1，明显高于报告设定中的 GPT-4o。COBOLAssist 则展示了生成之后修复回路能带来的效果：当把编译错误回传给模型继续修改时，GPT-4o 的编译成功率从 41.8% 提升到 95.89%。实际含义很明确：把模型接到编译器、测试和迭代修复上，领域代码生成才会变得更好，而不是只提示一次就结束。

#### 资料来源
- [Agentic Code Optimization via Compiler-LLM Cooperation](../Inbox/2026-04-05--agentic-code-optimization-via-compiler-llm-cooperation.md): Compiler-LLM cooperation for optimization with reported speedup over clang -O3.
- [COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation](../Inbox/2026-04-05--cobol-coder-domain-adapted-large-language-models-for-cobol-code-generation-and-translation.md): Domain-adapted COBOL model with strong code generation and translation results.
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): Compiler-guided repair loop sharply raises COBOL compilation success.

### Architecture reasoning remains weaker than code-time assistance
在多模态软件工具里，设计阶段的理解仍然是短板。SADU 用 154 张软件架构图和 2,431 个问答任务测试视觉语言模型。报告中的最佳总体准确率是 70.18%，一些常用模型低得多，这个基准里 gpt-4o-mini 只有 17.77%。当图更复杂时，准确率还会继续下降，尤其是在行为图和关系密集的检索问题上。这个问题很重要，因为代理系统已经在生成阶段做架构选择，但它们读取图表证据的能力仍然有限。这个语料显示，代码阶段辅助和设计阶段理解之间还有明显差距。

#### 资料来源
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): Benchmark evidence on VLM weakness for software architecture diagrams.
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): Architecture decisions are already happening in coding-agent workflows.
