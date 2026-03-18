---
source: hn
url: https://hjr265.me/blog/building-gittop-with-agentic-coding/
published_at: '2026-03-15T23:28:27'
authors:
- birdculture
topics:
- agentic-coding
- developer-tools
- git-analytics
- terminal-ui
- llm-assisted-programming
relevance_score: 0.06
run_id: materialize-outputs
---

# My First Agentic Coding Project: GitTop

## Summary
这篇文章介绍了一个名为 GitTop 的 Git 仓库终端监控工具，以及作者首次使用“全代理式编码”在单个周末内完成该项目的经历。核心价值不在算法创新，而在展示 LLM 代理能在较少人工编写代码的情况下完成一个中等规模、结构化良好的软件项目。

## Problem
- 要解决的问题是：如何从 Git 提交时间戳中直观分析一个仓库的开发活动模式，例如作者一天中何时最常提交代码。
- 现有一次性脚本或静态 HTML Git 统计工具可以回答部分问题，但缺少类似 `htop` 的交互式终端体验和可探索性。
- 更广义上，文章也在探讨：LLM 代理是否能承担从需求到实现的大部分编码工作，以及这对软件“作者感/所有权”意味着什么。

## Approach
- 构建了一个名为 GitTop 的 TUI 应用：使用 Go 开发，基于 Bubble Tea 做终端 UI、Lip Gloss 做样式、go-git 直接读取仓库数据而不调用 shell 中的 git。
- 开发方式是“fully agentic coding with Claude Code”：作者逐步描述需求、按功能引导，模型负责生成几乎全部实现，最终在 **26 次提交**后完成。
- 查询系统不是简单字符串搜索，而是设计成支持 `author:"alice"`、`path:*.go`、`branch:main and not path:vendor` 这类结构化语法的 DSL，并将查询编译为 AST 过滤节点，每个节点实现 `Match(*CommitInfo) bool`。
- 可视化上使用 Unicode braille 字符实现高分辨率图表；在 **80 列终端**中可达到等效 **160 列**的横向分辨率，其他柱状图还使用分数宽度块元素实现更细粒度渲染。
- 分支过滤没有把 `branch` 字段塞进每个提交对象，而是预先遍历匹配分支可达的提交并构建哈希集合，再通过提交哈希成员关系过滤，以保持数据模型简洁。

## Results
- 项目在一次周末实验中完成，作者称共经历 **26 次提交**，最终产出约 **4,800 行 Go 代码**，并形成一个 **7 页仪表盘**式 TUI 工具。
- GitTop 成功回答了作者最初的问题：在 Toph 项目上，提交主要集中在 **10:00–16:00**，且高峰在 **中午左右**。
- 图表渲染方面，文章给出具体实现收益：braille 图在 **80 列终端≈160 列有效分辨率**；柱状图可表示如 **3.5 单位宽**的分数长度，而不是只能取整到 3 或 4。
- 没有提供标准学术基准、公开数据集或与其他方法的定量对比结果，因此不存在传统意义上的 SOTA 指标。
- 最强的具体主张是：LLM 代理不仅完成了功能实现，还在若干设计点上做出较优工程选择，例如 AST 查询编译、分支哈希集过滤、以及更高分辨率的 Unicode 图表渲染。

## Link
- [https://hjr265.me/blog/building-gittop-with-agentic-coding/](https://hjr265.me/blog/building-gittop-with-agentic-coding/)
