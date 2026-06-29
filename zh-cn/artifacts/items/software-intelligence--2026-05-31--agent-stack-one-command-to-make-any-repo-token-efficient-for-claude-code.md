---
source: hn
url: https://github.com/drmahdikazempour/agent-stack
published_at: '2026-05-31T21:51:06'
authors:
- mahdikaz
topics:
- claude-code
- token-optimization
- code-intelligence
- developer-agents
- repo-automation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Agent-stack – one command to make any repo token-efficient for Claude Code

## Summary
## 概述
agent-stack 是一个一条命令的设置工具，用来为 Claude Code 和 Cursor 配置更省 token 的仓库工作流。它之所以重要，是因为仓库里的 agent 常常把上下文浪费在文件发现、噪声日志、过长指令和手动配置 hooks 上。

## 问题
- Claude Code 的省 token 工具分散在多个独立工具里，分别处理 shell 压缩、代码映射、用量测量、交接、hooks 和编辑器规则。
- 配置一个仓库时，往往要在 5 到 10 个工具之间做选择，合并 hooks，编写 CLAUDE.md，镜像 Cursor 规则，并手动测量用量。
- 直接后果是输入 token 用量更高，而且 agent 在开始处理代码库前要花更多时间做准备。

## 方法
- 主命令 `npx @drmahdikazempour/agent-stack init --all` 会检测主机、仓库类型、包管理器和 profile，然后生成 Claude Code 和 Cursor 文件。
- 它会写入并校验 `CLAUDE.md`、`AGENTS.md`、`.claudeignore`、skills、hooks、Cursor 规则和 `.agent-stack/graph.md`，并在失败时保留备份和回滚。
- 内置代码映射会索引源文件和导出符号，这样 agent 可以先 grep 一个紧凑文件，再打开源文件。
- 内置的 `compress` 命令会移除 ANSI 代码、折叠重复行，并在长命令输出进入上下文之前截短它。
- 用量测量依赖 `ccusage`；Stop hook 会把每次 turn 记录到 `.agent-stack/usage.jsonl`，`measure --since 7d` 会把当前输入 token/天与保存的基线对比。

## 结果
- 设置声明：`init --all` 可以在不到 2 分钟内把一个仓库从未配置状态变成优化后的 Claude Code 和 Cursor 设置。
- 示例安装输出声称生成了 20 个文件、接好了 2 个 hooks、验证了 `CLAUDE.md`、生成了代码映射，并给出了 12,340 tokens/天 的 7 天游基线。
- 生成的 `CLAUDE.md` 限制在启动时 ≤800 tokens，并由 `doctor` 检查。
- 代码映射示例索引了 142 个文件和 906 个顶层符号，让 agent 在符号搜索时只需打开 1 个目标文件，而不是读很多文件。
- 输出压缩器声称在一个 500 行日志上大约减少 60% 的字符。
- 测量示例显示当前输入 token/天为 7,180，基线为 12,340，减少 41.8%，目标至少是 40%；这些是 README 中的声明，不是独立基准测试。

## Problem

## Approach

## Results

## Link
- [https://github.com/drmahdikazempour/agent-stack](https://github.com/drmahdikazempour/agent-stack)
