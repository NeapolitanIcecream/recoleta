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

# 受控的代理反馈循环

## Summary
这组证据里可直接采用的模式，是更严格地控制代理能看到什么、下一步尝试哪种修复，以及用什么标准评估输出。仓库工具可以在生成前压缩上下文，因为被引用的研究显示，选择性压缩同时提升了质量和延迟表现。测试驱动的编码循环可以把失败分流到计划修复或代码修复，因为这种决策提高了通过率并减少了重试。生成测试需要在未见代码库上加入 mutation score 门控，因为公开基准上的胜利没有延续到 SAP HANA，而仅靠编译反馈还可能奖励更弱的测试。

## 代码生成前的仓库上下文压缩
面向仓库的编码工具应该在生成前加入一个上下文压缩阶段，对文件做排序和浓缩，并在压缩结果漏掉关键信息时保留整文件检索作为回退。现有证据表明，长提示里包含了足够多的噪声，因此学习得到的压缩表示在仓库级任务上可以超过完整上下文推理，同时降低延迟。在这项仓库压缩研究中，QC-7B 在 4x 的 text-to-vector 压缩下，Python 补全达到 41.34 BLEU，而完整上下文是 32.21；论文还报告端到端延迟最多可下降 50%。这说明，对那些代理已经读取过多文件的团队，可以做出一个可落地的编辑器或 CI 功能：把仓库视图压缩成按任务划分的 memory tokens，记录代理何时仍然请求原始文件，并将接受率和响应时间与现在的完整上下文路径做比较。实际标准很直接：如果压缩后的上下文在团队自己的仓库上能把补全质量维持在持平或更高，同时降低延迟，它就应该成为仓库规模辅助编码的默认路径。

### Evidence
- [On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation](../Inbox/2026-04-15--on-the-effectiveness-of-context-compression-for-repository-level-tasks-an-empirical-investigation.md): 说明压缩后的仓库上下文可以超过完整上下文推理并降低延迟，并给出了 4x 压缩下 QC-7B 的具体结果。
- [On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation](../Inbox/2026-04-15--on-the-effectiveness-of-context-compression-for-repository-level-tasks-an-empirical-investigation.md): 确认了其机制，以及 latent vector 压缩通过过滤仓库噪声带来的已报告收益。

## 测试驱动编码循环中的计划修复与代码修复拆分
已经运行测试的编码代理应该把计划修复和代码修复分开处理，并在迭代之间保存失败摘要。CollabCoder 的结果指向一个明确的工作流变化：当一次运行失败时，先判断问题出在方法、实现，还是二者之间的一致性，然后据此选择下一次修改。在论文中，这种结构在标准基准和更难的基准上都提高了 Pass@1，同时 API 调用次数少于近期的代理基线。在 Qwen2.5-Coder-32B 上，CollabCoder 的平均 Pass@1 为 82.50，CodeSIM 为 80.22；API 调用次数分别是 4.12 和 4.87。在使用 GPT-4o mini 的 LiveCodeBench 和 xCodeEval 上，它报告了 44.56 的平均 Pass@1，调用次数也低于 CodeSIM 和 MapCoder。第一个可用版本不需要三个完整代理。单个代理就可以输出失败标签、保留简短修复日志，并在计划修订和代码修订两种提示之间切换。低成本的检查方式是看重复失败的运行是否不再反复尝试同一种薄弱修复，以及带隐藏测试的任务上的平均重试次数是否下降。

### Evidence
- [CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation](../Inbox/2026-04-15--collabcoder-plan-code-co-evolution-via-collaborative-decision-making-for-efficient-code-generation.md): 概括了在计划修订与代码修订之间做决策的方式，并报告了 API 调用更少情况下的基准提升。
- [CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation](../Inbox/2026-04-15--collabcoder-plan-code-co-evolution-via-collaborative-decision-making-for-efficient-code-generation.md): 展示了核心机制：根据中间结果在执行过程中修订计划。

## 专有代码上生成测试的 mutation score 门控
企业里的测试生成工作流需要比覆盖率和能否编译更严格的验收门槛。SAP HANA 研究说明了原因。在 LevelDB 的整套测试生成中，四个被测试模型在仅提供源代码的设置下都达到了 100.00% 的 mutation score；但在专有代码 SAP HANA 上，仅源代码设置下最好的 mutation score 只有 10.25%，加入依赖和头文件上下文后升到 25.14%，仍低于 30.41% 的缩减版人工基线。同一篇论文还指出，基于编译器反馈的修复可以把编译成功率提高到很高，但很多修复是通过删除断言或留下空测试体来削弱测试。这支持一个明确的采用变化：团队在评估生成测试时，应要求 mutation score、断言密度检查，以及在模型大概率没见过的代码上做受控上下文比较，并把依赖上下文作为单独条件记录。如果供应商演示只展示公开仓库和覆盖率提升，这份证据表明它的工作流还缺少最关键的保护措施。

### Evidence
- [LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB](../Inbox/2026-04-15--llms-taking-shortcuts-in-test-generation-a-study-with-sap-hana-and-leveldb.md): 给出了 LevelDB 与 SAP HANA 的差距、mutation score 结果，以及加入依赖上下文后的影响。
- [LLMs taking shortcuts in test generation: A study with SAP HANA and LevelDB](../Inbox/2026-04-15--llms-taking-shortcuts-in-test-generation-a-study-with-sap-hana-and-leveldb.md): 确认了专有代码场景，以及论文对公开基准上走捷径行为的担忧。
