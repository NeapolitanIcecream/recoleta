---
source: arxiv
url: https://arxiv.org/abs/2605.17046v2
published_at: '2026-05-16T15:35:22'
authors:
- Robin-Nico Kampa
- Fabian Deuser
- "Anna B\xF6\xDFend\xF6rfer"
- Konrad Habel
- Norbert Oswald
topics:
- coding-agents
- ml-benchmark
- automated-ml-engineering
- code-intelligence
- agent-evaluation
- single-gpu-training
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# 1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?

## Summary
## 摘要
1GC-7RC 是一个面向自主编码智能体的基准，用于测试它们在固定计算限制下构建和训练机器学习模型的能力。它检验智能体能否在无互联网访问的情况下，用一块 A100 GPU 为七项机器学习任务编写有用的训练代码。

## 问题
- 现有的机器学习智能体基准通常允许使用预训练权重、时间限制较宽、评分方式开放，或任务覆盖范围较窄。
- 论文关注一个实际问题：编码智能体能否在语言、视觉、图、表格数据、时间序列和文本分类等任务中，从零设计、实现、训练并调优模型？
- 这一点很重要，因为机器学习团队可能会用编码智能体完成端到端模型工作，而基于固定指标的测试有助于比较智能体行为和失败模式。

## 方法
- 该基准包含 7 项任务：TinyShakespeare 语言建模、TinyImageNet 分类、Pascal VOC 分割、ogbg-molhiv 图分类、Forest Cover 表格分类、ETTh1 预测和 AG News 文本分类。
- 每项任务都会向智能体提供一个基线 `train.py`、一个锁定的 `prepare.py`、本地数据和一个指标。智能体可以编写改进版 `run_{x}.py` 文件、训练模型，并保存用于评分的检查点。
- 其中 6 项任务禁止使用预训练权重。分割任务允许使用两个预先下载的 DINOv3 骨干网络，因为在预算时间内从零训练出可用的 Pascal VOC 分割模型很难。
- 运行环境使用一块 NVIDIA A100 80 GB GPU，无互联网访问，不能安装软件包；各任务预算为 40 到 120 分钟。
- 评分使用确定性指标，并对每个智能体-任务组合重复运行 5 次。研究评估了 7 个智能体，共 245 次运行。

## 结果
- 该基准的基线结果为：T1 TinyShakespeare 3.438 bpb，T2 TinyImageNet 0.343 top-1 准确率，T3 Pascal VOC 0.660 mIoU，T4 ogbg-molhiv 0.706 AUROC，T5 Forest Cover 0.806 准确率，T6 ETTh1 0.384 MSE，T7 AG News 0.793 准确率。
- 摘录展示了一整行智能体结果：Claude Code with Sonnet 4.6 在 T1 上达到 2.2325 ± 0.2097 bpb，在 T2 上达到 0.6813 ± 0.0252 准确率，在 T3 上达到 0.8322 ± 0.0074 mIoU，在 T4 上达到 0.7663 ± 0.0116 AUROC，在 T5 上达到 0.9632 ± 0.0063 准确率，在 T6 上达到 0.3809 ± 0.0049 MSE，在 T7 上达到 0.9211 ± 0.0024 准确率。
- Sonnet 4.6 在全部 7 个可见任务指标上都超过了提供的基线，其中 TinyImageNet、Pascal VOC、Forest Cover 和 AG News 的可见相对提升最大。
- 论文报告 Sonnet 4.6 在 7 项任务上的总体相对基线得分为 +0.293。
- 研究比较了 7 个智能体：Claude Sonnet 4.6、Claude Opus 4.6、Claude Opus 4.7、通过 Codex CLI 使用的 GPT-5.5、通过 OpenCode 使用的 Qwen 3.6+，以及通过 OpenCode 使用的 Kimi K2.5/K2.6。所提供的摘录称，专有智能体优于开源替代方案，但完整的逐智能体表格在此处被截断。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17046v2](https://arxiv.org/abs/2605.17046v2)
