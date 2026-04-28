---
kind: ideas
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- evaluation
- repository-context
- multi-agent-workflows
- code-editing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/repository-context
- topic/multi-agent-workflows
- topic/code-editing
language_code: zh-CN
---

# 以仓库为依据的代码审查

## Summary
当前的编码代理研究指向三个明确变化：在 pull-request 审查中加入可执行规格检查，在评估中加入仓库上下文推理 trace，并在进行大范围模型搜索前，先通过 IDE 和语言服务器工具处理跨文件后续编辑。共同模式很直接：仓库级证据暴露出了最终补丁评分和局部编辑流程仍然会漏掉的失败。

## 用于可执行前置条件和后置条件的 Pull Request 检查
评估编码代理的团队可以在面向仓库任务的审查流程中加入可执行规格检查。CodeSpecBench 说明了原因：函数级规格生成的 pass rate 可达 47.0%，但在 500 个 SWE-bench Verified 问题上的仓库级表现中，最佳模型也只到 20.2%。这个差距指向了生产代码审查中的一个具体失效模式：代理可能生成一个看起来合理的补丁，但没有抓住预期的输入约束、状态假设或输出保证。

一个可行的实现方式是在 CI 中加入一步：让模型为 pull request 涉及的函数生成 preconditions 和 postconditions，用现有测试和生成测试来运行这些检查，并把不匹配的地方标出来供审查者查看。这很适合已经在 Python 服务或库中使用代理编写补丁的团队，因为输出结果可执行，而且可以用他们现在已经信任的同一套测试 harness 来检查。一个低成本试点是：在一个仓库的 bug-fix PR 上做一周试验，记录在补丁在审查中看起来仍然可接受的情况下，生成规格有多常失败，以及这些失败是否比现有测试更早暴露出隐藏的语义回归。

### Evidence
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): CodeSpecBench 提供了仓库级规格生成结果、基于执行的评估设计，以及 20.2% 的仓库 pass-rate 上限，这些都支持在 PR 审查中加入规格检查。

## 用于编码代理评估的仓库上下文输入与输出预测评测集
仓库基准不该只依赖最终补丁是否成功，还可以加入基于真实代码路径构建的输入预测和输出预测任务。R²Eval 显示了当评估停留在简短的独立代码片段上时，这个盲点有多大：平均输入预测准确率从 CRUXEval 上的 81.23% 降到真实仓库问题上的 16.91%，输出预测则从 80.37% 降到 28.15%。这个基准还会保留复杂运行时对象的原貌：先把复合类型和自定义类型序列化，再把预测结果反序列化回对象，用基于测试的方式评分。

这支持一种明确的流程调整，适用于模型厂商、内部评测团队，以及采购编码代理的企业：在扩大部署前，先加入一个小型的仓库上下文推理评测集。这个评测集不需要很大。只要从一个生产服务里选几十个带追踪的方法，配上序列化后的输入和预期输出，就能看出模型是否能跟住项目状态、依赖关系和大量对象参与的 API。一个低成本检查方式是：从最近的事故或不稳定修复中抽样方法，把这些 trace 上的得分与当前偏重代码片段的评测结果对比。如果同一个模型只在简单集合上表现强，部署风险就已经很明显了。

### Evidence
- [Evaluating LLMs Code Reasoning Under Real-World Context](../Inbox/2026-04-14--evaluating-llms-code-reasoning-under-real-world-context.md): R²Eval 提供了真实仓库中的输入/输出预测设置、对象序列化方法，以及从代码片段基准到仓库上下文推理时表现大幅下降的测量结果。

## 面向跨文件变更的工具路由后续编辑
跨文件编辑助手可以先把明显的结构性修改交给 IDE 和语言服务器工具处理，再让模型搜索代码库，这样能提高建议被接受的比例。TRACE 给出了一个具体模式：判断当前改动是否像 rename、signature update、clone update 或 diagnose-fix 这类情况，调用 rename 和 def-use analysis 等工具收集编辑位置，然后再让模型处理剩余的语义编辑。在 678 个项目的 38K 次提交上，这种方法相比此前系统把编辑定位 precision 提高了 43.76%，recall 提高了 9.96%，编辑生成准确率提高了 11.16%。交互式模拟中，它还报告了 27.71% 的建议接受率，同时耗时更低。

这可以作为 IDE 团队和代码审查自动化厂商的产品目标，场景是在初始补丁落地后处理后续编辑。眼前的产品形态可以很窄：开发者改完一个文件后，提供一个“propagate change”操作，先展示工具支持下找到的候选位置，再由模型写出补丁。一个低成本验证方式是：回放某个仓库最近的重构和 bug 修复提交，统计每次改动中第二个和第三个被修改文件上的建议有多少被接受。

### Evidence
- [Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction](../Inbox/2026-04-14--learning-project-wise-subsequent-code-edits-via-interleaving-neural-based-induction-and-tool-based-deduction.md): TRACE 提供了工具路由设计、具体的结构性编辑场景，以及跨项目在定位精度、生成准确率、耗时和建议接受率上的提升结果。
