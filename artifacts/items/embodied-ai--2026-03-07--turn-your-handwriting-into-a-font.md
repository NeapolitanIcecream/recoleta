---
source: hn
url: https://arcade.pirillo.com/fontcrafter.html
published_at: '2026-03-07T23:59:17'
authors:
- andonumb
topics:
- font-generation
- handwriting-vectorization
- opentype
- client-side-processing
- privacy-preserving
relevance_score: 0.02
run_id: materialize-outputs
---

# Turn Your Handwriting into a Font

## Summary
FontCrafter 是一个将手写扫描件自动转换为可安装字体的纯浏览器端工具，主打本地隐私、零注册和多格式导出。其核心价值在于把复杂的字形提取、矢量化和 OpenType 构建流程自动化，让普通用户也能快速生成可用的个人字体。

## Problem
- 它解决的是**如何把个人手写内容低门槛地制作成真实可安装字体**的问题，这对设计、教学、内容创作和品牌个性化很重要。
- 传统同类工具常依赖**云端处理、账号注册和付费功能门槛**，带来隐私、成本和使用摩擦。
- 仅把图片切出来还不够；真正可用的字体还需要**字形轮廓、字距、连字、替换规则和标准字体表**等完整字体工程支持。

## Approach
- 输入一张手写扫描图后，系统在浏览器本地运行多阶段图像处理：**自适应阈值分割 → 连通域检测 → Suzuki-Abe 轮廓追踪 → RDP 简化 → Chaikin 平滑 → 三次 Bézier 拟合**，把墨迹变成干净的矢量字形。
- 它**从零构建 OpenType 字体**，而不是套模板替换图片；字高、升部、降部、x-height 等度量直接从用户手写样本中估计。
- 为了让字体更像真实手写，系统在 GSUB 中加入**上下文替换（calt）**，每个字符最多保存 **3** 个手写变体，并在连续输入时轮换显示。
- 它还能自动生成**连字（如 ff、fi、th、st）**、类级别 kerning、重音/扩展字符，并支持 **OTF、TTF、WOFF2、Base64** 本地导出。
- 额外还支持 **COLR/CPAL 彩色字体**效果，如阴影、墨迹纹理和双色分层，全部在客户端通过 JavaScript 生成，无需服务器或 WebAssembly。

## Results
- 文本**没有提供标准基准测试或实验数据**，因此没有可验证的准确率、速度或与学术基线的量化比较。
- 具体功能结果包括：生成**超过 500 个 glyphs** 的标准字体，其中 **100+** 重音字符可由基础字母自动组合得到。
- 每个字符最多可保留 **3 个** 手写变体，并通过 **calt** 规则自动轮换，以减少重复字母机械感。
- 支持自动连字，示例包括 **ff、fi、fl、th、st**；支持 OTF/TTF/WOFF2/Base64 **4 种**输出格式。
- 文中声称 WOFF2 相比原始 OTF **通常可缩小 30–50%**，适合网页嵌入，但未给出该工具上的实测文件统计。
- 相比 Calligraphr，作者声称其差异在于：**0 注册、100% 本地处理、免费包含连字/上下文替换/彩色字体效果**，但未提供正式对比实验或用户研究数据。

## Link
- [https://arcade.pirillo.com/fontcrafter.html](https://arcade.pirillo.com/fontcrafter.html)
