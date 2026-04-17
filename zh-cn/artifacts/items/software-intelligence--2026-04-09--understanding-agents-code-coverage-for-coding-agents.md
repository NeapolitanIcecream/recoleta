---
source: hn
url: https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/
published_at: '2026-04-09T23:17:35'
authors:
- matt_d
topics:
- coding-agents
- code-coverage
- security-auditing
- agent-observability
- developer-tools
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding Agents: Code Coverage for Coding Agents

## Summary
## 摘要
这篇文章介绍了一个开源工具，用来重建并可视化编码代理在一次审计运行中实际读取了哪些代码。它帮助人工比较代理在不同提示词、模型和推理强度下的行为，并检查代理看了什么、漏了什么。

## 问题
- 编码代理在长时间审计运行后可以报告漏洞，但现有工具很难清楚展示代理实际检查了哪些文件和代码行。
- 这个缺口使人们难以判断代理是否搜索了相关攻击面、是否能公平比较不同运行结果，或如何指导后续审计。
- 对安全审计来说，这一点很重要，因为代理不可能在从未读取的代码里发现漏洞，而人工需要一种方法来找出盲区。

## 方法
- 该工具会解析 Claude Code 和 `codex-cli` 保存在本地的 `.jsonl` 会话日志，其中包含提示词、推理摘要和已执行的工具命令。
- 它把代理读取文件的动作转换为已覆盖的代码行区间，并将这些区间关联到对应读取行为的子任务或意图。
- 它通过一个 Web UI 展示结果，包括高亮显示的已覆盖代码行、项目 treemap、逐行覆盖次数，以及触及每个区域的子任务。
- 这个工具用于事后检查：人工可以比较提示词、模型、推理强度和重复运行，然后把后续审计引导到未覆盖区域。

## 结果
- 在一个 OpenSSH 预认证 RCE 审计任务中，GPT-5.4 在每种设置下的五次运行里都集中在更窄的一部分明显预认证攻击面上。
- GPT-5.4 的唯一覆盖代码行中位数会随着推理预算增加而上升：`gpt5.4-medium` 约为 8.3k，`gpt5.4-high` 约为 13.5k，`gpt5.4-xhigh` 约为 17.7k。
- GPT-5.4 每次运行触及的文件数也随着推理强度增加而上升：medium、high 和 xhigh 分别约为 24、35 和 40 个文件。
- Opus 4.6 覆盖了更多代码：唯一覆盖代码行的中位数中，`opus4.6-high` 约为 31.8k，`opus4.6-medium` 约为 30.3k，其中一次 medium 运行达到了约 50k 行。
- 在五次运行中，Opus 配置触及的不同文件数分别为 high 的 298 个和 medium 的 395 个，而 GPT-5.4 各设置保持在 40 到 62 个之间。
- 作者指出，覆盖率不是漏洞发现能力的直接指标，但重复运行仍然重要，因为代理行为具有概率性，随着时间推移可能会发现不同的漏洞。

## Problem

## Approach

## Results

## Link
- [https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/](https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/)
