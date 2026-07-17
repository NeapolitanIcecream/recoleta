---
source: arxiv
url: https://arxiv.org/abs/2607.14657v1
published_at: '2026-07-16T07:22:57'
authors:
- Ahmed Adnan
- Mushfiqur Rahman
- Antu Saha
- Oscar Chaparro
topics:
- ai-ml-maintenance
- issue-resolution
- software-engineering-for-ml
- reproducibility
- artifact-provenance
- human-ai-collaboration
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Rethinking Issue Resolution for AI/ML Systems

## Summary
## 摘要
论文认为，AI/ML 问题解决需要能够建模实验、不确定性以及源代码之外其他工件的工作流。对 TensorFlow、scikit-learn、MLflow 和 AutoGPT 中 100 个问题开展的定性研究，为迭代式、关注工件的框架提供了初步证据。

## 问题
- 传统的问题解决框架通常假设行为基本确定、调试以代码为中心，并采用通过/失败式验证，这些假设无法完全适用于 AI/ML 系统。
- 解决 AI/ML 问题可能需要修改数据集、提示词、模型、超参数、依赖项和基础设施，因此难以保证可复现性和可追溯性。

## 方法
- 作者对 2020–2025 年随机抽取的 100 个已关闭问题及其相关拉取请求进行了定性分析，其中 TensorFlow、scikit-learn、MLflow 和 AutoGPT 各包含 25 个问题。
- 两位作者独立对 988 个片段进行开放编码，通过共识解决分歧，并在现有问题解决编码表的基础上扩展了 AI/ML 特有的活动、挑战和缓解策略。
- 分析将传统解决阶段与模型性能监控、参数调优与训练、数据修改和模型功能分析等 AI/ML 活动进行了比较。
- 基于研究结果，论文提出了未来框架应支持的方向，包括跨阶段迭代式工作流、关注可复现性的验证、工件溯源、异构工件协调以及人机协作。

## 结果
- 研究在 100 个问题中识别出 947 项传统问题解决活动和 41 项 AI/ML 特有活动；其中 64 个问题被归类为 AI/ML 问题，18 个为混合问题，18 个为非 AI/ML 问题。
- AI/ML 特有活动的出现比例为：模型性能监控占 27% 的问题，参数调优与训练占 11%，数据修改占 7%，模型功能分析占 5%。
- 在 64 个 AI/ML 问题中，有 28 个（45%）需要修改生产代码之外的内容，包括提示词、数据集、超参数、依赖项、CI、Docker 或运行时配置。相比之下，非 AI/ML 问题中仅修改代码即可解决的比例为 83%，混合问题为 77%。
- 传统阶段同样较为常见：65% 的问题包含问题分析，62% 包含解决方案设计，54% 包含实现，53% 包含验证，42% 包含复现，34% 包含代码审查。
- 报告的挑战包括：9 个问题涉及将修复方案扩展到更大的数据集或分布式训练，6 个涉及理解模型架构，4 个涉及非确定性解决方案的验证，4 个涉及问题复现。开发者通过重复执行、统计检验、容器化环境、文档记录和分布式验证等方式进行缓解。
- 证据仍属初步结果：研究仅涵盖四个开源项目，并采用定性共识编码，没有提供编码者间一致性指标，因此这些模式未必能推广到其他 AI/ML 系统。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14657v1](https://arxiv.org/abs/2607.14657v1)
