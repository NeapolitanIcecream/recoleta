---
source: arxiv
url: https://arxiv.org/abs/2606.04594v1
published_at: '2026-06-03T08:32:13'
authors:
- Yile Gu
- Zhen Zhang
- Shaowei Zhu
- Xinwei Fu
- Jun Wu
- Yida Wang
- Baris Kasikci
topics:
- llm-inference
- silent-errors
- debugging
- code-intelligence
- llm-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Ekka: Automated Diagnosis of Silent Errors in LLM Inference

## Summary
## 摘要
Ekka 通过在中间模型状态上比较有问题的引擎和正确的参考实现，诊断 LLM 服务系统中的静默准确性和输出错误。它把人工的张量检查变成一个自动化代理流程，并对最可能出错的组件进行排序。

## 问题
- vLLM 和 SGLang 等系统中的静默错误会返回看起来合理的文本，但准确率下降或输出出错，运行时没有错误或警告。
- 论文提到一个 vLLM 的 Gemma 3 问题，Hellaswag 准确率下降了将近 30%，开发者花了数月才把原因追到滑动窗口注意力的误用。
- 根因可能出现在模型代码、kernel 后端、数值精度或服务逻辑中，只看输出很难找出故障组件。

## 方法
- Ekka 在同一模型、提示和设置下运行有问题的目标系统和参考实现，例如 HuggingFace Transformers。
- 它在复现错误时收集中间激活值和调用序列。
- 它为两个实现构建模型树，然后把语义匹配的组件映射起来，即使一侧把模块融合了，例如 QKV 投影。
- 它生成代码，用于对齐在形状、数据类型和内存布局差异下的激活值。
- 它计算一个错误比例来过滤小的数值差异，然后用变点分析找出目标系统和参考实现第一次明显分歧的位置。

## 结果
- 在真实静默错误基准上，Ekka 的 pass@1 诊断准确率为 80%，pass@5 诊断准确率为 88%。
- 这项基准研究收集了 90 个静默错误：48 个来自 vLLM，42 个来自 SGLang；其中 70 个已关闭 issue 用于分析。
- 在这 70 个已关闭 issue 中，准确率回归是最大的症状类别，占 43.8%。
- 根因占比分别是：框架实现 30.6%，模型实现 25.5%，kernel 后端 24.5%，数值精度 19.4%。
- Ekka 诊断了来自 vLLM 和 SGLang 的 17 个 issue，报告的准确率提升比现有系统高 24% 到 34%，每个案例平均成本约 30 美元。
- 它还诊断出 vLLM 和 SGLang 中 4 个新的静默错误，开发者已经确认了这 4 个错误。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04594v1](https://arxiv.org/abs/2606.04594v1)
