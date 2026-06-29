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

# 编码论文正在加入真实执行检查，并为长周期工作提供更好的把手

## Overview
4 月 20 日的编码研究最强的部分，是论文把系统和真实执行接得更紧。SolidCoder、OpenGame 和 OpenROAD 验证器都通过沙箱、浏览器或领域图检查行为，减少对表面正确输出的信任。另一条线规模更小，但也有用：测试放置方式和编辑历史都会影响开发者和模型能否保持工作可验证。

## Clusters

### Execution checks are moving earlier and getting more concrete
基于执行的编码是这一时期最清晰的信号。SolidCoder 用沙箱运行和基于性质的断言替代模型自检，然后保留修复过程中找到的每个失败测试。结果很具体：在 GPT-4o 上，pass@1 在 CodeContests 上达到 77.0%，高于 CodeSIM 的 72.7%；在 APPS 上达到 26.7%，高于 23.3%。消融中下降最大的是代码生成前的边界情况规划，去掉后 CodeContests 表现从 77.0% 降到 53.3%。代价是推理工作更多，所以这条路线更适合正确性比 token 预算更重要的场景。

#### Evidence
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): Summary with method and benchmark deltas for execution-backed coding

### Evaluation is expanding to interactive and domain-specific execution
有些论文已经把代码生成当作运行时系统问题，而不只是跟随提示词的任务。OpenGame 面向完整可玩的 2D 网页游戏，失败常来自场景连线、资源和跨文件状态。它的基准用无头浏览器执行，并评分 Build Health、Visual Usability 和 Intent Alignment；在 Claude Sonnet 4.6 下分别达到 72.4、67.2 和 65.1，每项都比使用同一模型的 Cursor 高约 6 分。在 EDA 方向，OpenROAD 验证器论文在执行前加入结构依赖图。单步任务上，它的通过率达到 82.5%，高于 tool-in-loop 调试的 76.0%，同时每个任务只用 1.00 次工具调用，而不是 1.77 次。多步任务上，报告的通过率从 30.0% 提升到 70.0%，再在轨迹级反思下到 84.0%。

#### Evidence
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): Summary with OpenGame method and benchmark results
- [Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging](../Inbox/2026-04-20--structural-verification-for-reliable-eda-code-generation-without-tool-in-the-loop-debugging.md): Summary with structural verification and OpenROAD efficiency gains

### Prompt-adjacent code structure affects what models keep and pass
测试格式本身开始成为模型的真实控制面。doctest 研究把内联 Python 测试和分离的 Rust 测试块放在 830+ 个生成文件和 12 个模型上比较。内联测试在生成后保留的概率高得多：在提示词提供 doctest 的情况下，除 Claude 3.5 Haiku 外，所有模型的保留率都是 100%，正确率也维持在 92–99% 区间。Rust 的结果更不稳定。有些 Claude 模型能保留并通过所有测试，但几个 Opus 版本会通过删掉所有测试块把保留率降到 0%。论文还报告说，即使 temperature 设为 0，确定性仍有缺口；在引用设置里，Mistral Medium 是 0%，Claude Opus 4.6 是 30–64%。这让提示词和文件结构成了可靠性的一部分，而不只是模型选择。

#### Evidence
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): Summary with preservation, correctness, and determinism findings

### Workflow control and provenance remain active, with lighter empirical support
接口层也在受到关注，不过这里的证据更偏定性。EvoGraph 在 VS Code 里把 AI 提示词和代码编辑记录成一个分支图，开发者可以回看、比较并合并不同路径。论文在 20 名参与者的研究中报告说，它更好地支持探索、提示词管理和追踪 AI 生成的变更，而且与基线界面相比，报告的认知负担更低。另一篇理论论文主张，多智能体编码应该在仓库规模上研究，因为即使局部任务看起来正确，交互效应也会拖坏代码库。这个判断在这一时期没有新的实验支持，但它和当天更大的重点一致：可追踪性、协作和围绕代理工作的系统级检查。

#### Evidence
- [Choose Your Own Adventure: Non-Linear AI-Assisted Programming with EvoGraph](../Inbox/2026-04-20--choose-your-own-adventure-non-linear-ai-assisted-programming-with-evograph.md): Summary with user study scope and reported workflow effects
- [More Is Different: Toward a Theory of Emergence in AI-Native Software Ecosystems](../Inbox/2026-04-20--more-is-different-toward-a-theory-of-emergence-in-ai-native-software-ecosystems.md): Summary with theory claim and cited system-level failure evidence
