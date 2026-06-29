---
source: arxiv
url: https://arxiv.org/abs/2604.25903v1
published_at: '2026-04-28T17:48:16'
authors:
- Ajmain Inqiad Alam
- Palash Roy
- Chanchal K. Roy
- Banani Roy
- Kevin A. Schneider
topics:
- llm-compression
- code-intelligence
- green-ai
- model-distillation
- software-engineering
- quantization
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Carbon-Taxed Transformers: A Green Compression Pipeline for Overgrown Language Models

## Summary
## 摘要
Carbon-Taxed Transformers 是一个面向代码语言模型的压缩流水线，能降低推理内存、延迟和 CO2 成本，同时保留大部分任务性能。它面向代码克隆检测、代码摘要和代码生成，覆盖仅编码器、编码器-解码器和仅解码器三类 Transformer。

## 问题
- 软件工程中使用的大语言模型运行成本高，部署慢，内存占用大，推理时能耗也高。
- 论文把推理效率和 CO2 排放当作设计约束，因为部署后的推理可能占据机器学习计算和能耗的主要部分。
- 以往压缩研究常常只对一个模型或一个任务使用一种方法，关于在软件工程工作负载上按顺序应用多步压缩的证据较少。

## 方法
- CTT 先用神经架构搜索，在严格的延迟和内存限制下找到更小的学生架构。
- 然后对层、注意力头、隐藏维度和前馈维度做结构化剪枝，只保留验证损失仍可接受的缩减结果。
- 它在训练前对剪枝后的模型做量化，让学生模型在低精度数值约束下学习。
- 它用知识蒸馏训练量化后的学生模型，让模型去匹配教师输出，而不是只依赖硬标签。
- 测试任务覆盖三类 Transformer：用于克隆检测的 UniXCoder 风格仅编码器模型、用于代码摘要的编码器-解码器模型，以及用于代码生成的仅解码器模型。

## 结果
- CTT 在评测的软件工程模型上报告了最高 49 倍的内存缩减。
- 推理延迟在克隆检测上下降 8-10 倍，在摘要上最高下降 3 倍，在生成上下降 4-7 倍。
- 报告中的推理 CO2 排放最高下降 81%。
- 性能保留方面，克隆检测准确率约为 98%，摘要约为 89%，文本生成指标最高为 91%。
- 在代码生成的 pass@1 上，压缩后的模型最高保留 68% 的性能。
- 两项消融研究表明，NAS→剪枝→量化→蒸馏的顺序，以及各个压缩组件本身，对这些收益都很重要。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25903v1](https://arxiv.org/abs/2604.25903v1)
