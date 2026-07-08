---
kind: trend
trend_doc_id: 1791
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
topics:
- coding agents
- software verification
- agentic code review
- trajectory diagnostics
- agent reliability
- developer learning
run_id: materialize-outputs
aliases:
- recoleta-trend-1791
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/agentic-code-review
- topic/trajectory-diagnostics
- topic/agent-reliability
- topic/developer-learning
language_code: zh-CN
---

# 代码智能体需要验证器、审查器和轨迹级修复

## Overview
当天的研究把代码智能体视为在工作过程中需要外部检查的系统。Aria 展示了由验证器把关的大规模证明搜索；SWE-Review 加入感知代码库的审查；TraceProbe 测量一次运行如何搜索、编辑和验证。当前重点是在工作流内部提供可靠性证据，最终任务分数只是多个信号之一。

## Clusters

### 由验证器把关的编码和证明生成
Aria 是这一时期最突出的结果。一个通用代码智能体编写 Coq 和 Lean 证明，验证框架会拒绝不可靠输出、被改动的引理、被丢弃的证明义务、发散的 tactic 和不安全的捷径。论文报告称，它覆盖了所有目标证明集：4,257 个 Iris 核心引理、217 个基于 Iris 构建的 Rust 库引理、318 个 reglang 定理，以及 72 个 Lean 移植引理。

SCOPE 将类似的控制模式用于普通代码生成。一个以证明器初始化的评论器识别草稿程序中缺失的语义义务，然后编码器按这些子目标修改代码。在 LiveCodeBench V6 上，pass@1 达到 39.4%，Reflexion 为 36.6%，仅编码器生成为 20.6%。增益最大的任务带有可以表述为子目标的具体约束。

#### Evidence
- [Harnessing Code Agents for Automatic Software Verification](../Inbox/2026-07-07--harnessing-code-agents-for-automatic-software-verification.md): Aria 摘要，包含验证框架设计，以及在 Coq、Iris、Rust、reglang 和 Lean 上报告的证明覆盖率。
- [SCOPE: Leveraging Subgoal Critiques for Code Generation](../Inbox/2026-07-07--scope-leveraging-subgoal-critiques-for-code-generation.md): SCOPE 摘要，包含用证明器训练的评论器设计和基准测试结果。

### 感知代码库的审查和运行诊断
SWE-Review 将代码审查纳入智能体循环。审查器可以检查代码库、运行命令、批准或要求修改，并给出修复指导。在 SWE-bench Verified 上，迭代式生成-审查-修改将 Qwen3-30B-A3B PR 的解决率提高到 56.9%，无审查基线为 27.5%。对于 Qwen3-Coder-30B-A3B，同一循环达到 68.8%，对比值为 50.9%。

TraceProbe 为代码智能体评估加入过程证据。它将原始轨迹转换为九类动作，并标注 failed、reverted、off-anchor、justified 等效果。在一个 SWE-Bench 示例中，两个智能体都完成了任务，但一个用 10 步完成且没有失败动作，另一个需要 49 步并多次经历恢复片段。这一区别会影响成本、审查负担和生产信任。

#### Evidence
- [SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review](../Inbox/2026-07-07--swe-review-closing-the-loop-on-issue-resolution-with-agentic-code-review.md): SWE-Review 摘要，包含基准构建、审查循环和解决率提升。
- [What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents](../Inbox/2026-07-07--what-resolve-rate-hides-trajectory-structure-diagnostics-for-coding-agents.md): TraceProbe 摘要，包含动作分类、反模式和 2,500 条轨迹研究。

### 智能体基础设施测试和运行时修复
LogicHunter 针对 LangChain、LlamaIndex 和 CrewAI 等智能体库中的故障。它从源代码、类型提示、模式、文档和代码库用法构建可执行种子测试，再将有效 API 调用变异为行为探针。它的智能体 oracle 在给故障打标签前，会检查文档、源代码、复现脚本和运行时状态。研究报告发现 40 个先前未知的 bug，其中 30 个得到确认，26 个已由开发者修复。

AgentTether 处理工具型智能体完成运行后的故障。它将一条轨迹转换为相互连接的 transition units，定位可疑子轨迹，并把修复指导带入下一次尝试。在使用 Qwen3.7-max 的 261 个 τ-bench 任务上，它修复了 69.11% 的初始失败任务，整体上比盲重试高 26.02 个百分点。

#### Evidence
- [LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle](../Inbox/2026-07-07--logichunter-testing-llm-agent-frameworks-with-an-agentic-oracle.md): LogicHunter 摘要，包含智能体库目标、智能体 oracle 和已确认 bug 数量。
- [AgentTether: Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation](../Inbox/2026-07-07--agenttether-graph-guided-diagnosis-and-runtime-intervention-for-reliable-llm-agent-operation.md): AgentTether 摘要，包含图引导诊断、受保护干预和修复率结果。

### IDE 内的开发者技能支持
智能体式编码中的人的部分出现在两个以 IDE 为中心的系统中。Prompt Coach 通过评分和与本地项目相关的苏格拉底式提问，训练开发者写出更好的代码生成提示。在一项包含 15 名开发者的研究中，一次 60 分钟会话将平均提示质量分数提高到 71.69，基线为 63.04。测得增益最大的方面是约束、错误处理和上下文意识。

SHIELD 的证据还不够成熟，但目标明确。它观察智能体的代码变更和推理轨迹，然后将选定概念转换为探针、短课和理解检查。论文报告了一个可运行的 VSCode 原型和一个 payment-webhook 演示，但没有用户研究结果或基准分数。

#### Evidence
- [Prompt Coach: An Empirical Evaluation of an Agentic Tutor for Learning Prompt Engineering in Software Development](../Inbox/2026-07-07--prompt-coach-an-empirical-evaluation-of-an-agentic-tutor-for-learning-prompt-engineering-in-software-development.md): Prompt Coach 摘要，包含 IDE 导师设计和前后测研究结果。
- [Agents That Teach: Towards Designing Incidental Learning Back into AI-Assisted Software Development](../Inbox/2026-07-07--agents-that-teach-towards-designing-incidental-learning-back-into-ai-assisted-software-development.md): SHIELD 摘要，包含知识债动机、原型组件和缺少实证结果。
