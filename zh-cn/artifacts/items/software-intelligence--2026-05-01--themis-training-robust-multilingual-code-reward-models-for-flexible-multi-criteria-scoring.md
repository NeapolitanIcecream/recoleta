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
## 摘要
Themis 训练代码奖励模型，用于从正确性、运行时间、内存、可维护性和安全性五个方面评估生成代码，覆盖八种编程语言。论文面向代码后训练场景，尤其是执行测试不可用或测试范围过窄的情况。

## 问题
- 代码后训练常使用测试用例执行，但这种方法只适用于可执行、独立完整的代码，并且主要奖励功能正确性。
- 真实代码质量还取决于运行时间、内存使用、可维护性和安全性，所以单一执行信号会漏掉开发者的常见需求。
- 现有代码奖励评测主要关注 Python 和有效-有缺陷的解答对，因此不能很好地测试多语言、多标准评分。

## 方法
- 作者构建了 Themis-CodeRewardBench，包含约 8.9k 个成对代码偏好、8 种语言和 5 个标准：功能正确性、执行效率、内存效率、可读性和可维护性，以及安全硬度。
- 他们在该基准上分析了 50 多个代码、数学和通用奖励模型，以找出现有代码评分的差距。
- 他们创建了 Themis-CodePreference，包含超过 350k 个代码偏好对，并创建了 Themis-GeneralPreference，包含超过 110k 个通用领域偏好。
- 他们使用成对偏好学习训练 600M 到 32B 参数规模的 Themis-RM 模型，并使用文本标准，让用户可以对 5 个代码质量维度中的任意子集评分。

## 结果
- 摘录没有给出 Themis-RM 的具体准确率、胜率或排名指标值。
- 基准贡献很具体：约 8.9k 个偏好、8 种语言、5 个评分维度，数据来自正确性、效率、内存、可维护性和安全性来源。
- 训练数据主张很具体：超过 350k 个开源代码偏好对，加上超过 110k 个通用偏好对。
- 模型套件覆盖 600M 到 32B 参数规模，并声称显示出正向缩放趋势。
- 论文声称多样化偏好带来跨语言迁移，并且多标准训练会提高可靠性，但摘录没有提供具体数值增益。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00754v3](https://arxiv.org/abs/2605.00754v3)
