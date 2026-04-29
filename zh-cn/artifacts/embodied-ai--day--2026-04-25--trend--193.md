---
kind: trend
trend_doc_id: 193
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
topics:
- robotics
- vision-language-action
- tactile sensing
- low-data post-training
- steerability
run_id: materialize-outputs
aliases:
- recoleta-trend-193
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/tactile-sensing
- topic/low-data-post-training
- topic/steerability
language_code: zh-CN
---

# 机器人适配研究正更贴近接触反馈和指令控制

## Overview
这一天的工作集中在能经受真实部署约束的机器人适配。一篇论文把触觉和力矩信号加入 VLA 策略，在接触密集型任务上将平均成功率接近翻倍。另一篇表明，如果模型在推理时保护预训练的视觉落地能力并使用提示引导，小规模后训练数据集也能保住指令跟随能力。

## Clusters

### 物理反馈正在成为实用的 VLA 输入
MoSS 为当天的论文中“将物理反馈直接接入视觉-语言-动作模型”提供了最有力的实证证据。它把触觉和力矩输入放在彼此独立的流中，再通过共享注意力让它们与动作模型交互。在四项真实机器人任务上，完整模型把 GR00T N1.5 的平均成功率从 20.8% 提高到 49.0%，把 pi_0 从 26.1% 提高到 45.9%。双信号设置的额外开销较小，为 1.11x。这里的任务组合很关键：杯子拆叠、鸡蛋抓放、白板擦除和插头插入都依赖接触线索，而单靠视觉可能会漏掉这些线索。

#### Evidence
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): 关于将触觉+力矩集成到 VLA 中的摘要和主要结果。

### 低数据适配的评价标准正在从任务拟合转向可控性
DeLock 关注一个更窄但重要的失败模式：低数据后训练会让机器人在学会任务后不再服从新的指令。论文在微调时让视觉编码器尽量接近其预训练状态，然后在测试时使用 Contrastive Prompt Guidance (CPG)，把动作生成偏向新的提示词。在 8 个任务、每个任务 20 次试验中，它在两个 concept-lock 测试上都得到 19/20，在多个 spatial-lock 测试上得到 11/20 到 14/20。与低数据 RETAIN 基线相比，提升幅度很大，包括 T2 上 19/20 对 0/20，以及 T8 上 13/20 对 1/20。消融实验也表明，CPG 承担了空间泛化中的很大一部分作用。

#### Evidence
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): 关于在低数据后训练下保持可控性的摘要、方法和基准结果。
