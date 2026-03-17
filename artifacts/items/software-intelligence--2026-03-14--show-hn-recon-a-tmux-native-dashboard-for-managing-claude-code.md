---
source: hn
url: https://github.com/gavraz/recon
published_at: '2026-03-14T23:21:07'
authors:
- gavra
topics:
- code-intelligence
- multi-agent-software-engineering
- human-ai-interaction
- terminal-ui
- tmux-tooling
relevance_score: 0.89
run_id: materialize-outputs
---

# Show HN: Recon – A tmux-native dashboard for managing Claude Code

## Summary
Recon 是一个 **tmux 原生** 的终端仪表盘，用于集中管理多个 Claude Code 代理会话，并在不离开终端的情况下查看状态、切换、创建、终止和恢复会话。它的价值主要在于提升多代理编码工作流的可见性与操作效率。

## Problem
- 多个 Claude Code 会话并行运行时，用户很难快速知道每个代理当前在做什么、是否卡住、是否需要人工批准。
- 在 tmux 中手动切换、查找、恢复和管理多个会话成本高，尤其在多仓库、多任务并行开发时更明显。
- 现有做法常依赖 `ps` 解析或工作目录启发式匹配，容易不准确，影响自动化和稳定管理。

## Approach
- 将每个 Claude Code 实例运行在独立的 tmux session 中，并由 Recon 提供统一的 TUI 仪表盘进行集中管理。
- 通过读取 `~/.claude/sessions/{PID}.json` 将 Claude 进程与 session ID 精确关联，避免使用 `ps` 或 CWD 启发式。
- 通过 `tmux list-panes`、`tmux capture-pane`、以及 `~/.claude/projects/.../*.jsonl` 增量解析，汇总每个会话的状态、上下文用量、模型、最近活跃时间等信息。
- 用状态栏检测机制识别会话是 `Input`、`Work`、`Idle` 还是 `New`，并在表格视图与 Tamagotchi 像素生物视图中实时展示。
- 提供 `launch/new/resume --json` 等命令，以及 tmux popup 快捷键，使新建、恢复、跳转和脚本化自动化都能从一个入口完成。

## Results
- 论文摘录未提供标准基准测试、对照实验或正式量化指标，因此**没有可报告的学术型性能数字**。
- 系统声明支持对多个 Claude Code 会话进行统一管理，刷新频率为**每 2 秒轮询一次**，并使用**增量 JSONL 解析**实现实时状态更新。
- 界面可显示具体上下文配额数字，例如 **45k/1M、12k/200k、90k/200k**，帮助用户判断 token 使用情况。
- 支持按工作目录进行房间分组，采用 **2×2 网格分页**；可在一个 dashboard 中查看、切换、终止、创建和恢复会话。
- 声称可处理**同一仓库中的多个会话而不冲突**，并支持 `recon --json` 供脚本和自动化流程集成。
- 相比手工 tmux 管理，其最强的具体改进主张是：用户可通过**单个快捷键**弹出仪表盘，快速识别哪些代理正在工作、休眠或等待批准，并直接跳转到对应会话。

## Link
- [https://github.com/gavraz/recon](https://github.com/gavraz/recon)
