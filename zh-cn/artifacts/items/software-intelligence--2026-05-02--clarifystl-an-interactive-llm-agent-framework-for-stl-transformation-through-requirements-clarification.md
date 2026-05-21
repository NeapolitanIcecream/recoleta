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
ClarifySTL 是一个交互式 LLM 智能体系统，会在把自然语言需求转换为信号时序逻辑（STL）之前，请用户修正含糊或有歧义的需求。它面向网络物理系统规格说明；在这类规格中，缺失时间边界、阈值或指代不清都可能生成错误的形式化公式。

## 问题
- 自然语言 CPS 需求常常省略精确的时间区间、数值阈值或条件逻辑，导致无法可靠生成 STL。
- 有歧义的表述可能对应多个有效的 STL 公式，因此直接的自然语言到 STL 模型可能编码错误的用户意图。
- 对处理实时约束和实值约束的领域专家来说，手写 STL 速度慢且容易出错。

## 方法
- ClarifySTL 先运行一个微调过的含糊性检测器，对时间、数值和条件逻辑方面的含糊性进行分类，然后用思维链提示提出有针对性的问题。
- 它根据用户回答重写需求，并重复含糊性检查，直到检测不到缺失的 STL 关键细节。
- 随后，它运行一个用三元组对比学习构建的歧义检测器，用于识别指代歧义和语义歧义。
- 对于有歧义的情况，它会生成多个 STL 候选公式，将它们反向翻译成自然语言，比较不同解释，询问用户以澄清，并重复检查。
- 最终澄清后的需求会发送给 LLM，用于生成 STL 公式。

## 结果
- 在 DeepSTL 上，ClarifySTL 报告的公式准确率比当前最佳模型高 13.92%，模板准确率高 12.08%。
- 在 STL-DivEn 上，ClarifySTL 报告的公式准确率比当前最佳模型高 12.57%，模板准确率高 12.99%。
- 在 AmbiEval 上，ClarifySTL 报告的含糊性和歧义平均检测准确率为 90.9%。
- 人工评估显示，它能澄清 93.8% 的有缺陷需求。
- 人工评估认为，93.3% 的含糊性澄清问题和 94.3% 的歧义澄清问题有效。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01209v1](https://arxiv.org/abs/2605.01209v1)
