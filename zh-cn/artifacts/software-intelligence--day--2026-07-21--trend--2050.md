---
kind: trend
trend_doc_id: 2050
granularity: day
period_start: '2026-07-21T00:00:00'
period_end: '2026-07-22T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u4EE3\u7801\u4ED3\u5E93\u667A\u80FD"
- "\u6267\u884C\u53CD\u9988"
- "\u8F6F\u4EF6\u6D4B\u8BD5"
- "\u4EE3\u7801\u57FA\u51C6"
run_id: materialize-outputs
aliases:
- recoleta-trend-2050
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u4EE3\u7801\u4ED3\u5E93\u667A\u80FD"
- "topic/\u6267\u884C\u53CD\u9988"
- "topic/\u8F6F\u4EF6\u6D4B\u8BD5"
- "topic/\u4EE3\u7801\u57FA\u51C6"
language_code: zh-CN
---

# 结构化上下文和执行反馈减少编码代理的浪费

## 概览
近期围绕编码代理控制机制的关注仍在持续，但目前最有力的证据已转向代理循环内部的工作。语义化的代码仓库结构减少了重复探索和脆弱编辑，执行反馈则引导更低成本的恢复和更有力的功能检查。大多数收益仍来自作者报告或特定任务，因此尚未确立其对广泛生产应用的影响。

## 研究发现

### 结构化的代码仓库上下文
三个系统用明确的软件结构取代了无定向的文本处理。TraceDev 将需求、设计和代码连接成可追溯性图谱；在 125 个用例上，它报告了 ETOUR 数据集 53.63% 和 SMOS 数据集 56.82% 的成功率。Source code algebra 则公开了重命名、参数变更等语义操作。在初步的跨文件探测中，它所使用的令牌数比基于文本编辑的基线少一个到两个数量级。JetBrains Context 在检索阶段通过增量语义索引应用了同一原则，据报告，代理交互轮数最多减少 68%，延迟最多减少 59%，执行成本最多减少 48%。共同机制是减少重复发现和分散编辑，但只有 TraceDev 提供了跨多个数据集的学术比较。

#### 资料来源
- [TraceDev: A Traceability-Driven Multi-agent Framework for Requirement-to-Code Development](../Inbox/2026-07-21--tracedev-a-traceability-driven-multi-agent-framework-for-requirement-to-code-development.md): 报告了 TraceDev 在两个数据集上的成功率及其基于可追溯性的代码仓库工作流。
- [Beyond Text Editing: Algebraic Manipulation of Source Code](../Inbox/2026-07-21--beyond-text-editing-algebraic-manipulation-of-source-code.md): 报告了初步跨文件编辑中更高的成功率，以及低一个到两个数量级的令牌使用量。
- [JetBrains Context: Repository Intelligence for Coding Agents](../Inbox/2026-07-21--jetbrains-context-repository-intelligence-for-coding-agents.md): 概述了语义代码仓库索引，以及据报告在交互轮数、延迟和成本方面的最大降幅。

### 失败成为路由和测试信号
执行结果正被用作控制输入，而不是最终结论。CodeRescue 在反思、重新规划和升级之间路由失败尝试；其经过校准的前沿上有一个点，在平均恢复成本仅为始终升级方案 35% 的情况下，成功率超过了始终升级方案。LISA 使用有效的 API 序列和基于文档的规约来发现不会导致崩溃的功能缺陷，在其评估中比 CITYWALK 多检测出 9 个重新引入的缺陷。这两项研究覆盖不同阶段，但都从运行时证据中提取了更多价值。CodeRescue 的保证适用于既定假设下的期望成本，而 LISA 仍要求开发者确认报告的候选缺陷。

#### 资料来源
- [CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents](../Inbox/2026-07-21--coderescue-budget-calibrated-recovery-routing-for-coding-agents.md): 报告了一个经过校准的路由点：在平均恢复成本为始终升级方案 35% 的情况下，其成功率超过始终升级方案。
- [LLM-Based Invariant Testing for Software Functional Bugs](../Inbox/2026-07-21--llm-based-invariant-testing-for-software-functional-bugs.md): 描述了规约引导的功能测试、多检测出的 9 个缺陷，以及需要开发者确认。

### 可执行基准揭示能力差距
新的代码评测强调全新的实例和可运行的正确性。Spaghetti Architect 生成经过预言机检查的五种语言程序，同时独立控制问题规模和表层混乱程度；在算术聚合任务上，随着内在规模增加，即使测试中最强的模型，其精确匹配准确率也降至零。SciCodePile 将一个 125GB 的科学代码语料库与 200 个可执行任务结合起来，其中评测中最强的模型达到的 Pass@1 也只有 12.30%。领域调优能够带来帮助——小模型的指令调优将 Pass@1 从 1.90% 提高到 9.10%——但该基准仅限于依赖项经过桩替换的纯 Python 函数。总体而言，这些结果表明，受控且可执行的测试仍明显比生成看似合理的代码更难。

#### 资料来源
- [Spaghetti Architect: A Contamination-Resistant, By-Construction-Labelled, Multi-Language Code Dataset Generator](../Inbox/2026-07-21--spaghetti-architect-a-contamination-resistant-by-construction-labelled-multi-language-code-dataset-generator.md): 详细说明了预言机验证、独立的难度控制，以及最强模型在规模扩大的算术聚合任务上准确率降至零的情况。
- [SciCodePile: A 128GB Corpus and Executable Benchmark for Challenging Scientific Code Generation](../Inbox/2026-07-21--scicodepile-a-128gb-corpus-and-executable-benchmark-for-challenging-scientific-code-generation.md): 报告了包含 200 个任务的可执行基准、12.30% 的最佳 Pass@1、调优收益和范围限制。
