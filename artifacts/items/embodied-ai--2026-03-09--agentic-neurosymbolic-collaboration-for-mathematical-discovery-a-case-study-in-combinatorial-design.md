---
source: arxiv
url: http://arxiv.org/abs/2603.08322v1
published_at: '2026-03-09T12:42:56'
authors:
- Hai Xia
- Carla P. Gomes
- Bart Selman
- Stefan Szeider
topics:
- neurosymbolic-ai
- mathematical-discovery
- combinatorial-design
- latin-squares
- llm-agents
relevance_score: 0.02
run_id: materialize-outputs
---

# Agentic Neurosymbolic Collaboration for Mathematical Discovery: A Case Study in Combinatorial Design

## Summary
本文通过一个人类+LLM智能体+符号工具的协作案例，展示了神经符号系统如何在组合设计中产生新的数学发现。核心成果是解决了 Latin square 在 \(n\equiv 1\pmod 3\) 情况下最小不平衡度的开放问题，并给出经 Lean 4 形式化验证的紧下界。

## Problem
- 论文要解决的是：当 \(n\equiv 1\pmod 3\) 时，Latin square 不可能达到完美空间平衡，此时**最小可能不平衡度是多少**；这是组合设计中的一个开放问题。
- 这个问题重要，因为 Latin square 广泛用于**实验设计**，而空间平衡直接关系到处理分配的均衡性；理论上也涉及 AI 是否能参与真正的数学发现。
- 作者还关心**发现过程本身**：神经模型、符号计算和人类研究者各自贡献了什么，哪些环节真正推动了新结果出现。

## Approach
- 核心机制很简单：让一个 LLM 智能体负责提出猜想、写代码、调度工具和整理证明；让 SageMath、Rust 穷举求解器、模拟退火等符号工具负责**严格验证、搜索和枚举**；让人类提供关键研究转向。
- 关键研究转向不是继续找零不平衡的构造，而是改问：**既然零不可能，最小正不平衡是多少**。这个 pivot 由人类提出，开启了新的优化问题。
- 智能体从数值结果中发现一个隐藏结构：任意两行之间的距离总是**偶数**。最简单地说，这个奇偶性约束让每对行的偏差至少比原先直觉多一倍，从而把下界从朴素估计推高到 \(4n(n-1)/9\)。
- 为达到该下界，作者提出新的构造概念 **near-perfect permutations**：其 shift correlation 只落在两个最优允许值 \(a\) 或 \(a+2\) 中；再由此构造 circulant Latin squares。
- 论文还加入多模型审阅与持久化记忆：多前沿 LLM 并行做**批评和找错**，项目状态文件/知识库用于跨 5 天约 15 个会话保持研究连续性；最终下界在 **Lean 4** 中形式化证明。

## Results
- 数学主结果：对所有 \(n\equiv 1\pmod 3\) 的 \(n\times n\) Latin square，证明了紧下界 **\(I(L)\ge 4n(n-1)/9\)**，并声称这解决了该情形下的开放问题。
- 该结果是**紧的**：通过 near-perfect permutations 构造的 circulant Latin squares 达到等号；例如 \(n=4\) 时，穷举全部 **576** 个 Latin squares，最小不平衡恰为 **\(16/3\)**，与公式 **\(4\cdot4\cdot3/9\)** 一致。
- 计算验证：模拟退火找到了所有 \(n\equiv 1\pmod 3\), **4\le n\le 52** 的 near-perfect permutations，且都达到最优值 **\(I^*=4n(n-1)/9\)**。表中示例包括：\(n=13\) 时 **\(I^*=208/3\)**（时间 **<1 s**），\(n=25\) 时 **\(800/3\)**（**2 s**），\(n=40\) 时 **\(2080/3\)**（**74 s**），\(n=52\) 时 **\(3536/3\)**（**32 s**）。
- 发现触发点的量化例子：在 \(n=13\) 上，朴素下界是 **26**，但模拟退火最优搜索先只找到 **69.3**，两者相差约 **2.7×**；这一异常促使智能体发现“所有距离皆为偶数”的关键奇偶结构。
- 形式化验证：主下界定理在 **Lean 4 + Mathlib** 中完成，约 **340 行**代码，覆盖 Fixed Sum、Parity Lemma 与主不等式。
- 对多模型协作的结论：并行前沿 LLM 在**批评/找错**上有效，曾发现 proof draft 的“circulant trap”；但在建设性断言上不可靠，例如其声称 inversion map 可达 **\(O(n^{5/2})\)** 不平衡，而实验显示实际约为 **\(\Theta(n^{3.6})\)**。

## Link
- [http://arxiv.org/abs/2603.08322v1](http://arxiv.org/abs/2603.08322v1)
