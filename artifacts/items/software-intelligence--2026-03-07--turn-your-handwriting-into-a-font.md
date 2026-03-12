---
source: hn
url: https://arcade.pirillo.com/fontcrafter.html
published_at: '2026-03-07T23:59:17'
authors:
- andonumb
topics:
- font-generation
- handwriting-recognition
- browser-based-tool
- opentype
- privacy-preserving
relevance_score: 0.22
run_id: materialize-outputs
---

# Turn Your Handwriting into a Font

## Summary
FontCrafter 是一个把手写扫描件直接转换为可安装字体的纯浏览器端工具，重点是**本地隐私处理**和**完整 OpenType 字体生成**。它不仅提取字形，还自动补全连字、上下文替代、字距调整和多格式导出。

## Problem
- 现有手写转字体工具常依赖**云端上传、账号注册或付费订阅**，对隐私、易用性和成本不友好。
- 仅把图片换进模板并不足够；真正可用的字体还需要**矢量轮廓、字形度量、字距、连字、扩展字符和导出格式**等完整字体工程。
- 这很重要，因为用户希望把自己的手写体用于设计、教学、内容创作和商业用途，同时又不想泄露原始手写数据。

## Approach
- 用户上传一张手写扫描图后，系统在浏览器本地运行多阶段图像处理：**自适应阈值化 → 连通域检测 → Suzuki-Abe 轮廓跟踪 → RDP 简化 → Chaikin 平滑 → 三次 Bézier 拟合**，把每个字符变成干净的矢量路径。
- 它不是套模板替换字形，而是**从零构建 OpenType 字体表**：使用 CFF 轮廓、1000 UPM，并从扫描结果中估计 ascender、descender、cap height、x-height 等真实度量。
- 为了让字体更像自然手写，它为每个字符保留最多 **3 个变体**，通过 **GSUB contextual alternates (`calt`)** 在输入时轮换，避免重复字母看起来完全一样。
- 它还自动生成 **ligatures (`liga`)**、类字距调整（kerning）、100+ 重音/扩展字符，以及可选 **COLR/CPAL 彩色字体效果**；最后本地导出 **OTF、TTF、WOFF2、Base64**。

## Results
- 文中**没有给出正式实验、基准数据或学术评测指标**，因此没有可核验的准确率、速度或质量分数。
- 具体能力声明：标准字体可生成**500+ glyphs**，其中包含**100+** 自动合成的重音和扩展字符。
- 变体机制声明：每个字符最多保留**3 个手写版本**，并通过 `calt` 自动轮换，以减少重复字符的机械感。
- 格式能力声明：支持导出 **4 种格式**（**OTF / TTF / WOFF2 / Base64**），且全部**本地生成**；其中 WOFF2 被称为通常比原始 OTF **小 30–50%**。
- 功能对比声明：相较 Calligraphr，作者声称 FontCrafter **无需账号、完全免费、本地处理**，并免费提供连字、上下文替代、彩色字体效果，以及 **WOFF2/Base64** 导出。
- 边界条件声明：当前**不支持** variable fonts、hinting、RTL 脚本、CJK 字符集和多页模板扫描。

## Link
- [https://arcade.pirillo.com/fontcrafter.html](https://arcade.pirillo.com/fontcrafter.html)
