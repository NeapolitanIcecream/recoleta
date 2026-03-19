---
source: arxiv
url: http://arxiv.org/abs/2603.11245v1
published_at: '2026-03-11T19:12:31'
authors:
- Xuhui Zhou
- Weiwei Sun
- Qianou Ma
- Yiqing Xie
- Jiarui Liu
- Weihua Du
- Sean Welleck
- Yiming Yang
- Graham Neubig
- Sherry Tongshuang Wu
- Maarten Sap
topics:
- user-simulation
- sim2real
- llm-evaluation
- interactive-agents
- human-feedback
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Mind the Sim2Real Gap in User Simulation for Agentic Tasks

## Summary
本文系统研究了在交互式智能体评测中，LLM 充当“用户模拟器”时与真实人类之间的 Sim2Real gap，并提出统一度量指标 USI。基于 451 名真实参与者、165 个任务和 31 个模拟器的对比，作者发现当前模拟器普遍让评测变得过于容易且反馈过于乐观。

## Problem
- 论文解决的问题是：LLM 用户模拟器是否真的像真实人类一样互动和打分；如果不真实，交互式 benchmark 可能高估智能体表现并误导优化方向。
- 这很重要，因为越来越多 NLP/agent benchmark 依赖模拟用户来同时**生成对话**和**提供评估信号**，一旦模拟偏离真实人类，训练与评测都会产生系统性偏差。
- 作者还进一步追问：规则奖励能否替代人类反馈；如果不能，仅靠自动 reward 会漏掉用户真正关心的体验质量。

## Approach
- 作者形式化定义了用户模拟中的 Sim2Real gap，将其拆成四个行为维度：communication style、information pattern、clarification、error reaction，以及两个评估维度：outcome calibration 和 evaluative alignment。
- 提出 **User-Sim Index (USI)**，把上述维度聚合成一个 0–100 分数，用来衡量某个 LLM 模拟器与真实人类在交互行为和反馈上的接近程度。
- 在 **τ-bench** 上做案例研究：用 **451 名真实参与者**替换原有 LLM 用户模拟器，覆盖 **165 个任务**，并与 **31 个 LLM 模拟器**做同任务、同 agent 的直接比较。
- 行为对齐用 Sørensen–Dice coefficient，比对词汇/结构特征；结果校准用 ECE；评价对齐用人类与模拟用户在多维问卷上的 MAE。
- 核心机制可以简单理解为：先让“真人用户”和“LLM 用户”分别与同一个 agent 完成同样任务，再比较他们**怎么说、何时澄清、犯错后怎么反应、给多少分**，最后汇总成 USI。

## Results
- 人类之间的一致性上限为 **USI 92.9±0.9**，而 **31 个 LLM 模拟器中最好仅 76.0±1.2（DeepSeek-V3.1）**，显示出明显 Sim2Real gap；其他较高者包括 **Llama-4-Maverick 73.9±0.8**、**Gemini2.0-Flash 73.3±0.4**、**Qwen3-235B 71.2±0.8**。
- 作者明确声称：LLM 模拟器会制造“easy mode”，把 agent 成功率抬高到高于真实人类基线；用于量化这种结果偏差的 ECE 中，人类为 **0.069±0.022**，而不少模型更高，如 **GPT-5.1: 0.331±0.030**、**GPT-4o-mini: 0.382±0.035**、**GPT-3.5-turbo: 0.582±0.035**。
- 在行为层面，模拟器显著比人类更合作、更统一、更少挫败感。文中示例：**GPT-4o** 的短回复比例只有 **1.0%**，而人类是 **29.0%**；**GPT-4o** 的礼貌回复比例 **49.0%**，人类仅 **15.3%**。
- 在综合维度上，最优模型 **DeepSeek-V3.1** 虽然总分最高，但仍显著低于人类：**D1 45.1 vs human 87.4**，**D2 86.6 vs 97.9**，**D3 74.5 vs 88.0**，**D4 87.6 vs 93.5**，**Eval 74.3 vs 97.4**。
- 在评估层面，LLM 模拟用户给分系统性偏高；文中指出 **GPT-5.1** 会把 AI assistant 的 **human-likeness 高估 55%**，把 **overall score 高估 18% 的评分尺度**。
- 规则奖励也不能替代人类反馈：τ-bench 的二元 reward 与人类感知质量“大体正交”，因为它只检查最终数据库状态，无法覆盖人类在成功、政策约束、效率、流畅度、复用意愿等多维评价。

## Link
- [http://arxiv.org/abs/2603.11245v1](http://arxiv.org/abs/2603.11245v1)
