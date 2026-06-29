---
kind: trend
trend_doc_id: 1403
granularity: week
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-08T00:00:00'
topics:
- coding agents
- agent evaluation
- software engineering
- runtime governance
- trace-based training
- repository benchmarks
- AI safety
run_id: materialize-outputs
aliases:
- recoleta-trend-1403
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/runtime-governance
- topic/trace-based-training
- topic/repository-benchmarks
- topic/ai-safety
language_code: zh-CN
---

# 编码代理需要轨迹、关卡和支出控制，自主性才可信

## Overview
本周研究把大型语言模型（LLM）代理视为受控的软件工作者。最有力的工作要求提供轨迹、可执行检查、工具限制和审查关卡。Claude Code 说明这已经不只是基准测试问题：编码代理正在进入软件供应链。

## Clusters

### 运行时控制和操作关卡
可靠性工作集中在谁可以执行操作、代理能看到哪些上下文，以及哪些工具调用需要检查。6 月 1 日的趋势把代理可靠性同受管理的权限、诊断和审查路径联系起来。6 月 6 日的趋势把同一问题推到产品层面：可编辑上下文、受保护的桌面操作和支出控制，成为代理执行实际工作时的实际要求。这使控制界面成为代理设计的一部分，而不是部署后才补上的内容。

#### Evidence
- [Capability Advertisement as a Market for Lemons: A Trust Layer for Heterogeneous Agent Networks](../Inbox/2026-06-02--capability-advertisement-as-a-market-for-lemons-a-trust-layer-for-heterogeneous-agent-networks.md)
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md)
- [From Company Brain to an AI Operating System](../Inbox/2026-06-07--from-company-brain-to-an-ai-operating-system.md)
- [Declarative Skills for AI Agents in Knowledge-Grounded Tool-Use Workflows](../Inbox/2026-06-05--declarative-skills-for-ai-agents-in-knowledge-grounded-tool-use-workflows.md)
- [Context Sculpting](../Inbox/2026-06-06--context-sculpting.md)
- [Without Intelligent Guardrails, Claude Code Is Pure Chaos](../Inbox/2026-06-01--without-intelligent-guardrails-claude-code-is-pure-chaos.md)

### 轨迹衍生的训练和诊断
训练工作把代理轨迹当作不只是日志。EvoTrainer 会在训练分支失败或改进时调整诊断，使用 rollout、配置、日志和代码 diff 来决定保留、剪枝、回滚还是合并分支。Socratic-SWE 把仓库求解轨迹转成可复用的修复技能，然后生成由执行结果检查的定向任务。报告的提升很具体：EvoTrainer 将 SWE-9B 提高到 38.16 Avg@8 BC%，而人工设计的强化学习设置为 33.77；Socratic-SWE 在三轮迭代后在 SWE-bench Verified 上达到 50.40%。

#### Evidence
- [EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning](../Inbox/2026-06-02--evotrainer-co-evolving-llm-policies-and-training-harnesses-for-autonomous-agentic-reinforcement-learning.md): 详述 EvoTrainer 的演进式诊断、分支决策和报告的 SWE-9B 提升。
- [Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills](../Inbox/2026-06-05--socratic-swe-self-evolving-coding-agents-via-trace-derived-agent-skills.md): 详述 Socratic-SWE 的轨迹衍生技能、任务验证和 SWE-bench Verified 结果。

### 完整软件循环的基准测试
评估工作关注代理能否处理软件工作的混乱部分：模糊需求、仓库定位、测试、提交和反复反馈。Asuka-Bench 在多轮反馈中评测 Web 应用创建，包含隐藏需求和浏览器渲染行为。TeleSWEBench 基于真实 srsRAN 5G 提交构建 734 个电信任务，并报告最强工具最多能达到 25% 的可发布变更率。这些结果把自主性声明绑定到可执行结果和领域代码上，因为文件定位和功能正确性都很重要。

#### Evidence
- [Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement](../Inbox/2026-06-04--asuka-bench-benchmarking-code-agents-on-underspecified-user-intent-and-multi-round-refinement.md): 解释 Asuka-Bench 的未充分说明请求、反馈轮次、浏览器检查和报告的通过率。
- [TeleSWEBench: A Commit-Driven Benchmark for Evaluating LLM-Powered Software Engineering in Telecommunications](../Inbox/2026-06-03--teleswebench-a-commit-driven-benchmark-for-evaluating-llm-powered-software-engineering-in-telecommunications.md): 解释 TeleSWEBench 的 734 个电信任务、两阶段评估和可发布变更率。

### AI 编写代码成为治理问题
本周最后出现了一个具体的生产信号。《经济学人》摘录报道了 Anthropic 的说法：Claude 编写了该公司 5 月发布代码的五分之四以上，而 Claude Code 发布前这一比例还只是低个位数。该来源没有给出受控安全结果，但清楚显示了治理问题：编码代理现在可以影响 AI 实验室发布的系统、工具和基础设施。审查、来源记录，以及对递归式软件工作的限制，需要在普通工程工作流中可见。

#### Evidence
- [Will artificial intelligence soon escape human control?](../Inbox/2026-06-07--will-artificial-intelligence-soon-escape-human-control.md): 概述 Claude Code 的递归式自我改进担忧，以及 Anthropic 报告的代码占比。
