---
kind: trend
trend_doc_id: 1955
granularity: day
period_start: '2026-07-16T00:00:00'
period_end: '2026-07-17T00:00:00'
topics:
- agent reliability
- evidence gating
- coding agents
- dynamic tools
- domain evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-1955
tags:
- recoleta/trend
- topic/agent-reliability
- topic/evidence-gating
- topic/coding-agents
- topic/dynamic-tools
- topic/domain-evaluation
language_code: zh-CN
---

# 可执行门控揭示静态代理评分遗漏的失败

## 概览
近期围绕工程化检查的进展正变得更加面向实际操作。当前证据支持将控制措施绑定到实际源状态、工具版本和领域规则。静态或纯文本的成功表现可能掩盖供应链、工作流和适应性方面的失败。这些研究大多范围较窄或处于早期阶段，因此确立的是具体的失败模式，而不是广泛的生产可靠性。

## 研究发现

### 证据门控执行
可靠的自动化越来越依赖模型之外的确定性控制。一项设置安全研究发现，跨生态系统的代理通常会漏掉恶意软件包来源；提示词只能帮助发现其明确提及的攻击维度，而覆盖名称、来源和版本的安装前检查弥补了大部分已观察到的差距。Proof-or-Stop 将同一原则应用于生命周期决策：只有在新鲜证据与受跟踪的源状态绑定后，“已测试”或“已完成”等声明才会推进。其门控循环在 10 个场景中记录了零次错误完成，并拒绝了测试的全部 18 类回执篡改，但评估仅限于一个模型系列和一个自托管语料库。

#### 资料来源
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): 报告了跨生态系统的来源盲点，以及确定性安装前验证的作用。
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): 报告了 10/10 个场景中零次错误完成，并拒绝了 18 类篡改，同时说明了评估限制。

### 覆盖领域完整性的评估
基准测试正将完整的可执行工作流——而不是看似合理的代码或最终答案——作为成功单位。Alipay-PIBench 测试支付集成中的端到端行为、签名与通知处理、退款保护以及业务状态一致性；提供官方领域技能后，平均评分标准通过率提高了 10.31 个百分点。StructureClaw 要求模型、验证记录、求解器输出和报告形成可追溯的链条；使用其受治理的工作流后，平均成功率从 56.8% 提高到 88.6%。Kaleidoscope 通过根据人工标注校准应用专属评判器，将这一模式扩展到已部署应用，但其证据仍来自一个未受控的四用例试点。

#### 资料来源
- [Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents](../Inbox/2026-07-16--alipay-pibench-a-realistic-payment-integration-benchmark-for-coding-agents.md): 定义了渐进式支付风险场景，并报告了领域技能带来的 10.31 个百分点平均提升。
- [StructureClaw: Traceable LLM Agents and an Executable Benchmark for Structural Engineering Workflows](../Inbox/2026-07-16--structureclaw-traceable-llm-agents-and-an-executable-benchmark-for-structural-engineering-workflows.md): 报告了工作流层面的成功率从 56.8% 提高到 88.6%。
- [Project Kaleidoscope: Contextual, Human-Aligned Evaluation for Real-World AI Applications](../Inbox/2026-07-16--project-kaleidoscope-contextual-human-aligned-evaluation-for-real-world-ai-applications.md): 介绍了情境化评分标准、人工校准以及为期三周的有限试点。

### 变化中的多模态条件
受控评估表明，在固定且以文本为主的环境中测得的能力无法直接迁移。在演化后的 Model Context Protocol（MCP）服务器上，GPT-5.4 和 Claude-Sonnet-4-6 的任务性能分别下降了 13.7% 和 14.4%。在使用截图等视觉证据进行仓库定位时，表现最强的代理也仅达到文件 Acc@5 38.96 和函数 Acc@10 22.45。维护工作中的证据显示出相关的范围问题：抽样的 64 个 AI/ML 问题中，有 28 个需要修改生产代码之外的内容，包括提示词、数据集、依赖项和运行时配置。因此，评估需要保留环境变化和异构工件，而不能将工作简化为静态代码快照。

#### 资料来源
- [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](../Inbox/2026-07-16--mcpevol-bench-benchmarking-llm-agent-performance-across-dynamic-evolutions-of-mcp-servers.md): 报告了前沿模型在真实 MCP 服务器演化下的性能下降。
- [MM-IssueLoc: A Controlled Benchmark for Evaluating Visual Evidence in Multimodal Repository-Level Issue Localization](../Inbox/2026-07-16--mm-issueloc-a-controlled-benchmark-for-evaluating-visual-evidence-in-multimodal-repository-level-issue-localization.md): 报告了在多模态仓库证据下较低的文件和函数定位准确率。
- [Rethinking Issue Resolution for AI/ML Systems](../Inbox/2026-07-16--rethinking-issue-resolution-for-ai-ml-systems.md): 发现迭代式工作流横跨数据集、提示词、模型配置及其他非代码工件。
