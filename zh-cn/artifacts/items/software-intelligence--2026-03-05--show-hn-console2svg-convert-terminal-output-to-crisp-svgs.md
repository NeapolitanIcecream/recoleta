---
source: hn
url: https://github.com/arika0093/console2svg
published_at: '2026-03-05T23:48:22'
authors:
- arika0093
topics:
- terminal-rendering
- svg-generation
- developer-tooling
- ci-automation
- command-line-interface
relevance_score: 0.52
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Console2svg – Convert terminal output to crisp SVGs

## Summary
console2svg 是一个把终端输出转换为清晰、可缩放 SVG 的命令行工具，重点解决终端截图模糊和文档素材难自动化生成的问题。它还支持动画 SVG、裁剪、回放和 CI 集成，面向开发文档与演示场景。

## Problem
- 终端内容通常被保存为 PNG 等位图，放大后文字会发糊，不适合高质量文档、博客和社交媒体展示。
- 现有方案往往依赖额外软件、难以在 CI 中稳定复现，且对动态命令执行、精确裁剪和跨平台支持不够友好。
- 对开发者而言，可重复生成与代码状态一致的终端演示素材很重要，因为文档截图过时或失真会降低可读性和可信度。

## Approach
- 核心方法是直接捕获终端输出或命令执行过程，并将其渲染为矢量 SVG，而不是先截图成像素图；因此文字在任意缩放下都保持清晰。
- 提供静态模式和视频模式（`-v`），可把命令执行动画保存为 SVG；还支持 `--timeout`、`--sleep` 控制长时间或非终止命令的录制展示。
- 通过 `--replay-save` / `--replay` 把终端交互记录为简单 JSON，再基于记录重放生成 SVG，使结果更可复现、也便于在 CI 中生成一致素材。
- 支持按像素、字符或文本模式裁剪输出，并可增加窗口边框、背景、渐变、图片背景、提示符和标题等外观选项，直接产出演示级图像。
- 工具强调“无依赖”和跨平台分发，可作为 npm、dotnet tool、静态二进制和 GitHub Action 使用，并自动调整 CI 环境变量以保留彩色输出。

## Results
- 论文/项目说明没有提供标准基准测试、公开数据集或与其他工具的定量对比结果，因此**没有量化性能或质量指标**可报告。
- 给出的最强具体主张是：生成的是 **SVG 矢量图**，文本“在任意缩放下保持清晰”，相对 PNG 等位图截图可避免模糊。
- 功能性结果包括：支持 **TrueColor**、**动画 SVG**、**基于文本模式的裁剪**、**背景/窗口装饰**、**CI 友好回放**、以及 **Windows/macOS/Linux** 跨平台运行。
- 兼容性主张包括：Windows 10+（需 ConPTY）、Linux、macOS；并注明 **v0.6.2 及以后** 原生支持 macOS arm64。
- 可复现性方面，回放文件包含如 `totalDuration: 10.9530099` 这样的执行时长与逐键事件时间戳，说明其不仅保存最终输出，还能重建交互过程，但这仍是功能展示而非对比实验结果。

## Link
- [https://github.com/arika0093/console2svg](https://github.com/arika0093/console2svg)
