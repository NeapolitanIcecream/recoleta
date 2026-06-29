---
source: arxiv
url: http://arxiv.org/abs/2604.23272v1
published_at: '2026-04-25T12:28:47'
authors:
- Jimin Lee
- Huiwon Jang
- Myungkyu Koo
- Jungwoo Park
- Jinwoo Shin
topics:
- vision-language-action
- multimodal-robot-learning
- tactile-sensing
- torque-feedback
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models

## Summary
## 总结
MoSS 通过为每种物理模态设置独立的模态流，并用共享注意力把触觉和扭矩反馈接入动作模型，将这些反馈加到预训练的视觉-语言-动作模型中。在真实的接触密集型机器人任务上，它的成功率高于只看视觉的 VLA，也高于只用单一物理模态的基线。

## 问题
- 标准 VLA 只根据视觉和语言做动作，在抓握力、接触检测和对齐依赖物理反馈的接触密集型操作中表现较弱。
- 以往工作通常一次只加入一种物理模态，比如触觉或扭矩，不能很好处理多种异构信号。
- 这对杯子叠放拆分、脆弱物体操作、板擦清理和插头插入等真实机器人任务很重要，因为单靠视觉输入会产生歧义，或者看不到接触事件。

## 方法
- MoSS 为每种物理模态，例如触觉和扭矩，接入一条独立的感知流，并连接到一个预训练的、基于扩散的 VLA 动作专家。
- 动作流和感知流在结构上保持分离，但通过联合跨模态自注意力交换信息，这样模型可以在不完全混合所有参数的情况下使用物理信号进行动作预测。
- 训练分两阶段：先冻结预训练 VLA，只训练新的感知流，让它们对齐现有的策略表示；然后解冻，整体联合微调。
- 一个辅助损失要求每条感知流预测动作时间范围内未来的物理信号，用来帮助模型学习接触动态，并更有效地使用反馈。

## 结果
- 在四个真实世界的接触密集型任务上，基础 GR00T N1.5 的平均成功率是 **20.8%**，基础 pi_0 的平均成功率是 **26.1%**。同时使用触觉和扭矩的 MoSS 在 GR00T N1.5 上达到 **49.0%** 平均成功率，在 pi_0 上达到 **45.9%**。
- 对于 **GR00T N1.5**，只用触觉的 MoSS 达到 **42.7%** 平均成功率，优于 **Tactile-VLA 30.2%** 和 **ForceVLA 34.4%**。只用扭矩的 MoSS 达到 **37.5%** 平均成功率，优于 **TA-VLA 33.3%**。同时使用触觉和扭矩时达到 **49.0%** 平均成功率。
- 对于 **pi_0**，只用扭矩的 MoSS 达到 **41.7%** 平均成功率，高于 **TA-VLA 34.4%**。同时使用触觉和扭矩时达到 **45.9%** 平均成功率，高于基础模型的 **26.1%** 平均成功率。
- **GR00T N1.5 + MoSS（触觉+扭矩）** 在各任务上的最佳结果分别是：Unstack Cup **54.2%**，PnP Egg **66.7%**，Board Erase **50.0%**，Plug Insertion **25.0%**。
- 在 GR00T N1.5 上的消融结果显示，完整 MoSS 在 Unstack Cup 上为 **54.2%**，在 PnP Egg 上为 **66.7%**。去掉解耦流后，结果降到 **33.3% / 50.0%**；去掉两阶段训练后，降到 **37.5% / 58.3%**；去掉未来预测后，降到 **45.8% / 58.3%**。
- 该设置下的推理开销很小：GR00T N1.5 每个动作块耗时 **21.0 ms**，MoSS 只加触觉时为 **22.4 ms（1.06x）**，只加扭矩时为 **21.9 ms（1.04x）**，两者都加时为 **23.4 ms（1.11x）**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23272v1](http://arxiv.org/abs/2604.23272v1)
