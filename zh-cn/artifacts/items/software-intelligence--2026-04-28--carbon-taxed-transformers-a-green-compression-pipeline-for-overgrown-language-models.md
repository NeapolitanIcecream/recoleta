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
Carbon-Taxed Transformers 是面向代码语言模型的压缩流水线，可降低推理内存、延迟和 CO2 成本，同时保留大部分任务性能。它面向克隆检测、代码摘要和代码生成，覆盖仅编码器、编码器-解码器和仅解码器 Transformer。

## 问题
- 软件工程中使用的大语言模型运行成本高、部署慢、占用内存大，推理阶段能耗高。
- 论文将推理效率和 CO2 排放作为设计约束，因为部署后的推理可能占据机器学习总计算量和能源使用的主要部分。
- 以往压缩工作通常把一种方法应用到一个模型或一项任务上，对软件工程工作负载中的有序多步骤压缩提供的证据较少。

## 方法
- CTT 首先使用神经架构搜索，在严格的延迟和内存限制下寻找更小的学生架构。
- 随后，它对层、注意力头、隐藏层大小和前馈层大小进行结构化剪枝，并且只在验证损失保持可接受时保留缩减。
- 它在训练前对剪枝后的模型进行量化，使学生模型在低精度数值约束下学习。
- 它使用知识蒸馏训练量化后的学生模型，匹配教师模型输出，而不是只依赖硬标签。
- 测试任务覆盖三类 Transformer：UniXCoder 风格的仅编码器克隆检测、编码器-解码器代码摘要，以及仅解码器代码生成。

## 结果
- CTT 报告称，在评估的软件工程模型中，内存最多减少 49×。
- 推理延迟在克隆检测中降低 8-10×，在摘要中最多降低 3×，在生成中降低 4-7×。
- 报告的推理 CO2 排放最多下降 81%。
- 性能保留情况报告为：克隆检测约 98% 准确率，摘要约 89%，文本生成指标最高 91%。
- 对于代码生成 pass@1，压缩模型最多保留 68% 的性能。
- 两项消融研究称，NAS→剪枝→量化→蒸馏的顺序以及各个压缩组件，都是取得所报告收益所需的因素。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25903v1](https://arxiv.org/abs/2604.25903v1)
