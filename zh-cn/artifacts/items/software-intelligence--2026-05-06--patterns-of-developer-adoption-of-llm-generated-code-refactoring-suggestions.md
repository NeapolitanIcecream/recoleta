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
本文研究开发者在真实的 GitHub 提交中如何使用 ChatGPT 的重构建议。核心结论是，开发者通常几乎不改动就提交这些建议，或者只选取较大建议中的一部分，丢弃其余内容。

## 问题
- 这篇论文针对的是 LLM 代码重构研究中的一个空缺：以往工作评估的是建议质量，而这项研究衡量的是开发者在实际仓库里如何应用这些建议。
- 这很重要，因为重构会影响可维护性和正确性，团队需要知道 ChatGPT 的输出何时可以直接复制、修改后使用，或只当作起点。
- 这项研究只覆盖链接到 ChatGPT 对话的提交，因此没有衡量被拒绝的建议。

## 方法
- 作者从 DevGPT 入手。这个数据集收录了 29,778 条 ChatGPT 提示和回复、19,106 个代码片段，以及 3,245 个提交对象，采集时间为 2023 年 7 月至 8 月。
- 他们用 25 个与重构相关的关键词筛选提交，去掉重复项和无效的 GitHub 链接，最后构建出一个经过整理的数据集，包含 169 个重构提交和 440 个变更文件数据点。
- 对每个变更文件，他们根据 GitHub 的统一 diff 重建提交前后的文件，提取 ChatGPT 代码块，并用归一化 Levenshtein 相似度把每个已提交文件映射到最相似的 ChatGPT 建议。
- 他们用 Jaccard 3-gram 相似度、归一化 Levenshtein 相似度、token 匹配率和 CrystalBLEU 来估计采纳程度。
- 他们手动检查了 190 个数据点，用来分类重构活动和开发者编辑方式，然后剔除 16 个把行为改动混入其中、并非纯重构的案例。

## 结果
- 开发者通常在 ChatGPT 对话中的 1 到 4 轮提示内得到一个被采纳的重构建议。
- Jaccard 3-gram 和归一化 Levenshtein 分数呈双峰分布：很多案例的相似度在 0.1 到 0.3 左右，也有很多案例高于 0.9。
- Token 匹配率主要集中在 0.9 以上，低值几乎没有密度。这说明很多 Jaccard 或 Levenshtein 较低的案例，来自开发者删掉了 ChatGPT 较大建议中没用的部分。
- 在手动检查的子集里，可读性是最常见目标，占 38%；可维护性排在第二，占 34%。
- 观察到的最常见重构活动是重命名，44 个案例；其次是改进文档，37 个；重组，36 个；以及拆分逻辑，33 个。
- 一个仓库 tisztamo/Junior 贡献了 143 个提交和 407 个文件，因此这个数据集存在明显的项目不平衡。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04835v1](https://arxiv.org/abs/2605.04835v1)
