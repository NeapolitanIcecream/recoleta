---
kind: ideas
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- execution-verification
- interactive-code-generation
- test-structure
- developer-tools
tags:
- recoleta/ideas
- topic/coding-agents
- topic/execution-verification
- topic/interactive-code-generation
- topic/test-structure
- topic/developer-tools
language_code: zh-CN
---

# Execution-verified coding workflows

## Summary
有执行验证的编码工作已经具体到足以支持明确的产品和流程改动。这里最清楚的几类是：把边界情况捕捉前置并配合沙箱回归检查、给交互式前端输出加浏览器运行后的接受检查，以及用内联测试处理来提高助手保留并通过提示测试的概率。

## Pre-write edge-case capture with sandboxed regression checks for high-risk code
在代码助手写第一行之前先问边界情况，这种做法在错误代价高的流程里已经更实用。SolidCoder 说明了最明显的切入点：去掉边界情况规划步骤后，GPT-4o 在 CodeContests 上的 pass@1 从 77.0% 降到 53.3%，损失比去掉后续修复步骤更大。同一篇论文把前置规划和基于性质的断言、沙箱执行、以及修复过程中发现的每个失败测试都保留下来结合在一起。

这里的方案很窄，也容易验证：在 IDE 或 PR 机器人里给容易出错的函数加一个写代码前的边界情况面板，然后自动生成性质检查，并在每次模型改动后保留不断增长的回归测试集。维护解析器、数据转换、定价逻辑和 API 适配器的团队会先受益，因为他们本来就要为合并后才暴露的边界错误付出成本。一个低成本验证方法是把这套流程跑在一组固定的线上缺陷工单上，把首次通过率和缺陷回流率和普通的只靠提示词助手做对比。代价是 token 和 API 用量更高，所以它更适合需要审查的关键代码路径，而不是常规样板代码。

### Evidence
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): Reports the execution-backed pipeline, pass@1 gains, and the large ablation drop from removing shift-left edge-case planning.
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): Abstract confirms the paper's core claim that sandboxed execution and pre-generation edge-case awareness close model planning and verification failures.

## Headless-browser acceptance checks for agent-built front-end flows
现在，构建交互式网页产品的团队可以用浏览器运行后的健康检查来评估代理输出，而不只看编译状态和人工抽查。OpenGame 很适合作为模板，因为它把生成的软件当作运行中的系统来处理：它使用可复用的项目骨架、保存下来的调试协议和重复的无头验证，然后把输出按 Build Health、Visual Usability 和 Intent Alignment 打分。在 150 个提示上，使用 Claude Sonnet 4.6 的 OpenGame 在每项指标上都比同样模型下的 Cursor 高大约 6 分。

具体的流程改动，是给生成仪表盘、微站、引导流程或轻量教育模拟的内部工具加一个由浏览器执行的评分卡。第一版不需要完整的游戏生成，只需要页面加载检查、控制台错误捕获、可见元素断言，以及一个简单规则来判断交互后输出是否符合请求。最直接的用户，是那些已经在演示代理生成的前端工作、又在文件、资源和状态之间的连线问题上反复出错的团队。一个低成本检查方法是挑一批最近的前端任务，每个任务运行助手 3 次，然后比较在加入浏览器执行和一个小修复循环前后的接受率。

### Evidence
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): Summarizes the OpenGame workflow, the headless-browser benchmark, and the metric gains over Cursor using the same model.
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): Abstract text states that interactive playability needs runtime verification and describes the evaluation pipeline built around headless browser execution and judged user-visible quality.

## Inline test rewrites before code generation
当团队希望助手在生成和编辑过程中把测试原样保留下来时，测试最好和生成代码放在一起。那篇 doctest 研究把这件事变成了操作问题，而不是风格问题。在 830 多个生成文件和 12 个模型上，内联 Python doctest 几乎总能被保留，而且正确率很高；分离的 Rust `#[test]` 块则让不同模型之间差异很大，其中几个 Claude Opus 版本把所有提供的测试块都删掉了。同一项研究还显示，temperature 0 也不能保证输出可重复。

一个实用做法是做一个仓库辅助工具，在模型调用前把生成提示和临时工作文件改写成内联测试形式，等通过后再展开回团队偏好的测试布局。这对脚手架生成、工具函数和迁移脚本最相关，因为这些场景里团队本来就会一次性要求模型给出实现和测试。低成本检查很简单：选一个任务族，在团队使用的模型上分别用内联测试和分离测试跑同样的提示，测测试保留率、通过率，以及多次 temperature 0 运行后的输出稳定性。如果某个模型总是在删测试，问题可能先在提示结构，而不是模型质量。

### Evidence
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): Gives the main empirical result that inline doctests preserve and pass far more reliably than separated test blocks.
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): Abstract content states the 830-plus file study, the preservation and correctness gap, and the lack of determinism even at temperature 0.
