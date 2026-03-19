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
- agent-evaluation
- human-in-the-loop
- llm-benchmarking
- sim2real-gap
relevance_score: 0.75
run_id: materialize-outputs
language_code: zh-CN
---

# Mind the Sim2Real Gap in User Simulation for Agentic Tasks

## Summary
本文系统研究了交互式代理评测中的用户模拟“Sim2Real gap”，即LLM模拟用户与真实人类用户之间的差距。作者通过真实人类实验、提出USI指标并评测31个模拟器，发现当前LLM用户模拟普遍让任务变得过于容易且评价过于乐观。

## Problem
- 论文要解决的问题是：**LLM用户模拟器是否真的像真实人类一样行为和打分**，以及这种偏差会不会误导代理系统的开发与评测。
- 这很重要，因为越来越多多轮、工具使用型 benchmark 依赖模拟用户来**生成对话**和**给出评价信号**；如果模拟不真实，模型会被优化到“讨好模拟器”而不是服务真实用户。
- 作者进一步追问三点：模拟用户的行为是否像人（RQ1）、模拟评价是否和真人一致（RQ2）、规则奖励能否替代人类反馈（RQ3）。

## Approach
- 作者**形式化定义**用户模拟中的 Sim2Real gap，并拆成六部分：4个行为维度（沟通风格D1、信息提供模式D2、澄清行为D3、错误反应D4）+ 结果校准（ECE）+ 评价一致性（Eval）。
- 提出一个新的综合指标 **User-Sim Index (USI)**，范围0到100，用来衡量某个LLM模拟器与真实用户在交互行为和反馈上的接近程度。
- 在 **$\tau$-bench** 上进行了据称首个完整真人替换实验：让 **451名真实参与者** 在 **165个任务** 上与同一代理交互，并与 **31个LLM模拟器** 做直接对比。
- 行为差异用 **Sørensen–Dice coefficient** 衡量，任务结果层面的模拟-真人偏差用 **ECE** 衡量，评价偏差用模拟打分与真人问卷之间的 **MAE** 衡量。
- 实验同时覆盖专有、开源和专门训练的用户模拟模型，并以人-人一致性作为自然上限参照。

## Results
- 最强模拟器的 **USI仅为76.0（DeepSeek-V3.1）**，明显低于**人类互标上限92.9**，说明即使最佳LLM模拟器也与真实用户存在显著差距。
- 在代表性模型中，**Gemini2.0-Flash** 的 USI 为 **73.3**，**GPT-5.1** 为 **70.9**，**GPT-4o** 为 **69.3**；作者据此指出**更强通用能力并不必然带来更真实的用户模拟**。
- 行为层面，模拟器普遍“过于合作、过于统一、缺少挫败感与模糊性”。例如 **GPT-4o** 中仅 **1.0%** 的回合是短回复，而真实人为 **29.0%**；**49.0%** 的 GPT-4o 回合带礼貌表达，而真实人为 **15.3%**。
- 评价层面，模拟器打分整体偏正向。作者给出的突出例子是：**GPT-5.1** 对AI助手“human-likeness”的评分相对真人**高估55%**，对总体得分**高估18%（按评分量表尺度）**。
- 结果校准方面，不同模型的 **ECE** 与真人仍有明显差距：人类互标 **0.069**，而 **GPT-5.1为0.331**、**GPT-4o为0.206**、**DeepSeek-V3.1为0.122**，说明模拟交互会系统性抬高或扭曲代理成功率。
- 规则奖励也不足以替代人类反馈：论文称 **$\tau$-bench 的二元规则奖励与人类感知质量“大体正交”**，因为它只检查最终数据库状态，无法覆盖政策性拒绝、交互流畅度、信任感、复用意愿等多维体验。

## Link
- [http://arxiv.org/abs/2603.11245v1](http://arxiv.org/abs/2603.11245v1)
