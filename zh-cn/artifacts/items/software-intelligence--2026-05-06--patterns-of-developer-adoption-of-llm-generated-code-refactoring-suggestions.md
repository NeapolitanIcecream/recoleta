---
source: arxiv
url: https://arxiv.org/abs/2605.04835v1
published_at: '2026-05-06T12:31:49'
authors:
- "David Sch\xF6n"
- Faiza Amjad
- Tehreem Asif
- Ranim Khojah
- Mazen Mohamad
- Francisco Gomes de Oliveira Neto
- Philipp Leitner
topics:
- code-refactoring
- llm-code-generation
- developer-adoption
- github-mining
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Patterns of Developer Adoption of LLM-Generated Code Refactoring Suggestions

## Summary
## 摘要
本文研究开发者如何在真实 GitHub 提交中使用 ChatGPT 的重构建议。主要结论是，开发者经常只做少量修改就提交这些建议，或者从较大的建议中选取部分内容并丢弃其余内容。

## 问题
- 本文处理的是 LLM 代码重构研究中的一个缺口：以往工作评估建议质量，本研究衡量开发者如何在实际代码库中应用这些建议。
- 这一点很重要，因为重构会影响可维护性和正确性，团队需要知道什么时候可以复制 ChatGPT 输出、编辑它，或把它当作起点。
- 研究只覆盖提交信息中链接到 ChatGPT 对话的提交，因此不衡量被拒绝的建议。

## 方法
- 作者从 DevGPT 开始，DevGPT 包含 2023 年 7 月至 8 月收集的 29,778 条 ChatGPT 提示和回答、19,106 个代码片段，以及 3,245 个提交对象。
- 他们用 25 个重构相关关键词筛选提交，移除重复项和无效 GitHub 链接，然后构建了一个人工整理的数据集，包含 169 个重构提交和 440 个变更文件数据点。
- 对每个变更文件，他们根据 GitHub unified diffs 重建提交前后的文件，提取 ChatGPT 代码块，并使用归一化 Levenshtein 相似度把每个已提交文件映射到最相似的 ChatGPT 建议。
- 他们用 Jaccard 3-gram 相似度、归一化 Levenshtein 相似度、token 匹配率和 CrystalBLEU 估计采纳程度。
- 他们人工检查 190 个数据点，对重构活动和开发者编辑进行分类，然后排除 16 个提交改变了行为而非仅做重构的案例。

## 结果
- 开发者通常在 ChatGPT 对话的 1 到 4 条提示内得到被采纳的重构建议。
- Jaccard 3-gram 和归一化 Levenshtein 分数呈双峰分布：许多案例处在 0.1 到 0.3 左右的低相似度区间，另有许多案例高于 0.9。
- token 匹配率集中在 0.9 以上，低值区间几乎没有密度，这表明许多低 Jaccard 或 Levenshtein 案例来自开发者删除了较大 ChatGPT 建议中未使用的部分。
- 在人工检查的子集中，可读性是最常见的目标，占 38%；可维护性其次，占 34%。
- 最常见的重构活动是重命名 44 例、改进文档 37 例、重组 36 例、拆分逻辑 33 例。
- 一个代码库 tisztamo/Junior 贡献了 143 个提交和 407 个文件，因此数据集存在强烈的项目不均衡。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04835v1](https://arxiv.org/abs/2605.04835v1)
