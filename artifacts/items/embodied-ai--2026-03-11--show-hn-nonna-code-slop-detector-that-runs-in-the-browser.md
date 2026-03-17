---
source: hn
url: http://www.babush.me/nonna/
published_at: '2026-03-11T23:45:42'
authors:
- babush
topics:
- code-quality
- static-analysis
- browser-based
- privacy-preserving
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: Nonna – code slop detector that runs in the browser

## Summary
这是一个名为 Nonna 的浏览器端“代码 slop 检测器”，用于本地分析上传的 Python 文件或压缩包。给定内容更像产品页面摘录，而不是研究论文，因此可确认的信息很有限。

## Problem
- 试图解决“代码 slop”检测问题，即帮助用户识别代码中低质量、冗余或可疑的模式。
- 该问题之所以重要，是因为代码质量问题会影响可维护性、审查效率以及开发者对自动生成代码或大型代码库的信任。
- 从页面描述看，它尤其强调隐私与易用性：分析在本地浏览器中完成，不需要把代码上传到服务器。

## Approach
- 核心机制似乎是：用户上传 `.py` 或 `.zip`，工具在浏览器本地对代码进行分析，并与某个“预索引语料库（pre-indexed corpus）”进行比对或检索。
- 页面中出现了 `Pairs`、`Packages` 和“Loading pre-indexed corpus...”，暗示它可能通过代码片段配对、包级统计或语料匹配来发现“slop”。
- 最简单地说：它像一个前端运行的代码检查器，把你的 Python 代码拿来和已有语料做对照，找出可疑的低质量模式。
- 明确可见的实现特征是**纯本地分析**："Files are analyzed locally — nothing is uploaded to a server"。

## Results
- 提供的文本**没有任何量化实验结果**，没有数据集、指标、基线或精度/召回率数字。
- 最强的具体声明是：支持上传 `.py` / `.zip` 进行分析。
- 另一项具体声明是：分析在浏览器本地完成，文件不会上传到服务器。
- 页面还声明会加载“预索引语料库”，表明系统依赖现成语料进行检测，但未说明规模、来源或效果。

## Link
- [http://www.babush.me/nonna/](http://www.babush.me/nonna/)
