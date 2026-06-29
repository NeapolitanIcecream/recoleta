---
source: arxiv
url: https://arxiv.org/abs/2605.00754v3
published_at: '2026-05-01T16:07:34'
authors:
- Indraneil Paul
- "Goran Glava\u0161"
- Iryna Gurevych
topics:
- code-reward-models
- code-intelligence
- preference-learning
- multilingual-code
- software-post-training
- code-quality
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Themis: Training Robust Multilingual Code Reward Models for Flexible Multi-Criteria Scoring

## Summary
## 总结
Themis 训练代码奖励模型，对生成代码的正确性、运行时间、内存、可维护性和安全性进行评分，覆盖 8 种编程语言。本文面向那类没有执行测试可用，或测试范围过窄的代码后训练场景。

## 问题
- 代码后训练通常依赖测试用例执行，这只适用于可执行的、自包含的代码，而且主要只奖励功能正确性。
- 真实的代码质量还取决于运行时间、内存占用、可维护性和安全性，所以单一的执行信号会漏掉很多开发者需求。
- 现有的代码奖励评估主要聚焦 Python 和有效-有 bug 的解答对，因此并不能很好地测试多语言、多标准评分。

## 方法
- 作者构建了 Themis-CodeRewardBench，包含约 8.9k 个成对代码偏好、8 种语言和 5 个标准：功能正确性、执行效率、内存效率、可读性与可维护性，以及安全性。
- 他们在这个基准上评估了 50 多个代码、数学和通用奖励模型，找出现有代码评分中的缺口。
- 他们创建了 Themis-CodePreference，包含超过 350k 个代码偏好对，以及 Themis-GeneralPreference，包含超过 110k 个通用领域偏好。
- 他们使用成对偏好学习训练了 Themis-RM，参数规模从 600M 到 32B 不等，并加入文本化标准，让用户可以对 5 个代码质量维度中的任意子集打分。

## 结果
- 摘要没有给出 Themis-RM 的准确率、胜率或排序指标的具体数值。
- 基准贡献很明确：约 8.9k 个偏好、8 种语言、5 个评分维度，数据来源覆盖正确性、效率、内存、可维护性和安全性。
- 训练数据规模也很明确：超过 350k 个开源代码偏好对，加上超过 110k 个通用偏好对。
- 这套模型覆盖 600M 到 32B 参数，作者声称它显示出正向的规模扩展趋势。
- 论文还声称，使用多样偏好训练能带来跨语言迁移，并提高多标准训练下的可靠性，但摘要没有给出具体数值提升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00754v3](https://arxiv.org/abs/2605.00754v3)
