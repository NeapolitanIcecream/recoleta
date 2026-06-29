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
本文研究压缩长篇仓库上下文是否会帮助或损害仓库级代码任务。结果显示，压缩能降低成本，而且在学习到的潜变量方法上，某些代码基准的表现甚至超过完整上下文推理。

## 问题
- 仓库级代码补全和生成需要很长的多文件上下文，输入越长，延迟和内存成本就越高。
- 长提示词还会把有用证据淹没在无关的仓库文本里，也可能超出模型上下文窗口，迫使模型截断输入。
- 先前的上下文压缩研究主要集中在自然语言上。它在代码任务中的价值并不清楚，因为代码更依赖跨文件依赖和语法。

## 方法
- 论文做了一个统一的实证比较，评估 **8** 种压缩方法，分成 **3** 类：文本到文本（更短的 token 序列）、文本到向量（学习到的潜变量记忆 token）和文本到图像（把代码渲染成图像供 VLM 使用）。
- 研究在 **ComplexCodeEval** 上评估两个仓库级任务：代码补全和代码生成，使用 **100 个 Python + 100 个 Java** 留出样本。
- 模型来自 **Qwen2.5** 系列：基于文本的方法用 **Qwen2.5-Coder 3B/7B**，视觉压缩用 **Qwen2.5-VL 3B/7B**。
- 对于文本到向量，研究把上下文切成多个片段，再压缩成少量学习到的记忆 token；有的变体保持片段彼此独立，有的变体会把记忆传递到后续片段。
- 研究同时衡量任务质量和部署成本，把压缩推理与 **完整上下文** 和 **无上下文** 基线在多个压缩比下进行比较。

## 结果
- 主要结论：在 **4 倍压缩** 下，**文本到向量** 方法在 Python 补全上比完整上下文推理最高高出 **28.3% BLEU**。表中 **QC-7B T2V-SS** 在 Python 补全上达到 **41.34 BLEU**，完整上下文为 **32.21**，约高 **28.3%**。
- 在 **QC-7B** 上，文本到向量在多个设置里也超过了完整上下文的其他补全指标：Python 补全 **EM 42-44 对 33**，Java 补全 **BLEU 最高 35.12 对 32.60**，Java 补全 **ES 最高 60.29 对 55.90**。
- 在代码生成上，文本到向量在 Python 任务里经常优于完整上下文，模型包括 **QC-3B** 和 **QC-7B**。例如，**QC-7B T2V-QS** 在 Python 生成上的 **BLEU** 是 **13.58**，完整上下文为 **10.49**；**QC-3B T2V-QC** 是 **12.43**，完整上下文为 **10.27**。
- **文本到图像** 在中等压缩下的补全结果接近完整上下文，但在生成任务上会下降。比如，**QV-7B** 在 **4 倍** 压缩下的 Python 补全是 **24.11 BLEU**，完整上下文是 **24.91**；Python 生成则降到 **4.52**，完整上下文为 **9.19**。
- **文本到文本** 在轻度压缩下有用，但通常不如完整上下文，而且在生成任务上的退化更快。比如，**QC-7B T2T-LL2** 的 Python 补全是 **30.32 BLEU**，完整上下文是 **32.21**；Python 生成是 **7.54**，完整上下文是 **10.49**。
- 效率结果：三类方法都比完整上下文解码更省推理成本。论文报告，在高压缩比下，端到端延迟最高可降低 **50%**；文本到图像在最佳 **4 倍** 设置下延迟降低 **33%**；文本到文本在中等压缩比下总延迟降低 **35% 以上**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13725v1](http://arxiv.org/abs/2604.13725v1)
