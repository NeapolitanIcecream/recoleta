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

# 基于仓库的代码审查

## Summary
当前的 coding agent 工作指向三个具体变化：把可执行规格检查加进 pull request 审查，把仓库上下文推理 trace 加进评估，并在广泛的模型搜索之前，先把跨文件后续编辑交给 IDE 和语言服务器工具。共同模式很简单：仓库证据暴露出最终补丁评分和本地编辑流程仍然漏掉的失败。

## Pull request checks for executable preconditions and postconditions
评估 coding agent 的团队可以把可执行规格检查加入仓库任务的审查流程。CodeSpecBench 说明了这件事为什么重要：函数级规格生成的通过率达到 47.0%，但在 500 个 SWE-bench Verified 问题上的仓库级表现，最好模型也只到 20.2%。这个差距指向生产代码审查里的一个明确失败模式：agent 可能生成看起来合理的补丁，却没有捕捉到预期的输入约束、状态假设或输出保证。

一个可行做法是在 CI 里增加一步：让模型针对 pull request 涉及的函数写出前置条件和后置条件，把它们和现有测试及生成测试一起运行，再把不匹配的地方标出来供审查者检查。对已经在 Python 服务或库里使用 agent 生成补丁的团队，这个流程很合适，因为输出是可执行的，而且可以用他们今天信任的同一套测试工具来检查。一个低成本试点是对一个仓库里的 bug 修复 PR 做一周试验：记录生成的规格有多常失败，但补丁在审查里仍然看起来可接受，以及这些失败是否比现有测试更早暴露隐藏的语义回归。

### Evidence
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): CodeSpecBench provides the repository-level spec-generation results, execution-based evaluation design, and the 20.2% repo pass-rate ceiling that supports adding spec checks to PR review.

## Repository-context input and output prediction suites for coding-agent evaluation
仓库基准可以不再只依赖最终补丁是否成功，而是加入基于真实代码路径的输入和输出预测任务。R²Eval 说明了当评估只停留在短的独立代码片段时，盲区有多大：在 CRUXEval 上，平均输入预测准确率是 81.23%，在真实仓库问题上降到 16.91%；输出预测从 80.37% 降到 28.15%。这个基准还通过序列化复合类型和自定义类型，保留了复杂运行时对象，再把预测反序列化回对象，用测试来评分。

这支持对模型供应商、内部评估团队和购买 coding agent 的企业做一个明确的流程调整：在扩大部署前，先加一个小型的仓库上下文推理套件。这个套件不需要很大。只要从一个生产服务里抽出几十个有追踪的 method，配上序列化输入和预期输出，就能看出模型是否能跟上项目状态、依赖关系和大量对象的 API。一个便宜的检查方式是，从最近的事故或不稳定修复里抽样方法，把这些 trace 的得分和现在那种偏代码片段的评估结果对比。如果同一个模型只在简单集合上看起来强，部署风险已经很清楚了。

### Evidence
- [Evaluating LLMs Code Reasoning Under Real-World Context](../Inbox/2026-04-14--evaluating-llms-code-reasoning-under-real-world-context.md): R²Eval provides the real-repository input/output prediction setup, object serialization method, and the measured collapse from snippet benchmarks to repository-context reasoning.

## Tool-routed follow-up edits for cross-file changes
跨文件编辑助手可以先把明显的结构性修改交给 IDE 和语言服务器工具处理，再让模型去搜索代码库，这样能提高被接受的概率。TRACE 给出了一种具体模式：先判断当前修改像不像重命名、签名更新、克隆更新，或者诊断-修复案例，再调用 rename 和 def-use 分析之类的工具收集编辑位置，然后把剩下的语义修改交给模型。它在 678 个项目的 38K 次提交上，把编辑位置精度提高了 43.76%，召回率提高了 9.96%，编辑生成准确率提高了 11.16%。在交互式模拟里，它还报告了 27.71% 的建议接受率，并且时间成本更低。

这适合做成 IDE 团队和代码审查自动化厂商的功能，重点是初始补丁落地后的后续修改。直接的产品形态可以很窄：开发者改完一个文件后，提供一个“传播变更”动作，先显示工具支持的候选位置，再让模型写补丁。一个低成本验证方式是回放某个仓库最近的重构和 bug 修复提交，统计每次变更里第二个和第三个被触及文件的已接受建议数量。

### Evidence
- [Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction](../Inbox/2026-04-14--learning-project-wise-subsequent-code-edits-via-interleaving-neural-based-induction-and-tool-based-deduction.md): TRACE provides the tool-routing design, the specific structural edit cases, and the cross-project gains in location precision, generation accuracy, time cost, and suggestion acceptance.
