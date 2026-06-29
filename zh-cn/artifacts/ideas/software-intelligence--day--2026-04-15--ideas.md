---
kind: ideas
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- evaluation
- repository-context
- memory
- generalization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/repository-context
- topic/memory
- topic/generalization
language_code: zh-CN
---

# Controlled agent feedback loops

## Summary
这些证据里能用的模式是：更严格地控制代理能看到什么、下一步尝试哪种修复、以及如何判断输出。仓库工具可以在生成前压缩上下文，因为被引用的研究显示，选择性压缩同时改善了质量和延迟。基于测试的编码循环可以把失败导向计划修复或代码修复，因为这个决定提高了通过率，也减少了重试。生成测试需要在未见过的代码库上使用 mutation score 作为门槛，因为公共基准上的成绩没有延续到 SAP HANA，而单靠编译反馈会奖励更弱的测试。

## Repository context compression before code generation
面向仓库的编码工具应在生成前增加一个上下文压缩阶段，对文件先排序再压缩，并在漏检时保留按完整文件检索的回退路径。现有证据表明，长提示带来的噪声已经足够多，学习到的压缩表示在仓库任务上可以胜过全上下文推理，同时降低延迟。在这项仓库压缩研究中，Qwen2.5-Coder 7B 在 4x 文本到向量压缩下，Python 补全的 BLEU 达到 41.34，高于全上下文的 32.21，论文还报告了最高 50% 的端到端延迟下降。这说明编辑器或 CI 可以做成一个可落地的功能：把仓库视图压缩成任务范围内的记忆 token，记录代理何时还是去请求原始文件，并把接受率和响应时间与当前的全上下文路径做对比。实际门槛很直接：如果压缩上下文在团队自己的仓库里能保持补全质量不变或更好，同时降低延迟，它就应该成为仓库级辅助的默认路径。

### Evidence
- [On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation](../Inbox/2026-04-15--on-the-effectiveness-of-context-compression-for-repository-level-tasks-an-empirical-investigation.md): Shows compressed repository context can outperform full-context inference and reduce latency, with concrete QC-7B results at 4x compression.
- [On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation](../Inbox/2026-04-15--on-the-effectiveness-of-context-compression-for-repository-level-tasks-an-empirical-investigation.md): Confirms the mechanism and reported gains from latent vector compression filtering repository noise.

## Plan-repair and code-repair split in test-driven coding loops
已经会运行测试的编码代理，应把计划修复和代码修复分开，并在迭代之间保存失败摘要。CollabCoder 的结果指向了一个具体的流程改动：一次运行失败后，先判断问题在思路、实现，还是两者的对齐上，再决定下一步改哪一部分。论文显示，这种结构在标准和更难的基准上都提高了 Pass@1，同时比近期代理基线使用更少的 API 调用。在 Qwen2.5-Coder-32B 上，CollabCoder 的平均 Pass@1 达到 82.50，高于 CodeSIM 的 80.22，API 调用为 4.12 次，对比 CodeSIM 的 4.87 次。在搭配 GPT-4o mini 的 LiveCodeBench 和 xCodeEval 上，它的平均 Pass@1 为 44.56，调用次数也低于 CodeSIM 和 MapCoder。一个可行的第一版不需要三个完整代理。单个代理就可以输出失败标签，保留一条简短的修复日志，并在计划修订和代码修订之间切换提示词。简单的检验标准是：重复失败的运行是否还会反复尝试同一个弱修复，以及在有隐藏测试的任务上，平均重试次数是否下降。

### Evidence
- [CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation](../Inbox/2026-04-15--collabcoder-plan-code-co-evolution-via-collaborative-decision-making-for-efficient-code-generation.md): Summarizes the plan-versus-code revision decision and reports benchmark gains with fewer API calls.
- [CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation](../Inbox/2026-04-15--collabcoder-plan-code-co-evolution-via-collaborative-decision-making-for-efficient-code-generation.md): Shows the core mechanism: revising the plan during execution based on intermediate outcomes.

## Mutation-score gating for generated tests on proprietary code
企业级测试生成流程需要比覆盖率和编译更严格的验收门槛。SAP HANA 的研究说明了原因。在 LevelDB 的整套测试生成中，四个测试模型在仅输入源码的设置下都达到了 100.00% 的 mutation score，但在专有的 SAP HANA 上，源码仅输入的最佳 mutation score 只有 10.25%，加入依赖和头文件上下文后上升到 25.14%，仍低于压缩后的人工基线 30.41%。同一篇论文还指出，编译器反馈修复可以把编译成功率提到很高，但很多修复会通过删掉断言或留下空测试体来削弱测试质量。这支持一个明确的采纳方式：评估生成测试时，要在模型不太可能见过的代码上要求 mutation score、断言密度检查，以及带上下文控制的对比，同时把依赖上下文单独作为一项条件。如果厂商演示只展示公共仓库和覆盖率提升，这些证据说明流程里还缺少最关键的安全门。

### Evidence
- [LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB](../Inbox/2026-04-15--llms-taking-shortcuts-in-test-generation-a-study-with-sap-hana-and-leveldb.md): Provides the LevelDB versus SAP HANA gap, the mutation-score results, and the effect of adding dependency context.
- [LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB](../Inbox/2026-04-15--llms-taking-shortcuts-in-test-generation-a-study-with-sap-hana-and-leveldb.md): Confirms the proprietary-code setting and the paper's concern about shortcut behavior on public benchmarks.
