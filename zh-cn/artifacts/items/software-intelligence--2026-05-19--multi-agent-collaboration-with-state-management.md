---
source: arxiv
url: https://arxiv.org/abs/2605.20563v1
published_at: '2026-05-19T23:45:33'
authors:
- Mengyang Liu
- Taozhi Chen
- Zhenhua Xu
- Xue Jiang
- Yihong Dong
topics:
- multi-agent-coding
- state-management
- conflict-detection
- llm-code-generation
- software-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-agent Collaboration with State Management

## Summary
## 摘要
STORM 是一个面向共享工作区的状态管理器，供编辑同一代码库的 LLM 代理使用。它在每次写入前检查代理看到的文件视图是否仍然最新，因此过期修改会被拒绝，代理还能用新代码重试。

## 问题
- 并行的软件代理可能同时编辑共享文件或相互依赖的文件，这会造成接口失配、工作被覆盖和集成失败。
- Git worktree 隔离避免了运行时互相干扰，但它把冲突留到最后合并时才处理，这时语义冲突更难诊断和修复。
- 这对自动化软件生产很重要，因为更大的代码任务需要并行工作，而糟糕的冲突处理会抵消使用多个代理带来的收益。

## 方法
- STORM 维护一个共享工作区，并给每个文件分配一个版本计数器。
- 每个代理都有一个读取快照：它读过的文件集合，以及当时看到的文件版本。
- 在接受写入之前，STORM 会检查代理读取快照中的每个文件是否仍然是同一版本。如果有任何文件发生变化，写入就会被拒绝。
- 拒绝写入时，STORM 会返回当前目标文件、用于直接冲突的 diff，以及过期的依赖文件，这样代理可以带着当前上下文重试。
- 代理还会在代码中留下结构化的意图注释，这让其他代理能直接看出附近代码为什么被改动。

## 结果
- 在使用 Claude Sonnet 4.6 的 Commit0-Lite 上，STORM 的加权通过率为 46.2，宏平均通过率为 82.5；GitWorktree 分别是 24.6 / 63.8，单代理分别是 20.7 / 66.4。
- 在使用 Claude Sonnet 4.6 的 PaperBench Code-Dev 上，STORM 得分为 74.1；GitWorktree 为 72.7，单代理为 68.7。
- 论文报告，STORM 相比 git-worktree 多代理基线，在 Commit0-Lite 上提升 +18.7 个宏平均百分点，在 PaperBench 上提升 +1.4 分。
- STORM-Combined 取得了 Claude Sonnet 4.6 的最佳成绩：Commit0-Lite 上加权 49.2、宏平均 87.6，PaperBench 上 78.2。
- 在 Qwen 3.6 Plus 下，STORM 在 Commit0-Lite 上的加权分数为 61.4，GitWorktree 为 16.7；在 PaperBench 上，STORM 为 55.0，GitWorktree 为 51.6。
- 在 Commit0-Lite 的 Sonnet 扩展测试中，把最大工程师数从 2 提高到 8，使总通过率从 38.2% 升到 69.7%，宏平均通过率从 71.3% 升到 87.1%；成本从 $199 升到 $429，墙钟时间维持在约 13 小时。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20563v1](https://arxiv.org/abs/2605.20563v1)
