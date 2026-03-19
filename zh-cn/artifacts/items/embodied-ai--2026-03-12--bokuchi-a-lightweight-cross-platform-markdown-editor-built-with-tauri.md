---
source: hn
url: https://bokuchi.com/
published_at: '2026-03-12T23:22:44'
authors:
- nogajun
topics:
- markdown-editor
- tauri
- rust
- cross-platform
- lightweight-app
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Bokuchi: A lightweight, cross-platform Markdown editor built with Tauri

## Summary
Bokuchi 是一款基于 Tauri 与 Rust 的轻量级跨平台 Markdown 编辑器，主打实时预览、低内存占用和快速启动。它面向需要简单高效写作工具的用户，强调比 Electron 类编辑器更轻、更快。

## Problem
- 许多 Markdown 编辑器基于 Electron，常见问题是内存占用高、启动慢，影响日常写作体验。
- 用户通常需要跨平台、一致的编辑体验，以及实时预览、多文档、查找替换等基础生产力功能。
- 轻量化很重要，因为写作工具应尽量减少系统资源消耗并随时可用。

## Approach
- 使用 **Tauri + Rust** 而非 Electron 构建应用，以更小的运行时开销实现桌面 Markdown 编辑器。
- 提供 **分栏实时预览**：左侧编辑、右侧即时渲染，降低写作与检查格式之间的切换成本。
- 支持 **多文档编辑**、全文查找替换、导出占位符（如 `{{author}}`）等常用写作功能。
- 通过 **跨平台支持**（macOS、Windows、Linux）、多主题和可配置设置，提升通用性与可用性。
- 提供 **14 种界面语言**，增强国际化覆盖。

## Results
- 声称相较于 **基于 Electron 的编辑器**，内存占用 **低于其三分之一**（即少于约 33%）。
- 声称应用启动时间 **低于 1 秒**。
- 支持 **3 大桌面平台**：macOS、Windows、Linux。
- 提供 **14 种 UI 语言**。
- 文本未提供标准基准测试、数据集、对照实验或更细粒度测评，因此缺少可独立验证的学术型定量结果。

## Link
- [https://bokuchi.com/](https://bokuchi.com/)
