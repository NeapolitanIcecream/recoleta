---
source: arxiv
url: http://arxiv.org/abs/2603.02510v1
published_at: '2026-03-02T20:41:07'
authors:
- Liu Yang
- Zeyu Nie
- Andrew Liu
- Felix Zou
- "Deniz Altinb\xFCken"
- Amir Yazdanbakhsh
- Quanquan C. Liu
topics:
- code-generation
- parallel-computing
- irregular-data
- agentic-search
- llm-finetuning
- hpc
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ParEVO: Synthesizing Code for Irregular Data: High-Performance Parallelism through Agentic Evolution

## Summary
ParEVO旨在让大模型自动生成针对不规则数据结构的高性能并行代码，解决并发正确性和性能同时很难保证的问题。它把领域微调与进化式代理搜索结合起来，在编译器、竞态检测器和性能分析器反馈下迭代修复和加速代码。

## Problem
- 不规则并行任务（如稀疏图、非平衡树、非均匀网格）难以静态调度，容易出现竞态、死锁和负载不均，导致并行代码既难写又难优化。
- 通用LLM存在明显“顺序偏置”，在这类任务上常生成错误的OpenMP/并发代码，甚至比串行更慢。
- 这很重要，因为现代性能提升越来越依赖并行计算，而不规则并行正是HPC和真实软件系统中的核心难点。

## Approach
- 构建 **Parlay-Instruct** 数据集：通过 Teacher-Student-Critic / Critic-Refine 式流程合成并严格执行验证，得到 **13,820** 个已编译、已通过测试的并行编程样本，重点覆盖 ParlayLib 原语和性能优化轨迹。
- 对 **DeepSeek、Qwen、Gemini** 等模型做领域微调，使其学会把自然语言需求映射到 ParlayLib / Rust RPB 这类高层并行原语，而不是直接写脆弱的低层线程同步代码。
- 提出 **Evolutionary Coding Agent (ECA)**：一次生成多个候选程序，编译运行后用编译错误、单测结果、动态竞态检测、运行时间/profile 作为“适应度”，再继续变异和选择。
- 搜索阶段结合 **MAP-Elites** 保持候选多样性，并以代码长度、圈复杂度、同步原语使用频率等特征避免搜索塌缩。
- 核心机制可简单理解为：先把模型教会“正确的并行积木”，再让代理在真实机器反馈上不断试错，直到代码既正确又快。

## Results
- 在 **ParEval** 基准上，ParEVO报告 **平均 106× speedup**，**最大 1103× speedup**，覆盖整个综合任务套件。
- 在高复杂度不规则图问题上，达到 **13.6× speedup**，并声称优于 **GPT-5-Thinking** 和 **Gemini-3-Pro** 等商用模型。
- 相比专家手写基线，在某些高度不规则内核（如 **Maximal Independent Set**）上可达到 **最高 4.1× speedup**。
- 论文还报告并发编程中的“alignment tax”：微调后 **Pass@1 从 0.42 提升到 0.76**，但峰值性能 **Speedup 从 21.7× 降到 13.6×**，说明更安全的高层原语会牺牲部分极限速度。
- 数据集规模方面，最终保留 **13,820** 个验证样本，并划分为 **13,120** 个训练样本和 **700** 个测试样本。
- 文本摘录未给出更完整的逐模型分项表格，但最强的定量主张是：ParEVO在正确性与不规则并行性能上同时显著超过通用LLM，并在部分任务上达到或超过专家实现。

## Link
- [http://arxiv.org/abs/2603.02510v1](http://arxiv.org/abs/2603.02510v1)
