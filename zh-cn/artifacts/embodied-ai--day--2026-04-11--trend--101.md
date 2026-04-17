---
kind: trend
trend_doc_id: 101
granularity: day
period_start: '2026-04-11T00:00:00'
period_end: '2026-04-12T00:00:00'
topics:
- embodied-ai
- vla-robustness
- world-models
- zero-shot-vision
run_id: materialize-outputs
aliases:
- recoleta-trend-101
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vla-robustness
- topic/world-models
- topic/zero-shot-vision
language_code: zh-CN
---

# 具身模型开始按韧性和可复用的视觉理解来评判

## Overview
4 月 11 日的研究不多，但信号很清楚。最强的工作都在要求模型满足两点：输入被破坏时还能继续工作，视觉预测器还能在不增加额外监督的情况下跨任务复用。STRONG-VLA 给出了机器人方向最清楚的硬指标。ZWM 则用有限的自然视频提出了更宽泛的学习主张。

## Clusters

### 鲁棒 VLA 训练成为一个明确的评测目标
STRONG-VLA让这一天的重点落在具身控制中的失效容忍能力上。论文认为，鲁棒性训练应拆成两步：先在扰动下学习，再恢复干净任务上的保真度。证据很具体。在 LIBERO 上，OpenVLA 在已见扰动和未见扰动下分别提升 +12.60% 和 +7.77%，OpenVLA-OFT 分别提升 +14.48% 和 +13.81%，pi0 分别提升 +16.49% 和 +5.58%。干净输入下的性能与基线接近。这个基准本身也很关键。它覆盖文本和视觉两种模态下的 28 类扰动，包括 semantic drift 和 dynamic visual artifacts 等留出测试项。这让论文对应的是部署中的问题，如遮挡、指令损坏和传感器噪声，而不只是合成压力测试。

#### Evidence
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md): 摘要给出了两阶段方法、包含 28 类扰动的基准，以及 OpenVLA、OpenVLA-OFT 和 pi0 的主要增益。

### 一个视觉预测器被要求支持多种零样本任务
Zero-shot World Model，也就是 ZWM，构成了当天的第二个重点：用稀疏的自然视频学到广泛的视觉能力。设定很具体。模型完整看到第一帧，再看到下一帧大约 10% 的内容，然后学习预测其余部分。测试时，研究者通过很小的输入干预，在不做任务专门训练的情况下读出光流、深度、分割和简单物理推理。论文称，只用儿童第一视角视频也能做到这一点：BabyZWM 使用来自 34 名儿童的 868 小时视频训练，连只用单个儿童 132 小时数据的版本，在大多数任务上也很接近。最强的结果在于覆盖面。同一个预测器据称在 TAP-Vid-DAVIS 光流上有竞争力，在 UniQA-3D 深度上超过 90%，在 SpelkeBench 分割上表现很强，在论文的短时尺度物理基准上接近 100%。

#### Evidence
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): 摘要描述了带掩码的双帧预测器、零样本读出方法，以及跨任务结果。
