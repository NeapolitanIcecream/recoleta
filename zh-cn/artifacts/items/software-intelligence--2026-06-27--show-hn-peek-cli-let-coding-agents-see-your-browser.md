---
source: hn
url: https://github.com/puffinsoft/peek-cli
published_at: '2026-06-27T22:50:37'
authors:
- BeverlyHills001
topics:
- coding-agents
- browser-screenshots
- developer-tools
- human-ai-interaction
- agent-safety
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Peek-CLI: let coding agents see your browser

## Summary
## 摘要
peek-cli 为编码代理提供一种只读方式，用于从已打开的浏览器标签页捕获截图。它面向需要检查正在运行的 Web 应用、但不应获得浏览器控制权的代理。

## 问题
- 编码代理常常需要来自 localhost 应用、UI 测试或基于浏览器的工作流的视觉反馈，但许多配置不允许它们查看浏览器。
- 直接控制浏览器可能带来安全风险，因为代理可能点击、输入、注入脚本或更改用户数据。
- 这个工具对代理辅助的前端工作有价值，因为截图可以帮助代理验证 UI 状态并调试视觉输出。

## 方法
- Chrome 扩展从已打开的标签页捕获截图，并通过本地 WebSocket 守护进程传输。
- CLI 使用 `peeked start` 启动守护进程，使用 `peeked list` 列出可见标签页，并使用 `peeked at <url>` 保存某个标签页的截图。
- 代理通过插件或 skill 经由 CLI 请求截图，文中给出了 Claude Code 和 Codex 的设置路径。
- 安全模型是只读的：摘录称代理可以请求截图，但不能访问浏览器、注入脚本或执行操作。
- 用户必须在每次启动时连接一次代理，这增加了一个手动批准步骤。

## 结果
- 摘录中未提供基准测试结果、用户研究、延迟数字或准确性指标。
- 该工具声称至少支持 3 个具名代理客户端：Claude Code、Codex 和 Copilot。
- 示例流程展示了 3 个核心 CLI 命令：`peeked start`、`peeked list` 和 `peeked at <url>`。
- 安全声明中允许代理执行的操作只有 1 个：捕获截图。
- 该项目是 MIT 许可证下的开源软件；Chrome 扩展仍在等待批准，因此目前需要手动安装。

## Problem

## Approach

## Results

## Link
- [https://github.com/puffinsoft/peek-cli](https://github.com/puffinsoft/peek-cli)
