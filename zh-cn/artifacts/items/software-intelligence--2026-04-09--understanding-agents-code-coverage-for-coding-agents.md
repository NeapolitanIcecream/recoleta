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
## 总结
这篇文章介绍了一个开源工具，用来重建并可视化代码代理在一次审计运行中读了哪些代码。它帮助人们比较不同提示、模型和推理强度下的代理行为，并查看代理看过什么、漏看了什么。

## 问题
- 代码代理在长时间审计后可以报告漏洞，但现有工具很难看清它们实际检查了哪些文件和代码行。
- 这个缺口让人难以判断代理是否搜索了相关攻击面，难以公平比较不同运行，也难以指导后续审计。
- 对安全审计来说，这一点很重要，因为代理读不到的代码里就找不到漏洞，而人类需要一种方法来发现盲区。

## 方法
- 该工具解析 Claude Code 和 `codex-cli` 生成的本地 `.jsonl` 会话日志，其中包含提示、推理摘要和执行过的工具命令。
- 它把代理的文件阅读动作转换成被覆盖的行范围，并把这些范围和读取时对应的子任务或意图关联起来。
- 它在一个网页界面里展示结果，显示高亮的已覆盖代码行、项目树图、每行的覆盖次数，以及触及每个区域的子任务。
- 这个工具用于事后检查：人们可以比较不同提示、模型、推理强度和重复运行，然后把后续审计引向未覆盖的区域。

## 结果
- 在 OpenSSH 预认证远程代码执行审计任务中，GPT-5.4 在每种设置下的五次运行里，都把重点放在更窄的一段显然属于预认证攻击面的代码上。
- GPT-5.4 的唯一覆盖代码行中位数会随着推理预算上升：`gpt5.4-medium` 约 8.3k 行，`gpt5.4-high` 约 13.5k 行，`gpt5.4-xhigh` 约 17.7k 行。
- GPT-5.4 每次运行触及的文件数也随着推理强度上升：medium、high 和 xhigh 分别大约是 24、35 和 40 个文件。
- Opus 4.6 覆盖的代码更多：`opus4.6-high` 的唯一覆盖代码行中位数约 31.8k，`opus4.6-medium` 约 30.3k，其中一次 medium 运行接近 50k 行。
- 在五次运行中，Opus 配置在 high 下触及了 298 个不同文件，medium 下触及了 395 个，而 GPT-5.4 的设置一直在 40 到 62 之间。
- 作者指出，覆盖率不是直接的漏洞发现指标，但重复运行仍然重要，因为代理行为是随机的，随着时间推移会暴露不同的漏洞。

## Problem

## Approach

## Results

## Link
- [https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/](https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/)
