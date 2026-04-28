---
kind: trend
trend_doc_id: 410
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
topics:
- coding-agents
- evaluation
- repository-context
- multi-agent-workflows
- code-editing
run_id: materialize-outputs
aliases:
- recoleta-trend-410
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/repository-context
- topic/multi-agent-workflows
- topic/code-editing
language_code: zh-CN
---

# 可在真实仓库中核查的证据，已经成了当前代码 agent 仍未达到的标准

## Overview
这一天最强的信号是，代码研究正在把重点收紧到那些可以在真实仓库里核查的证据上。CodeSpecBench、R²Eval 和 Ace 从不同角度指向同一个限制：与单纯的生成速度相比，语义理解、仓库上下文和团队协同仍然更限制当前的代码 agent。

## Clusters

### 评估正在走出只看最终答案打分的阶段
这一天的基准测试在持续提出一个更严格的问题：模型是否真正理解程序意图，以及它能否用可核查的证据解释这种意图。CodeSpecBench 测试可执行的前置条件和后置条件，在 500 个 SWE-bench Verified 问题上，仓库级最高通过率只有 20.2%。CodeRQ-Bench 进一步评估推理本身。它的 VERA 评估器在生成、摘要和分类任务上都超过了此前的评估器，AUCROC 最高提升 0.26。结论很直接：只看输出质量，仍然会掩盖很大的语义和推理缺口。

#### Evidence
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): 可执行规格基准测试，以及仓库级通过率。
- [Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks](../Inbox/2026-04-14--beyond-output-correctness-benchmarking-and-evaluating-large-language-model-reasoning-in-coding-tasks.md): 推理质量基准测试，以及 VERA 相比此前评估器的提升。

### 真实仓库仍在打破人们对基准测试的信心
仓库上下文仍然是代码模型失去大部分表面能力的地方。R²Eval 从十个真实 Python 项目中构建输入和输出预测任务，结果显示，与 CRUXEval 相比，输入预测的平均准确率从 81.23% 降到 16.91%，输出预测从 80.37% 降到 28.15%。CodeSpecBench 用另一种形式显示了同样的模式：函数级规格生成的通过率可以接近 47.0%，而仓库级表现仍停留在约 20%。这个结果在不同任务形式中都一致。真实项目的结构、依赖关系和大量对象状态依然难以处理。

#### Evidence
- [Evaluating LLMs Code Reasoning Under Real-World Context](../Inbox/2026-04-14--evaluating-llms-code-reasoning-under-real-world-context.md): 真实项目推理基准测试，相比 CRUXEval 出现大幅下降。
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): 函数级与仓库级规格结果对比。

### 多 agent 编码正在变成工作流基础设施
Agent 工作也开始被建模为协同问题，而不只是生成问题。Ace 把人和 agent 放进同一个实时工作空间，提供共享聊天、提示历史、预览和云端会话，并把团队对齐视为许多 agent 并行运行时的瓶颈。OpenRig 从本地运维角度处理同一问题：用 YAML 定义一个混合 agent 团队，在受管 tmux 会话中运行它，检查拓扑，并在关闭后恢复。对 Claude Code 源码的分析则补上了这一趋势下的架构层。论文认为，agent 循环本身很简单，而系统的大部分复杂性都在权限、上下文压缩、可扩展性、委派和持久化上。

#### Evidence
- [One Developer, Two Dozen Agents, Zero Alignment](../Inbox/2026-04-14--one-developer-two-dozen-agents-zero-alignment.md): 以共享上下文和规划为中心的多人协作编码工作空间。
- [Show HN: OpenRig – agent harness that runs Claude Code and Codex as one system](../Inbox/2026-04-14--show-hn-openrig-agent-harness-that-runs-claude-code-and-codex-as-one-system.md): 面向混合 agent 团队的本地运行框架，支持拓扑控制和恢复。
- [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](../Inbox/2026-04-14--dive-into-claude-code-the-design-space-of-today-s-and-future-ai-agent-systems.md): 基于源码分析，拆解代码 agent 系统复杂性实际所在的位置。

### 项目级编辑会奖励明确的工具使用
跨文件编辑正在变成一个工具路由问题。TRACE 把神经预测与 IDE 和语言服务器工具结合起来，比如 rename 和 def-use analysis，然后判断什么时候调用工具比大范围神经搜索更合适。在 678 个项目的 3.8 万次提交上，它把编辑位置精度提高了 43.76%，召回率提高了 9.96%，编辑生成准确率提高了 11.16%，都超过了此前系统。它的交互式模拟还报告了 27.71% 的建议接受率，同时耗时更低。这是一个明确的信号：项目范围的编辑需要模型周围有清晰的结构支持，而不只是更大的上下文窗口。

#### Evidence
- [Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction](../Inbox/2026-04-14--learning-project-wise-subsequent-code-edits-via-interleaving-neural-based-induction-and-tool-based-deduction.md): 面向项目级后续编辑的神经与工具混合系统，并给出了可量化提升。
