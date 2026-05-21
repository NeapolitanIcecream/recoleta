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
论文训练了 mitRE-embed-Qwen-0.6B，这是一个经过调优的 Qwen3-Embedding-0.6B 模型，用于匹配源代码函数和经过剥离的 Ghidra 反编译函数。它面向符号名缺失时的可扩展二进制逆向工程搜索。

## 问题
- 逆向工程师经常面对被剥离的二进制文件，其中函数名、变量名和参数名已经丢失，因此很难把反编译代码匹配到已知源代码。
- BSim 和 FLIRT 等现有工具可以帮助做函数关联，但开放文本嵌入模型尚未覆盖用简单文本输入进行源代码到反编译代码、反编译代码到源代码的双向搜索。
- 更好的检索能帮助分析人员在大型二进制文件中识别已知函数，无需自定义 AST 或图预处理。

## 方法
- 作者使用宽松许可的 Assemblage WinPE 划分构建成对数据：近 500,000 对源代码/反编译函数，总计超过 100 万个函数，训练/测试按 95/5 划分，并使用无头 Ghidra 反编译。
- 他们用对比式 InfoNCE 损失微调 Qwen3-Embedding-0.6B：反编译函数作为锚点，匹配的源代码函数作为正样本，同一批次中的其他源代码函数作为负样本。
- 训练使用 1 个 epoch、964 步、有效批量大小 512、温度 0.05、AdamW、学习率 2e-5 及余弦调度、bf16，以及 4 块 NVIDIA H100 GPU。
- 评估在两个方向上使用余弦相似度检索，候选池包括过滤后的 29,499 个函数，以及源代码加反编译代码合并后的 58,999 个函数。
- 论文比较了 11 个嵌入模型，测试了一个 FP8 量化变体，并在 Signsrch 常量关联任务上检查迁移效果。

## 结果
- 在候选池同时包含两种表示的 Decompiled-to-Source 搜索中，mitRE-embed-Qwen-0.6B 达到 MRR 0.4104、Recall@1 0.3065、Recall@10 0.6427；BinSeek-Embedding 的 MRR 为 0.0802、Recall@1 为 0.0594、Recall@10 为 0.1221。
- 在候选池同时包含两种表示的 Source-to-Decompiled 搜索中，该模型达到 MRR 0.4104 和 Recall@10 0.6337；按 MRR 计，最强的非 MITRE 基线是 SFR-Embedding-Mistral，得分 0.1429。
- 使用过滤后的候选池时，它在 Decompiled-to-Source 上达到 MRR 0.6207 和 Recall@10 0.8353，在 Source-to-Decompiled 上达到 MRR 0.5962 和 Recall@10 0.8094。
- FP8 量化模型保持了接近的检索质量：Decompiled-to-Source 合并候选池 MRR 为 0.4083，而全精度为 0.4104；Source-to-Decompiled 过滤候选池 MRR 为 0.5950，而全精度为 0.5962。
- 在 Signsrch Constant-to-Other-Constants 上，该模型的 MAP 为 0.062765，高于 Qwen3-Embedding-0.6B 的 0.038412 和 BinSeek-Embedding 的 0.037864；在 Group-to-Constants 上，embeddinggemma-300m 以平均精度 0.022182 领先，mitRE-embed-Qwen-0.6B 得分 0.019732。
- FP8 量化的权重占用 0.72 GB VRAM，全精度为 1.12 GB；在五次试验中嵌入 10,000 对函数时，其耗时为全精度推理时间的 88.6%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05251v1](https://arxiv.org/abs/2605.05251v1)
