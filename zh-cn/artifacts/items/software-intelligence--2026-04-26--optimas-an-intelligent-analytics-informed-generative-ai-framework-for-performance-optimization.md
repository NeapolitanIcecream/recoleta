---
source: arxiv
url: http://arxiv.org/abs/2604.23892v1
published_at: '2026-04-26T21:34:51'
authors:
- Mohammad Zaeed
- Tanzima Z. Islam
- Vladimir Indic
topics:
- llm-code-optimization
- gpu-performance
- multi-agent-systems
- hpc
- performance-profiling
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization

## Summary
## 摘要
Optimas 是一个自动化的 GPU 代码优化系统，它把运行时性能证据输入 LLM，再编译并验证生成的代码。论文的核心主张是，带诊断信息的生成可以把性能分析器输出转成正确的代码修改，并在多组实验中提升性能。

## 问题
- GPU 性能调优仍然依赖人工，因为性能分析器能显示瓶颈，却不会生成代码修改；而只给源代码的 LLM 在作者的初步测试中没能找到任何能带来改进的优化。
- 原始性能分析数据太大、噪声太多，不能直接作为 LLM 输入；单个 kernel 可能产生数百 MB 的 trace，而现有模型有上下文长度限制。
- 正确性和加速都需要基于执行的验证，因为能编译的代码仍然可能没有命中真正的瓶颈，或者破坏输出语义。

## 方法
- Optimas 构建了一个多智能体流程，包含分析、提示构建和评估代理。系统自动化了大约 90% 的工作流，并且会把编译失败重试最多三次。
- 它先选出覆盖至少 80% 运行时间的最小热点 kernel 集合，再把诊断信息压缩成来自三个来源的简洁摘要：Roofline 分析、PC stall 采样和硬件计数器交互分析。
- 对于 PC 采样，它只保留每个源代码行占主导的 stall 信号。论文给出一个具体压缩例子：一个 41 行 kernel 的原始 PC trace 在聚合后从 990 MB 缩到 10 MB，再压缩成小于 6 KB 的摘要。
- 对于硬件计数器，它使用一种基于 ensemble orthogonal matching pursuit 的稀疏特征选择方法，挑出大约 5 个最能解释运行时间变化的计数器，然后把这些计数器映射成自然语言描述。
- 提示词包含代码、诊断摘要和约束条件，这些约束把修改限制在相关区域内，并要求每一处修改都引用它所针对的证据。随后，框架会编译、运行、检查逐位正确性，并测量性能。论文还引入 EAR 指标，用来评估证据覆盖、修改定位，以及测得的变化是否与诊断一致。

## 结果
- 摘要报告了在 10 个基准和 2 个 HPC mini-application 上进行的 3,410 次真实实验。
- 作者声称生成代码的正确率为 100%，并且在这些实验中超过 98.82% 实现了性能提升。
- NVIDIA GPU 上报告的平均加速幅度在 8.02% 到 79.09% 之间。
- 论文指出，不带诊断信息的纯代码基线产生了 0% 的有效优化。
- 在 GPT-5 的可见结果表中，若干基准的提升幅度很大：Accuracy 在 PC+Roofline 下达到 79.09%，Sobol 在 PC 下达到 41.60%，Dot 在多种设置下达到 36.73%，Copy/Mul/Add/Triad 大多处于 30% 左右到 30% 以上。
- 摘录中的结果表被截断，因此提供的文本里没有完整的逐基准总计、全部模型对比和完整 EAR 指标值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23892v1](http://arxiv.org/abs/2604.23892v1)
