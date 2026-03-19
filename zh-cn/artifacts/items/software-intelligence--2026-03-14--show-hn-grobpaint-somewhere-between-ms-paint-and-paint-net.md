---
source: hn
url: https://github.com/groverburger/grobpaint
published_at: '2026-03-14T22:41:28'
authors:
- __grob
topics:
- image-editor
- cross-platform
- vanilla-js
- python-backend
- desktop-app
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: GrobPaint: Somewhere Between MS Paint and Paint.net

## Summary
GrobPaint 是一个介于 MS Paint 和 Paint.NET 之间的轻量级跨平台图像编辑器，重点是在 macOS 等平台提供足够实用的绘图与图层能力。它用原生 Web 技术和极小的 Python 后端实现，强调无构建、低依赖和可直接运行。

## Problem
- 解决 Paint.NET 无法在 macOS 运行、而更重型工具又过于臃肿的问题。
- 面向只需要常见绘图、图层、选择和导出功能的用户，降低安装、构建和使用门槛。
- 这很重要，因为跨平台轻量图像编辑工具能填补“功能够用但不复杂”的实际生产空白。

## Approach
- 核心方法是用 **vanilla JavaScript + ES modules** 构建前端，再用一个很小的 **Python + pywebview** 外壳提供原生窗口；没有 npm、没有 bundler、没有构建步骤。
- 在最简单层面，它就是把常用图像编辑能力做成一个可直接运行的网页应用，并在桌面端用 Python 包一层以获得更原生的体验。
- 功能上提供图层系统、16 种混合模式、常见绘图/选择/变换工具、调色、缩放/平移、多文档和剪贴板粘贴。
- 通过原生 `.gbp` 项目格式保存图层信息；该格式本质上是 ZIP，内含 `manifest.json` 和各图层 PNG，便于简单持久化与导出。
- 可在 pywebview 中运行，也可退化到浏览器模式；甚至可以直接打开 `index.html`，只是文件对话框会退化为浏览器上传/下载。

## Results
- 提供了较完整的“够用型”编辑器能力：**16 种 blend modes**、多种绘图与选择工具、图层增删改合并、透明度控制、裁剪、缩放、翻转、sprite sheet 处理等。
- 代码规模约 **2500 行 vanilla JavaScript**，拆分为 **4 个模块**，依赖极少；除可选 `pywebview` 外，浏览器侧仅提到 **1 个 CDN 依赖（JSZip）**。
- 运行要求为 **Python 3.9+**；可通过 `python grobpaint.py` 直接启动，并可打包生成 **macOS app** 或二进制版本。
- 文本中**没有提供标准数据集、基准测试或定量性能指标**，因此没有可核验的精度/速度/用户研究数值结果。
- 最强的具体主张是：它在 **跨平台、低依赖、无构建流程** 的前提下，覆盖了介于 MS Paint 与 Paint.NET 之间的大部分核心编辑需求，尤其填补了 macOS 上的 Paint.NET 式空白。

## Link
- [https://github.com/groverburger/grobpaint](https://github.com/groverburger/grobpaint)
