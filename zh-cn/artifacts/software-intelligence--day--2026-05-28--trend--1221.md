---
kind: trend
trend_doc_id: 1221
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
topics:
- coding agents
- software verification
- code review automation
- vulnerability repair
- agent evaluation
- program analysis
run_id: materialize-outputs
aliases:
- recoleta-trend-1221
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/code-review-automation
- topic/vulnerability-repair
- topic/agent-evaluation
- topic/program-analysis
language_code: zh-CN
---

# 编码代理正在接受操作性证据、审查门控和可执行检查的评判

## Overview
当天最强的信号是 AI 编码系统的操作性证据。论文在真实会话中测量代理如何失败，在生产中限制低风险审查，并用规格或领域不变量测试生成代码。RADAR、TRAILS 和 Agora 把重点放在同一件事上：只发布能够被检查、约束或复现的内容。

## Clusters

### Developer control and production review
编码代理现在是在真实开发工作流中接受评判，而不只是看最终补丁。一项对 20,574 个 IDE 和命令行会话的大型研究发现了 16,118 个有证据支撑的失配事件。约束违规是最大的症状类别，占 38.33%，只有 9.33% 的事件在日志里显示出可见的解决过程。大多数可见修复都需要开发者明确施压。

RADAR 展示了同一问题在生产侧的情况。Meta 在落地前，会把低风险 diff 送入源码资格规则、Diff Risk Score、大语言模型审查和确定性检查。这个系统审查了 535K 多个 diff，落地了 331K 多个，在已报告的部署中，其回滚率和生产事故率都低于非 RADAR diff。

#### Evidence
- [How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions](../Inbox/2026-05-28--how-coding-agents-fail-their-users-a-large-scale-analysis-of-developer-agent-misalignment-in-20574-real-world-sessions.md): Large-scale real-world session analysis with misalignment categories, costs, and resolution rates.
- [Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency](../Inbox/2026-05-28--automating-low-risk-code-review-at-meta-radar-risk-calibration-and-review-efficiency.md): Production deployment of risk-calibrated automated code review at Meta.

### Executable evidence for generated software
几篇论文把正确性当作一种需要具体检查的行为主张。TRAILS 针对生成代码的 oracle 问题：先在生成的输入上执行候选程序，再让大语言模型把每个输入输出对和自然语言规格说明进行比对。在 LiveCodeBench 和 CoCoClaNeL 上，它的 Matthew 相关系数优于零样本 chain-of-thought 基线，但每个任务的 token 成本更高。

Projectional decoding 在生成过程中加入检查。它在 token 流旁边保留一个部分图模型，并屏蔽违反语义约束的 token。在 CLEVR 的领域专用语言程序上，Qwen3 系列模型的语义有效性达到 73.33% 到 79.67%。CODEFUSE-DeBench 对逆向工程给出一个提醒：只看重新编译不够，因为最好的反编译器加修复模型只达到 22.3% 的完全加部分行为重叠，精确 stdout 匹配只有 1.2%。

#### Evidence
- [Inferring Code Correctness from Specification](../Inbox/2026-05-28--inferring-code-correctness-from-specification.md): TRAILS evaluates generated code by executing inputs and judging outputs against specifications.
- [Projectional Decoding: Towards Semantic-Aware LLM Generation](../Inbox/2026-05-28--projectional-decoding-towards-semantic-aware-llm-generation.md): Projectional decoding enforces semantic constraints during generation and reports CLEVR DSL validity gains.
- [CODEFUSE-DEBENCH: An Empirical Study on Readability, Recompilability, and Functionality](../Inbox/2026-05-28--codefuse-debench-an-empirical-study-on-readability-recompilability-and-functionality.md): DeBench measures readability, recompilability, and behavioral functionality for decompiled code.

### Security failures, repair memory, and pre-generation signals
这一时期的安全研究聚焦两个实际失效模式：很小的提示变化会生成漏洞代码，修复代理会忘记有用的修复。提示脆弱性研究在五种语言上使用 CWEval，发现单字符变动就能把安全输出改成有漏洞的输出。隐藏状态探针在预测联合的功能+安全目标时，平均留出集 AUC 约为 0.70，其中输入处理类漏洞比安全默认类缺陷更容易预测。

EvoRepair 通过在多次漏洞尝试之间保存带分数的修复经验，减少重复修复。它的循环会检索相关的 CVE 或 CWE 经验，在 Docker 中打补丁，概括修复轨迹，并更新经验库。使用 GPT-5-mini 时，它在 PATCHEVAL 上报告 93.47%，在 SEC-bench 上报告 87.00%，在论文比较中的 12 个自动漏洞修复基线之上。

#### Evidence
- [Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs](../Inbox/2026-05-28--minimal-prompt-perturbations-lead-to-code-vulnerabilities-prompt-fragility-and-hidden-state-signals-in-coding-llms.md): Prompt perturbation study showing security flips and hidden-state vulnerability prediction results.
- [EvoRepair: Enhancing Vulnerability Repair Agents Through Experience-Based Self-Evolution](../Inbox/2026-05-28--evorepair-enhancing-vulnerability-repair-agents-through-experience-based-self-evolution.md): Experience-based vulnerability repair agent with PATCHEVAL and SEC-bench results.

### Domain-aware agents for protocol bugs
Agora 表明，协议漏洞发现需要带有明确状态和领域约束的代理。这个系统把工作分给协调器、策略代理和测试生成代理。它会生成带触发条件、动作序列、预期错误行为和 oracle 检查的假设。

在 Raft、EPaxos、HotStuff 和 BullShark 的实现上，Agora 报告了 15 个此前未知的协议级安全漏洞。使用 GPT-5.2、Gemini 3.0 Pro Preview、Claude Sonnet 4.5 和 Qwen3 Coder 的 ReAct 风格基线一共找到了 22 个实现漏洞，但在已报告的测试里没有发现协议级逻辑漏洞。

#### Evidence
- [Agora: Toward Autonomous Bug Detection in Production-Level Consensus Protocols with LLM Agents](../Inbox/2026-05-28--agora-toward-autonomous-bug-detection-in-production-level-consensus-protocols-with-llm-agents.md): Agora’s multi-agent protocol testing method and reported consensus-bug findings.
