---
source: arxiv
url: http://arxiv.org/abs/2604.04238v1
published_at: '2026-04-05T19:44:02'
authors:
- Benjamin Mikek
- Danylo Vashchilenko
- Bryan Lu
- Panpan Xu
topics:
- code-optimization
- compiler-llm
- multi-agent-systems
- llvm
- program-synthesis
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Code Optimization via Compiler-LLM Cooperation

## Summary
## 摘要
这篇论文提出了 ACCLAIM，这是一个多智能体系统，把标准编译器 pass 与 LLM 在源代码、IR 和汇编层面的改写结合起来。目标是在不放弃编译器可靠性的前提下，获得 LLM 发现的优化；论文报告的评测结果显示，相比 **clang -O3**，平均加速最高可达 **1.25×**。

## 问题
- 编译器很可靠，但可能会漏掉一些需要从更高层理解程序意图才能发现的优化机会。
- LLM 能找到幅度更大的改写，但经常会生成错误代码；论文引用的错误代码比例在 **10% 到 90%** 之间，其中一项先前结果显示，表现最好的未增强模型错误改写率为 **42%**。
- 这一点很重要，因为在大规模场景下，即使运行时间只有小幅改善也有价值，而当前的 LLM 优化方法通常只在单一抽象层级上工作，不能覆盖完整的编译流程。

## 方法
- 论文将优化定义为跨多个抽象层级的 **rewrites** 和 **lowerings** 搜索，例如 **C source**、**LLVM IR** 和 **x86 assembly**。
- 论文构建了 **ACCLAIM**，这是一个多智能体系统，包含一个 **guiding agent**、针对各抽象层级的 **level-specific optimization agents**，以及一个 **testing agent**。
- guiding agent 决定何时调用常规编译器组件、何时调用 LLM 优化器，然后利用测试反馈来保留、重试或回退候选程序。
- testing agent 以通过测试的比例来检查 **correctness**，并以相对原始程序的运行时间改进来衡量 **performance**。
- 核心思路很直接：在语义推理有帮助的地方让 LLM 改写代码，然后让编译器在这些改写之前或之后执行其正常的已验证 pass。

## 结果
- 文中报告的主要结果是：在一组标准 **C programs** 上，相比 clang -O3，平均加速达到 **1.25×**。
- 摘要称，在各方法计算预算相同的条件下，compiler-LLM cooperation **优于现有编译器优化和按层级划分的 LLM 基线方法**。
- 论文还说，该方法优于在相同计算预算下的 **naive multi-level baselines**。
- 在动机示例中，LLM 在源代码层面把一个 population-count 计算从 **O(k log k)** 改为 **O(log k)**；或者在 IR 层面通过引入 **@llvm.ctpop.i32**，把它改为 **O(k)**。
- 在该 IR 改写之后，LLVM 向量化会把每次循环迭代中的 **8 repetitions** population-count 调用排布为 **2 instructions with 4 operations each**；论文称，在支持常数时间 popcount 的硬件上，这可以将运行时间缩短 **4×**。
- 这段摘录没有提供更完整的基准测试表、数据集规模、方差，或除 **1.25×** 这一标题结果之外的各基线具体数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04238v1](http://arxiv.org/abs/2604.04238v1)
