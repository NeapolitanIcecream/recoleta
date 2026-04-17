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

# 编程代理研究正转向显式控制面

## Overview
当天最强的一组工作，把编程代理收紧在显式结构、受限动作和不确定条件下的判断上。Contract-Coding 给出了最清楚的代码仓库级结果，DeepGuard 展示了更突出的安全提升之一，而 HiL-Bench 表明，请求帮助仍是一个薄弱点。贯穿这些工作的主线是可检查的控制：契约、护栏，以及能暴露判断缺失的评测。

## Clusters

### 结构化计划正在支撑代码仓库规模的编程工作
面向代码仓库规模的编程论文持续先写清结构，再生成代码。Contract-Coding 是目前最清楚的结果：它把描述不足的请求转成 Language Contract，用这个契约协调文件生成，并在 Greenfield-5 上报告了很强的多文件表现。在 Roguelike 上，它达到 47% 的成功率，高于 OpenHands 的 30%、MetaGPT 和 ChatDev 的 10%，以及 FLOW 的 0%。同一篇论文还报告了 Hierarchical Execution Graph 带来的速度提升，把 Roguelike 的运行时间从 510s 降到 232s。第二篇论文把目标从软件工单扩展到更广的范围：在一个 Odoo ERP 案例研究里，编程代理能完成简单的业务流程，但一旦策略约束和相互依赖的决策增多，得分就会下降。共同点是显式的任务结构。它在代码仓库规模上有帮助，但当业务规则必须和执行过程保持一致时，系统仍然吃力。

#### Evidence
- [Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm](../Inbox/2026-04-10--contract-coding-towards-repo-level-generation-via-structured-symbolic-paradigm.md): 代码仓库级基于契约的生成与基准结果。
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md): 即使有工具访问，更难的业务流程仍会让编程代理失效的证据。

### 编程代理的安全正在同时进入模型和工具循环
安全和控制正体现为具体的工程选择，而不只是模型调优。DeepGuard 在五个代码 LLM 上，相比 SVEN 将安全且正确的代码生成平均提高了 11.9%；其中 Qwen2.5-Coder-3B 的 sec-pass@1 从 70.47% 提升到 80.76%，同时把 pass@1 保持在接近基础模型的水平。Zup 的生产论文在工具层也说明了同一点：为了提高可靠性，定向字符串替换编辑优于整文件重写；shell 访问需要分层限制；团队会先用 approval mode，再逐步给代理更多自由。这两篇论文把控制面放在两个位置：模型内部用于安全偏置，模型外部用于限制动作范围和执行审查。

#### Evidence
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md): 多层安全信号带来的安全代码生成量化提升。
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md): 更安全、更可靠的编程代理的生产设计选择。

### 基准测试正在检验判断力，而不只是执行力
评测对“合格的自主性”要求更严了。HiL-Bench 表明，强模型仍然难以在正确的时间请求澄清。在 SQL 任务上，拥有完整信息时，pass@3 为 86% 到 91%；当代理必须自己决定何时调用 ask_human() 时，pass@3 降到 5% 到 38%。在 SWE 任务上，下降更明显：完整信息下的 64% 到 88%，在选择性升级后变成 2% 到 12%。另一项实证研究在可观测性工作中发现了同类差距。在 77 个代码仓库里，58.4% 的仓库中，人类比代理更常修改日志；代理对建设性日志请求有 67% 的时间未能遵从；生成后的日志修复中，72.5% 由人类完成。当前编程代理能执行很多任务，但仍然会错过该何时提问、何时记录日志，以及何时需要为后续人工处理留下线索。

#### Evidence
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md): 关于选择性升级和 ask_human 表现差距的基准证据。
- [Do AI Coding Agents Log Like Humans? An Empirical Study](../Inbox/2026-04-10--do-ai-coding-agents-log-like-humans-an-empirical-study.md): 代理在日志工作上投入不足，并把修复工作留给人类的实证证据。
