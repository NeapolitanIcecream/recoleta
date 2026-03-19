---
source: hn
url: https://git-hunk.paulie.app/
published_at: '2026-03-03T23:32:04'
authors:
- shhac
topics:
- git-tooling
- code-automation
- developer-tools
- llm-agents
- ci-cd
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Git-hunk – Stage hunks by hash, no "-p" required

## Summary
`git-hunk` 是一个为 Git 局部暂存提供非交互式、可脚本化接口的工具，用稳定哈希替代 `git add -p` 的人工提示。它主要面向自动化、CI/CD 和 LLM/Agent 工作流，使按 hunk 选择与暂存变得确定且可编程。

## Problem
- Git 内建的局部暂存主要依赖 `git add -p`，这是交互式提示流程，自动化程序、CI/CD 与 LLM 代理都难以可靠使用。
- 交互式 hunk 选择要求人类在键盘前逐步确认，阻塞无人值守的软件生产流程。
- 交互式流程还存在 hunk 顺序不稳定、结果不够确定的问题，不利于脚本、多步代理执行和可复现操作。

## Approach
- 核心方法是给每个 diff hunk 生成一个**稳定内容哈希**，然后通过哈希来 `list`、`diff`、`add`，完全不需要交互提示。
- 哈希机制基于 `SHA1(file_path + '\0' + stable_line + '\0' + diff_lines)`，其中使用“不可变一侧”的行号作为锚点，以避免某个 hunk 被暂存后影响其他 hunk 的标识。
- 工作流被简化为三步：先枚举所有 hunk 及其哈希，再按哈希查看具体 diff，最后按哈希执行暂存。
- 设计上的关键点是：暂存一个 hunk 后，其余 hunk 的哈希保持不变，从而支持可靠的多步脚本和 agent 操作。
- 工具还提供 `--porcelain`、`count`、哈希前缀选择等机器友好接口，便于 CI、脚本和代理集成。

## Results
- 文本**没有提供标准基准测试或实验数据**，没有报告准确率、速度、成功率等量化评测结果。
- 明确声称相较 `git add -p`，该方法实现了 **0 次交互提示** 的 hunk 暂存流程：通过 `list`、`diff`、`add` 三个命令完成选择与暂存。
- 论文式主张的关键改进包括：**deterministic across runs**、**machine-readable output**、**fully non-interactive**，但未给出数值对比基线。
- 给出的最强具体机制性结果是：在示例中暂存 `a3f7c21` 后，剩余 hunk `b82e0f4` 与 `c91d3a8` 的哈希保持不变，说明多步 staged 操作中的标识稳定性。
- 适用场景上，作者明确宣称其可用于 **LLM agents、Scripts & CI、Humans** 三类用户，但未提供任务完成率或生产效率提升数字。

## Link
- [https://git-hunk.paulie.app/](https://git-hunk.paulie.app/)
