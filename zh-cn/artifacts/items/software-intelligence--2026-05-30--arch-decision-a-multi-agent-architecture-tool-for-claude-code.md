---
source: hn
url: https://github.com/jsingh6/arch-decision
published_at: '2026-05-30T22:45:31'
authors:
- jsingh2525
topics:
- architecture-decision-records
- code-intelligence
- multi-agent-systems
- claude-code
- software-engineering-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Arch-Decision – A multi-agent architecture tool for Claude Code

## Summary
## 概述
arch-decision 是一个 Claude Code 插件。它接收 GitHub issue、Jira 任务或普通需求，在分析代码库并获得人工批准后，生成一份 Architecture Decision Record。它针对的是阻碍团队记录架构决策原因的时间成本。

## 问题
- 团队常常在没有 ADR 的情况下做出架构决策，所以后来改代码的人会重新经历同样的争论。
- 作者说，一名资深工程师需要 2–4 小时来研究代码库、比较方案并写出 ADR。
- 这个工具的重要性在于，ADR 能把设计意图保留在代码附近，但手工编写带来的阻力足以让团队跳过这一步。

## 方法
- 这个插件运行在 Claude Code 里，接受 GitHub issue 链接、Jira 文本或自然语言需求。
- 一个 8 阶段协调器会检测语言、已有 ADR 和项目上下文；读取问题；提出澄清问题；生成方案；等待批准；写出 ADR；并把它链接回原始 issue。
- 在第 2 阶段，3 个探查代理并行运行，检查既有实现、代码影响和约束。
- 在第 4 阶段，它生成 3 种方案：Minimal、Clean 和 Pragmatic。
- 一个汇总器把代理输出合并成权衡表和推荐结果，然后第 6 阶段的批准关卡会阻止文件写入，直到用户签字。

## 结果
- 宣称的时间减少：ADR 准备时间从资深工程师的 2–4 小时降到几分钟；文中提到的一次运行在 5 分钟内完成。
- 案例：在 refinedev/refine 的 issue #7338 上，工具在 `crudFiltersToColumnFilters` 中找到了既有实现，识别出 `packages/core` 中的约束，并建议在 antd wrapper 作用域内使用 `onParse` 回调。
- 独立对照：根据摘录，社区 PR #7385 使用了与工具建议相同的回调名称、作用域和位置。
- 这个系统有 8 个阶段、3 个并行探查代理、3 个生成的方案、1 个汇总代理，以及 1 个必需的人工批准关卡。
- 摘录没有提供基准测试套件、样本量、准确率、消融实验，也没有与其他代码代理进行受控对比。

## Problem

## Approach

## Results

## Link
- [https://github.com/jsingh6/arch-decision](https://github.com/jsingh6/arch-decision)
