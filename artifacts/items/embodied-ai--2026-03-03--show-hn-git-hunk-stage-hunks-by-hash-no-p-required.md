---
source: hn
url: https://git-hunk.paulie.app/
published_at: '2026-03-03T23:32:04'
authors:
- shhac
topics:
- git-tooling
- developer-tools
- automation
- ci-cd
- llm-agents
relevance_score: 0.08
run_id: materialize-outputs
---

# Show HN: Git-hunk – Stage hunks by hash, no "-p" required

## Summary
这是一个面向 Git 的非交互式分块暂存工具，用稳定哈希替代 `git add -p` 的交互提示，使脚本、CI/CD 和 LLM 代理能够确定性地选择并暂存代码 hunk。
它的核心价值在于把“只能人工操作的部分暂存”变成“机器可读、可自动化、可复现”的工作流。

## Problem
- 它解决的是 Git 内置的部分暂存主要依赖 `git add -p` 交互式提示的问题，因此**自动化系统、CI/CD、脚本和 LLM agents 无法可靠使用**。
- 交互式 hunk 选择还会带来**人工在场要求、阻塞流水线、hunk 顺序不稳定**等问题，影响可复现性与程序化控制。
- 这很重要，因为现代开发越来越依赖代理式编程、自动提交和流水线；如果无法非交互地精确暂存代码片段，很多自动化开发场景就会卡住。

## Approach
- 核心方法很简单：**先给每个 diff hunk 分配一个稳定内容哈希，再按哈希查看和暂存该 hunk**，而不是通过 `y/n/q/...` 提示逐个交互选择。
- 工作流被拆成三个非交互命令：`list` 枚举 hunk、`diff` 按哈希查看、`add` 按哈希暂存；因此整个过程可脚本化、可编排。
- 哈希机制使用 `SHA1(file_path + '\0' + stable_line + '\0' + diff_lines)`，其中 `stable_line` 来自“不可变一侧”的行号锚点，以避免暂存一个 hunk 后导致其他 hunk 的标识变化。
- 关键机制是**剩余 hunk 的哈希在多步暂存过程中保持不变**；这使得分步自动化选择成为可靠流程，而不会因为前一步操作改变后续标识。
- 工具还提供 `--porcelain`、`count`、`--exclusive`、`--oneline` 等接口，强化脚本、CI 和人机协作场景中的机器可读性与确定性。

## Results
- 文中**没有提供标准论文式定量实验结果**，没有数据集、准确率、吞吐、时延或对比基线数字。
- 最强的具体声明是：相较 `git add -p`，该工具实现了 **3 个明确步骤**（Enumerate / Select / Stage）且**0 个交互提示**，把部分暂存变为完全非交互流程。
- 它声称 hunk 标识采用 **SHA-1** 稳定内容哈希，并在示例中展示：暂存 `a3f7c21` 后，其余 hunk 如 `b82e0f4`、`c91d3a8` 的哈希**保持不变**。
- 相比内置交互式方案，作者明确宣称其优势包括 **fully non-interactive、deterministic across runs、machine-readable output、stable content hashes**，目标受益对象包括 **LLM Agents、Scripts & CI、Humans**。
- 提供的可用命令至少包括 **4 类**：`list`、`diff`、`add`、`count`；并支持哈希前缀与范围查看（如 `a3f7`、`a3f7:3-5`），体现出面向程序化工作流的接口设计。

## Link
- [https://git-hunk.paulie.app/](https://git-hunk.paulie.app/)
