---
source: hn
url: https://github.com/fashton28/mux
published_at: '2026-06-28T23:42:55'
authors:
- fashton28
topics:
- claude-code
- tmux
- session-management
- developer-tools
- human-ai-interaction
- coding-agents
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Mux – A tmux overlay for managing Claude Code sessions

## Summary
## 摘要
Mux 是一个 tmux 浮层，面向同时运行多个 Claude Code 会话的用户。它显示哪个会话需要输入，并让用户跳到对应窗格。

## 问题
- 在多个 tmux 窗格中运行 Claude Code 时，很容易漏掉等待输入的阻塞会话；这会浪费代理辅助编码的时间。
- 仅靠 tmux，无法在一个视图中显示 Claude 状态、工作目录、状态持续时间和实时窗格预览。

## 方法
- 核心方法很直接：读取 Claude Code 自己的状态文件，并把它们匹配到当前 tmux 服务器上的活动窗格。
- 它在 tmux 内打开一个 fzf 浮动浮层，每个活动 Claude 会话占一行。
- 每行显示状态、tmux 会话、工作目录，以及状态变化后的分钟数。
- 它按状态排序，让等待中的会话排在工作中、空闲和未知会话之前；在每个分组内，卡住时间最长的会话排在最前。
- Enter 切换到选中的窗格；ctrl-x 发送带保护的 SIGTERM 来终止一个 Claude 会话。

## 结果
- 摘录没有报告基准测试、用户研究、延迟或采用量数据。
- 它声称支持单键跳转：按 Enter 会切换到选中的 Claude 窗格，包括其他 tmux 窗口中的窗格。
- 浮层打开时，它会刷新列表和计时器，并以分钟报告状态持续时间，例如等待 2899m 和等待 304m。
- 它把列表限制为当前 tmux 服务器上的活动 Claude 会话，因此每一行都可以直接打开。
- 它暴露 5 个子命令：mux、mux list、mux preview <pane>、mux jump <pane> <window> <session> 和 mux kill <pid>。
- 正常使用需要 3 个外部工具：tmux、fzf 和 jq，其中 fzf >= 0.38。

## Problem

## Approach

## Results

## Link
- [https://github.com/fashton28/mux](https://github.com/fashton28/mux)
