---
source: hn
url: https://github.com/Kapperchino/agent-joe
published_at: '2026-06-12T23:13:59'
authors:
- kapperchino
topics:
- coding-agent
- rust
- terminal-ui
- shell-safety
- developer-tools
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Agent Joe – a Rust only coding agent with no shell access

## Summary
Agent Joe 是一个只支持 Rust 的终端编码代理，通过移除 shell 访问来降低任意命令执行的风险。它面向更安全的本地代码工作，但作者说它的表现仍然比 Codex 差。

## Problem
- 连接到 LLM 提供方的 CLI 编码代理可以运行任意 shell 命令，这会给终端带来安全风险。
- 通用工具也暴露了很多操作；这个项目把可执行动作收窄到 Rust 专用操作。

## Approach
- 构建一个开源的 TUI 编码工具，只适用于 Rust 项目。
- 阻止 shell 访问，这样代理就不能执行任意终端命令。
- 将工具集限制为 Rust 专用操作，减少代理能做的事情。
- 使用类似 Claude Code 和 Codex 的 TUI，并强制使用 Vim 键位绑定。

## Results
- 摘要里没有基准测试数字或数据集结果。
- 作者说它“目前运行得相当好”，可以作为只支持 Rust 的编码代理使用。
- 作者也说它不如 Codex。
- 作者给出的差距原因是提示词不够好，以及没有计划模式。
- 这个项目是开源的，被当作更安全的编码代理工作流的概念验证。

## Link
- [https://github.com/Kapperchino/agent-joe](https://github.com/Kapperchino/agent-joe)
