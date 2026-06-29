---
source: arxiv
url: https://arxiv.org/abs/2605.05251v1
published_at: '2026-05-05T17:53:51'
authors:
- Eric Wolos
- Michael Doyle
topics:
- code-embeddings
- binary-reverse-engineering
- function-search
- contrastive-learning
- decompiled-code
- code-intelligence
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Identifier-Free Code Embedding Models for Scalable Search

## Summary
## 摘要
本文训练了 mitRE-embed-Qwen-0.6B，这是一个经过调优的 Qwen3-Embedding-0.6B 模型，用于把源代码函数与去符号的 Ghidra 反编译函数匹配起来。它面向符号名缺失时的可扩展二进制逆向搜索。

## 问题
- 逆向工程师经常面对去符号二进制，函数名、变量名和参数名都不见了，因此把反编译代码和已知源代码匹配起来很难。
- BSim 和 FLIRT 等现有工具有助于函数关联，但开放式文本嵌入模型还没有覆盖只用简单文本输入的、源代码到反编译代码以及反编译代码到源代码的双向搜索。
- 这很重要，因为更好的检索可以帮助分析人员在大型二进制中识别已知函数，而不需要自定义 AST 或图预处理。

## 方法
- 作者使用允许性许可的 Assemblage WinPE 切分数据构建配对数据：近 500,000 对源代码/反编译函数对，总计超过 100 万个函数，训练/测试划分为 95/5，并使用无头 Ghidra 进行反编译。
- 他们用对比式 InfoNCE 损失微调 Qwen3-Embedding-0.6B：反编译函数作为锚点，匹配的源函数作为正样本，批次中的其他源函数作为负样本。
- 训练使用 1 个 epoch、964 个 step、有效 batch size 512、temperature 0.05、AdamW、2e-5 学习率配合余弦调度、bf16，以及 4 张 NVIDIA H100 GPU。
- 评估使用余弦相似度检索，双向进行，候选池分别为 29,499 个函数的过滤池，以及 58,999 个函数的源代码加反编译代码合并池。
- 论文比较了 11 个嵌入模型，测试了一个 FP8 量化版本，并检查了对 Signsrch 常量关联任务的迁移效果。

## 结果
- 在反编译到源代码搜索、且两种表示都在候选池中的设置下，mitRE-embed-Qwen-0.6B 的 MRR 为 0.4104，Recall@1 为 0.3065，Recall@10 为 0.6427；BinSeek-Embedding 的 MRR 为 0.0802，Recall@1 为 0.0594，Recall@10 为 0.1221。
- 在源代码到反编译代码搜索、且两种表示都在候选池中的设置下，该模型的 MRR 为 0.4104，Recall@10 为 0.6337；非 MITRE 基线中 MRR 最高的是 SFR-Embedding-Mistral，数值为 0.1429。
- 在过滤候选池下，反编译到源代码的 MRR 为 0.6207，Recall@10 为 0.8353；源代码到反编译代码的 MRR 为 0.5962，Recall@10 为 0.8094。
- FP8 量化模型保持了接近的检索质量：反编译到源代码、合并候选池下的 MRR 为 0.4083，而全精度为 0.4104；源代码到反编译代码、过滤候选池下的 MRR 为 0.5950，而全精度为 0.5962。
- 在 Signsrch 的 Constant-to-Other-Constants 任务上，该模型的 MAP 为 0.062765，领先于 Qwen3-Embedding-0.6B 的 0.038412 和 BinSeek-Embedding 的 0.037864；在 Group-to-Constants 任务上，embeddinggemma-300m 以平均精度 0.022182 领先，mitRE-embed-Qwen-0.6B 的分数为 0.019732。
- FP8 量化在权重上使用 0.72 GB VRAM，而全精度为 1.12 GB；在 5 次试验中嵌入 10,000 对函数时，FP8 的推理时间占全精度的 88.6%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05251v1](https://arxiv.org/abs/2605.05251v1)
