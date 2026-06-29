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
1GC-7RC 是一个面向自主编码代理的基准，用来测试它们在固定算力限制下构建和训练机器学习模型的能力。它检验代理能否在单张 A100 GPU 上、且不能访问互联网的条件下，在七个机器学习任务上写出有用的训练代码。

## 问题
- 现有的机器学习代理基准往往允许使用预训练权重、宽松的时间限制、开放式评分，或者覆盖更窄的任务范围。
- 这篇论文关注一个实际问题：编码代理能否从零开始，在语言、视觉、图、表格数据、时间序列和文本分类任务上设计、实现、训练并调参模型？
- 这很重要，因为机器学习团队可能会用编码代理完成端到端的模型工作，而固定的、基于指标的测试可以用来比较代理行为和失败模式。

## 方法
- 基准包含 7 个任务：TinyShakespeare 语言建模、TinyImageNet 分类、Pascal VOC 分割、ogbg-molhiv 图分类、Forest Cover 表格分类、ETTh1 预测和 AG News 文本分类。
- 每个任务都给代理一个基线 `train.py`、一个锁定的 `prepare.py`、本地数据和一个指标。代理可以编写改进版 `run_{x}.py` 文件，训练模型，并保存可计分的检查点。
- 有 6 个任务禁止使用预训练权重。分割任务允许使用两个预先下载好的 DINOv3 主干，因为在这个预算内很难从零训练出有用的 Pascal VOC 分割结果。
- 运行环境使用一张 NVIDIA A100 80 GB GPU、不能联网、不能安装包，每个任务的时间预算为 40 到 120 分钟。
- 评分使用确定性指标，并把每个代理-任务组合重复 5 次。研究共评估 7 个代理，总计 245 次运行。

## 结果
- 基准的基线结果是：T1 TinyShakespeare 3.438 bpb，T2 TinyImageNet 0.343 top-1 accuracy，T3 Pascal VOC 0.660 mIoU，T4 ogbg-molhiv 0.706 AUROC，T5 Forest Cover 0.806 accuracy，T6 ETTh1 0.384 MSE，T7 AG News 0.793 accuracy。
- 摘录中展示了完整的一行代理结果：Claude Code with Sonnet 4.6 在 T1 上达到 2.2325 ± 0.2097 bpb，在 T2 上达到 0.6813 ± 0.0252 accuracy，在 T3 上达到 0.8322 ± 0.0074 mIoU，在 T4 上达到 0.7663 ± 0.0116 AUROC，在 T5 上达到 0.9632 ± 0.0063 accuracy，在 T6 上达到 0.3809 ± 0.0049 MSE，在 T7 上达到 0.9211 ± 0.0024 accuracy。
- Sonnet 4.6 在可见的 7 个任务指标上都优于所给基线，在 TinyImageNet、Pascal VOC、Forest Cover 和 AG News 上的可见相对提升最大。
- 论文报告 Sonnet 4.6 相对于基线的 7 个任务综合得分为 +0.293。
- 研究比较了 7 个代理：Claude Sonnet 4.6、Claude Opus 4.6、Claude Opus 4.7、通过 Codex CLI 的 GPT-5.5、通过 OpenCode 的 Qwen 3.6+，以及通过 OpenCode 的 Kimi K2.5/K2.6。给出的摘录说闭源代理优于开源替代方案，但这里完整的逐代理表格被截断了。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17046v2](https://arxiv.org/abs/2605.17046v2)
