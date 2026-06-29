---
source: hn
url: https://perceptiontheory.bearblog.dev/context-sculpting/
published_at: '2026-06-06T23:20:01'
authors:
- perceptronblues
topics:
- agent-harnesses
- context-management
- software-agents
- code-intelligence
- multi-agent-systems
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Context Sculpting

## Summary
## 总结
Context Sculpting 测试了一个双模型 agent harness：更强的外层模型可以在轮次之间重写较弱的内层模型上下文。这个案例研究显示，主动重写上下文是可行的，但运行结果也显示出较高的成本、延迟和控制策略风险。

## 问题
- 大多数聊天和 agent 系统把上下文窗口当作只能追加的日志。这会保留过时文件、失败路径、工具噪声和干扰性证据，浪费 token，并把长时间运行的软件 agent 引向错误方向。
- 这里的具体问题是，一个模型能否通过删除误导性状态、压缩历史或引导下一步，来管理另一个模型的工作上下文。
- 这对代码修复和基于语料的回答很重要，因为模型当前的上下文会影响它读什么、改什么、引用什么、验证什么，以及什么时候停止。

## 方法
- 原型使用 Pi agent harness，包含一个内层任务 agent 和一个外层控制 agent。报告中的运行使用 `gpt-5.4-mini` 作为内层模型，`gpt-5.4` 作为外层模型。
- 每次内层 agent 轮次后，外层 agent 读取完整的内层上下文，并选择一个动作：`pass_through`、`rewrite_context`、`rollback` 或 `terminate`。
- Demo 1 使用了两类任务：一个小型、带文件的任务管理器 CLI 修复任务，以及一个包含干扰文档的本地语料综合任务。每种任务各运行 2 次仅内层运行和 2 次外层 harness 运行，共 8 次运行。
- Demo 2 把外层提示改成 `intervention_targeted` 配置，加入了更嘈杂的任务，并用较低的 thinking effort 降低了内层模型设置。

## 结果
- Demo 1 的 8 次运行全部成功完成，8 次验证检查全部通过，触发了 0 次 guardrail，估算成本为 $0.7079。
- Demo 1 没有产生上下文重写。在 4 次 harness 运行中，外层 agent 共进行了 16 次调用：12 次 `pass_through`、4 次 `terminate`、0 次 `rewrite_context`、0 次 `rollback`。完整 harness 的成本比仅内层运行高 14 倍，但通过率没有提高。
- Demo 2 的 4 次运行总成本约为 $1.26。在 2 次 harness 运行中，外层 agent 共进行了 15 次调用：14 次 `rewrite_context`、1 次 `terminate`、0 次 `rollback`，这说明了主动的上下文重写。
- 在嘈杂的综合任务中，外层 agent 先使用了早期的 `inject` 重写，随后使用了 `compact` 重写，内层 agent 在下一轮写出了最终答案。摘录没有给出这项任务相对于基线的准确率变化。
- 在代码修复任务中，控制组在 7 轮、42.7 秒、约 $0.015 的情况下通过。使用 harness 的运行也通过了，但用了 12 轮、566.9 秒、约 $1.06、12 次外层调用和 12 次重写，随后触发了 `maxInnerTurns` guardrail。
- 最强的结论是可行性，不是基准突破。这个案例研究表明，提示策略可以把外层 agent 从被动监督变成激进的上下文编辑，而且这种激进编辑会让一次成功运行的成本高得多。

## Problem

## Approach

## Results

## Link
- [https://perceptiontheory.bearblog.dev/context-sculpting/](https://perceptiontheory.bearblog.dev/context-sculpting/)
