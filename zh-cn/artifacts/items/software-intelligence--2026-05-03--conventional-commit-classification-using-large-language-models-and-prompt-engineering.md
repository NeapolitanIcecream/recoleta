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
## 总结
本文测试开源 LLM 是否能在不微调的情况下，把代码 diff 分类到 Conventional Commit 类型。少样本提示给出最佳平均准确率，但单次最佳结果只有在一个 InfluxDB 数据集上的 0.6154 准确率。

## 问题
- 许多仓库的提交消息缺少结构，这会限制变更日志生成、语义化版本控制和发布自动化。
- 现有提交分类器通常需要标注数据集、预处理、特征工程，以及在项目术语或标签变化时重新训练。
- 这篇论文研究只靠提示词的 LLM 分类，能否降低 Conventional Commit 标签的配置成本。

## 方法
- 作者从 InfluxDB GitHub 仓库挖掘了 3,200 条大致平衡的提交，并把 Conventional Commit 类型作为真实标签。
- 每个样本都根据它的代码 diff 进行分类；没有对模型做微调。
- 他们测试了零样本、少样本和思维链提示。
- 他们用准确率、精确率、召回率和 F1 评估 Mistral-7B-Instruct、LLaMA-3-8B 和 DeepSeek-R1-32B。

## 结果
- 单次最佳结果：Mistral-7B-Instruct 配合少样本提示，在 3,200 条 InfluxDB 提交上达到 0.6154 准确率、0.3823 精确率、0.6154 召回率和 0.4706 F1。
- DeepSeek-R1-32B 在不同提示词下的平均模型表现最好：0.563 准确率、0.587 精确率、0.563 召回率和 0.538 F1。
- 少样本提示在不同模型上的平均提示表现最好：0.531 准确率和 0.468 F1；零样本是 0.431 准确率和 0.399 F1。
- 思维链提示没有提高准确率：它的平均准确率是 0.468，低于少样本的 0.531。
- LLaMA-3-8B 的平均表现最弱，在各类提示下只有 0.372 准确率和 0.366 F1。
- 论文没有把结果和已训练的 ML 或微调后的 LLM 基线做比较，所以这些结果更适合用来指导提示词选择，而不是建立新的准确率基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02033v1](https://arxiv.org/abs/2605.02033v1)
