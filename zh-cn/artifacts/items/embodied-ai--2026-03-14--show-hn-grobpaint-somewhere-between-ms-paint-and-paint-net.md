---
source: hn
url: https://github.com/groverburger/grobpaint
published_at: '2026-03-14T22:41:28'
authors:
- __grob
topics:
- image-editor
- cross-platform
- vanilla-javascript
- pywebview
- layered-editing
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: GrobPaint: Somewhere Between MS Paint and Paint.net

## Summary
GrobPaint 是一个轻量级、跨平台的图像编辑器，定位在 MS Paint 和 Paint.NET 之间，主打“够用而不臃肿”。它用原生 Web 技术和极小的 Python 后端实现，在 macOS 等 Paint.NET 不支持的平台上提供替代方案。

## Problem
- 解决的问题是：Paint.NET 不支持 macOS，而更重型的编辑器又过于复杂或臃肿，用户缺少一个跨平台、轻量但功能完整的中间选择。
- 这很重要，因为许多用户只需要图层、选择、基础绘图和文件导出等常用功能，不需要 Photoshop 级别的复杂度。
- 该项目还试图降低开发和分发复杂度，避免 npm、打包器和繁重依赖。

## Approach
- 核心方法很简单：前端使用 **vanilla JavaScript + ES modules** 实现编辑器主体，后端仅用一个很小的 **Python + pywebview** 壳来提供原生窗口能力。
- 如果没有 pywebview，它会自动退回到浏览器运行模式；也可以直接打开 `index.html`，以浏览器文件输入/下载替代原生文件对话框。
- 功能设计上聚焦“实际需要的工具”：图层、16 种混合模式、矩形/魔棒选择、常见绘图工具、画布缩放平移、剪贴板粘贴、多文档标签页、精灵表处理等。
- 项目格式 `.gbp` 采用 **ZIP + manifest.json + 分层 PNG** 的结构来保存图层、透明度、可见性和混合模式，机制直接且易于移植。
- 工程实现强调极简：约 **2500 行** 原生 JavaScript、分成 **4 个模块**，除浏览器侧 JSZip 外几乎无额外依赖，也没有 npm、bundler 或 build step。

## Results
- 文本**没有提供正式基准测试或用户研究的量化结果**，因此没有准确的性能、效率或对比指标可报告。
- 给出的最具体结果是功能覆盖：支持 **16 种 blend modes**、多种绘图/选择/变换工具，以及 **PNG/JPEG/BMP/GIF** 和原生 `.gbp` 格式。
- 工程规模方面，应用约为 **2500 行 vanilla JavaScript**，拆分为 **4 个模块**，Python 依赖要求为 **Python 3.9+**。
- 分发方面，可通过 `build.sh` 生成 macOS 的 `dist/GrobPaint.app` 或二进制版本，说明其跨平台和可部署性是主要卖点。
- 相比 Paint.NET/Photoshop，这项工作的核心主张不是性能突破，而是在 **跨平台、轻量实现、低依赖** 与 **实用编辑能力** 之间取得平衡。

## Link
- [https://github.com/groverburger/grobpaint](https://github.com/groverburger/grobpaint)
