---
kind: trend
trend_doc_id: 969
granularity: day
period_start: '2026-05-12T00:00:00'
period_end: '2026-05-13T00:00:00'
topics:
- agent evaluation
- benchmark security
- agent tracing
- MCP governance
- software assurance
- code translation
- LLM testing
run_id: materialize-outputs
aliases:
- recoleta-trend-969
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/benchmark-security
- topic/agent-tracing
- topic/mcp-governance
- topic/software-assurance
- topic/code-translation
- topic/llm-testing
language_code: zh-CN
---

# Agent 研究正把分数和工具操作作为审计目标

## Overview
当天最强的信号是 agentic 系统的可审计性。BenchJack 在 agent 运行前攻击基准执行框架。Rollout Cards 要求评估发布 rollout 证据。Cloudflare 的 Model Context Protocol (MCP) 部署显示，企业工具访问中也存在同一个控制问题。

## Clusters

### 基准完整性
这一时期，agent 基准分数受到直接的对抗压力。BenchJack 审计了 10 个 agent 基准，并为全部 10 个生成了可运行的奖励破解利用，在其分类体系中发现 219 个不同缺陷。它的修补循环在 4 个可修复基准上把可被攻破任务比例降到 10% 以下，并在 3 次迭代内完全修补了 WebArena 和 OSWorld。

Rollout Cards 处理的是相关的报告问题。论文认为，agent 研究需要发布 rollout 记录、声明的评分视图、报告规则和省略字段清单。在对 50 个热门代码库的审计中，没有任何一个在标题分数旁报告失败、出错或跳过的 rollout。对固定产物重新评分后，报告分数最高变化 20.9 分，并可能改变 tau-bench 上的模型排名。

#### Evidence
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack 关于基准利用、缺陷数量和修补结果的结果。
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout-card 提案，以及报告规则会改变 agent 基准结论的证据。

### 可追踪的 agent 运行
agent 运行工作正被作为证据管理问题处理。一项关于决策可重建性的试点研究，用 7 类属性测试了 6 种供应商 SDK 机制，包括 MCP 和 OpenTelemetry GenAI。严格治理完整性介于 42.9% 到 85.7% 之间；在大多数受调查机制中，推理证据缺失或不可用。

Cloudflare 的 MCP 架构为工具访问给出了生产侧方案。它把 MCP 服务器从员工机器迁移出来，置于集中审批、基于 OAuth 的访问检查、审计日志、数据丢失防护规则和默认拒绝写入控制之后。它的 Code Mode 将一个内部门户的工具定义上下文从 52 个工具约 9,400 个 token，降到 2 个门户工具约 600 个 token。

一个提示词规格审计案例研究显示，多 agent 编排内部也有类似问题。Claude sub-agents 在 9 轮中检查了 8 个 AEGIS 提示词和合约文件，发现 51 个一致性缺陷。高严重性缺陷全部是跨通道 schema 不匹配，其中包括一个字段名不匹配，可能导致静默运行时失败。

#### Evidence
- [Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes](../Inbox/2026-05-12--property-level-reconstructability-of-agent-decisions-an-anchor-level-pilot-across-vendor-sdk-adapter-regimes.md): 关于跨 SDK 证据机制重建 agent 决策的试点结果。
- [Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments](../Inbox/2026-05-12--scaling-mcp-adoption-our-ref-architecture-simpler-safer-cheaper-deployments.md): Cloudflare MCP 治理架构，以及 Code Mode 降低 token 的说法。
- [Iterative Audit Convergence in LLM-Managed Multi-Agent Systems: A Case Study in Prompt Engineering Quality Assurance](../Inbox/2026-05-12--iterative-audit-convergence-in-llm-managed-multi-agent-systems-a-case-study-in-prompt-engineering-quality-assurance.md): 多 agent 提示词规格审计结果和缺陷分类。

### 可检查的软件和数据工作
多篇论文通过把输出绑定到可执行或结构化证据，让 LLM 软件工作更容易检查。Agentic Interpretation 将程序分析目标分解为局部声明，并把每个判断记录在有限证据格中。论文还没有实现或基准结果，因此其价值在于为可审计的 LLM 辅助分析提供形式化设计，而非已测得的性能。

在代码迁移方面，cozy 在符号执行下比较 C 和 Rust 二进制文件，并要求开发者只审查它发现的行为差异。报告的实验规模较小，覆盖插入排序、一个 watch 更新函数和一个 box blur 滤波器，但它们展示了用于翻译保证的具体路径级审查流程。

旧式 APL 到 C# 翻译和神经科学数据复用都使用基于运行的检查。APL 研究构建对齐数据集，并通过编译和运行测试来评估生成的 C#，但摘录没有提供最终准确率数字。neurodata 基准让 Claude Code 和 Codex 执行 48 个数据集转换任务；每次运行都产生了输出，但完全无错误复用很少见，并且作为评审的 agent 漏掉了错误。

#### Evidence
- [Agentic Interpretation: Lattice-Structured Evidence for LLM-Based Program Analysis](../Inbox/2026-05-12--agentic-interpretation-lattice-structured-evidence-for-llm-based-program-analysis.md): Agentic Interpretation 的基于格的证据模型，以及其声明缺少实验结果。
- [Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution](../Inbox/2026-05-12--finding-a-crab-in-the-c-assured-translation-via-comparative-symbolic-execution.md): cozy 的比较符号执行方法，以及小规模 C/Rust 验证实验。
- [Neural Code Translation of Legacy Code: APL to C#](../Inbox/2026-05-12--neural-code-translation-of-legacy-code-apl-to-c.md): APL 到 C# 数据集构建，以及编译并运行的评估流水线。
- [Neurodata Without Boredom: Benchmarking Agentic AI for Data Reuse](../Inbox/2026-05-12--neurodata-without-boredom-benchmarking-agentic-ai-for-data-reuse.md): agentic neurodata 复用基准结果，以及关于人工审查的发现。

### 面向开放式 LLM 输出的测试方法
语料中的测试研究关注难以定义精确预期答案的情况。变形测试综述回顾了 93 项主要研究，并把该领域组织为两个方向：用变形测试评估 LLM 系统，以及用 LLM 帮助发现关系、转换输入、实现测试并运行闭环检查。它的主张处于综述层面；它报告文献范围和类别，没有报告经过基准测试的缺陷检测收益。

面向教育的代码审查给出了一个更窄的任务适配例子。一个使用参数高效微调（PEFT）微调的 Code Llama 7B 模型，在错误反馈准确率上达到 61%，在下一步帮助性上达到 60%；基线提示分别为 20% 和 26%。学生研究规模较小，只有 7 名 CS1 学生，因此最有力的主张是，本地开放模型在有边界的反馈任务上经过定向适配后可以改进。

#### Evidence
- [Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey](../Inbox/2026-05-12--bidirectional-empowerment-of-metamorphic-testing-and-large-language-models-a-systematic-survey.md): 综述范围、分类体系，以及缺少基准式性能主张。
- [Fine-Tuning Models for Automated Code Review Feedback](../Inbox/2026-05-12--fine-tuning-models-for-automated-code-review-feedback.md): 微调 Code Llama 代码审查反馈设置，以及报告的准确率和帮助性结果。
