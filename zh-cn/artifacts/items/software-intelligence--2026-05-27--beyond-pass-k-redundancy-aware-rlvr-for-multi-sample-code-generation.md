---
source: arxiv
url: https://arxiv.org/abs/2605.28022v1
published_at: '2026-05-27T06:26:52'
authors:
- Le Bronnec Florian
- Alexandre Verine
- Rio Yokota
- Benjamin Negrevergne
topics:
- code-generation
- rlvr
- pass-at-k
- code-diversity
- software-foundation-models
- program-similarity
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond pass@k: Redundancy-Aware RLVR for Multi-Sample Code Generation

## Summary
## 总结
论文主张，多样本代码生成需要减少近重复程序，不能只提高单样本正确率。论文给 RLVR 加入了基于 JPlag 的反冗余奖励，并报告了在多个代码基准上的更好 Pass@k 结果。

## 问题
- Pass@k 只在 k 个采样程序里有一个通过测试时给模型奖励，但它不衡量这些样本是否覆盖了不同实现。
- 只优化正确性的 RLVR 会让模型重复生成相似的正确程序；当用户需要很多候选时，这会浪费有限的采样预算。
- 这一点对代码智能系统很重要，因为多样本生成在基准评测和实际程序合成流程里都很常见。

## 方法
- 论文用 JPlag 衡量实现层面的冗余。JPlag 是一个代码相似度工具，对变量改名、格式和注释的影响比字面重叠更小。
- 论文把 JPlag 多样性定义为采样组内两两 JPlag 相似度均值的 1 减去该值。
- 论文比较了只优化正确性的 RLVR、Pass@k-RLVR、PKPO，以及一个新的 JPlag-RLVR 目标，模型包括 Qwen3-4B、Qwen3-8B 和 Olmo3-7B。
- JPlag-RLVR 保留可执行正确性奖励，并加入组级反冗余奖励；该奖励用 leave-one-out 优势来鼓励样本让组内冗余更低。
- 评测在每个提示上采样 200 个生成结果，数据集是 MBPP、Code-Contest 和 TACO-Cobalt。

## 结果
- 在 2745 组提示级比较中，只优化正确性的 Base-RLVR 在 57.2% 的情况下降低了 JPlag 多样性，JDiv 平均变化为 -0.046；Pass@k-RLVR 在 66.9% 的情况中提高了 JPlag 多样性，JDiv 平均变化为 +0.123。
- 在同一组汇总比较中，JPlag-RLVR 在 77.4% 的情况中提高了 JPlag 多样性，JDiv 平均变化为 +0.298。它的 Pass@1、Pass@10 和 Pass@100 平均变化分别为 +16.4、+19.7 和 +17.3。
- 在 Qwen3-4B 的 MBPP 上，JPlag-RLVR 达到 Pass@1 93.2、Pass@10 98.9、Pass@100 99.3 和 JDiv 0.822；同一指标下，Base-RLVR 分别是 72.4、82.4、86.8 和 0.301。
- 在 Qwen3-8B 的 MBPP 上，JPlag-RLVR 的 Pass@10 为 98.5、Pass@100 为 99.2；Base-RLVR 分别为 88.0 和 90.8，PKPO 分别为 97.1 和 99.0。
- 在 Qwen3-8B 的 TACO 上，JPlag-RLVR 的 Pass@10 为 55.5、Pass@100 为 68.7；Base-RLVR 分别为 48.2 和 58.5，PKPO 分别为 51.0 和 64.7。
- 论文声称，JPlag 奖励通常能与专门面向 Pass@k 的目标持平或更好，同时还能生成冗余更少的代码样本。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28022v1](https://arxiv.org/abs/2605.28022v1)
