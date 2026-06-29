---
kind: trend
trend_doc_id: 1072
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
topics:
- agent reliability
- code generation
- runtime verification
- multi-agent systems
- code model calibration
run_id: materialize-outputs
aliases:
- recoleta-trend-1072
tags:
- recoleta/trend
- topic/agent-reliability
- topic/code-generation
- topic/runtime-verification
- topic/multi-agent-systems
- topic/code-model-calibration
language_code: zh-CN
---

# Agent reliability is an engineering control problem

## Overview
这一天最强的信号是运行时纪律。STORM、OpenComputer 和 DIFFCODEGEN 指向同一个要求：在团队信任更长的自主工作之前，代理需要最新状态、可执行检查，以及围绕模型输出的低成本验证。

## Clusters

### State and authority controls for agents
几篇工作都把大语言模型（LLM）代理看作受控运行时的一部分。STORM 会在代理读到过期文件后拒绝写入，然后返回新上下文，让代理重试。生产代理架构论文在工具边界上给出了同样的思路：模型提出方案，确定性代码做验证，接受的动作被提交，拒绝的动作会得到带类型的反馈。Capframe 用 Model Context Protocol（MCP）给出这个思路的具体版本，配合限定范围的能力令牌和对工具调用的确定性策略检查。

共同的问题很实际。并行代理会互相覆盖，或基于旧假设执行。使用工具的代理也可能拿到过多权限。这组工作里最强的方案，都在模型周围加了版本检查、提交规则、拒绝回执和审计记录。

#### Evidence
- [Multi-agent Collaboration with State Management](../Inbox/2026-05-19--multi-agent-collaboration-with-state-management.md): STORM uses shared workspace state, file version counters, stale-write rejection, and reports gains on Commit0-Lite and PaperBench.
- [A Methodology for Selecting and Composing Runtime Architecture Patterns for Production LLM Agents](../Inbox/2026-05-19--a-methodology-for-selecting-and-composing-runtime-architecture-patterns-for-production-llm-agents.md): The runtime architecture paper defines a proposer-verifier-commit-reject contract and audits failures at the model-to-action boundary.
- [Show HN: Capframe – capability tokens for AI agent tool calls](../Inbox/2026-05-19--show-hn-capframe-capability-tokens-for-ai-agent-tool-calls.md): Capframe maps MCP tool access, issues scoped capability tokens, and enforces deterministic runtime policy on tool calls.

### Verifiable agent evaluation
OpenComputer 和 AgentAtlas 都主张把评估放到最终成功分数之外。OpenComputer 构建了 1,000 个桌面任务，覆盖 33 个应用，并用和真实应用状态绑定的程序化检查来评分，包括浏览器配置文件、文件、数据库和已保存文档。这很重要，因为截图评分会漏掉隐藏的状态错误。

AgentAtlas 看的是轨迹本身。它给 Act、Ask、Refuse、Stop、Confirm 和 Recover 这类控制决策打标签，然后显示提示词格式和评估轴会改变模型排名。它的审计还发现，现有代理基准对记忆、状态和效率的覆盖都很弱。证据表明，代理评估需要任务结果，也需要轨迹级检查。

#### Evidence
- [OpenComputer: Verifiable Software Worlds for Computer-Use Agents](../Inbox/2026-05-19--opencomputer-verifiable-software-worlds-for-computer-use-agents.md): OpenComputer provides verifier-grounded desktop tasks, 33 applications, 1,000 tasks, and state-based scoring.
- [AgentAtlas: Beyond Outcome Leaderboards for LLM Agents](../Inbox/2026-05-19--agentatlas-beyond-outcome-leaderboards-for-llm-agents.md): AgentAtlas defines control and trajectory labels, audits 15 benchmarks, and reports axis-sensitive model rankings.

### Diagnostic feedback as an optimizer
optimize_anything 把基于 LLM 的搜索扩展成一个通用循环：编辑文本制品，给它打分，把诊断性侧信息传回给提出者，再试另一个候选项。同一个 API 被用在提示词、代码、代理结构、调度策略、CUDA 内核和数值求解器上。报告中的收益在评估器能返回有用侧信息时最强，比如轨迹、性能分析数据、成本或图像。

DIFFCODEGEN 把一种更窄的运行时证据用于代码选择。它采样多个候选程序，对输入做模糊测试，比较观察到的行为，对候选项聚类，然后返回最大行为组的 medoid。这样就避免了生成后的额外 LLM 调用，并且报告的时间和 token 使用量都远低于以前依赖公开测试或模型裁判的测试时选择方法。

#### Evidence
- [optimize_anything: A Universal API for Optimizing any Text Parameter](../Inbox/2026-05-19--optimize-anything-a-universal-api-for-optimizing-any-text-parameter.md): optimize_anything uses evaluator scores plus side_info diagnostics and reports gains across agent architecture search, scheduling, CUDA, prompts, and coding-agent skills.
- [Code Generation by Differential Test Time Scaling](../Inbox/2026-05-19--code-generation-by-differential-test-time-scaling.md): DIFFCODEGEN selects candidates using fuzzing and behavioral clustering, with reported time and token savings over prior test-time scaling methods.

### Selective code automation
两篇可靠性论文关注代码模型何时该行动。defer-and-recover 论文先校准正确性分数，接受阈值以上的输出，并把不确定案例送去验证或恢复步骤，比如编译器检查、静态分析、提示词增强和任务分解。结果显示，它在 MBPP+ 和缺陷预测上有更好的 Brier 分数和期望校准误差，但也指出，没有哪个不确定性指标能跨任务通用。

input-adaptation 论文测试的是另一个控制点。它会在推理时，当有效性分数很低时，改写或调整输入。早期结果在漏洞检测上最清楚：CodeBERT 经过潜在变换后，准确率从 63.36% 提高到 76.75%，而现有不确定性指标仍然是较弱的错误检测器。这个结论范围不大，但很实用：代码自动化需要针对任务的置信处理，而不是一个通用置信分数。

#### Evidence
- [When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions](../Inbox/2026-05-19--when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predictions.md): The defer-and-recover paper reports calibrated selective prediction and recovery paths for uncertain code outputs.
- [On-the-Fly Input Adaptation for Reliable Code Intelligence](../Inbox/2026-05-19--on-the-fly-input-adaptation-for-reliable-code-intelligence.md): The input-adaptation paper reports near-chance uncertainty metrics and accuracy gains from input or latent transformations on vulnerability detection.
