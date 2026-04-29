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
Optimas 是一个自动化 GPU 代码优化系统。它把运行时性能证据输入 LLM，然后对生成的代码进行编译和验证。论文的核心结论是，由诊断信息引导的生成方法可以把性能分析器的输出转成正确的代码修改，并在大量实验中提升性能。

## 问题
- GPU 性能调优仍然主要依赖人工，因为性能分析器只能显示瓶颈，不能直接产出代码修改；而在作者的初步测试中，只给 LLM 源代码时，它一次也没有找到能带来性能提升的优化。
- 原始性能分析数据过大且噪声过多，不能直接输入 LLM；单个 kernel 就可能产生数百 MB 的跟踪数据，而当前模型有上下文长度限制。
- 正确性和加速效果都需要基于执行的验证，因为代码即使能够编译，也可能没有命中真正的瓶颈，或者破坏输出语义。

## 方法
- Optimas 构建了一条多智能体流水线，包含性能分析、诊断分析、提示构造和评估智能体。系统将约 90% 的流程自动化，并在编译失败时最多重试三次。
- 它会选出覆盖至少 80% 运行时间的最小热点 kernel 集合，然后把诊断信息压缩成来自三个来源的紧凑摘要：Roofline 分析、PC stall 采样和硬件计数器交互分析。
- 对于 PC 采样，它只保留每个源代码行上的主导 stall 信号。论文给出一个具体压缩例子：一个 41 行的 kernel，其原始 PC 跟踪在聚合后从 990 MB 缩小到 10 MB，最终摘要不到 6 KB。
- 对于硬件计数器，它使用基于 ensemble orthogonal matching pursuit 的稀疏特征选择方法，挑选出大约 5 个最能解释运行时间变化的计数器，再把这些计数器映射为自然语言描述。
- 提示词包含代码、诊断摘要，以及限制条件：修改只能发生在相关区域，并且每一处修改都必须说明其针对的证据。之后，框架会编译、运行、检查 bit-for-bit 正确性并测量性能。论文还引入了 EAR 指标，用来评估证据覆盖度、修改定位是否准确，以及实测变化是否与诊断一致。

## 结果
- 摘要称，论文报告了 3,410 次真实实验，覆盖 10 个基准测试和 2 个 HPC mini-application。
- 作者声称，代码生成的正确率达到 100%，并且在超过 98.82% 的实验中实现了性能提升。
- 论文报告的 NVIDIA GPU 平均加速范围为 8.02%–79.09%。
- 论文称，没有诊断信息、只看代码的基线方法得到的有效优化率为 0%。
- 在可见的 GPT-5 结果表中，部分基准的提升幅度很大：Accuracy 在 PC+Roofline 设置下达到 79.09%，Sobol 在 PC 设置下达到 41.60%，Dot 在多个设置下达到 36.73%，而 Copy/Mul/Add/Triad 大多处于 30% 出头到接近 40% 的区间。
- 提供的结果表节选不完整，因此无法从现有文本中获得每个基准的完整汇总、全部模型对比和完整的 EAR 指标数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23892v1](http://arxiv.org/abs/2604.23892v1)
