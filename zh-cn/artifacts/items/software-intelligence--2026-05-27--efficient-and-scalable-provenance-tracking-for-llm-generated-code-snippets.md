---
source: arxiv
url: https://arxiv.org/abs/2605.28510v1
published_at: '2026-05-27T14:12:17'
authors:
- Andrea Gurioli
- Davide D'Ascenzo
- Federico Pennino
- Maurizio Gabbrielli
- Stefano Zacchiroli
topics:
- code-provenance
- llm-generated-code
- code-retrieval
- plagiarism-detection
- vector-search
- software-compliance
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Efficient and Scalable Provenance Tracking for LLM-Generated Code Snippets

## Summary
## 总结
HybridSourceTracker 在大规模语料库上把 LLM 生成的代码片段追溯到可能的源片段。它把一个 3 亿参数的代码编码器和 Winnowing 指纹重排序结合起来，在避免全量线性扫描的同时保持较高的匹配质量。

## 问题
- 代码 LLM 可能直接复现训练样本，或复现改写后的变体，这会给开发者带来抄袭、署名和许可证合规风险。
- 基于 Winnowing 的检测器对代码相似度判断有效，但把查询和十亿级训练语料逐一比较太慢，因为搜索成本会随着语料规模增长。
- 纯精确匹配的追溯系统在标识符或局部名称变化后，会漏掉很多经过改写的片段。

## 方法
- SourceTracker 把代码片段和完整代码片段编码成 1024 维向量，然后用 Qdrant 的 HNSW 向量检索找出附近的片段。
- 该模型使用 ModularStarEncoder 的前 9 层，总计 3 亿参数，并用 CLIP 对比损失训练，让匹配的片段-代码片段对在向量空间中更接近。
- 训练使用 TheStackV2 的 1000 万片段子集中的 60 token 片段；其中 50% 是逐字复制，50% 替换了常见标识符，用来模拟改名后的代码。
- HybridSourceTracker 先取向量检索的前 100 个候选，再只对这些候选应用 Winnowing 指纹和 Jaccard 相似度。
- 这样把昂贵的精确比较限制在固定规模的集合上，查询复杂度就随语料规模按对数增长。

## 结果
- 在一个 10 万片段的体外搜索空间里，面对改写后的查询，HST 在 30 token 窗口上与 Winnowing 的 MRR 持平，在 60 token 及以上窗口上超过它。
- 论文报告称，HST 在至少 60 token 的窗口上比 Winnowing 最高高出 5.4%，同时通过 Qdrant 保持对数时间检索。
- 在 10 万片段、type-2 克隆的条件下，与 OLMoTrace 比较时，HST 在更长窗口上明显更强：OLMoTrace 在 60 token 时的 MRR 为 44.3%，与 HST 相差 -45.3 个百分点，这意味着 HST 为 89.6%。
- 同一组 OLMoTrace 对比还表明，HST 在 120 token 时的 MRR 为 95.4%，240 token 时为 98.2%，480 token 时为 99.3%。
- 只有在 7 token 时 OLMoTrace 表现更好：MRR 为 26.1%，比 HST 高 15.6 个百分点，这意味着 HST 为 10.5%。
- 该系统在 TheStackV2 的 1000 万片段子集上训练和评估，最终报告的搜索空间实验范围为 1,000 到 100,000 个样本，窗口长度为 7 到 480 token。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28510v1](https://arxiv.org/abs/2605.28510v1)
