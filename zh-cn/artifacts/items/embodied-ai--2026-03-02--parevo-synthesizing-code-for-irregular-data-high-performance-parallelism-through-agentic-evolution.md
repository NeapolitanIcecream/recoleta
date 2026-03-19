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
- program-synthesis
- evolutionary-search
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# ParEVO: Synthesizing Code for Irregular Data: High-Performance Parallelism through Agentic Evolution

## Summary
ParEVO针对不规则数据上的并行代码生成，试图让大模型不仅能写出能跑的并行程序，还能写出真正高性能且无数据竞争的实现。它把领域微调与基于编译、竞态检测和性能剖析的进化式搜索结合起来，面向HPC中的图、稀疏结构等难题。

## Problem
- 论文解决的是：如何为**不规则数据结构**（如图、稀疏矩阵、非均匀网格）自动合成**正确且高性能**的并行代码。
- 这很重要，因为现代性能提升越来越依赖并行计算，但这类任务的负载不均衡、依赖关系动态变化，人工编写并发代码门槛高，LLM也常因**竞态、死锁、错误同步**而失败。
- 现有LLM存在明显“顺序偏置”，往往只会给串行代码外层套并行循环，导致错误或性能反而下降。

## Approach
- 先构建一个经过执行验证的训练集 **Parlay-Instruct**：基于593个人工种子样例和DMOJ题目，通过“Teacher-Student-Critic”/“Critic-Refine”流程生成并筛选，最终得到**13,820**个可编译、可通过测试的并行任务样本。
- 核心思想是让模型学习**高层并行原语**而不是低层线程细节：把自然语言需求映射到ParlayLib中的 `filter`、`scan`、`reduce`、`sort` 等原语，从而更容易得到“结构上正确”的并行算法。
- 在模型层面，作者微调了专用模型，包括 **DeepSeek-6.7B**、**Qwen3-30B**（C++/Rust）和 **Gemini-2.5-Pro** 适配版本，使其更理解ParlayLib语义、并行模式和Rust安全并发习惯。
- 在推理时使用 **Evolutionary Coding Agent (ECA)**：生成一批候选代码，交给**编译器、单测、动态竞态检测器、性能分析器**评估，再根据这些外部工具反馈做“变异/交叉/修复”，逐代优化代码。
- 搜索中结合**性能最优选择**与 **MAP-Elites** 多样性维护；若候选程序编译失败、测试失败或触发数据竞争/死锁，则适应度直接置为0。

## Results
- 在 **ParEval** 基准上，ParEVO报告**平均 106× speedup**，最大达到**1103×**，说明其生成的并行实现相对基线可获得极大加速。
- 在**高度复杂的不规则图问题**上，报告**13.6× 平均加速**，并声称优于商业模型如 **GPT-5-Thinking** 和 **Gemini-3-Pro**。
- 相比专家人工基线，进化式方法在某些高度不规则kernel上可达到**最高 4.1× speedup**；文中举例为 **Maximal Independent Set**。
- 作者还报告了一个“正确性-速度”权衡：微调后 **Pass@1 从 0.42 提升到 0.76**，但峰值速度从**21.7×**下降到**13.6×**，原因是模型更倾向使用安全的高层原语而非激进但风险更高的原子操作。
- 数据集方面，训练语料包含**13,820**个验证后的instruction-tuning样本，其中**13,120**用于训练、**700**用于保留测试；性能对比样本要求优化版至少达到**1.2×**速度提升后才纳入。

## Link
- [http://arxiv.org/abs/2603.02510v1](http://arxiv.org/abs/2603.02510v1)
