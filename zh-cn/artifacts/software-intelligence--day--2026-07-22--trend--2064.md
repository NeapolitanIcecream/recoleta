---
kind: trend
trend_doc_id: 2064
granularity: day
period_start: '2026-07-22T00:00:00'
period_end: '2026-07-23T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u7A0B\u5E8F\u4FEE\u590D"
- "\u4EE3\u7801\u4F18\u5316"
- "\u6D4B\u8BD5\u751F\u6210"
- "\u4ED3\u5E93\u4E0A\u4E0B\u6587"
run_id: materialize-outputs
aliases:
- recoleta-trend-2064
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u7A0B\u5E8F\u4FEE\u590D"
- "topic/\u4EE3\u7801\u4F18\u5316"
- "topic/\u6D4B\u8BD5\u751F\u6210"
- "topic/\u4ED3\u5E93\u4E0A\u4E0B\u6587"
language_code: zh-CN
---

# 可执行反馈优于仅依赖提示的编码工作流

## 概览
近期关于编码代理控制机制的研究仍在推进，但今天的证据表明，控制信号正变得更加针对具体任务。性能分析器、变异补丁、静态分析和仓库上下文在循环中引导生成并验证结果。报告的收益幅度较大，但它们来自不同基准，不能据此确定某一种架构总体上更优。

## 研究发现

### 性能优化
当代理获得经过测量的运行时证据，而不是宽泛的指令时，仓库级优化效果更好。PerfAgent 使用采样性能分析器识别热点，验证每个补丁，并将加速结果反馈给代理，最多进行五轮。在 GPT-5.1 下，GSO 上与专家表现匹配的补丁比例从 19.6% 提升至 39.2%，SWE-efficiency-Lite 上则从 26% 提升至 74%。

MoST 提供了另一种互补的可执行指导。它将提交和技术文档中的优化知识转换为经过验证的 Semgrep 规则，其中包括跨语言和跨架构迁移的策略。在 351 个历史任务上，它生成的与开发者补丁完全匹配的补丁比 SemOpt 多 24.44%–180.00%。这些研究共同表明，相比无指导生成，针对具体任务的测量和经过验证的规则是更强的优化信号。

#### 资料来源
- [PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization](../Inbox/2026-07-22--perfagent-profiler-guided-iterative-refinement-for-repository-level-code-optimization.md): 报告了性能分析器指导的迭代、正确性验证，以及 GSO 和 SWE-efficiency-Lite 上与专家表现匹配的补丁比例。
- [Multi-Source and Cross-Scenario Strategy-Guided Code Optimization](../Inbox/2026-07-22--multi-source-and-cross-scenario-strategy-guided-code-optimization.md): 描述了跨来源策略提取、Semgrep 规则验证，以及 351 个任务上的开发者补丁匹配结果。

### 作为区分器的测试
测试生成的评判标准正转向测试能否将正确补丁与看似合理但错误的补丁区分开，而不只是测试能否运行。CoHarden 使用语义变异来检验生成的缺陷复现测试。严格测试使修复解决率提高 8.5 个百分点，而宽松测试没有带来提升，错位测试则使解决率下降 3.6 个百分点。

CATGen 处理的是更早出现的可靠性边界：在依赖复杂的项目中，生成的单元测试必须先通过编译，覆盖率才有意义。它检索项目和框架上下文，以确定性方式创建脚手架，并应用静态分析修复。在八个工业项目中，编译成功率提高了 24.72%–38.05%，而 token 使用量减少了 66.83%–83.86%。共同结果是，当确定性检查环绕模型生成过程时，测试产物会更有用。

#### 资料来源
- [Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes](../Inbox/2026-07-22--beyond-fail-to-pass-iterative-hardening-of-co-generated-bug-reproduction-tests-and-fixes.md): 区分了严格、宽松和错位的缺陷复现测试，并测量了它们对后续修复的不同影响。
- [Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation](../Inbox/2026-07-22--context-matters-improving-the-practical-reliability-of-llm-based-unit-test-generation.md): 报告了显式上下文和确定性修复带来的编译、覆盖率、生成时间及 token 使用量收益。

### 生成前置的仓库上下文
两个系统首先组装周围的软件上下文，以缩小生成范围。AutoGlue 在行为驱动开发步骤所属的场景中解释每个步骤，然后检索相关规格说明和项目 API。与少样本提示相比，它使 API F1 提高了 58.7%，但只有 46.1% 的输出可以直接使用。

CATGen 也会在要求模型完成固定的测试骨架之前，检索类结构、外部调用和测试框架。其工业项目结果表明，这种分工可以提高编译成功率，同时减少修复循环。现有证据仅覆盖面向 Java 的测试和胶水代码任务，因此更广泛的仓库编辑能力仍未得到证实。

#### 资料来源
- [Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development](../Inbox/2026-07-22--bridging-behavior-and-implementation-automated-java-glue-code-generation-for-behavior-driven-development.md): 在 1,307 个 Java 行为步骤对上评估了场景解释和面向项目的检索。
- [Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation](../Inbox/2026-07-22--context-matters-improving-the-practical-reliability-of-llm-based-unit-test-generation.md): 在专有 Java 项目和 Defects4J 上使用了五类项目上下文及确定性脚手架。
