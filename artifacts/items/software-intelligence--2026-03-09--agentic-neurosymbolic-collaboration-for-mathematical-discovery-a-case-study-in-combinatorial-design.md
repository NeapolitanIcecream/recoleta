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
- agentic-ai
- neurosymbolic-reasoning
- mathematical-discovery
- multi-agent-deliberation
- formal-verification
- combinatorial-design
relevance_score: 0.78
run_id: materialize-outputs
---

# Agentic Neurosymbolic Collaboration for Mathematical Discovery: A Case Study in Combinatorial Design

## Summary
本文通过一个人类、LLM 智能体与符号计算工具协作的案例，展示了 AI 可以参与开放式数学发现，而不只是求解预设问题。核心产出是在组合设计中的拉丁方不平衡问题上，证明了当 $n\equiv 1\pmod{3}$ 时的紧下界，并用 Lean 4 进行了形式化验证。

## Problem
- 论文要解决的问题是：当 $n\equiv 1\pmod{3}$ 时，拉丁方的最小可达不平衡度是多少；此前完美平衡不可能，而最小正不平衡一直是开放问题。
- 这很重要，因为拉丁方是组合设计与实验设计中的基础对象，空间平衡性直接关系到设计质量；同时，这也是检验 AI 是否能参与“真正数学发现”的代表性问题。
- 作者还想回答一个方法论问题：在人类、LLM 与符号工具的协作中，各自到底贡献了什么，哪些环节可靠，哪些不可靠。

## Approach
- 核心机制是一个**agentic neurosymbolic**工作流：LLM 智能体负责提出假设、写代码、调用 SageMath/Rust 求解器/模拟退火，并把结果整理成猜想和证明草稿；人类负责战略转向；符号工具负责严格验证与搜索。
- 研究起初尝试从“完美排列/零不平衡”入手，但代数逆向分析失败；人类据此做出关键 pivot，把问题改成“最小正不平衡是多少”。
- 智能体随后从数值实验里发现一个隐藏结构：所有行对距离都是偶数。最简单地说，就是“理论最优值在这里不是整数，而实际距离又必须是偶数，所以每对行至少要偏离得更多”，这把朴素下界翻倍并最终推出全局下界。
- 作者进一步提出**near-perfect permutations**：让移位相关值只落在两个最接近最优的偶数上，从而构造达到该下界的循环拉丁方。
- 系统还用了并行多模型审稿和两层持久记忆。前者主要用于挑错，后者用于跨多天、多 session 保留项目状态、死路记录和知识文件，而无需更新模型参数。

## Results
- 数学主结果：对所有 $n\equiv 1\pmod{3}$ 的 $n\times n$ 拉丁方，都有不平衡下界 $I(L)\ge 4n(n-1)/9$；论文声称这是**紧的**下界，并且解决了该情形下的开放问题。
- 关键对比：在 $n=13$ 时，朴素下界只有 $n(n-1)/6=26$，但模拟退火搜索最优只找到 $69.3$，促使智能体发现“偶性约束”；最终理论下界变为 $4n(n-1)/9=208/3\approx 69.3$，与搜索结果吻合。
- 小规模精确验证：对 $n=4$，穷举全部 $576$ 个拉丁方后，最小不平衡恰为 $16/3=4\cdot4\cdot3/9$，精确匹配新下界。
- 构造性结果：作者定义 near-perfect permutations，并报告对所有 $n\equiv 1\pmod{3}$、$4\le n\le 52$ 都找到了实现最优值的例子。例如 $n=10$ 时最优不平衡为 $40$，$n=22$ 为 $616/3$，$n=52$ 为 $3536/3$。
- 计算效率：表中给出 near-perfect permutation 搜索时间，从 $n=4,7,10,13$ 的小于 1 秒，到 $n=40$ 的 74 秒、$n=43$ 的 139 秒、$n=52$ 的 32 秒。
- 形式化验证：下界定理在 Lean 4 + Mathlib 中完成形式化，约 **340 行** Lean 代码。
- 方法论发现：并行前沿 LLM 审稿对**批评和错误检测**较可靠，成功抓出“循环情形误推广到一般情形”等错误；但对建设性数学结论不可靠，例如其声称逆元映射可达 $O(n^{5/2})$ 不平衡，实验却显示约为 $\Theta(n^{3.6})$。

## Link
- [http://arxiv.org/abs/2603.08322v1](http://arxiv.org/abs/2603.08322v1)
