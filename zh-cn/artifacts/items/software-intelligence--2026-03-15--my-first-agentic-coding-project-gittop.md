---
source: hn
url: https://hjr265.me/blog/building-gittop-with-agentic-coding/
published_at: '2026-03-15T23:28:27'
authors:
- birdculture
topics:
- agentic-coding
- code-generation
- tui-application
- git-analytics
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# My First Agentic Coding Project: GitTop

## Summary
GitTop 是一个用全代理式编码方式快速构建的 Git 仓库 TUI 仪表盘，作者借此评估 LLM 在真实软件实现中的能力与体验。文章核心价值不在算法突破，而在展示代理式编程如何在单次会话内产出一个可用、结构不差的中等规模工具，并引出“作者感/所有权”的人机协作问题。

## Problem
- 要解决的问题是：如何把 Git 提交时间与仓库活动以 **交互式终端界面** 直观呈现，而不是依赖一次性脚本或静态 HTML 报告。
- 更深层的问题是：**全代理式编码** 是否能在较少人工写代码的情况下完成一个真实、非玩具的软件项目，这对自动化软件生产和代码智能很重要。
- 文章还提出了一个人机协作层面的关键问题：当人负责目标、判断与迭代，而代理负责实际编码时，开发者是否仍然“拥有”这个项目。

## Approach
- 作者使用 **Claude Code** 进行“one feature at a time”的全代理式开发：人类给出需求、方向和反馈，代理负责编写实现，最终完成 GitTop。
- 技术栈是 **Go + Bubble Tea + Lip Gloss + go-git**，目标产物是类似 htop 的 Git 仓库 TUI 仪表盘，而不是调用 shell 的 git 命令。
- 过滤系统采用一个小型 **DSL**，支持如 `author:"alice"`、`path:*.go`、`branch:main and not path:vendor` 的结构化查询；代理将解析逻辑重构为基于 **Participle** 的 AST/节点匹配模型，每个节点实现 `Match(*CommitInfo) bool`。
- 图表渲染使用 **Unicode braille** 实现更高分辨率的迷你图，并在其他柱状图中使用 Unicode block 元素实现分数宽度显示，提升终端可视化精度。
- 分支过滤没有污染主数据模型，而是通过预计算“匹配分支可达提交”的哈希集合，再基于提交哈希做成员过滤，保持 `CommitInfo` 结构简洁。

## Results
- 项目在 **单个周末**、通过 **26 次提交** 完成，最终规模约 **4,800 行 Go 代码**，产出为一个 **7 页** 的终端仪表盘；这是文中最直接的生产率结果。
- GitTop 成功回答了作者的原始分析问题：在 Toph 项目上，提交主要集中在 **10:00–16:00**，并在 **中午附近达到峰值**。
- 终端图表声称可在 **80 列终端** 中通过 braille 编码达到等效 **160 列分辨率**（每字符 2×4 点阵），并用分数块元素实现诸如 **3.5 个字符宽** 的柱形显示，而不是只能取整到 3 或 4。
- 作者强调多个实现细节是代理**主动给出的较优工程选择**，如 Participle 解析器重构、分数宽柱状图、以及基于哈希集合的分支过滤架构，但文中**没有提供标准基准、对照实验或系统化量化评测**。
- 因此，文章的 strongest claim 不是模型性能 SOTA，而是：在较少手写代码的前提下，代理能在一次真实项目构建中产出“可用且工程结构不差”的软件，并暴露出新的 **human-AI authorship/ownership** 体验问题。

## Link
- [https://hjr265.me/blog/building-gittop-with-agentic-coding/](https://hjr265.me/blog/building-gittop-with-agentic-coding/)
