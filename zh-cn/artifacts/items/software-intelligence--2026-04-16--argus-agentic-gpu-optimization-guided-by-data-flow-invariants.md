---
source: arxiv
url: http://arxiv.org/abs/2604.18616v1
published_at: '2026-04-16T15:49:31'
authors:
- Haohui Mai
- Xiaoyan Guo
- Xiangyun Ding
- Daifeng Li
- Qiuchu Yu
- Chenzhun Guo
- Cong Wang
- Jiacheng Zhao
- Christos Kozyrakis
- Binhang Yuan
topics:
- gpu-kernel-optimization
- agentic-code-generation
- data-flow-invariants
- llm-coding-agents
- static-analysis
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ARGUS: Agentic GPU Optimization Guided by Data-Flow Invariants

## Summary
## 摘要
Argus 是一个用于生成高性能 GPU kernel 的 agentic 系统。它不给编码 agent 只看通过或失败测试，而是提供编译时的数据流不变式。根据文中结果，在 AMD MI300X 上，它生成的 GEMM、flash attention 和 MoE kernel 达到手工优化汇编吞吐量的水平，并且大幅超过之前的 agentic 系统。

## 问题
- 现有的 LLM 编码 agent 可以写出功能正确的 GPU kernel，但在 GEMM、attention 和 MoE 这类工作负载上，性能往往远低于手工优化库。
- 峰值 GPU 性能依赖很多相互耦合的选择：分块、shared memory 分阶段、软件流水、指令调度、寄存器使用和数据布局变换。单元测试看不出 kernel 违反了哪条全局约束。
- 这很重要，因为这些 kernel 占据了 LLM 推理的大部分时间，即使只提高一点效率，在部署规模上也能减少大量 GPU 成本。

## 方法
- Argus 在 GPU kernel 生成中加入了 **数据流不变式**。这是编译期规则，用来规定数据元素在 kernel 分块、重排、分阶段和计算时应如何保持对齐。
- 它使用一个基于 tile 的 Python DSL，包含 **tag functions** 和 **tag assertions**。tag functions 会给张量元素附加符号标签，比如逻辑坐标。tag assertions 会检查正确的元素是否在使用点汇合，比如在 matrix-core 指令中。
- 编译器通过对布局代数做抽象解释，再结合 SMT 求解，在编译时验证这些不变式。如果检查失败，它会返回一个具体反例，指出线程、数据元素和程序点。文中称这带来 **zero runtime overhead**，因为标签只存在于编译阶段。
- 一个 agentic 优化流程使用 LLM planner 和 in-context reinforcement learning 来选择优化、编写不变式、编译、测试、分析性能，并根据不变式违反和运行时性能修改 kernel。

## 结果
- 在 **AMD MI300X** 上，Argus 报告的 **GEMM、flash attention 和 MoE** kernel 吞吐量达到最先进 **手工优化汇编** 的有效吞吐量的 **99–104%**。
- 与现有 **agentic baseline** 相比，它在评估的工作负载家族上报告了 **2–1543×** 更高的几何平均吞吐量。
- 对于 **flash attention**，它比被称为最强 baseline 的 **KernelFalcon** 快 **2.4×**。
- 被评估的 kernel 家族占目标平台上 LLM 推理 GPU 执行时间的 **90% 以上**，所以这些提升指向主要的服务瓶颈。
- 在 **KernelBench** 上，Argus 报告 **Level 1** 任务正确率为 **100%**，**Level 2** 任务正确率为 **90%**。
- 这段摘录没有给出更细的按数据集拆分结果、消融实验，或每个工作负载家族的精确 baseline 数值，除了上面的总体现比之外。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18616v1](http://arxiv.org/abs/2604.18616v1)
