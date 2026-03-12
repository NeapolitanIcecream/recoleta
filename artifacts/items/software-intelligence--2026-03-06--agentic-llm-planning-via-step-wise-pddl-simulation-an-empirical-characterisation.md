---
source: arxiv
url: http://arxiv.org/abs/2603.06064v1
published_at: '2026-03-06T09:16:49'
authors:
- "Kai G\xF6bel"
- Pierrick Lorang
- Patrik Zips
- "Tobias Gl\xFCck"
topics:
- llm-planning
- pddl-simulation
- agentic-llm
- blocksworld
- classical-planning
relevance_score: 0.67
run_id: materialize-outputs
---

# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

## Summary
本文研究大模型是否能通过与PDDL环境逐步交互来提升任务规划能力，并发布了开源工具 PyPDDLEngine。结论是：逐步交互相对一次性生成只有小幅收益，且代价显著更高。

## Problem
- 任务规划要求从初始状态生成动作序列以到达目标，这对机器人与自主体系统很关键。
- 现有研究尚不清楚：LLM 作为规划器时，逐步执行、观察状态并重试，是否比直接一次性生成完整计划更有效。
- 这个问题重要，因为软件智能体在“执行-看反馈-修正”范式下表现很好，但规划领域的反馈是否同样有用并不明确。

## Approach
- 作者提出 **PyPDDLEngine**：一个支持 STRIPS-style PDDL 的交互式仿真引擎，通过 MCP 将 7 类规划操作暴露为 LLM 工具调用，如初始化、查询状态、查询可行动作、执行单步动作、重置、查看历史、验证完整计划。
- 设计两种 LLM 规划方式：**Direct LLM** 直接一次输出完整计划，失败后从头重试；**Agentic LLM** 每次选一步动作、观察新状态、必要时重置后继续搜索。
- 与两种经典规划器比较：Fast Downward **lama-first** 作为主要经典基线，**seq-sat-lama-2011** 作为计划质量参考。
- 在 102 个 IPC Blocksworld 实例上统一使用 **180 秒**预算，比较成功率、失败模式、共解实例上的计划长度，以及 token 成本。

## Results
- 经典规划器最强：Fast Downward **lama-first** 与 **seq-sat-lama-2011** 都解出 **87/102 = 85.3%**；Direct LLM 解出 **65/102 = 63.7%**；Agentic LLM 解出 **68/102 = 66.7%**，仅比 Direct 高 **3.0 个百分点**。
- 成本显著上升：Direct 平均每次运行 **28,488 tokens**，Agentic 为 **169,864 tokens**；按每个成功解归一化后分别为 **44,705** vs **254,796 tokens/solution**，Agentic 约为 **5.7×** 成本，只多解出 **3** 个实例，对应约 **1,440 万** 额外 tokens。
- Agentic 引入了新的失败模式：有 **6** 个实例发生“提前退出”，即模型错误判断问题不可解；其中 **4/6** 个实例实际上被 Direct LLM 解出，说明交互反馈并未稳定提升判断能力。
- 在 **49** 个四方法共解实例上，两种 LLM 在多数难度区间给出的计划比 **seq-sat-lama-2011** 还短，例如区间 **30–40** 中 Direct/Agentic/FD-seq 平均长度分别为 **59.7 / 60.3 / 63.3**，区间 **40–50** 为 **78.0 / 78.6 / 92.6**。作者认为这更像是训练数据中的模式召回，而不是可泛化规划能力。
- 硬例中有一个显著个案：实例 **101** 上，两种 Fast Downward 和 Direct LLM 都超时，而 Agentic LLM 找到一个 **186 步**有效计划，耗时 **108–136 秒**；但作者强调单一样本不足以证明稳定突破。
- 总体最强主张是：逐步 PDDL 反馈带来的收益有限，因为它主要告诉模型“动作是否合法”，不像编译器报错或测试失败那样提供外部、客观、可定向的纠错信号。

## Link
- [http://arxiv.org/abs/2603.06064v1](http://arxiv.org/abs/2603.06064v1)
