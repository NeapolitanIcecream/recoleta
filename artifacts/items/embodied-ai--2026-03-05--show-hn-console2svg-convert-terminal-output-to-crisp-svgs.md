---
source: hn
url: https://github.com/arika0093/console2svg
published_at: '2026-03-05T23:48:22'
authors:
- arika0093
topics:
- terminal-svg
- developer-tools
- cli-visualization
- ci-automation
- documentation
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: Console2svg – Convert terminal output to crisp SVGs

## Summary
console2svg 是一个把终端输出直接转换成清晰、可缩放 SVG 的命令行工具，重点解决截图模糊和文档维护麻烦的问题。它还支持动画、裁剪、回放和 CI 集成，面向开发文档与演示场景。

## Problem
- 传统终端截图通常保存为 PNG 等光栅图，放大后文字会发糊，不利于高质量文档、博客和演示。
- 终端内容经常需要展示动态执行过程、局部裁剪或统一外观，现有方案在这些工作流上不够方便。
- 在 CI 中自动生成终端图像时，颜色、环境变量和可复现性容易出问题，导致代码与文档截图不一致。

## Approach
- 核心方法很简单：运行一个命令或读取管道中的终端输出，捕获带颜色/控制序列的文本，再把它渲染成矢量 SVG，而不是位图截图。
- 提供静态模式和视频模式；视频模式把命令执行过程保存成动画 SVG，适合展示交互或命令运行过程。
- 提供 replay 机制：先记录键盘输入与时间戳到 JSON，再根据该记录重新生成 SVG，从而提高可复现性并便于在 CI 中重建演示。
- 提供多种后处理能力，包括按像素/字符/文本模式裁剪、窗口边框与背景样式、自定义颜色/提示符/标题等，使输出更适合发布。
- 为 CI 场景自动设置 TERM=xterm-256color、COLORTERM=truecolor、FORCE_COLOR=3，并删除可能让库关闭颜色的 CI/TF_BUILD 变量，以尽量保留彩色终端效果。

## Results
- 文本未提供标准学术基准或实验数据，因此**没有定量性能结果、准确率或与基线的系统性数值比较**。
- 具体能力声明包括：支持 **truecolor**、**动画 SVG**、**文本模式裁剪**、**背景/窗口装饰**、**回放 JSON** 和 **CI 自动生成**。
- 平台覆盖声明：支持 **Windows 10+（ConPTY）**、**Linux**、**macOS**，且 **v0.6.2+** 原生支持 macOS arm64。
- 默认/可配置参数给出了一些明确数值：宽度默认 **100 字符**（pty 模式），高度在 pty 模式下**自动适配**；回放文件中若总时长偏差超过 **1 秒** 会报超时错误。
- 示例中展示了动画录制与截断能力，如 `--timeout 5`、`--sleep 0.5` 用于导出长时间运行命令的动画 SVG，但未给出与其他工具相比的速度、体积或质量数字提升。
- 主要“突破”更像产品特性组合：**零依赖分发**（npm、dotnet tool、静态二进制）、**动画 SVG 输出**、**基于文本锚点裁剪**、**可重放交互录制**，以及对文档/博客/社交媒体的直接适配。

## Link
- [https://github.com/arika0093/console2svg](https://github.com/arika0093/console2svg)
