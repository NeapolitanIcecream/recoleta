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
- latent-action
- robot-manipulation
- video-vae
relevance_score: 0.97
run_id: materialize-outputs
---

# Chain of World: World Model Thinking in Latent Motion

## Summary
本文提出 CoWVLA，把世界模型的时间推理与潜在动作的紧凑运动表示结合起来，在潜在运动空间中“思考”机器人未来动态。核心目标是在不重建整段冗余视频背景的情况下，提升 VLA 的动态理解、动作学习效率与控制性能。

## Problem
- 现有 world-model VLA 通过预测未来帧学习环境动态，但要重建大量静态背景像素，序列长、训练低效，容易把容量浪费在“复制画面”而非建模关键运动上。
- 现有 latent-action 方法虽然紧凑，但通常只编码两帧之间的变化，缺少连续时间建模，也较少学习“什么在动、在哪里动、之后场景会怎样变化”的世界知识。
- 这很重要，因为机器人操作需要长期时序推理与可泛化的环境动态理解，而不只是短时动作映射。

## Approach
- 使用预训练视频 VAE 作为 latent motion extractor，将一个视频片段显式分解为 structure latent 和 motion latents，得到更紧凑、可解释的连续运动表示，而不是直接预测整帧像素。
- 在预训练阶段，模型输入语言指令和初始帧，并通过一个可学习的 motion query `Q` 去预测整段视频的 latent motion，同时预测终止帧，从而学习“从当前状态到未来状态”的潜在动态链条。
- 为避免偷看未来，`Q` 采用因果掩码，只能看见指令和初始帧，不能直接访问终止帧或未来观测。
- 在 co-fine-tuning 阶段，把稀疏 keyframes 与离散 action tokens 放进同一个自回归解码器中联合建模；同一个 `Q` 汇总整段时间范围内的潜在动态，并与多步动作预测对齐。
- 该机制本质上是：先学会用压缩的“运动代码”描述世界如何变化，再把这种动态先验接到真实动作生成上。

## Results
- 在 **LIBERO** 上，CoWVLA 平均成功率 **0.956**，高于 **TLA 0.952**、**UniVLA 0.950**、**pi_0 0.942**、**villa-X 0.901**、**FlowVLA 0.881**。分项上：SPATIAL **0.972**、OBJECT **0.978**、GOAL **0.946**、LONG **0.928**。
- 在 **LIBERO-LONG** 上，CoWVLA 达到 **0.928**，超过 **TLA 0.920**、**UniVLA 0.914**、**GR00T N1 0.906**，说明其长时序任务表现更强。
- 在 **SimplerEnv-WidowX** 上，CoWVLA 平均 **0.760**，优于 **FlowVLA 0.740**、**UniVLA 0.687**、**villa-X 0.625**、**LAPA 0.573**、**CogACT 0.513**。各任务为：Stack Block **0.625**、Put Carrot **0.667**、Put Spoon **0.792**、Put Eggplant **0.958**。
- 与训练前版本相比，在 **SimplerEnv-WidowX** 上从 **0.729** 提升到 **0.760**；其中 Stack Block 从 **0.458** 升到 **0.625**，Put Eggplant 从 **0.917** 升到 **0.958**，表明 co-fine-tuning 能把潜在动态先验转化为更强控制性能。
- 视频 VAE 重建指标显示其潜在表示具有较好保真度：预训练/微调后 **PSNR 32.7/33.4**，**SSIM 0.923/0.934**，**LPIPS 0.122/0.123**。
- 论文还给出效率层面的定性主张：相比未来帧重建式 world models，CoWVLA 避免重建冗余中间帧，因而具有“moderate computational efficiency”，但摘录中未提供更详细的训练/推理开销对比数字。

## Link
- [http://arxiv.org/abs/2603.03195v1](http://arxiv.org/abs/2603.03195v1)
