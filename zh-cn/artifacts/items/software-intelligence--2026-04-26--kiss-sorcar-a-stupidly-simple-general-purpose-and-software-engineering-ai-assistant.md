---
source: arxiv
url: http://arxiv.org/abs/2604.23822v1
published_at: '2026-04-26T17:59:06'
authors:
- Koushik Sen
topics:
- software-engineering-agent
- code-intelligence
- llm-agents
- vscode-extension
- terminal-bench
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# KISS Sorcar: A Stupidly-Simple General-Purpose and Software Engineering AI Assistant

## Summary
## 总结
KISS Sorcar 是一个本地、开源的 VS Code 助手，面向软件工程和通用任务，建立在一个五层的精简代理栈之上。论文声称，简单的分层设计，加上严格的续接、工具使用和 git 隔离，能在 Terminal Bench 2.0 上达到或超过更强的商业编码代理。

## 问题
- LLM 编码助手在长任务上会失效，因为上下文窗口会耗尽，一个错误步骤就可能打乱整个会话，代理还会在死胡同里循环。
- 生成的代码通常需要清理，因为代理在运行诸如 linter、类型检查器和测试之前就停了。
- 当代理直接修改当前工作树时，变更很难检查或撤销，这在真实的软件开发中很重要。

## 方法
- 系统使用一个五层继承栈，每一层只增加一项职责：带预算跟踪的 ReAct 执行、跨受上下文限制的子会话续接、编码和浏览器工具、持久聊天历史，以及 git worktree 隔离。
- 续接的做法是强制代理在一个子会话结束时输出按时间顺序排列的总结，说明它做了什么、为什么这么做，以及相关代码片段；下一个子会话从这些总结开始。
- 软件工程层给模型提供 shell、read、edit、write、browser、user-question、Docker，以及可选的并行子代理工具。
- 最外层的 worktree 层为每个任务创建单独的 git 分支和 worktree，通过基线提交保留脏的本地状态，并支持从 git 元数据恢复崩溃。
- 作者把框架保持得很小，核心五个代理类加起来大约 1,850 行代码，并报告说他们用这个系统本身在 4.5 个月内完成了系统构建。

## 结果
- 在 Terminal Bench 2.0 上，KISS Sorcar 使用 **Claude Opus 4.6** 报告了 **62.2% 的总体通过率**，对应 **89 个任务**、每个任务 **5 次试验**，共 **445 次试验**中的 **277 次**通过。
- 它报告了 **78.7% 的 pass@any**（**89 个任务中有 70 个**至少成功一次）和 **43.8% 的 pass@all**（**89 个任务中有 39 个**五次试验都成功）。
- 论文把这个结果与同一基准上的 **Claude Code 58%** 和 **Cursor Composer 2 61.7%** 做比较，声称它略优于两者。
- 每次试验的成本和运行时间分别报告为 **0.45 美元中位数**、**0.90 美元均值**，以及 **202 秒中位数**、**446 秒均值**。
- 任务稳定性较复杂：**39 个始终通过的任务**、**19 个始终失败的任务**，以及 **31 个结果混合的任务**。
- 评估细节会影响分数：作者在前期尝试后认为不可行的 **9 个任务**被直接跳过，而被跳过的任务仍算失败。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23822v1](http://arxiv.org/abs/2604.23822v1)
