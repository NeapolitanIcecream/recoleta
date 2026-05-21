---
kind: ideas
granularity: day
period_start: '2026-04-29T00:00:00'
period_end: '2026-04-30T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- LLM coding
- software engineering
- code generation benchmarks
- agent orchestration
- hot fixes
- AI education
- service recommendation
tags:
- recoleta/ideas
- topic/llm-coding
- topic/software-engineering
- topic/code-generation-benchmarks
- topic/agent-orchestration
- topic/hot-fixes
- topic/ai-education
- topic/service-recommendation
language_code: zh-CN
---

# LLM 辅助开发中的代码责任

## Summary
LLM 编码工作需要围绕紧急修复、类规模评估任务和研究仓库中的公开声明设置更严格的关口。共同压力在于：模型生成或修改代码后，团队仍要对代码行为负责。

## 针对测试覆盖率和评审者分配的热修复拉取请求检查
在生产仓库中使用编码代理的团队，应在 CI 和评审策略中加入单独的热修复路径。一个低成本做法是：当某个 PR 关联到过去 12 小时内创建的 issue，并且在 24 小时内关闭或请求合并时，将其标记为可能的热修复；随后要求给出明确的测试变更决定、指定一名人类负责人，并为任何跳过的回归测试创建后续 issue。

这种运营风险可以衡量。在 Hot Fixing in the Wild 中，热修复比常规修复更小，参与评审的人更少；Qwen 标记的热修复中，29.73% 的 PR 修改了测试，而常规修复为 54.42%。同一研究还发现，热修复的合并率更高，包括在 Qwen 标记的子集中，bot 作者和人类作者的合并率相近。这一组合说明，在生产压力最高的修复场景中存在评审缺口。

### Evidence
- [Hot Fixing in the Wild](../Inbox/2026-04-29--hot-fixing-in-the-wild.md): 概述了热修复的时间过滤条件、人工验证、更小的 PR、更少的评审者、更低的测试编辑率和更高的合并率。
- [Hot Fixing in the Wild](../Inbox/2026-04-29--hot-fixing-in-the-wild.md): 摘要报告了超过 61,000 个仓库中的热修复，并描述了协作减少、变更小且有针对性、评审有限以及测试文件修改更少。

## 带依赖错误标签的类级编码助手评估
评估编码助手的工程团队，应在内部测试套件中加入类级任务，尤其是包含共享状态、方法调用，以及分布在多个方法中的领域逻辑的任务。这个测试可以用现有内部类构建，规模不必大：把一个自包含类拆成规格说明和骨架，让助手重新生成它，运行原始测试，然后把失败标注为逻辑、依赖、API 或语法失败。

ClassEval-Pro 为这类评估给出了具体目标形态。它的 300 个 Python 任务使用横跨 11 个领域的完整类，生成的类比旧的类级任务更大、连接更多。五个 LLM 的整体生成结果中，类级 Pass@1 只有 27.9% 到 45.6%。在 500 个手工标注的失败中，逻辑错误占 56.2%，依赖错误占 38.0%；因此，跨方法协调是助手上线时可以实际测量的一项指标。

### Evidence
- [ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation](../Inbox/2026-04-29--classeval-pro-a-cross-domain-benchmark-for-class-level-code-generation.md): 描述了 ClassEval-Pro 的 300 个类级任务、任务构建方式、Pass@1 范围和失败类别。
- [ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation](../Inbox/2026-04-29--classeval-pro-a-cross-domain-benchmark-for-class-level-code-generation.md): 报告了自底向上生成带来的提升、组合式生成的下降，以及手工标注失败中逻辑错误和依赖错误占主导。

## 与基准输出绑定的 README 和论文声明检查
使用 LLM 协同编写代码和文档的研究软件团队，应把声明检查放进仓库工作流。一个可行实现是在合并前检查 README 或论文变更，要求每条新的性能、正确性或能力声明链接到命令、基准输出、源文件或 issue 台账条目。缺少证据的声明可以在文本发布前创建一个受跟踪的待办项。

Comet-H 说明了为什么这类支持层对长时间 LLM 辅助运行有用。控制器会重新读取工作区，跟踪理论、仓库、公开声明、证据、效用假设和未完成义务；当论文或 README 发生变化时，它会强制执行溯源和审计。论文报告了 46 个研究软件仓库，并且一个深入分析的静态分析仓库在 90 个案例的基准上达到 F1 = 0.768，而次优基线为 0.364。对大多数团队来说，可发布、可复用的部分是这套工作流：文档变更应随附对应证据。

### Evidence
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): 概述了 Comet-H 跟踪的工作区组成部分、溯源和审计步骤、未完成义务，以及报告的仓库和基准结果。
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): 摘要指出了幻觉累积，以及论点、可执行系统、基准表面和公开声明之间的不同步。
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): 描述了根据代码和基准重新检查论文与 README，并报告了 46 个仓库的组合以及静态分析基准结果。
