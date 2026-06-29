---
source: hn
url: https://arxiv.org/abs/2605.16517
published_at: '2026-05-23T22:23:12'
authors:
- daureg
topics:
- enterprise-llm
- code-intelligence
- software-engineering
- llm-finetuning
- developer-tools
- internal-code-data
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Customizing an LLM for Enterprise Software Engineering

## Summary
## 摘要
Gemini for Google（GfG）把 Gemini 适配到 Google 内部的软件工程工作中，使用专有开发数据、继续训练和后训练。论文声称，在一项包含 29,000 名开发者的盲测中，它降低了交互成本，并提高了代码保留率。

## 问题
- 企业软件团队会生成大量关于代码变更、评审、部署和维护工作的私有痕迹，但通用 LLM 不会直接从这些公司特定数据中学习。
- 更好的内部模型很重要，因为软件工程辅助必须符合本地代码、工具、架构和评审要求。
- 额外的内部数据训练有一个主要风险：它可能通过灾难性遗忘损害模型的通用能力。

## 方法
- 作者构建了 Gemini for Google，这是一个面向 Google 内部软件工程环境调优的 Gemini 适配版。
- 他们整理了一个规模达到万亿 token 的专有软件工程数据集。
- 训练包括继续预训练和后训练，使模型既能学习内部代码和工作流，又能继续作为助手使用。
- 在定制过程中，使用了中期训练策略来减少灾难性遗忘。
- 论文还描述了基于该定制模型部署下游开发者应用。

## 结果
- 在一项包含 29,000 名 Google 开发者的盲测 A/B 研究中，GfG 在开发者交互指标上优于未命名基线。
- 与基线相比，每轮平均迭代次数下降了 23%，这意味着开发者完成请求所需的来回轮次更少。
- 与基线相比，代码保留率提高了约 17%，这意味着更多生成或辅助生成的代码继续被使用。
- 该适配过程按 4 个方面展开：信号提取、数据准备、全栈调优和下游应用部署。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.16517](https://arxiv.org/abs/2605.16517)
