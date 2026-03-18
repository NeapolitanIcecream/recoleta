---
source: arxiv
url: http://arxiv.org/abs/2603.14646v1
published_at: '2026-03-15T22:54:03'
authors:
- Thuy Ngoc Nguyen
- Duy Nhat Phan
- Cleotilde Gonzalez
topics:
- theory-of-mind
- temporal-memory
- llm-evaluation
- belief-tracking
- social-reasoning
relevance_score: 0.02
run_id: materialize-outputs
---

# Dynamic Theory of Mind as a Temporal Memory Problem: Evidence from Large Language Models

## Summary
本文将动态心智理论（ToM）重新表述为一个**时间记忆与检索**问题，而不只是单步静态推断。作者提出 DToM-Track，用多轮对话测试大语言模型能否跟踪他人信念随时间的变化轨迹。

## Problem
- 现有 ToM 评测大多只问“某一时刻别人相信什么”，忽略了现实交互里更关键的能力：**在更新发生后还能记住并取回先前信念**。
- 这很重要，因为人机长期交互需要系统持续跟踪用户不断变化的信念、目标和误解；如果只能抓住“最新状态”，就会在历史一致性和社会推理上出错。
- 作者要回答的是：LLM 是否真的具备动态 ToM，还是只擅长根据最近信息推断当前信念？

## Approach
- 提出 **DToM-Track** 评测框架，构造带有预先安排的信念更新的多轮对话，并专门考察三类动态问题：**更新前信念回忆**、**更新后当前信念推断**、**更新发生时点检测**。
- 对话通过受控的 **LLM–LLM role-play** 生成；每个角色在每轮发言前都有隐藏的“inner speech”来显式记录其私有心理状态，但对对话对方不可见，从而制造信息不对称。
- 框架维护结构化的心理状态追踪器，记录信念类型、来源轮次、是否被更新、以及更新前内容，从而自动生成时序问题，也支持二阶信念与 false belief 问题。
- 使用多阶段 LLM 过滤流程验证：计划中的更新是否真的在对话中实现、问答是否可回答且干扰项合理；最终得到一个包含 **5,794** 道题的数据集。
- 在 **6 个模型** 上做零样本多选评测：LLaMA 3.3-70B、Mistral Large、Ministral-14B、GPT-4o-mini、LLaMA 3.1-8B、LLaMA 3.2-3B。

## Results
- 数据集规模为 **5,794** 题；题型分布包括 Temporal **1,807 (31.2%)**、False Belief **1,761 (30.4%)**、Second-Order **768 (13.3%)**、Update Detection **591 (10.2%)**、Post-Update **527 (9.1%)**、Pre-Update **340 (5.9%)**。
- 总体准确率上，6 个模型都高于 **25%** 随机基线；范围为 **35.7%**（LLaMA 3.2-3B）到 **63.3%**（LLaMA 3.3-70B），GPT-4o-mini 为 **55.1%**。
- 按题型平均看，**Update Detection 67.5%** 最高，**Post-Update 63.9%** 次之，但 **Pre-Update 仅 27.7%**，说明模型更会回答“现在相信什么”，却很难回忆“更新前相信什么”。
- 与标准 ToM 题相比，动态记忆明显更难：**Pre-Update 27.7%** 低于 **False Belief 44.7%**，表明“追踪信念轨迹”是不同于经典 false-belief 推理的独立挑战。
- 最强模型 LLaMA 3.3-70B 在各题型上的准确率分别为：Temporal **65.5%**、Update Detection **76.1%**、Post-Update **71.3%**、False Belief **59.2%**、Second-Order **62.0%**、Pre-Update **40.9%**；即便最强模型也在更新前信念回忆上显著掉点。
- 论文的核心经验结论是：这种“后更新强、前更新弱”的稳定不对称现象跨模型家族和规模都存在，支持作者关于 **recent-information bias / interference** 的解释。

## Link
- [http://arxiv.org/abs/2603.14646v1](http://arxiv.org/abs/2603.14646v1)
