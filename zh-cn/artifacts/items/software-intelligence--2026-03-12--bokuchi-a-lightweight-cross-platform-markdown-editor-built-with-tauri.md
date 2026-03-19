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
relevance_score: 0.19
run_id: materialize-outputs
language_code: zh-CN
---

# Bokuchi: A lightweight, cross-platform Markdown editor built with Tauri

## Summary
Bokuchi 是一个基于 Tauri 和 Rust 的轻量级跨平台 Markdown 编辑器，主打低内存占用、快速启动和实时预览。它面向需要简单高效写作工具的用户，用更轻的技术栈替代常见的 Electron 方案。

## Problem
- 许多 Markdown 编辑器依赖 Electron，通常带来更高的内存占用和更重的运行开销。
- 用户需要一个可在 macOS、Windows 和 Linux 上一致运行、且启动迅速的写作工具。
- 除了基础编辑，用户还需要实时预览、多文档处理、查找替换和导出占位符等实用能力。

## Approach
- 采用 **Tauri + Rust** 构建应用，而不是 Electron，以减少资源消耗并提升启动速度。
- 提供 **分栏编辑/预览**：左侧编辑 Markdown，右侧实时渲染预览。
- 集成常见写作工作流功能，如多文档支持、全文查找替换、导出时变量占位符扩展。
- 提供可定制界面与行为设置，包括多主题和 14 种界面语言支持。

## Results
- 声称相较于 **Electron-based editors**，内存占用 **低于三分之一**（即使用不到其 1/3 的内存）。
- 声称启动时间 **低于 1 秒**。
- 支持 **3 大桌面平台**：macOS、Windows、Linux。
- 提供 **14 种 UI 语言**。
- 文本未提供标准基准测试、数据集、实验设置或与特定竞品的可复现实验结果。

## Link
- [https://bokuchi.com/](https://bokuchi.com/)
