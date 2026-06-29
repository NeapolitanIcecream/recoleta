---
source: arxiv
url: https://arxiv.org/abs/2605.19369v1
published_at: '2026-05-19T05:04:42'
authors:
- Ravishka Rathnasuriya
- Wei Yang
topics:
- code-calibration
- selective-prediction
- uncertainty-estimation
- code-intelligence
- abstention
- program-analysis
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions

## Summary
## 总结
本文提出了一个面向部署的代码模型决策流程：只有当经过校准的正确率分数超过阈值时才接受预测，低置信度样本则交给分析工具或恢复步骤处理。

## 问题
- 代码模型会对漏洞、缺陷、补全、生成和修复结果给出很高的错误置信度，这会让 IDE 和 CI 自动化变得有风险。
- 标准校准可以降低平均误差，但仍可能无法按正确性对单个代码预测排序，因此不一定支持选择性预测。
- 弃权之后还需要后续动作，比如静态分析、验证、提示增强或人工复核；否则只是把错误藏起来。

## 方法
- 系统从分类和生成式代码模型中提取不确定性信号，包括预测分布、类似熵的分数、边际、方差和采样分歧。
- 校准把这些信号映射为逐样本的正确率概率；文中给出的方案包括用于生成任务的加权 logistic 标定和用于分类任务的基于 logit 的正确率估计。
- 在推理阶段，可调阈值会接受高于分数截断线的输出，并对低分输出延期处理。
- 延期的生成样本会经过基于 MCP 的恢复流程，例如提示增强、文档注入、多样化解码、编译器检查、验证器、长度约束或任务拆分。
- 延期的分类样本可以用静态分析器、程序切片、规则验证器或安全模式检查来复核。

## 结果
- 在 MBPP+ 上，加权 Platt 校准把 DeepSeek-Coder-7B 的 Brier 分数从 0.273 和 ECE 从 0.223 降到 Brier 0.162 和 ECE 0.072；Platt scaling 为 0.224/0.103，isotonic regression 为 0.216/0.143。
- 在 MBPP+ 上，加权 Platt 校准把 CodeLlama-7B 的 Brier 分数从 0.220 和 ECE 从 0.108 降到 Brier 0.172 和 ECE 0.045；isotonic regression 达到 0.215/0.054。
- 在缺陷预测中，文中报告的 logit/置信度方法把 DeepSeek-Coder-7B 的 Brier 分数从 0.130 和 ECE 从 0.029 降到 Brier 0.098 和 ECE 0.012。
- 在缺陷预测中，同一方法把 Qwen-Coder-7B 的 Brier 分数从 0.137 和 ECE 从 0.023 降到 Brier 0.089 和 ECE 0.011。
- 论文报告，在 MBPP+ 生成任务中，覆盖率为 80% 时选择性预测准确率超过 70%；在缺陷预测中，覆盖率为 80% 时准确率超过 90%。
- 作者评估了 16 种不确定性指标，覆盖缺陷预测、漏洞检测和代码生成，结果发现没有一种与任务无关的指标能在缺少任务特定校准的情况下可靠支持弃权。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19369v1](https://arxiv.org/abs/2605.19369v1)
