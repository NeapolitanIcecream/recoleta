---
source: arxiv
url: https://arxiv.org/abs/2605.19365v1
published_at: '2026-05-19T04:55:49'
authors:
- Ravishka Rathnasuriya
- Wei Yang
topics:
- code-intelligence
- input-adaptation
- uncertainty-estimation
- vulnerability-detection
- code-language-models
- inference-time-reliability
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# On-the-Fly Input Adaptation for Reliable Code Intelligence

## Summary
## 总结
这篇论文提出在推理时做输入适配，用来减少代码语言模型的错误预测，而且不需要重训、改架构或额外标注。初步结果显示，这种方法在漏洞检测上能提升准确率，而现有的不确定性指标对代码任务的错误检测能力较弱。

## 问题
- 即使只做保持语法不变的编辑，比如变量改名、控制流重组或语句重排，只要程序行为不变，代码语言模型的预测也会改变。
- 重训、改架构和提示词调优都会增加成本，需要部署工作，而且在不同任务或不同模型家族之间可能无法迁移。
- 可靠的代码智能很重要，因为在漏洞检测、修复、生成和审查中，错误输出会带来安全风险和生产风险。

## 方法
- 该方法先给模型输出分配一个有效性分数。对分类器来说，它使用子模型方差和到类别原型的距离等信号。对生成器来说，它使用解码信号和不同提示变体之间的一致性。
- 如果有效性分数低于任务阈值，方法就会改写或调整输入，然后重新做推理。
- 输入空间适配使用保持语义不变的编辑，包括变量改名、控制流重组、代码简化、提示改写、同义词替换和约束重排。
- 潜空间适配把输入嵌入推向与更高预测可靠性相关的区域，同时加入保持语义的边界。
- 候选适配会用有效性分数进行搜索和排序；文中提出的搜索方法包括进化搜索和受约束解码。

## 结果
- 现有的不确定性指标在检测生成错误时效果较弱：在 HumanEval+ 和 MBPP+ 上，使用 DeepSeek-Coder-7B 和 CodeLlama-7B 时，ROC-AUC 介于 0.466 到 0.666 之间。
- 在漏洞检测分类器上，不确定性指标也接近随机水平：在 DeepSeek-Coder-7B 和 CodeLlama-7B 上，ROC-AUC 介于 0.559 到 0.621 之间。
- 在使用 CodeBERT 的漏洞检测任务上，基础准确率为 63.36%；输入变换达到 71.52%（+8.16 个百分点），潜空间变换达到 76.75%（+13.39 个百分点）。
- 在使用 GraphCodeBERT 的漏洞检测任务上，基础准确率为 62.99%；输入变换达到 65.26%（+2.27 个百分点），潜空间变换达到 68.32%（+5.33 个百分点）。
- 报告的开销是：输入变换每个输入 49.92 到 59.4 秒，潜空间变换每个输入 2 到 3 秒。
- 该摘录没有给出生成适配、扩散引导、自回归修订或完整端到端方法的完整定量结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19365v1](https://arxiv.org/abs/2605.19365v1)
