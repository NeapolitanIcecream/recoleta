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
Argus 是一个用于生成高性能 GPU kernel 的智能体系统。它给编码智能体提供编译期数据流不变量，而不是只依赖通过/失败测试。在 AMD MI300X 上，它报告的 GEMM、flash attention 和 MoE kernel 达到了与手工优化汇编相当的吞吐量，并且相比此前的智能体系统有大幅领先。

## 问题
- 现有的 LLM 编码智能体可以写出功能正确的 GPU kernel，但在 GEMM、attention 和 MoE 等工作负载上，性能往往远低于手工优化库。
- GPU 的峰值性能依赖许多相互耦合的选择同时成立：分块、共享内存暂存、软件流水、指令调度、寄存器使用以及数据布局变换。单元测试无法指出 kernel 违反了哪个全局约束。
- 这很重要，因为这些 kernel 占了 LLM 推理时间的大部分，即使效率只有小幅提升，在大规模部署时也能明显降低 GPU 成本。

## 方法
- Argus 在 GPU kernel 生成中加入了**数据流不变量**。这些是编译期规则，用来规定数据元素在 kernel 进行分块、重排、暂存和计算时应如何保持对齐关系。
- 它使用一种基于 tile 的 Python DSL，并引入了 **tag functions** 和 **tag assertions**。tag functions 给张量元素附加符号标签，比如逻辑坐标。tag assertions 检查在使用点是否汇聚了正确的元素，例如在矩阵核心指令中。
- 编译器在编译期用基于布局代数的抽象解释和 SMT 求解来验证这些不变量。如果检查失败，它会返回一个具体反例，其中包含线程、数据元素和程序位置。论文称这带来**零运行时开销**，因为这些 tag 只存在于编译阶段。
- 该优化框架使用一个带智能体的流程：由 LLM planner 和 in-context reinforcement learning 共同选择优化策略、编写不变量、编译、测试、分析性能，并根据不变量违规信息和运行时性能反馈修改 kernel。

## 结果
- 在 **AMD MI300X** 上，Argus 报告其 **GEMM、flash attention 和 MoE** kernel 达到了最先进**手工优化汇编**有效吞吐量的 **99–104%**。
- 与现有**智能体基线**相比，它在所评测工作负载族上的几何平均吞吐量高出 **2–1543×**。
- 对于 **flash attention**，它报告相对 **KernelFalcon** 有 **2.4×** 加速，并将其称为最强基线。
- 在目标平台上，被评测的 kernel 类别占 LLM 推理中 GPU 执行时间的 **90% 以上**，因此这些性能提升对应的是主要服务瓶颈。
- 在 **KernelBench** 上，Argus 报告 **Level 1** 任务的正确率为 **100%**，**Level 2** 任务的正确率为 **90%**。
- 给定摘录没有提供更细的分数据集拆分、消融实验，或除上述头部对比外每个工作负载族的精确基线数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18616v1](http://arxiv.org/abs/2604.18616v1)
