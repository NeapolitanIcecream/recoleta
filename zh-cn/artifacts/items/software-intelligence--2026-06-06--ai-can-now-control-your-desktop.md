---
source: hn
url: https://clawdcursor.com
published_at: '2026-06-06T23:14:25'
authors:
- AmDab
topics:
- desktop-automation
- mcp
- ai-agents
- human-ai-interaction
- code-intelligence
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# AI Can now control your desktop

## Summary
## 摘要
clawdcursor 是一个用于桌面控制的 MCP 工具，允许 AI 模型通过可访问性 API、OCR、截图和受保护的动作调用来操作本地应用。它面向编辑器内运行的代理和本地自动化，不带遥测。

## 问题
- AI 编码代理通常停留在编辑器里，无法操作原生桌面应用、浏览器窗口、安装程序或操作系统对话框。
- 只靠像素控制成本高，也不稳定，因为即使应用的可访问性元数据已经能识别按钮、输入框和菜单，它还是会把截图发给视觉模型。
- 桌面自动化需要统一的权限和安全路径，因为点击、输入、文件操作和破坏性动作都会影响用户的机器。

## 方法
- 该系统提供一个 MCP 入口，可以通过 stdio 在 Claude Code、Cursor、Windsurf 或 Zed 中运行，也可以作为位于 127.0.0.1:3847/mcp 的 HTTP MCP 守护进程运行。
- 它先尝试可访问性树，再尝试 OCR，最后才在画布式 UI 上使用截图和视觉。
- 它提供 6 组紧凑工具：computer、accessibility、window、system、browser 和 task。另有 94 工具的细粒度接口可用于兼容性和调试。
- 每次工具调用都会经过 safety.evaluate()，破坏性操作需要确认。
- 它通过原生 UIA、Windows.Media.Ocr、AT-SPI、Tesseract、X11、Wayland，以及 macOS 的 Accessibility 和 Screen Recording 权限支持 macOS、Windows 和 Linux。

## 结果
- 摘要没有给出基准准确率、延迟、成本或任务完成率结果。
- 紧凑版 MCP 目录有 6 个工具，并声称比 94 工具的细粒度目录小约 12 倍。
- 紧凑版目录声称使用约 1,500 个 token。
- 批量确定性操作可以把 N 次工具调用合并成 1 次受保护调用。
- 该产品声称只在本地运行、只通过 localhost 访问、没有遥测，并支持 macOS、Windows、Linux、X11 和 Wayland。

## Problem

## Approach

## Results

## Link
- [https://clawdcursor.com](https://clawdcursor.com)
