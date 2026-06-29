---
source: arxiv
url: https://arxiv.org/abs/2606.06492v1
published_at: '2026-06-04T17:59:46'
authors:
- Liliana Hotsko
- Yinxi Li
- Yuntian Deng
- Pengyu Nie
topics:
- code-intelligence
- repository-level-adaptation
- lora-adapters
- hypernetworks
- software-evolution
- code-language-models
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution

## Summary
## 摘要
Code2LoRA 为冻结的代码语言模型生成按仓库定制的 LoRA 适配器，因此仓库知识在推理时进入适配器权重，而不需要额外输入 token。它同时处理固定的仓库快照和逐次提交的代码变更。

## 问题
- 代码语言模型需要仓库级上下文，才能解析导入、API、辅助函数和项目约定。
- RAG 和依赖上下文方法在每次查询时都会增加 token 和检索成本。按仓库微调和 LoRA 训练在大量仓库上成本很高，而且随着提交改动代码，这些方法很快过时。
- 这会影响编程助手，因为真实项目通常文件多、规模大，而且持续变化。

## 方法
- 一个冻结的 Qwen3-Embedding-0.6B 编码器把仓库文件按 4096 token 分块，块之间重叠 512 token，再对块做均值池化得到 1024 维文件向量，然后用加权均值加最大池化聚合所有文件。
- 训练好的超网络把仓库嵌入映射为 Qwen2.5-Coder-1.5B 的 rank-16 LoRA 矩阵。基础语言模型和仓库编码器保持冻结。
- Code2LoRA-Static 把一个仓库快照映射为一个适配器。
- Code2LoRA-Evo 先用仓库快照初始化 GRU 状态，再用提交 diff 的嵌入更新它，并在每次代码变更后生成新的适配器。
- 生成的适配器覆盖七种投影类型：q、k、v、o、gate、up 和 down。

## 结果
- 论文构建了 RepoPeftBench，包含 604 个 Python 仓库：512 个分布内仓库和 92 个时间分布外仓库。
- 静态轨道：Code2LoRA-Static 在跨仓库测试上的 exact match 达到 63.8%，比 FFT + RAG 的 53.9% 高 9.9 个百分点。RAG 得分为 39.7%，依赖解析上下文为 48.2%，Single LoRA 为 47.4%。
- 静态轨道的仓库内测试：Code2LoRA-Static 的 exact match 达到 66.2%，高于论文报告的按仓库 LoRA 上限基线 64.0%。
- 演化轨道跨仓库：Code2LoRA-Evo 的 exact match 达到 60.3%，Single LoRA 为 55.1%，Code2LoRA-Static 为 55.7%。
- 演化轨道仓库内：Code2LoRA-Evo 的 exact match 达到 64.5%，Single LoRA 为 61.3%，Code2LoRA-Static 为 60.6%，按仓库 LoRA 为 64.2%。
- 演化轨道还报告了 Code2LoRA-Evo 在跨仓库测试上的 0.810 EditSim 和 0.763 CodeBLEU，以及在仓库内测试上的 0.828 EditSim 和 0.790 CodeBLEU。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06492v1](https://arxiv.org/abs/2606.06492v1)
