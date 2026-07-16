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

# 机器人适配工作正在更贴近接触和指令控制

## 概览
这一天的重点很集中，都是在处理能承受真实部署约束的机器人适配。一个工作把触觉和力矩信号加入 VLA 策略，在接触密集任务上的平均成功率几乎翻倍。另一个工作表明，只要模型保护好预训练的视觉 grounding，并在推理时用提示引导，小规模后训练也能保住指令跟随能力。

## 研究发现

### 物理反馈开始成为可用的 VLA 输入
MoSS 给了当天最强的实证理由，把物理反馈直接加入视觉-语言-动作模型。它把触觉和力矩输入分成独立通道，再通过共享注意力让它们与动作模型交互。在四个真实机器人任务上，完整模型把 GR00T N1.5 的平均成功率从 20.8% 提高到 49.0%，把 pi_0 从 26.1% 提高到 45.9%。在双信号设置下，报告的额外开销只有 1.11x。这里的任务组合很关键：杯子拆叠、鸡蛋抓放、板擦除和插头插入都依赖视觉单独看不到的接触线索。

#### 资料来源
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): 触觉+力矩整合到 VLA 中的总结和主要结果。

### 低数据适配现在更看重可操控性，而不只是任务匹配
DeLock 关注的是一个更窄但很重要的失败模式：低数据后训练会让机器人在学会任务后不再服从新指令。论文在微调时让视觉编码器尽量保持预训练状态，然后在测试时用 Contrastive Prompt Guidance（CPG）把动作生成偏向新提示词。在 8 个任务、每个 20 次试验的设置下，它在两个概念锁定测试上得到 19/20，在几个空间锁定测试上得到 11/20 到 14/20。相对低数据基线 RETAIN，提升幅度很大，包括 T2 上 19/20 对 0/20，T8 上 13/20 对 1/20。消融也显示，CPG 承担了大部分空间泛化工作。

#### 资料来源
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): 保留低数据后训练下可操控性的总结、方法和基准结果。
