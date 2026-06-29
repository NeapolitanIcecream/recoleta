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

# 真实仓库证据是当前代码代理仍然达不到的标准

## Overview
这一天最强的信号是，代码研究正在收紧到可在真实仓库中核查的证据上。CodeSpecBench、R²Eval 和 Ace 从不同角度指向同一个限制：语义理解、仓库上下文和团队协调，比原始生成速度更能限制当前代码代理的能力。

## Clusters

### Evaluation is moving past final-answer scoring
这一天的基准测试继续提出一个更严格的问题：模型是否抓住了程序意图，并且能用可核查的证据解释这种意图。CodeSpecBench 测试可执行的前置条件和后置条件，仓库级别的最佳通过率是在 500 个 SWE-bench Verified 问题上达到 20.2%。CodeRQ-Bench 则直接评估推理本身。它的 VERA 评估器在生成、总结和分类任务上都优于之前的评审器，最高提升达到 0.26 AUCROC。这个信息很直接：只看输出质量，仍然会掩盖很大的语义和推理差距。

#### Evidence
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): Executable specification benchmark and repo-level pass rates.
- [Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks](../Inbox/2026-04-14--beyond-output-correctness-benchmarking-and-evaluating-large-language-model-reasoning-in-coding-tasks.md): Reasoning-quality benchmark and VERA gains over prior evaluators.

### Real repositories keep breaking benchmark confidence
仓库上下文仍然是代码模型最容易暴露真实水平不足的地方。R²Eval 从十个真实 Python 项目里构建输入和输出预测任务，与 CRUXEval 相比，输入预测的平均准确率从 81.23% 跌到 16.91%，输出预测从 80.37% 跌到 28.15%。CodeSpecBench 也显示了同样的模式，只是换了一种形式：函数级规格生成的通过率可以接近 47.0%，而仓库级表现仍然接近 20%。这种结果在不同任务形式里都一致。真实项目结构、依赖关系和大量对象状态，依然很难处理。

#### Evidence
- [Evaluating LLMs Code Reasoning Under Real-World Context](../Inbox/2026-04-14--evaluating-llms-code-reasoning-under-real-world-context.md): Real-project reasoning benchmark with large drops versus CRUXEval.
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): Function-level versus repo-level specification results.

### Multi-agent coding is turning into workflow infrastructure
代理工作也越来越被建模为协调问题，而不只是生成问题。Ace 把人和代理放进同一个实时工作区，共享聊天、提示历史、预览和云会话，并把在多个代理并行运行时的团队对齐看作瓶颈。OpenRig 从本地运维角度处理同一个问题：用 YAML 定义混合代理团队，在受管的 tmux 会话里运行，查看拓扑，并在关闭后恢复。Claude Code 的源码分析给这一趋势补上了底层架构视角。论文认为代理循环本身很简单，而系统复杂度主要落在权限、上下文压缩、扩展性、委派和持久化上。

#### Evidence
- [One Developer, Two Dozen Agents, Zero Alignment](../Inbox/2026-04-14--one-developer-two-dozen-agents-zero-alignment.md): Multiplayer coding workspace centered on shared context and planning.
- [Show HN: OpenRig – agent harness that runs Claude Code and Codex as one system](../Inbox/2026-04-14--show-hn-openrig-agent-harness-that-runs-claude-code-and-codex-as-one-system.md): Local harness for mixed-agent teams, topology control, and restore.
- [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](../Inbox/2026-04-14--dive-into-claude-code-the-design-space-of-today-s-and-future-ai-agent-systems.md): Source-based breakdown of where coding-agent system complexity actually lives.

### Project-wide editing rewards explicit tool use
跨文件编辑正在变成一个工具路由问题。TRACE 把神经预测和 IDE、语言服务器工具结合起来，比如重命名和 def-use 分析，然后决定什么时候调用工具比大范围神经搜索更合适。在 678 个项目的 38K 次提交上，它比之前的系统将编辑位置精度提高了 43.76%，召回率提高了 9.96%，编辑生成准确率提高了 11.16%。它的交互式模拟还报告了 27.71% 的建议接受率，而且时间成本更低。这说明项目级编辑需要模型外的明确结构，而不只是更大的上下文窗口。

#### Evidence
- [Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction](../Inbox/2026-04-14--learning-project-wise-subsequent-code-edits-via-interleaving-neural-based-induction-and-tool-based-deduction.md): Hybrid neural-plus-tool system for project-wide subsequent edits with measured gains.
