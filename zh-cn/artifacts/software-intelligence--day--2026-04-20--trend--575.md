---
kind: trend
trend_doc_id: 575
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
topics:
- coding-agents
- execution-verification
- interactive-code-generation
- test-structure
- developer-tools
run_id: materialize-outputs
aliases:
- recoleta-trend-575
tags:
- recoleta/trend
- topic/coding-agents
- topic/execution-verification
- topic/interactive-code-generation
- topic/test-structure
- topic/developer-tools
language_code: zh-CN
---

# 代码研究论文正在加入真实执行检查，并为长周期工作提供更好的控制点

## Overview
4 月 20 日的代码研究里，最强的结果来自那些把论文工作更直接地接到真实执行上的方法。SolidCoder、OpenGame 和 OpenROAD verifier 都通过检查沙箱、浏览器或领域图中的实际行为，降低了人们对表面上看似正确输出的信任。第二条线索规模更小，但有实际价值：测试放置方式和编辑历史都会影响开发者和模型能否让工作保持可验证。

## Clusters

### 执行检查正在前移，也变得更具体
这一时期最明确的信号是由执行结果支撑的代码生成。SolidCoder 用沙箱运行和基于性质的断言替代模型自检，并在修复过程中保留发现的每一个失败测试。改进很具体：在 GPT-4o 上，CodeContests 的 pass@1 达到 77.0%，高于 CodeSIM 的 72.7%；APPS 上为 26.7%，而 CodeSIM 为 23.3%。消融实验里影响最大的是代码生成前的边界情况规划，移除后 CodeContests 表现会从 77.0% 降到 53.3%。代价是推理开销更高，所以在正确性比 token 预算更重要的场景中，这条路线更有吸引力。

#### Evidence
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): 关于执行支撑代码生成的方法与基准变化的摘要

### 评估正在扩展到交互式执行和特定领域执行
有些论文现在把代码生成当作运行时系统问题，而不只是提示跟随任务。OpenGame 面向可完整运行的 2D 网页游戏，这类任务的失败通常来自场景连接、资源文件和跨文件状态。它的基准通过无头浏览器执行来评估，并打分 Build Health、Visual Usability 和 Intent Alignment；使用 Claude Sonnet 4.6 时，分数分别达到 72.4、67.2 和 65.1，在每项指标上都比使用同一模型的 Cursor 高约 6 分。在 EDA 领域，OpenROAD verifier 论文在执行前加入了结构依赖图。在单步任务上，它的通过率达到 82.5%，高于 tool-in-loop debugging 的 76.0%，同时每个任务只需 1.00 次工具调用，而不是 1.77 次。在多步任务上，文中报告的通过率从 30.0% 提高到 70.0%，再借助 trajectory-level reflection 提高到 84.0%。

#### Evidence
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): 包含 OpenGame 方法和基准结果的摘要
- [Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging](../Inbox/2026-04-20--structural-verification-for-reliable-eda-code-generation-without-tool-in-the-loop-debugging.md): 包含结构验证和 OpenROAD 效率提升的摘要

### 靠近提示的代码结构会影响模型保留和通过哪些内容
测试格式本身正在成为一个真实的模型控制面。doctest 研究比较了内联 Python 测试和分离的 Rust 测试块，覆盖 830 多个生成文件和 12 个模型。内联测试更容易在生成过程中被保留下来：在提示中提供 doctest 时，除了 Claude 3.5 Haiku 之外，所有模型的保留率都是 100%，正确率保持在 92–99% 区间。Rust 的结果更不稳定。有些 Claude 模型保留并通过了全部测试，而几个 Opus 版本会通过删除所有测试块把保留率降到 0%。论文还报告，temperature 0 仍然存在确定性缺口，在文中设置下，Mistral Medium 为 0%，Claude Opus 4.6 为 30–64%。这说明可靠性不只取决于模型选择，提示和文件结构也会影响结果。

#### Evidence
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): 包含保留率、正确率和确定性结果的摘要

### 工作流控制和来源追踪仍然活跃，但实证支持较弱
接口层也在受到关注，不过这里的证据更偏定性。EvoGraph 在 VS Code 中把 AI 提示和代码编辑记录为分支图，开发者可以回看、比较并合并不同路径。在一项有 20 名参与者的研究中，论文报告说，它在探索、提示管理和跟踪 AI 生成修改方面支持更好，而且报告的认知负担低于基线界面。另一篇理论论文认为，多智能体编程应在仓库尺度上研究，因为交互效应即使在局部任务看起来正确时，也会让代码库变差。这个说法在这一时期没有新的实验支持，但它与当天更广泛的关注点一致：围绕 agent 工作的可追溯性、协同和系统级检查。

#### Evidence
- [Choose Your Own Adventure: Non-Linear AI-Assisted Programming with EvoGraph](../Inbox/2026-04-20--choose-your-own-adventure-non-linear-ai-assisted-programming-with-evograph.md): 包含用户研究范围和报告工作流影响的摘要
- [More Is Different: Toward a Theory of Emergence in AI-Native Software Ecosystems](../Inbox/2026-04-20--more-is-different-toward-a-theory-of-emergence-in-ai-native-software-ecosystems.md): 包含理论主张和所引系统级失败证据的摘要
