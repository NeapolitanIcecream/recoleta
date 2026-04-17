---
kind: trend
trend_doc_id: 301
granularity: week
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-13T00:00:00'
topics:
- coding-agents
- verification
- benchmarks
- security
- repo-scale-evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-301
tags:
- recoleta/trend
- topic/coding-agents
- topic/verification
- topic/benchmarks
- topic/security
- topic/repo-scale-evaluation
language_code: zh-CN
---

# coding-agent 研究现在把验证界面当作核心系统设计

## Overview
本周的 coding-agent 研究在每个关键步骤都留下证据时最有说服力。重心已经转向可执行控制：书面规格、精确编辑空间、运行时检查和持久的工具边界。与前一周相比，这份简报更具体地说明了这些控制点位于哪里：仓库任务内部、安全修复流程中，以及智能体的写入路径上。

## Clusters

### 书面规格正成为标准的智能体输入
这一周里，较强的论文持续把智能体行为拉回到模型外部可检查的形式。需求、契约、架构描述符和类型化失败信号，都成了规划与审查的硬边界。实际收益是仓库级工作更清晰，循环中的隐含假设更少。ReCodeAgent 和 REAgent 把生成过程绑定到明确的任务描述上，后续工作则把同样的思路扩展到形式化规格和持久写入路径。

#### Evidence
- [We need re-learn what AI agent development tools are in 2026](../Inbox/2026-04-07--we-need-re-learn-what-ai-agent-development-tools-are-in-2026.md)
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md)
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md)
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md)
- [From Helpful to Trustworthy: LLM Agents for Pair Programming](../Inbox/2026-04-11--from-helpful-to-trustworthy-llm-agents-for-pair-programming.md)
- [CODESTRUCT: Code Agents over Structured Action Spaces](../Inbox/2026-04-07--codestruct-code-agents-over-structured-action-spaces.md)

### 基准开始评整个工作流，而不只是答案
评测开始更严格地围绕精确编辑、端到端任务和运行时证据展开。这改变了“成功”的判定标准。本周的论文关注的是：智能体能否完成一个仓库任务、遵守设计规则、说明它使用了哪些证据，并把成本或动作次数控制在限制内。CLI-Tool-Bench、SWD-Bench 和 HiL-Bench 等基准都指向同一个方向：有用的分数来自带有可见约束的长任务，而不是小型、孤立的补全。

#### Evidence
- [Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development](../Inbox/2026-04-08--evaluating-repository-level-software-documentation-via-question-answering-and-feature-driven-development.md)
- [Edit, But Verify: An Empirical Audit of Instructed Code-Editing Benchmarks](../Inbox/2026-04-06--edit-but-verify-an-empirical-audit-of-instructed-code-editing-benchmarks.md)
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md)
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md)
- [SysTradeBench: An Iterative Build-Test-Patch Benchmark for Strategy-to-Code Trading Systems with Drift-Aware Diagnostics](../Inbox/2026-04-06--systradebench-an-iterative-build-test-patch-benchmark-for-strategy-to-code-trading-systems-with-drift-aware-diagnostics.md)
- [Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution](../Inbox/2026-04-07--does-pass-rate-tell-the-whole-story-evaluating-design-constraint-compliance-in-llm-based-issue-resolution.md)

### 验证和安全检查正进入写入路径
无论是编码还是安全工作，验证现在都放进了动作循环内部。测试、运行时插桩、执行落地和护栏都被当作门禁，只有通过检查，智能体的提交或修复才会被接受。本周的研究也继续保持对局限的现实判断：安全方向的工作报告了可被利用的生成代码，以及在混乱的多步场景中较弱的可靠性；同时，DeepGuard 和 Verify Before You Fix 这类系统也在改进检查路径。

#### Evidence
- [TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories](../Inbox/2026-04-08--tracesafe-a-systematic-assessment-of-llm-guardrails-on-multi-step-tool-calling-trajectories.md)
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md)
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md)
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md)
- [Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents](../Inbox/2026-04-12--resilient-write-a-six-layer-durable-write-surface-for-llm-coding-agents.md)
- [Cryptographic delegation receipts to close the user-to-operator agent trust gap](../Inbox/2026-04-06--cryptographic-delegation-receipts-to-close-the-user-to-operator-agent-trust-gap.md)
