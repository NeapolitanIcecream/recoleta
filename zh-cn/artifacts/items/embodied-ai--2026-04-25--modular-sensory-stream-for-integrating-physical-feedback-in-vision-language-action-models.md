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
## 摘要
MoSS 通过独立的模态流，将触觉和力矩反馈加入预训练的视觉-语言-动作模型，并通过共享注意力与动作模型交互。在真实的高接触机器人任务中，它的成功率高于纯视觉 VLA，也高于只使用单一物理反馈模态的基线。

## 问题
- 标准 VLA 根据视觉和语言执行动作，因此在高接触操作中表现较弱，因为抓握力、接触检测和对齐依赖物理反馈。
- 以往工作通常一次只加入一种物理模态，比如触觉或力矩，难以较好处理多种异构信号。
- 这会影响真实机器人任务，例如杯子拆叠、易碎物体操作、擦板和插头插入，因为仅靠视觉输入可能存在歧义，或漏掉接触事件。

## 方法
- MoSS 为每种物理模态接入一条独立的感知流，例如触觉和力矩，并连接到预训练的基于扩散的 VLA 动作专家。
- 动作流和感知流在结构上保持分离，但通过联合跨模态自注意力交换信息，因此模型可以利用物理信号进行动作预测，而不需要把所有参数完全混合。
- 训练分为两个阶段：先冻结预训练 VLA，只训练新的感知流，使其与现有策略表示对齐；再解冻并联合微调整个模型。
- 一个辅助损失要求每条感知流在动作时域内预测未来的物理信号，用来帮助模型学习接触动态，并更有效地利用反馈。

## 结果
- 在四个真实世界高接触任务上，基础 GR00T N1.5 的平均成功率为 **20.8%**，基础 pi_0 为 **26.1%**。同时使用触觉和力矩的 MoSS 在 GR00T N1.5 上达到 **49.0% avg**，在 pi_0 上达到 **45.9% avg**。
- 对于 **GR00T N1.5**，仅使用触觉的 MoSS 达到 **42.7% avg**，高于 **Tactile-VLA 30.2%** 和 **ForceVLA 34.4%**。仅使用力矩的 MoSS 达到 **37.5% avg**，高于 **TA-VLA 33.3%**。同时使用触觉和力矩时达到 **49.0% avg**。
- 对于 **pi_0**，仅使用力矩的 MoSS 达到 **41.7% avg**，而 **TA-VLA** 为 **34.4%**。同时使用触觉和力矩时达到 **45.9% avg**，高于基础模型的 **26.1% avg**。
- 论文报告的 **GR00T N1.5 + MoSS (tactile+torque)** 各任务最佳结果为：Unstack Cup **54.2%**、PnP Egg **66.7%**、Board Erase **50.0%**、Plug Insertion **25.0%**。
- 在 GR00T N1.5 上的消融实验显示，完整 MoSS 在 Unstack Cup 和 PnP Egg 上分别达到 **54.2%** 和 **66.7%**。去掉解耦模态流后降至 **33.3% / 50.0%**，去掉两阶段训练后降至 **37.5% / 58.3%**，去掉未来预测后降至 **45.8% / 58.3%**。
- 在论文报告的设置中，推理开销较小：GR00T N1.5 每个动作块耗时 **21.0 ms**，MoSS 加入仅触觉后为 **22.4 ms (1.06x)**，仅力矩后为 **21.9 ms (1.04x)**，同时加入两者后为 **23.4 ms (1.11x)**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23272v1](http://arxiv.org/abs/2604.23272v1)
