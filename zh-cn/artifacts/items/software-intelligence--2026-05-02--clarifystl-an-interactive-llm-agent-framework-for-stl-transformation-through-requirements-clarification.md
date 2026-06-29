---
source: arxiv
url: https://arxiv.org/abs/2605.01209v1
published_at: '2026-05-02T02:55:06'
authors:
- Yue Fang
- Zhi Jin
- Jie An
- Hongshen Chen
- Xiaohong Chen
- Naijun Zhan
topics:
- llm-agents
- requirements-engineering
- signal-temporal-logic
- formal-specification
- human-ai-interaction
- cyber-physical-systems
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification

## Summary
## 摘要
ClarifySTL 是一个交互式 LLM 智能体系统，会先让用户修正含糊或有歧义的自然语言需求，再把它们转换为信号时序逻辑（STL）。它面向 साइber-physical system 规格，缺失的时间边界、阈值或不清楚的指代都可能生成错误的形式化公式。

## 问题
- 自然语言的 CPS 需求常常省略精确的时间区间、数值阈值或条件逻辑，导致无法忠实生成 STL。
- 含糊的表述可能对应多个有效的 STL 公式，直接的 NL-to-STL 模型可能会写入错误的用户意图。
- 对处理实时和实值约束的领域专家来说，手写 STL 既慢又容易出错。

## 方法
- ClarifySTL 先运行一个经过微调的模糊性检测器，分类时间、数值和条件逻辑上的模糊表达，然后用 Chain-of-Thought 提示提出针对性问题。
- 它会根据用户回答重写需求，并重复检查模糊性，直到不再检测到缺失的 STL 关键信息。
- 接着，它运行一个基于 triplet contrastive learning 的歧义检测器，用于识别指代歧义和语义歧义。
- 对于有歧义的情况，它会生成多个 STL 候选，把它们反向翻译回自然语言，比较不同解释，向用户询问澄清，并重复检查。
- 最后，澄清后的需求会送入 LLM 生成 STL 公式。

## 结果
- 在 DeepSTL 上，ClarifySTL 的 Formula Accuracy 比当前最优模型高 13.92%，Template Accuracy 高 12.08%。
- 在 STL-DivEn 上，Formula Accuracy 高 12.57%，Template Accuracy 高 12.99%。
- 在 AmbiEval 上，它对模糊性和歧义性的平均检测准确率为 90.9%。
- 人工评估显示，它澄清了 93.8% 的有缺陷需求。
- 人工评估将 93.3% 的模糊性澄清问题和 94.3% 的歧义性澄清问题评为有效。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01209v1](https://arxiv.org/abs/2605.01209v1)
