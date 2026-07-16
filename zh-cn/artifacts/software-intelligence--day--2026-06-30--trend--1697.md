---
kind: trend
trend_doc_id: 1697
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
topics:
- coding agents
- software maintenance
- performance engineering
- C-to-Rust migration
- agent governance
- benchmarking
run_id: materialize-outputs
aliases:
- recoleta-trend-1697
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-maintenance
- topic/performance-engineering
- topic/c-to-rust-migration
- topic/agent-governance
- topic/benchmarking
language_code: zh-CN
---

# 编码代理需要明确工件，才能获得信任

## 概览
当天最强的证据支持这样一类编码代理：将模型输出绑定到明确的软件工件，包括功能映射、性能分析 traces、编译器错误、基准和审批记录。FeatX、MOA 和 AdaTrans 显示出最清晰的收益，而协议和成本研究暴露了治理和任务经济性方面的限制。

## 研究发现

### 仓库级代码编辑
FeatX 和 MOA 要求大语言模型（LLM）先处理软件证据，再编辑代码。FeatX 将仓库功能映射到 Java 类和方法，然后通过三阶段代理生成 diff。其研究报告称，相比 ChatGPT，NASA-TLX 工作负荷从 12.5 降至 7.4；在 38 个提交上，函数级修改定位的 F1 为 0.385。

MOA 将同样的做法用于内存优化。它把性能分析 traces 转换为经过验证的反模式、静态检查器和补丁。在 OpenHarmony 上，它报告了 13 个反模式、10,067 个检测到的低效实例、769 个生成补丁，以及 92.5% 的专家接受率。这些结果说明当前重点很明确：当源码映射、运行时 traces 和验证循环缩小任务范围时，代理表现最强。

#### 资料来源
- [FeatX: Editing Software by Editing Features for Repository-Level Code Evolution](../Inbox/2026-06-30--featx-editing-software-by-editing-features-for-repository-level-code-evolution.md): FeatX 摘要，以及报告的用户研究和定位指标。
- [MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale](../Inbox/2026-06-30--moa-a-profiling-guided-llm-framework-for-memory-optimization-automation-at-codebase-scale.md): MOA 摘要、基于性能分析的流程，以及 OpenHarmony 结果。

### 编译器引导的迁移和 Java 性能基准
AdaTrans 展示了编译器反馈如何推动更安全的 C 到 Rust 迁移。它将 Rust 编译器错误映射到修复模板和文档，然后检查构建和输出行为。在 104 个算法问题上，它报告了 95.51% 的编译通过率、81.09% 的解题率，以及 1.19% 的 unsafe 文件率。

JETO-Bench 为性能修复代理提供了更难的 Java 目标。它的收集工具扫描了 3,686 个仓库和近 180 万个提交，然后生成了 660 个执行时间改进补丁和 91 个经过人工验证的可执行任务。OpenHands 修复了这 91 个任务中的 13 个。该基准还发现，许多 Java 项目缺少能够证明执行时间改进的测试，这限制了自动评分。

#### 资料来源
- [AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair](../Inbox/2026-06-30--adatrans-automated-c-to-rust-transformation-via-error-adaptive-repair.md): AdaTrans 方法和 C 到 Rust 迁移结果。
- [JETO-Bench: A Reproducible Benchmark for Execution Time Improvement Patches in Java](../Inbox/2026-06-30--jeto-bench-a-reproducible-benchmark-for-execution-time-improvement-patches-in-java.md): JETO-Bench 收集规模、已验证任务数量，以及 OpenHands 结果。

### 代理成本和治理控制
代理能力的衡量正在同时考虑任务成本和决策控制。Artificial Analysis 报告称，Claude Sonnet 5 在其 Intelligence Index 上得分 53，比 Sonnet 4.6 高 6 分。在 max effort 下，它每个任务使用的输出 token 约多 40%，在 AA-Briefcase 和 GDPval-AA 上的代理式轮次约为三倍，使标准定价下测得的成本升至每任务 $2.29。

治理研究增加了第二个约束。一项协议研究发现，MCP、A2A、ACP、ANP 和 ERC-8004 对六个治理维度都没有完整支持：成员资格、审议、投票、异议保留、人工升级和审计/重放。Serval 的 Catalyst 产品给出了一个场景下的产品级做法：拟议的自动化变更会先暂存以供审查，团队可以要求发布前经过第二人审批。

#### 资料来源
- [Claude Sonnet 5: strong agentic performance at a higher cost per task](../Inbox/2026-06-30--claude-sonnet-5-strong-agentic-performance-at-a-higher-cost-per-task.md): Claude Sonnet 5 基准、token 使用量、轮次数和成本发现。
- [Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express](../Inbox/2026-06-30--governance-gaps-in-agent-interoperability-protocols-what-mcp-a2a-and-acp-cannot-express.md): 跨代理互操作协议的治理缺口分析。
- [Catalyst: Automating a task forever should be easier than doing it manually once](../Inbox/2026-06-30--catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once.md): Catalyst 的暂存、审批和自动化设置细节。

### 代码理解数据和混淆测试
两篇论文让代码代理评估减少对干净代码片段的依赖。CoCoMUT 提取 Java 方法上下文，包括调用方、被调用方、类数据、文档，以及源码-字节码对齐。在 20 个仓库中，它生成了 56,512 条方法上下文记录，并将 97.8% 的已识别项目调用目标对齐到源码方法。

混淆代码研究测试了当名称和控制流被扭曲时，模型是否仍能跟踪程序行为。推理调优模型与人类任务难度呈正 Spearman 相关，而代码模型和指令调优模型的对齐接近于零。随着调度器复杂度上升，控制流扁平化会降低准确率。这关系到代码审查、审计、逆向工程和安全工作，因为表层线索可能会误导判断。

#### 资料来源
- [CoCoMUT: A Tool for Code-Context Mining and Automated Dataset Generation](../Inbox/2026-06-30--cocomut-a-tool-for-code-context-mining-and-automated-dataset-generation.md): CoCoMUT 提取方法和数据集质量结果。
- [Do Machines Struggle Where Humans Do? LLM and Human Comprehension of Obfuscated Code](../Inbox/2026-06-30--do-machines-struggle-where-humans-do-llm-and-human-comprehension-of-obfuscated-code.md): 混淆代码评估设置，以及模型与人类对齐结果。
