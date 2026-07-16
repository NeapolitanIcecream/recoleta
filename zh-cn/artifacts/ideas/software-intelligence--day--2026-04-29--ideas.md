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

# LLM 辅助开发的代码责任

## 摘要
LLM 编码工作需要在紧急修复、类级评估任务和研究仓库中的公开声明上设更严的门槛。共同的压力是：模型生成或修改代码之后，谁来负责它的行为。

## 热修复拉取请求的测试覆盖和评审者分配检查
使用生产仓库中的编码代理的团队，应在 CI 和评审策略里单独加一条热修复路径。一个低成本做法是：如果 PR 关联的 issue 在 12 小时内创建，且 PR 在 24 小时内关闭或寻求合并，就把它标成可能的热修复，然后要求明确决定是否改测试、指定一名人类负责人，并为任何跳过的回归测试补一个后续 issue。

这种操作风险可以量化。在《Hot Fixing in the Wild》中，热修复比常规修复更小，涉及的评审者更少；在用 Qwen 标注的样本里，热修复 PR 修改测试的比例是 29.73%，而常规修复是 54.42%。同一项研究还发现，热修复的合并率更高，在 Qwen 标注子集中，机器人作者和人类作者的合并率也接近。这组结果说明，在生产压力最大的那类修复里，评审会出现空档。

### 资料来源
- [Hot Fixing in the Wild](../Inbox/2026-04-29--hot-fixing-in-the-wild.md): Summarizes the timing filters, manual validation, smaller PRs, fewer reviewers, lower test-edit rate, and higher merge rate for hot fixes.
- [Hot Fixing in the Wild](../Inbox/2026-04-29--hot-fixing-in-the-wild.md): The abstract reports hot fixes across more than 61,000 repositories and describes reduced collaboration, small targeted changes, limited review, and fewer test-file modifications.

## 带依赖错误标签的类级编码助手评估
评估编码助手的工程团队，应把类级任务加入内部测试集，尤其是那些包含共享状态、多方法调用和分散在多个方法中的领域逻辑的任务。一个有用的测试可以直接从现有内部类构建：把一个自包含类拆成规格和骨架，让助手重新生成，再运行原始测试，然后把失败标成逻辑、依赖、API 或语法错误。

ClassEval-Pro 给出了这类评估的具体目标形态。它的 300 个 Python 任务使用 11 个领域中的完整类，生成出来的类比旧的类级任务更大，也更连通。在五个 LLM 上，整体生成的 class-level Pass@1 只有 27.9% 到 45.6%。在 500 个人工标注失败里，逻辑错误占 56.2%，依赖错误占 38.0%，这把跨方法协作变成了助手上线时可以直接测量的点。

### 资料来源
- [ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation](../Inbox/2026-04-29--classeval-pro-a-cross-domain-benchmark-for-class-level-code-generation.md): Describes ClassEval-Pro’s 300 class-level tasks, task construction, Pass@1 range, and failure categories.
- [ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation](../Inbox/2026-04-29--classeval-pro-a-cross-domain-benchmark-for-class-level-code-generation.md): Reports bottom-up gains, compositional generation collapse, and the dominance of logic and dependency errors in manually annotated failures.

## 与基准输出绑定的 README 和论文声明检查
使用 LLM 共写代码和文档的研究软件团队，应把声明检查放进仓库工作流。一个可行做法是在合并前检查 README 或论文改动，要求每条新的性能、正确性或能力声明都链接到命令、基准输出、源文件或 issue 账本条目。没有证据的声明，可以在文本发布前先打开一个跟踪中的待办。

Comet-H 说明了为什么这层支持对长期的 LLM 辅助运行有用。控制器会重新读取工作区，追踪理论、仓库、公开声明、证据、效用假设和待解决义务，然后在论文或 README 变化时强制做 grounding 和审计。论文报告了 46 个研究软件仓库，以及一个深入的静态分析仓库在 90 个案例的基准上达到 F1 = 0.768，而次优基线是 0.364。对大多数团队来说，最值得保留的是这个流程：文档改动应带着证据一起提交。

### 资料来源
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): Summarizes Comet-H’s tracked workspace parts, grounding and audit steps, open obligations, and reported repository and benchmark results.
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): The abstract names hallucination accumulation and desynchronization between thesis, executable system, benchmark surface, and public claims.
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): Describes re-checking papers and READMEs against code and benchmarks and reports the 46-repository portfolio and static-analysis benchmark result.
