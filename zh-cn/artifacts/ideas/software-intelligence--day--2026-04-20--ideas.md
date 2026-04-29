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

# 经执行验证的编码工作流

## Summary
基于执行验证的编码工作，已经具体到足以支持明确的产品和流程改动。这里最清楚的几个方向是：与沙箱回归检查配套的前置边界情况捕获、面向交互式前端输出的浏览器运行验收检查，以及通过内联测试处理来提高助手保留并通过提示测试的概率。

## 面向高风险代码的编写前边界情况捕获与沙箱回归检查
对于错误代价高的工作流，一种在写下第一行代码前先询问边界情况的代码助手，现在已经很有落地性。SolidCoder 给出了最清楚的发力点：去掉边界情况规划这一步，会让 GPT-4o 在 CodeContests 上的 pass@1 从 77.0% 降到 53.3%，损失远大于去掉后续修复步骤。该论文还把这种前置规划与基于性质的断言、沙箱执行，以及在修复过程中保留每一个失败测试结合在一起。

这里的实现范围很窄，也容易验证：在 IDE 或 PR 机器人里，为容易出错的函数加入一个编写前的边界情况面板，然后自动生成性质检查，并在每次模型版本更新时保留一个持续增长的回归测试集。维护解析器、数据转换、定价逻辑和 API 适配器的团队会最先在意，因为他们已经在为合并后暴露出的隐藏边界条件故障付出代价。一个低成本验证办法是，把这套流程跑在一组固定的生产缺陷工单上，对比它和标准的仅提示词助手在首次正确率以及缺陷复发率上的差异。代价是 token 和 API 使用量更高，因此它更适合审查要求高的代码路径，不太适合常规样板代码。

### Evidence
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): 报告了基于执行的流水线、pass@1 提升，以及去掉前置边界情况规划后出现的大幅消融下降。
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): 摘要确认了论文的核心观点：沙箱执行和生成前的边界情况识别能够弥合模型在规划和验证上的失误。

## 针对 agent 构建前端流程的无头浏览器验收检查
构建交互式 Web 产品的团队，现在可以用浏览器运行的健康检查来评估 agent 输出，而不是只看编译状态和人工抽查。OpenGame 是个有用的模板，因为它把生成的软件当作正在运行的系统来处理：它使用可复用的项目骨架、已保存的调试协议和反复的无头验证，然后从 Build Health、Visual Usability 和 Intent Alignment 三个指标给输出打分。在 150 个提示上，使用 Claude Sonnet 4.6 的 OpenGame 在每个指标上都比使用同一模型的 Cursor 高约 6 分。

一个直接的流程改动，是把浏览器执行的评分卡加入生成仪表盘、微型站点、引导流程或轻量教育模拟的内部工具。第一版不需要完整的游戏生成。它需要页面加载检查、控制台错误捕获、可见元素断言，以及一个用于判断交互后输出是否符合请求的简单评分规则。最直接的用户，是那些已经在演示 agent 生成前端工作、但还在处理跨文件、资源和状态连接出错的团队。一个低成本检查办法是，取最近一批前端任务积压，对每个任务运行三次助手，对比加入浏览器执行和一个小型修复循环前后的验收率。

### Evidence
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): 总结了 OpenGame 的工作流、无头浏览器基准，以及它在使用同一模型时相对 Cursor 的指标提升。
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): 摘要说明交互式可玩性需要运行时验证，并描述了围绕无头浏览器执行和对用户可见质量进行判断而建立的评估流水线。

## 代码生成前先做内联测试改写
如果团队希望助手在生成和编辑过程中保留提示中给出的测试，那么这些测试应该放在生成代码旁边。doctest 研究把这件事变成了一个操作问题，而不是风格问题。在 830 多个生成文件和 12 个模型上，内联的 Python doctest 几乎都能被完整保留，而且正确率也很高；分离的 Rust 测试块则在不同模型之间出现很大波动，其中几个 Claude Opus 版本甚至删除了所有提供的测试块。同一研究还显示，temperature 0 并不能保证输出可重复。

一个实用做法，是做一个仓库辅助工具：在调用模型前，把生成提示和临时工作文件改写成内联测试形式，等通过验收后，再展开回团队偏好的测试布局。这最适合脚手架生成、工具函数和迁移脚本，因为团队本来就会在一次调用里要求模型同时生成实现和测试。低成本检查很简单：选一个任务类别，在团队实际使用的模型上，用相同提示分别跑内联测试和分离测试，然后在多次 temperature-0 运行中衡量测试保留率、通过率和输出稳定性。如果某个模型总是在丢测试，问题可能先出在提示结构，而不是模型质量。

### Evidence
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): 给出了主要实证结果：与分离测试块相比，内联 doctest 在保留和通过上要稳定得多。
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): 摘要内容说明了 830 多个文件的研究、保留率与正确率差距，以及即使在 temperature 0 下也缺乏确定性。
