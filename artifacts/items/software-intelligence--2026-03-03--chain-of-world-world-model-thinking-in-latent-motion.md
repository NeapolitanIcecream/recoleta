---
source: arxiv
url: http://arxiv.org/abs/2603.03195v1
published_at: '2026-03-03T12:52:06'
authors:
- Fuxiang Yang
- Donglin Di
- Lulu Tang
- Xuancheng Zhang
- Lei Fan
- Hao Li
- Chen Wei
- Tonghua Su
- Baorui Ma
topics:
- vision-language-action
- world-model
- latent-motion
- robot-learning
- embodied-ai
relevance_score: 0.78
run_id: materialize-outputs
---

# Chain of World: World Model Thinking in Latent Motion

## Summary
CoWVLA提出一种把“世界模型”的时序推理与“潜在动作”的紧凑表示结合起来的VLA预训练范式，用潜在运动链而不是逐帧重建来学习机器人动态。它旨在更高效地学习视觉-语言-动作控制，同时保留对未来状态和世界变化的理解。

## Problem
- 现有world-model VLA通常通过预测未来图像帧来学习动态，但会浪费大量容量在静态背景和冗余像素重建上，训练代价高。
- 现有latent-action方法虽更紧凑，却通常只建模相邻两帧变化，缺少连续时序推理，也较少学习“场景会如何演化”的世界知识。
- 这很重要，因为机器人控制不仅要输出动作，还要理解动作如何持续改变环境，尤其在长时程、多步骤操控中更关键。

## Approach
- 使用预训练视频VAE作为**latent motion extractor**，把视频片段显式拆成结构latent和运动latent；运动部分进一步由两个方向的运动表示组成，再拼成统一的latent motion向量。
- 在预训练阶段，模型输入“指令 + 初始帧 + 一个可学习的motion query”，学习预测整段视频的连续latent motion，并预测终止帧，而不是重建所有中间帧。
- 通过因果mask，motion query只能看见指令和初始帧，不能偷看未来帧，迫使模型真正推断未来动态。
- 在co-fine-tuning阶段，把稀疏关键帧和离散动作序列放进统一自回归解码器中，联合学习动作token、关键帧token和latent motion的一致性。
- 这样做的直观机制是：先让模型学会“这段视频里的核心运动是什么”，再把这种运动理解对齐到实际动作生成上，从而兼顾紧凑表示、可解释性和时序世界建模。

## Results
- 在**LIBERO**上，CoWVLA平均成功率为**0.956**，优于UniVLA的**0.950**、TLA的**0.952**、villa-X的**0.901**、FlowVLA的**0.881**。分项上达到：SPATIAL **0.972**、OBJECT **0.978**、GOAL **0.946**、LONG **0.928**。
- 在**SimplerEnv-WidowX**上，CoWVLA平均为**0.760**，高于FlowVLA的**0.740**、UniVLA的**0.687**、villa-X的**0.625**、LAPA的**0.573**。具体任务为：Stack Block **0.625**、Put Carrot **0.667**、Put Spoon **0.792**、Put Eggplant **0.958**。
- 论文声称其同时超过现有**world-model**与**latent-action**方法；例如对最佳world-model基线FlowVLA，SimplerEnv平均提升**+0.020**（0.760 vs 0.740）；对最佳latent-action基线TLA，LIBERO平均提升**+0.004**（0.956 vs 0.952）。
- 视频VAE重建质量在SimperEnv相关评测中达到：预训练PSNR/SSIM/LPIPS为**32.7 / 0.923 / 0.122**，微调后为**33.4 / 0.934 / 0.123**，同时下游平均成功率从**0.729**提升到**0.760**。
- 实现上，latent motion extractor在**237k**机器人视频上适配训练；主干使用**8.5B**参数的Emu3，这支持其“大规模预训练+下游机器人控制”的设定，但文中对计算效率主要给出定性表述为“moderate computational efficiency”，未提供更细的吞吐/成本对比数字。

## Link
- [http://arxiv.org/abs/2603.03195v1](http://arxiv.org/abs/2603.03195v1)
