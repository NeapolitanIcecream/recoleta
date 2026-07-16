---
kind: trend
trend_doc_id: 277
granularity: day
period_start: '2026-04-10T00:00:00'
period_end: '2026-04-11T00:00:00'
topics:
- coding-agents
- repo-generation
- secure-code
- human-in-the-loop
- evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-277
tags:
- recoleta/trend
- topic/coding-agents
- topic/repo-generation
- topic/secure-code
- topic/human-in-the-loop
- topic/evaluation
language_code: zh-CN
---

# 代码代理研究正在围绕显式控制面展开

## 概览
当天最强的工作都在把代码代理收紧到显式结构、受限动作和不确定条件下的判断上。Contract-Coding 给出最清楚的仓库级结果，DeepGuard 提供了更明显的安全提升，HiL-Bench 则显示请求帮助仍然是弱项。主线是可检查的控制：合约、护栏，以及能暴露判断缺口的评估。

## 研究发现

### Structured plans are carrying repo-scale coding work
仓库级代码论文一直在先写结构，再写代码。Contract-Coding 的结果最清楚：它把一个表述不完整的请求转成 Language Contract，用这个合约协调文件生成，并在 Greenfield-5 上报告了很强的多文件表现。在 Roguelike 上，它达到 47% 成功率，高于 OpenHands 的 30%、MetaGPT 和 ChatDev 的 10%，以及 FLOW 的 0%。这篇论文还报告了 Hierarchical Execution Graph 带来的速度提升，把 Roguelike 运行时间从 510s 降到 232s。另一篇论文把目标扩展到软件工单之外：在一个 Odoo ERP 案例研究中，代码代理能处理简单的业务流程，但一旦政策约束和相互依赖的决策叠加，得分就会下降。共同点是显式任务结构。它在仓库规模上有用，但当业务规则必须和执行保持一致时，还是会吃力。

#### 资料来源
- [Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm](../Inbox/2026-04-10--contract-coding-towards-repo-level-generation-via-structured-symbolic-paradigm.md): Repo-level contract-based generation and benchmark results.
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md): Evidence that harder business workflows break coding agents even with tool access.

### Coding-agent safety is moving into both the model and the tool loop
安全和控制更多体现在具体工程选择上，而不只是模型调参。DeepGuard 在五个代码大模型上把安全且正确的代码生成率平均提高了 11.9%，其中 Qwen2.5-Coder-3B 的 sec-pass@1 从 70.47% 升到 80.76%，同时 pass@1 仍接近基座模型。Zup 的生产论文在工具层面给出同样的结论：有针对性的字符串替换编辑比整文件重写更可靠，shell 访问需要分层限制，团队先用 approval mode，再逐步给代理更多自由。合在一起，这些论文把控制面放在两个地方：模型内部做安全偏置，模型外部做受限动作和审查。

#### 资料来源
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md): Quantified secure code generation gains from multi-layer security signals.
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md): Production design choices for safer, more reliable coding agents.

### Benchmarks are testing judgment, not just execution
评估正在更严格地界定什么才算合格的自主性。HiL-Bench 显示，强模型仍然很难在合适的时机请求澄清。在 SQL 任务上，当代理必须决定何时调用 `ask_human()` 时，pass@3 从完全信息下的 86% 到 91% 降到 5% 到 38%。在 SWE 任务上，降幅更大：完全信息下的 64% 到 88% 变成选择性升级下的 2% 到 12%。另一项实证研究在可观测性工作里发现了类似差距。在 77 个仓库中，58.4% 的仓库里人类修改日志的频率高于代理，代理有 67% 的时间没有遵守建设性的日志请求，而人类完成了 72.5% 的生成后日志修复。现在的代码代理能执行很多任务，但它们还是会漏掉何时该问、何时该记日志，以及以后何时需要留痕。

#### 资料来源
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md): Benchmark evidence on selective escalation and ask_human performance gaps.
- [Do AI Coding Agents Log Like Humans? An Empirical Study](../Inbox/2026-04-10--do-ai-coding-agents-log-like-humans-an-empirical-study.md): Empirical evidence that agents underserve logging and leave repair work to humans.
