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
- agentic-agents
- symbolic-planning
- blocksworld
relevance_score: 0.54
run_id: materialize-outputs
---

# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

## Summary
本文研究LLM是否能像智能体一样，在PDDL模拟器中逐步执行动作并利用状态反馈来改进任务规划。结论是：这种“agentic”闭环方法相对直接一次性出计划只有小幅提升，而且成本高很多，仍明显落后于经典规划器。

## Problem
- 要解决的问题是：LLM做任务规划时，逐步执行并观察PDDL状态反馈，是否比直接一次性生成完整计划更有效，这对自主机器人任务规划很重要。
- 现有LLM规划工作多是直接生成计划或把PDDL交给经典求解器，缺少把LLM放进真实符号状态空间里逐步搜索的系统性评测。
- 关键意义在于区分：LLM到底是在“真正规划”，还是主要依赖训练数据记忆；以及闭环反馈在规划中是否像在代码代理中那样有效。

## Approach
- 作者提出 **PyPDDLEngine**：一个开源PDDL逐步仿真引擎，通过MCP把7类规划操作暴露为LLM工具调用，如初始化、查当前状态、查可执行动作、单步执行、重置、查历史、验证完整计划。
- 在agentic设置中，LLM不是先写完整计划，而是每次选一个动作，执行后读取新状态，再决定下一步；必要时可重置并重试，相当于把LLM当作交互式搜索策略。
- 论文在102个IPC Blocksworld实例上比较4种方法：Fast Downward lama-first、Fast Downward seq-sat-lama-2011、直接LLM规划（Claude Haiku 4.5）、以及基于PyPDDLEngine的agentic LLM规划；统一预算为180秒。
- 评测指标包括成功率、共解实例上的计划长度、失败模式，以及token成本，从而分析agentic反馈带来的收益和代价。
- 作者还比较了不同难度区间和最难实例，分析逐步反馈是否提供了真实的全局进展信号。

## Results
- 在 **102个IPC Blocksworld** 实例上，**Fast Downward** 两个配置都解出 **87/102（85.3%）**；**直接LLM** 解出 **65/102（63.7%）**；**agentic LLM** 解出 **68/102（66.7%）**。也就是说，agentic相对直接法仅提升 **3.0 个百分点**，但仍落后经典规划器 **18.6 个百分点**。
- 成本方面，直接LLM平均每次运行消耗 **28,488 tokens**，agentic为 **169,864 tokens**，约 **5.97×**；按“每个成功解”归一化，直接法是 **44,705 tokens/solution**，agentic是 **254,796 tokens/solution**，约 **5.7×**。多得到的 **3个** 解，总计大约多花 **1,440万 tokens**。
- 失败模式上，agentic方法新增了 **6 个 early exit**（实例32、88、89、96、98、100），其中 **4/6** 个实例其实被直接LLM解出，说明它会错误判断“不可解”。
- 在最难的 **15个** Fast Downward超时实例中，两种LLM都只共同解出 **1个**（实例86）；agentic额外解出 **3个**（76、78、101），直接法额外解出 **1个**（100）。其中实例 **101** 最突出：两种Fast Downward和直接LLM都超时，而agentic在 **108–136秒** 内找到一个 **186步** 的有效计划。
- 在 **49个共解实例** 上，两种LLM在大多数难度区间生成的计划都比 **seq-sat-lama-2011** 更短。例如在 **40–50** 区间，FD lama为 **197.1** 步，FD seq为 **92.6** 步，直接LLM为 **78.0** 步，agentic为 **78.6** 步；在 **30–40** 区间，FD seq为 **63.3**，直接LLM为 **59.7**，agentic为 **60.3**。作者认为这更像是训练数据中的近最优模式召回，而不是可泛化的规划推理。
- 论文最核心的结论是：PDDL逐步反馈只告诉模型“动作是否可执行”，缺少像编译错误/测试失败那样的外部、客观、方向性纠错信号，因此agentic闭环在该任务中的收益有限。

## Link
- [http://arxiv.org/abs/2603.06064v1](http://arxiv.org/abs/2603.06064v1)
