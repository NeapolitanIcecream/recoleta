---
source: arxiv
url: http://arxiv.org/abs/2604.13725v1
published_at: '2026-04-15T11:00:17'
authors:
- Jia Feng
- Zhanyue Qin
- Cuiyun Gao
- Ruiqi Wang
- Chaozheng Wang
- Yingwei Ma
- Xiaoyuan Xie
topics:
- repository-level-code
- context-compression
- code-intelligence
- long-context-llms
- code-generation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation

## Summary
## 摘要
本文研究压缩长仓库上下文对仓库级代码任务是有帮助还是有损害。结果显示，压缩可以降低成本，而且在一些代码基准上，基于学习式潜向量的方法表现超过了全上下文推理。

## 问题
- 仓库级代码补全和生成需要较长的多文件上下文，随着输入长度增加，延迟和内存成本也会上升。
- 长提示还会让有用证据淹没在无关的仓库文本中，也可能超出模型的上下文窗口，导致截断。
- 以往的上下文压缩工作主要关注自然语言。它对代码任务是否有价值并不明确，因为代码更依赖跨文件依赖关系和语法。

## 方法
- 论文对 **8 种压缩方法** 做了统一的实证比较，覆盖 **3 种范式**：text-to-text（更短的 token 序列）、text-to-vector（学习得到的潜在记忆 token）和 text-to-image（将代码渲染为图像供 VLM 使用）。
- 它在 **ComplexCodeEval** 上评估了两个仓库级任务：代码补全和代码生成，使用 **100 个 Python + 100 个 Java** 留出样本。
- 模型来自 **Qwen2.5** 系列：文本方法使用 **Qwen2.5-Coder 3B/7B**，视觉压缩使用 **Qwen2.5-VL 3B/7B**。
- 对于 text-to-vector，上下文会被切分为多个片段，并压缩成一小组学习得到的记忆 token；其中一些变体保持片段彼此独立，另一些则在片段之间传递记忆。
- 研究同时衡量任务质量和部署成本，在多个压缩比下，将压缩推理与 **full-context** 和 **no-context** 基线进行比较。

## 结果
- 核心结论：在 **4x compression** 下，**text-to-vector** 方法在 Python 补全上最多可比 full-context inference 高出 **28.3% BLEU**。表中 **QC-7B T2V-SS** 在 Python completion 上达到 **41.34 BLEU**，而 full context 为 **32.21**，增幅约 **28.3%**。
- 在 **QC-7B** 上，text-to-vector 在若干设置中也提升了其他补全指标：Python completion 的 **EM 42-44 vs 33**，Java completion 的 **BLEU 最高 35.12 vs 32.60**，以及 Java completion 的 **ES 最高 60.29 vs 55.90**。
- 在代码生成任务上，text-to-vector 在 Python 上经常超过 full context，覆盖 **QC-3B** 和 **QC-7B**。例如：**QC-7B T2V-QS** 在 Python generation 上得到 **13.58 BLEU**，而 full context 为 **10.49**；**QC-3B T2V-QC** 得到 **12.43 BLEU**，而 full context 为 **10.27**。
- **Text-to-image** 在中等压缩率下的补全任务上接近 full context，但在生成任务上下降更明显。例如：**QV-7B** 在 **4x** 下的 Python completion 为 **24.11 BLEU**，而 full context 为 **24.91**；Python generation 降到 **4.52**，而 full context 为 **9.19**。
- **Text-to-text** 在轻度压缩时有一定作用，但通常仍低于 full context，并且在生成任务上退化更快。例如：**QC-7B T2T-LL2** 的 Python completion 为 **30.32 BLEU**，而 full context 为 **32.21**；Python generation 为 **7.54**，而 full context 为 **10.49**。
- 效率方面：三种范式都比 full-context decoding 的推理成本更低。论文报告，在较高压缩比下，端到端延迟最高可降低 **50%**；text-to-image 在其最佳 **4x** 设置下延迟降低 **33%**；text-to-text 在中等压缩比下总延迟降低 **超过 35%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13725v1](http://arxiv.org/abs/2604.13725v1)
