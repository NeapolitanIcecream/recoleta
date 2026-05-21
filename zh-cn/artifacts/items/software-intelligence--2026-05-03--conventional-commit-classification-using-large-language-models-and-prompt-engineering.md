---
source: arxiv
url: https://arxiv.org/abs/2605.02033v1
published_at: '2026-05-03T19:52:39'
authors:
- H. M. Sazzad Quadir
- Sakib Al Hasan
- Md. Nurul Ahad Tawhid
topics:
- commit-classification
- conventional-commits
- prompt-engineering
- code-intelligence
- software-repository-mining
- large-language-models
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Conventional Commit Classification using Large Language Models and Prompt Engineering

## Summary
## 摘要
这篇论文测试开源 LLM 是否能在不微调的情况下把代码 diff 分类为 Conventional Commit 类型。few-shot 提示的平均准确率最高，但单次最佳结果只是在一个 InfluxDB 数据集上达到 0.6154 准确率。

## 问题
- 许多仓库的提交信息缺少结构，限制了变更日志生成、语义化版本控制和发布自动化。
- 现有提交分类器通常需要标注数据集、预处理、特征工程，并且在项目术语或标签变化时需要重新训练。
- 论文研究仅用提示的 LLM 分类是否能降低 Conventional Commit 标签分类的设置成本。

## 方法
- 作者从 InfluxDB GitHub 仓库挖掘了 3,200 个大致均衡的提交，并使用 Conventional Commit 类型作为真实标签。
- 每个样本都根据其代码 diff 进行分类；没有对任何模型进行微调。
- 他们测试了 zero-shot、few-shot 和思维链提示。
- 他们用准确率、精确率、召回率和 F1 评估 Mistral-7B-Instruct、LLaMA-3-8B 和 DeepSeek-R1-32B。

## 结果
- 单次最佳运行：Mistral-7B-Instruct 使用 few-shot 提示，在 3,200 个 InfluxDB 提交上达到 0.6154 准确率、0.3823 精确率、0.6154 召回率和 0.4706 F1。
- DeepSeek-R1-32B 在不同提示下的模型平均表现最好：0.563 准确率、0.587 精确率、0.563 召回率和 0.538 F1。
- few-shot 提示在不同模型下的平均提示表现最好：0.531 准确率和 0.468 F1；zero-shot 为 0.431 准确率和 0.399 F1。
- 思维链提示没有提高准确率：其平均准确率为 0.468，低于 few-shot 的 0.531。
- LLaMA-3-8B 的平均表现最弱，在不同提示下为 0.372 准确率和 0.366 F1。
- 论文没有与训练过的 ML 基线或微调后的 LLM 基线比较，因此这些结果更支持提示选择指导，而不是新的准确率基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02033v1](https://arxiv.org/abs/2605.02033v1)
