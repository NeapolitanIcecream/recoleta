---
kind: ideas
granularity: day
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent systems
- coding agents
- software engineering
- monitoring
- code review
- requirements engineering
tags:
- recoleta/ideas
- topic/agent-systems
- topic/coding-agents
- topic/software-engineering
- topic/monitoring
- topic/code-review
- topic/requirements-engineering
language_code: zh-CN
---

# 代理可靠性工程接口

## 摘要
代理可靠性工作正在进入日常工程界面：编译器输出、监控队列、IDE 评审流程和操作前门控。最实用的改动足够小，可以先在一个语言工具链、一个受监管的代理工作流或一条代码评审路径里试点。

## 面向代理的编译器诊断，用于类型化修复循环
编译器和类型检查器团队应该增加一种面向代理的诊断模式，把完整的修复上下文发给编码代理，同时保留给开发者的简洁信息。Type-Error Ablation 研究在 Shplait 中直接测试了这一点：2,400 次 qwen2.5-coder:14b 修复试验比较了完整的统一栈输出、接近错误位置、最少类型错误信息和无类型测试套件反馈。更丰富的类型诊断改善了修复表现，97.9% 的修复在消除类型错误后也通过了语义测试。

一个成本低的试点是在有类型的语言服务器或 CI 修复流程里加一个功能开关。当代理是使用方时，工具可以在结构化工件里加入完整约束追踪、推断类型、候选来源位置和失败测试摘要。团队可以把最近的类型失败分别走一遍当前诊断模式和面向代理的模式，然后比较修复率、语义测试通过率和编辑尝试次数。对已经让代理读取编译器输出并修改代码的团队来说，这是一项具体的工具链改动。

### 资料来源
- [Type-Error Ablation and AI Coding Agents](../Inbox/2026-06-01--type-error-ablation-and-ai-coding-agents.md): Summarizes the Shplait experiment, diagnostic modes, 2,400 qwen2.5-coder trials, and the 97.9% semantic-test result.
- [Type-Error Ablation and AI Coding Agents](../Inbox/2026-06-01--type-error-ablation-and-ai-coding-agents.md): States the controlled comparison between unification-stack context, proximate location, minimal type error, and dynamic test feedback.
- [Type-Error Ablation and AI Coding Agents](../Inbox/2026-06-01--type-error-ablation-and-ai-coding-agents.md): States the primary experiment scale and the authors’ recommendation to consider separate human and AI reporting modes.

## 带严重性分流的结构监控，适用于文档密集型代理
在审计、金融、医疗、法律或其他文档密集型流程里运行多阶段代理的团队，应该先测试结构监控，再调任务级准确率告警。监控研究发现，集成缺陷会遮蔽任务级信号：单次运行内监控发现了 CV = 0.02 的确定性阶段缺陷，跨运行监控发现了 CV = 1.25 的波动性失败，结构监控则发现了 CV = 0.00 的集成缺口。它的分流方法把 97% 的发现送去自动跟踪，约 2% 送去人工调查。

这个做法本质上是一个带三种作用范围的评估层：单次运行内检查、重复运行的方差检查，以及对缺失或断开的阶段连接做明确检查。发现结果应带有严重性标签，用来决定进入分析师队列还是自动跟踪。试点可以把一小批真实或合成案例重新送入当前代理，测出多少告警是确定性的低严重度缺陷，多少会在不同运行之间波动，以及严重性分流减少了多少人工复核量。

### 资料来源
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md): Describes the three monitoring scopes, variance signal, FMEA-style severity routing, synthetic audit-agent testbed, and 43x review-volume reduction.
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md): Gives the paper’s claim that structural defects dominate early production agent failures and describes the monitoring and triage method.
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md): Reports that task-level errors were indistinguishable from clean baselines and that deterministic triage routed 97% of findings to automated tracking.

## 面向 LLM 生成多文件改动的风险排序 IDE 评审流程
IDE 团队和开发工具团队应该为 LLM 生成的多文件改动加一条评审路径：先给出改动概览，按风险给文件排序，再把评审者引导到高风险片段。JetBrains 的参与式设计研究发现，实践者把信任校准看作评审中的核心问题。它提出的流程有三个层级：概览、文件分析和代码片段评审，并使用了 risk-per-file、risk-per-line、judge、walk-through、zooming in/out 和 security cage 等构件。

第一版可以是一个 pull request 或 IDE 扩展，把代理动作日志、测试结果、变更文件元数据、所有权数据和静态分析警告合成一个文件风险分数。评审者仍然要看代码，但这个工具可以通过标出代理碰到敏感代码、跨过模块边界或改动安全相关路径的位置，让大规模生成改动没那么难看懂。下一步应该做一项受控评审任务，和普通 diff 视图对比缺陷发现率、评审时间和评审者信心。

### 资料来源
- [Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes](../Inbox/2026-06-01--trust-calibrated-code-review-a-participatory-design-study-of-review-workflows-for-llm-generated-multi-file-changes.md): Summarizes the trust-calibrated review problem, the three-level workflow, design constructs, validation survey, and evidence limits.
- [Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes](../Inbox/2026-06-01--trust-calibrated-code-review-a-participatory-design-study-of-review-workflows-for-llm-generated-multi-file-changes.md): States the JetBrains study method, the N=43 prototype evaluation, and the workflow constructs including risk-per-line and risk-per-file.
