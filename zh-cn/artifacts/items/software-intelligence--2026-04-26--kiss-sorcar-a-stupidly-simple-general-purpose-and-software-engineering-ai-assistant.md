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
## 摘要
KISS Sorcar 是一个在本地运行、开源的 VS Code 助手，用于软件工程和通用任务，底层是一个小型的五层 agent 栈。论文称，简单的分层设计，加上严格的续接机制、工具调用和 git 隔离，可以在 Terminal Bench 2.0 上达到或超过更强的商用代码 agent。

## 问题
- LLM 代码助手在长任务上经常失败，因为上下文窗口会耗尽，一次错误步骤就可能带偏整个会话，agent 还会在死胡同里循环。
- 生成的代码常常还需要清理，因为 agent 会在运行 linter、类型检查器和测试之前就停下。
- 当 agent 直接修改当前工作树时，变更很难检查或撤销，而这在真实的软件开发中很重要。

## 方法
- 该系统使用五层继承栈，每一层只增加一个职责：带预算跟踪的 ReAct 执行、跨受上下文限制的子会话续接、代码和浏览器工具、持久聊天历史，以及 git worktree 隔离。
- 续接通过强制 agent 在结束子会话时写出按时间顺序排列的总结来实现，内容包括它做了什么、为什么这样做，以及相关代码片段；下一个子会话从这些总结开始。
- 软件工程层为模型提供 shell、read、edit、write、browser、user-question、Docker，以及可选的并行子 agent 工具。
- 最外层的 worktree 层会为每个任务创建单独的 git 分支和 worktree，通过一个基线提交保留本地未提交状态，并支持基于 git 元数据的崩溃恢复。
- 作者将框架控制在较小规模，核心五个 agent 类总计约 1,850 行代码，并称他们在 4.5 个月里用这个系统构建了系统本身。

## 结果
- 在 Terminal Bench 2.0 上，KISS Sorcar 报告在 **Claude Opus 4.6** 下的**总体通过率为 62.2%**，即 **89 个任务**、**每个任务 5 次试验**、共 **445 次**试验运行中的 **277/445**。
- 它报告 **78.7% 的 pass@any**（**70/89** 个任务至少成功一次）以及 **43.8% 的 pass@all**（**39/89** 个任务在五次试验中全部成功）。
- 论文将其与同一基准上的 **Claude Code 的 58%** 和 **Cursor Composer 2 的 61.7%** 对比，并称其对两者都有小幅优势。
- 论文报告每次试验的成本和运行时间中位数分别为 **$0.45** 和 **202 s**，均值分别为 **$0.90** 和 **446 s**。
- 任务稳定性情况不一：**39 个始终通过的任务**、**19 个始终失败的任务**、以及 **31 个结果混合的任务**。
- 评分会受到评估细节影响：作者对他们在先前尝试后判断为不可行的 **9 个任务**进行了 **hard-skip**，而被跳过的任务仍计为失败。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23822v1](http://arxiv.org/abs/2604.23822v1)
