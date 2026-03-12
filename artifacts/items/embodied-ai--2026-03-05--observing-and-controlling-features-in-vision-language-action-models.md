---
source: arxiv
url: http://arxiv.org/abs/2603.05487v1
published_at: '2026-03-05T18:53:50'
authors:
- Hugo Buurmeijer
- Carmen Amo Alonso
- Aiden Swann
- Marco Pavone
topics:
- vision-language-action
- mechanistic-interpretability
- activation-steering
- representation-control
- openvla
- robot-policy
relevance_score: 0.94
run_id: materialize-outputs
---

# Observing and Controlling Features in Vision-Language-Action Models

## Summary
本文提出一个用于视觉-语言-动作模型（VLA）的内部可解释与可控框架：先“观察”隐藏特征，再用最小线性干预去“控制”这些特征。核心目标是在**不微调模型**的前提下，实时引导机器人行为，同时尽量保持原有闭环能力与自然动作。

## Problem
- VLA虽强，但其行为常常**不可预测、难以在线纠正**，也可能与用户偏好或安全约束不一致。
- 现有LLM中的activation steering思想**不能直接迁移**到VLA，因为VLA是多模态输入、连续动作输出、且处于闭环机器人控制中。
- 关键问题是：能否从VLA内部表示中**读出与行为相关的特征**，并以**轻量、精确、尽量不破坏原策略**的方式在线操控这些特征？

## Approach
- 提出两个形式化概念：**feature-observability**（某层隐藏状态里能否读出目标特征）与 **feature-controllability**（能否通过修改某层隐藏状态把特征推到目标区间）。
- 用一个**线性observer/probe**从Transformer某层激活中预测机器人状态或动作特征；论文主要关注末端位姿、姿态与夹爪状态/动作等可测可控变量。
- 用一个**最小范数线性干预**：在隐藏表示上加一个偏移向量，使经observer读出的特征落入期望区间；当observer是线性的且目标是一维区间时，干预有**闭式解**。
- 将observer与controller嵌入推理时前向传播，在选定层在线执行，形成**无需再训练/微调**的闭环 steering 机制。
- 方法在两类VLA上验证：**OpenVLA**（Transformer-based）与 **π₀.₅**（Transformer + flow-matching hybrid）。

## Results
- 论文明确声称：在 **Libero / π₀.₅** 与 **BridgeData V2 / OpenVLA** 上，机器人**状态和动作可由线性probe从表示空间中观测出来**，且这些观测对小扰动具有鲁棒性。
- 论文声称：通过**目标化、轻量级的线性干预**，可以**可靠地引导机器人行为**，并且**保留闭环能力**，实现无需微调的在线对齐。
- 论文还声称：该方法支持**实时**地按用户偏好和任务要求对VLA进行对齐，且额外运行时开销**很小/可忽略**，因为observer与controller都采用线性计算和闭式控制解。
- 该摘录**没有给出完整的定量结果数字**（如成功率、误差、相对基线提升百分比）；只提到图3展示了与“均值预测/多数类预测”基线的比较、图4展示了不同层干预对动作（如delta yaw）的影响，但具体数值在摘录中缺失。
- 因此，最强的具体结论是：**线性可观测 + 最小线性可控**在两种代表性VLA架构上成立，并可用于**在线、无微调**的行为转向。

## Link
- [http://arxiv.org/abs/2603.05487v1](http://arxiv.org/abs/2603.05487v1)
