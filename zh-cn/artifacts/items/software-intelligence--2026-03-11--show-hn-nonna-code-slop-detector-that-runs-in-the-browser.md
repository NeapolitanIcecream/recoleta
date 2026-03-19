---
source: hn
url: http://www.babush.me/nonna/
published_at: '2026-03-11T23:45:42'
authors:
- babush
topics:
- code-analysis
- browser-based
- privacy-preserving
- python-tools
- local-inference
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Nonna – code slop detector that runs in the browser

## Summary
这是一款名为 Nonna 的浏览器端“代码 slop 检测器”，用于本地分析上传的 Python 文件或压缩包。其核心价值在于无需上传代码到服务器即可完成检测，更强调隐私友好的轻量代码质量分析。

## Problem
- 要解决的问题是：如何检测代码中的“slop”（可理解为低质量、冗余或可疑模式）而不把源代码发送到远端服务。
- 这很重要，因为代码分析常涉及私有仓库、商业源码或敏感逻辑，开发者通常关心隐私与数据外泄风险。
- 现有摘录没有说明“slop”的严格定义、检测范围或适用场景细节。

## Approach
- 工具以浏览器应用形式运行，用户可上传 `.py` 或 `.zip` 文件进行分析。
- 分析过程在本地执行，文本明确声明“nothing is uploaded to a server”，即不依赖服务器端代码上传。
- 系统会加载一个“pre-indexed corpus”，暗示它可能将待测代码与预索引语料进行配对、包级或相似性相关分析。
- 界面中出现 “Pairs” 和 “Packages”，说明它可能支持以文件对或包级别组织检测结果，但摘录未给出算法细节。

## Results
- 提供的摘录**没有给出任何定量结果**，没有数据集、准确率、召回率、误报率、速度或与基线方法的对比数字。
- 最强的具体声明是：支持上传 `.py` / `.zip` 分析，并且**所有分析均在本地浏览器中完成**，代码**不会上传到服务器**。
- 还声明会“Loading pre-indexed corpus...”，表明系统具备可直接使用的预索引语料能力，但未说明规模与效果。

## Link
- [http://www.babush.me/nonna/](http://www.babush.me/nonna/)
