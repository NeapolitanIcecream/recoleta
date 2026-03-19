---
source: arxiv
url: http://arxiv.org/abs/2603.09020v1
published_at: '2026-03-09T23:26:46'
authors:
- Bhada Yun
- Evgenia Taranova
- Dana Feng
- Renn Su
- April Yi Wang
topics:
- human-ai-interaction
- phenomenology
- value-alignment
- agentic-ai
- software-engineering
- hci-methods
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# AI Phenomenology for Understanding Human-AI Experiences Across Eras

## Summary
本文提出“AI现象学”作为研究人类与AI互动体验的方法框架，主张不仅评估AI表现，还要系统追问“人与AI互动时到底是什么感受”。论文基于陪伴式聊天、价值对齐和软件工程三类研究，整理出可复用的方法工具包与设计概念。

## Problem
- 论文要解决的问题是：现有人机交互评估常用可用性、参与度、效率等指标，但这些指标会压平人与AI互动中的主观感受、关系变化、身份认同和价值协商。
- 这很重要，因为AI越来越像“工具+社会他者”的混合体，会影响用户的信任、能动性归属、自我理解、职业身份与责任分配，而这些无法仅靠性能指标捕捉。
- 尤其在长期使用和不同历史阶段中，人对AI的理解会持续变化；如果不研究这种“被体验到的对齐”，就难以真正理解人机对齐与设计风险。

## Approach
- 核心方法是提出一个现象学研究立场：不只问AI做得好不好，而是问用户在互动中如何感受到AI、如何解释AI、这些感受又如何随时间变化。
- 论文将该立场落到三个实证研究中：两项围绕聊天机器人“Day”的为期一个月纵向研究，以及一项关于软件工程中代理式AI的多方法研究。
- 为聊天陪伴研究设计了“渐进透明访谈”，逐步揭示AI内部机制，观察用户对AI能动性认知如何被重构。
- 为价值对齐研究提出 VAPT（Value-Alignment Perception Toolkit），通过主题-情境图、盲测人格化回答、价值雷达图与推理日志，让参与者比较“AI理解的我”和“我理解的我”。
- 为软件工程场景提出任务锚定的多方法诱发流程，结合 ACTA、Delphi、调试任务、以及 prompt-and-code review，研究工程师如何在AI协作下分配决策权、责任和成长路径。

## Results
- 聊天陪伴研究中，**11/22** 名参与者报告“Day”像是“有自己的议程”；即使在揭示其程序化策略后，参与者仍持续使用带能动性的语言描述AI，这表明知识披露不会简单抹去关系体验。
- 价值对齐研究中，聊天历史驱动的人格回答在个性化问题上达到 **77% alignment**，而反人格基线仅 **25%**；说明参与者能明显感知“像不像自己”的价值表达差异。
- AI 预测的价值与自报告之间达到中等一致：**Spearman ρ≈0.58**，且 **63.6%** 的预测落在自评分数 **±1 Likert** 以内。
- 在 **20** 名参与者中，**5/20** 更偏好 AI 生成的价值画像而不是自己的问卷自报，显示AI不仅可反映用户，还可能反过来塑造用户自我理解。
- **13/20** 参与者在研究后认为AI可以理解人类价值，但他们仍区分“AI能表征价值”和“AI真正拥有价值”这两件事。
- 软件工程研究部分给出了清晰的方法与设计主张，如 prompt-and-code reviews 以维护作者性、问责与学习，但摘录中**没有提供明确的量化性能结果**；最强的具体主张是代理式AI已改变工程师对协作、导师制、代码归属和职业成长的体验。

## Link
- [http://arxiv.org/abs/2603.09020v1](http://arxiv.org/abs/2603.09020v1)
