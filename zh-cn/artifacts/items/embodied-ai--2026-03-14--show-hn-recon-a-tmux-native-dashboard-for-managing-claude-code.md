---
source: hn
url: https://github.com/gavraz/recon
published_at: '2026-03-14T23:21:07'
authors:
- gavra
topics:
- developer-tools
- tmux-dashboard
- agent-orchestration
- terminal-ui
- claude-code
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Recon – A tmux-native dashboard for managing Claude Code

## Summary
Recon 是一个基于 tmux 的终端仪表盘，用来集中管理多个 Claude Code 会话，并让用户无需离开终端即可查看、切换、创建、终止和恢复代理。它的价值在于把多代理编程工作流从分散的 tmux 会话整合成一个统一、可视化且可脚本化的控制界面。

## Problem
- 当用户同时运行多个 Claude Code 代理时，缺少一个统一界面来查看每个代理的状态、是否卡住、最近活动和上下文使用情况。
- 仅靠手动切换 tmux 会话，难以及时发现哪些会话正在工作、哪些在等待审批、哪些已空闲，这会降低多代理开发效率。
- 恢复历史会话、在同一仓库中管理多个会话、以及将这些状态暴露给脚本自动化，都需要更可靠的会话识别和状态检测机制。

## Approach
- 核心方法很简单：让每个 Claude Code 实例运行在各自的 tmux session 中，再由 Recon 统一读取 tmux 和 Claude 本地状态文件，生成一个集中式 TUI 仪表盘。
- 它通过 `tmux list-panes` 获取 pane/session 信息，通过 `~/.claude/sessions/{PID}.json` 将进程可靠映射到 Claude 会话，而不是依赖 `ps` 或工作目录启发式。
- 它读取 `~/.claude/projects/.../*.jsonl` 和 `tmux capture-pane` 中的状态栏文本，判断会话是 Input、Work、Idle 还是 New，并显示模型、token 上下文和最近活跃时间。
- 界面提供两种视图：表格仪表盘和类电子宠物的像素生物可视化视图；同时支持 `recon --json` 作为脚本接口。
- 它还提供新建、恢复、命名恢复、弹窗快捷键和按仓库分房间展示等操作，使多会话管理直接嵌入 tmux 工作流。

## Results
- 文本中**没有提供正式基准、用户研究或量化实验结果**，因此没有可报告的准确率、延迟、效率提升百分比或与基线工具的对比数字。
- 给出的最具体运行特性包括：实时状态轮询周期为 **每 2 秒**，房间布局为 **2×2 网格并支持分页**。
- 支持显示 token 上下文使用量，示例包括 **45k/1M、12k/200k、8k/200k、90k/200k、3k/1M**。
- 支持至少 **6 个**并行会话的集中展示示例，覆盖 **Input / Work / Idle / New** 4 类状态。
- 声称的主要改进是：可靠的 PID→session 匹配、无需离开终端的集中管理、同仓库多会话无冲突、以及可恢复历史会话与 JSON 脚本化输出。

## Link
- [https://github.com/gavraz/recon](https://github.com/gavraz/recon)
