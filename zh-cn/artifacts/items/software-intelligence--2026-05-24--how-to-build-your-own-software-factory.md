---
source: hn
url: https://web.navan.dev/posts/2026-05-06-how-to-build-your-own-software-factory.html
published_at: '2026-05-24T22:57:00'
authors:
- _doctor_love
topics:
- software-factory
- coding-agents
- code-intelligence
- agent-orchestration
- software-validation
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# How to build your own software factory

## Summary
## 摘要
这篇文章给出了一套软件工厂的实用设计：围绕编码代理搭建系统，把可重复的工程工作变成可验证、可审计的任务。它的核心判断是，团队应先自动化边界清楚的产品线，例如依赖更新、CVE 修复、易碎测试分流或仓库迁移。

## 问题
- 团队常把编码代理当成整个工厂，然后得到代码改动，却没有足够的验证、证据或停止规则。
- 遗留软件工作依赖隐藏上下文：日志、运行手册、CI 行为、客户路径、已知的易碎测试和资深工程师的判断。
- 当输入任务含糊、代理无法返回 no-op，或者成功只取决于代理自己的说法时，代理运行就会失败。

## 方法
- 在扩展自动化之前，先选 1 条狭窄的产品线，例如覆盖固定一组仓库的依赖更新。
- 为每个任务定义一个 seed：工单、漏洞公告、日志、迁移规格、仓库列表、故障历史，或启动运行的其他输入。
- 把提示词改成 task packet，包含意图、来源、范围、非目标、复现步骤、允许使用的工具、验证、no-op 规则、所需证据和输出格式。
- 用外层工厂循环包住编码代理循环：接入、分类、复现、规划、实现、验证、收集证据、决定终态，再把失败反馈回系统。
- 在可能的情况下，在代理之外验证行为，使用测试、场景、日志、截图、追踪、数字孪生或其他审查者可以检查的证据。

## 结果
- 文章没有给出定量基准结果、准确率分数、成本数据或测得的生产力提升。
- 它定义了工厂工位的 4 种终态：PR_READY、NO_OP、ESCALATE 和 RETRYABLE_FAILURE。
- 它给出一个具体的边界示例：跨 10 个仓库的依赖更新工单，只有在更新适用、能构建、通过测试并保持对外行为不变时，才应打开 PR。
- 它把 fleet 规模描述成另一类工作：在 500 个仓库里做 1 次依赖更新，需要仓库选择、隔离工作区、集中跟踪、重试、成本上限、审查队列和审计日志。
- 它建议验证修订最多重试 1 到 2 次，然后停止，而不是让代理在没有清晰终态的情况下循环。

## Problem

## Approach

## Results

## Link
- [https://web.navan.dev/posts/2026-05-06-how-to-build-your-own-software-factory.html](https://web.navan.dev/posts/2026-05-06-how-to-build-your-own-software-factory.html)
