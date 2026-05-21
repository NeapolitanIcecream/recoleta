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
BMW 测试了 7B 代码 LLM 能否把一条自然语言请求转换成一次完整的多文件 Xtext DSL 项目更新。论文的主要主张是，QLoRA 微调让仓库规模的 DSL 生成达到可供开发者审查和生成器检查的可用水平。

## 问题
- 企业 DSL 变更常常涉及多个文件、文件夹、导入和相互依赖的声明，因此单文件代码生成不符合真实工作流。
- 在 BMW 的这个场景中，DSL 是生成 Java 和 TypeScript 的源头；小的 DSL 错误可能破坏下游生成器，或生成错误的市场配置。
- 开发者仍然手写这些 DSL 工件，这需要领域知识，并会拖慢市场专属配置的创建或修改。

## 方法
- 该方法把整个 DSL 文件夹树序列化为保留路径的 JSON：文件夹和文件变成键，文件内容变成字符串。
- 每个任务使用一条指令、一个当前项目快照和一个目标项目快照，让模型学习在一次响应中输出完整的更新后仓库状态。
- 数据集包含 774 个训练样本和 105 个留出评估样本，操作包括为市场、属性和金融产品执行 create、add 和 delete。
- 研究比较了 Qwen2.5-Coder-7B-Instruct 和 DeepSeek-Coder-6.7B/7B-Instruct 在 zero-shot prompting、one-shot prompting 和 QLoRA fine-tuning 下的表现。
- 评估结合了 exact match、BLEU、valid JSON、仅变更相似度指标、基于文件夹/文件键的结构保真度、开发者审查，以及通过现有 DSL-to-code 生成器执行检查。

## 结果
- 论文报告称，在测试的模型和指标中，微调是最强设置；在 105 个样本的留出集上，多文件输出的结构保真度为 1.00。
- 在任务适配前，原始模型通常已经能保持 JSON 包装有效：Qwen-Raw 达到 0.895 valid JSON，DeepSeek-Raw 达到 0.848 valid JSON。
- one-shot prompting 优于 zero-shot prompting，但论文说明其提升小于 QLoRA 微调。
- 人工审查使用了 4 名熟悉 DSL 的开发者、20 个生成输出和 5 种操作类型，每种类型 4 个样本。
- 评审者在 8 个评分质量维度中的 2 个维度上完全一致，即 25%；在 8 个维度中的 7 个维度上评分差距在 ±1 分以内，即 87.5%。
- 提供的摘录不包含完整结果表，因此这里没有微调后的 exact-match、BLEU 和 change-similarity 精确分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24678v1](https://arxiv.org/abs/2604.24678v1)
