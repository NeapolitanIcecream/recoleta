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

# Agent research is treating scores and tool actions as audit targets

## 概览
当天最强的信号是智能体系统的可审计性。BenchJack 在智能体运行前就攻击基准 harness。Rollout Cards 要求评估发布回放证据。Cloudflare 的模型上下文协议（MCP）部署把同样的控制问题带进了企业工具访问。

## 研究发现

### Benchmark integrity
在这一时期，智能体基准分数直接承受对抗性压力。BenchJack 审计了 10 个智能体基准，并为全部 10 个生成了可用的奖励黑客利用，按其分类法共发现 219 个不同缺陷。它的修补循环把 4 个可修复基准上的可黑客任务比例降到 10% 以下，并在 3 轮内完全修补了 WebArena 和 OSWorld。

Rollout Cards 处理的是另一类报告问题。论文主张，智能体研究需要回放记录、声明的评分视图、报告规则和缺失字段清单。在对 50 个热门仓库的审计中，没有一个在头条分数旁报告失败、出错或跳过的回放。重新评分已修复的工件后，报告分数最多变化 20.9 分，并且可能在 tau-bench 上交换模型排名。

#### 资料来源
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack results on benchmark exploits, flaw count, and patching outcomes.
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout-card proposal and evidence that reporting rules change agent benchmark conclusions.

### Traceable agent operations
智能体运行工作正在被当作证据管理问题来看待。一个关于决策可重构性的试点测试了 6 种厂商 SDK 方案，包括 MCP 和 OpenTelemetry GenAI，对照 7 类属性。严格治理完整性介于 42.9% 到 85.7% 之间，而且在大多数受调查方案中，推理证据缺失或不可用。

Cloudflare 的 MCP 架构给工具访问提供了生产侧方案。它把 MCP 服务器从员工机器上移开，放到集中审批、基于 OAuth 的访问检查、审计日志、数据丢失防护规则和默认拒绝写入控制之后。它的 Code Mode 把一个内部门户的工具定义上下文从 52 个工具约 9,400 个 token 降到两个门户工具约 600 个 token。

一个提示规范审计案例研究显示，多智能体编排内部也有类似问题。Claude 子代理分 9 轮检查了 8 个 AEGIS 提示和契约文件，发现 51 个一致性缺陷。高严重性缺陷全都是跨 lane 的 schema 不匹配，包括一个字段名不一致，这本来可能导致静默运行失败。

#### 资料来源
- [Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes](../Inbox/2026-05-12--property-level-reconstructability-of-agent-decisions-an-anchor-level-pilot-across-vendor-sdk-adapter-regimes.md): Pilot results on reconstructing agent decisions across SDK evidence regimes.
- [Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments](../Inbox/2026-05-12--scaling-mcp-adoption-our-ref-architecture-simpler-safer-cheaper-deployments.md): Cloudflare MCP governance architecture and token-reduction claim for Code Mode.
- [Iterative Audit Convergence in LLM-Managed Multi-Agent Systems: A Case Study in Prompt Engineering Quality Assurance](../Inbox/2026-05-12--iterative-audit-convergence-in-llm-managed-multi-agent-systems-a-case-study-in-prompt-engineering-quality-assurance.md): Multi-agent prompt-specification audit results and defect taxonomy.

### Checkable software and data work
几篇论文通过把输出和可执行或结构化证据绑定，让 LLM 软件工作更容易检查。Agentic Interpretation 把程序分析目标拆成局部主张，并把每个判断记录到一个有限证据格中。论文目前还没有实现或基准结果，所以它的价值在于为可审计的 LLM 辅助分析提供形式化设计，而不是测得的性能。

在代码迁移方面，cozy 在符号执行下比较 C 和 Rust 二进制，只让开发者检查它发现的行为差异。报告中的实验规模很小，只覆盖插入排序、手表更新函数和 box blur 滤镜，但它展示了一种具体的路径级审查流程，用于翻译保证。

旧 APL 到 C# 的翻译和神经科学数据复用都使用基于运行的检查。APL 研究构建了对齐数据集，并通过编译和运行测试来评估生成的 C#，不过摘录没有给出最终准确率。神经数据基准在 48 个数据集转换任务上运行了 Claude Code 和 Codex；每次运行都有输出，但完全无错误的复用很少，而且作为裁判的智能体漏掉了错误。

#### 资料来源
- [Agentic Interpretation: Lattice-Structured Evidence for LLM-Based Program Analysis](../Inbox/2026-05-12--agentic-interpretation-lattice-structured-evidence-for-llm-based-program-analysis.md): Agentic Interpretation’s lattice-based evidence model and stated lack of experimental results.
- [Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution](../Inbox/2026-05-12--finding-a-crab-in-the-c-assured-translation-via-comparative-symbolic-execution.md): cozy’s comparative symbolic execution method and small C/Rust validation experiments.
- [Neural Code Translation of Legacy Code: APL to C#](../Inbox/2026-05-12--neural-code-translation-of-legacy-code-apl-to-c.md): APL-to-C# dataset construction and compile-and-run evaluation pipeline.
- [Neurodata Without Boredom: Benchmarking Agentic AI for Data Reuse](../Inbox/2026-05-12--neurodata-without-boredom-benchmarking-agentic-ai-for-data-reuse.md): Agentic neurodata reuse benchmark results and human-review finding.

### Testing methods for open-ended LLM outputs
本语料中的测试研究集中在那些很难定义精确预期答案的情况。关于变形测试的综述回顾了 93 项主要研究，并把这一领域分成两个方向：用变形测试评估 LLM 系统，以及用 LLM 帮助发现关系、转换输入、实现测试和运行闭环检查。它的主张是综述层面的；它报告的是文献范围和分类，而不是基准化的缺陷检测增益。

面向教育的代码评审给出了一个更窄的任务适配例子。一个用参数高效微调（PEFT）微调的 Code Llama 7B 模型，在错误反馈准确率上达到 61%，在下一步有用性上达到 60%，而基线提示分别是 20% 和 26%。这项学生研究规模很小，只有 7 名 CS1 学生，所以最强的结论是，本地开源模型在针对有限反馈任务进行定向适配后可以改进。

#### 资料来源
- [Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey](../Inbox/2026-05-12--bidirectional-empowerment-of-metamorphic-testing-and-large-language-models-a-systematic-survey.md): Survey scope, taxonomy, and lack of benchmark-style performance claims.
- [Fine-Tuning Models for Automated Code Review Feedback](../Inbox/2026-05-12--fine-tuning-models-for-automated-code-review-feedback.md): Fine-tuned Code Llama code-review feedback setup and reported accuracy/helpfulness results.
