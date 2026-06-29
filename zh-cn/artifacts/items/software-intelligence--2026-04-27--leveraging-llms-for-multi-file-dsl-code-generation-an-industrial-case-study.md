---
source: arxiv
url: https://arxiv.org/abs/2604.24678v1
published_at: '2026-04-27T16:38:01'
authors:
- Sivajeet Chand
- Kevin Nguyen
- Peter Kuntz
- Alexander Pretschner
topics:
- code-generation
- domain-specific-languages
- multi-file-editing
- qlora-fine-tuning
- software-engineering
- industrial-case-study
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Leveraging LLMs for Multi-File DSL Code Generation: An Industrial Case Study

## Summary
## 摘要
宝马测试了 7B 代码 LLM 能否把一条自然语言请求变成一个完整的多文件 Xtext DSL 项目更新。论文的主要结论是，QLoRA 微调让仓库级 DSL 生成达到足以支持开发者审查和生成器检查的程度。

## 问题
- 企业 DSL 变更常常会涉及多个文件、文件夹、导入和依赖声明，所以单文件代码生成和真实工作流程并不匹配。
- 在这个宝马场景中，DSL 是 Java 和 TypeScript 生成的上游输入；很小的 DSL 错误就可能破坏下游生成器，或产生错误的市场配置。
- 开发者现在仍然手工编写这些 DSL 工件，这需要领域知识，也会让创建或修改特定市场配置时变慢。

## 方法
- 该方法把整个 DSL 文件夹树序列化为保留路径的 JSON：文件夹和文件变成键，文件内容变成字符串。
- 每个任务都使用一条指令、当前项目快照和目标项目快照，因此模型学习的是一次输出完整的更新后仓库状态。
- 数据集包含 774 个训练样本和 105 个留出评估样本，任务包括市场、属性和金融产品的创建、添加和删除操作。
- 研究比较了 Qwen2.5-Coder-7B-Instruct 和 DeepSeek-Coder-6.7B/7B-Instruct 在零样本提示、单样本提示和 QLoRA 微调下的表现。
- 评估结合了完全匹配、BLEU、有效 JSON、仅变更部分相似度指标、针对文件夹/文件键的结构保真度、开发者评审，以及通过现有 DSL 到代码生成器的执行检查。

## 结果
- 论文报告，微调在所测试的模型和指标上都是最强设置，多文件输出在 105 个留出样本上的结构保真度达到 1.00。
- 在任务适配前，原始模型通常已经能保持 JSON 外壳有效：Qwen-Raw 的有效 JSON 率为 0.895，DeepSeek-Raw 为 0.848。
- 单样本提示优于零样本提示，但论文指出，它的提升小于 QLoRA 微调。
- 人工评审使用了 4 名熟悉 DSL 的开发者、20 个生成输出、5 种操作类型，每种类型 4 个样本。
- 评审者在 8 个质量维度中的 2 个维度上完全一致，占 25%；在 8 个维度中的 7 个维度上误差在 ±1 分以内，占 87.5%。
- 提供的摘录没有包含完整结果表，所以这里看不到微调后的准确率、BLEU 和变更相似度的具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24678v1](https://arxiv.org/abs/2604.24678v1)
