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

# 具身模型按韧性和可复用的视觉理解来评判

## Overview
4 月 11 日的内容不多，但很清楚。最强的工作都在要求模型在输入被污染时仍能工作，以及让视觉预测器在无需额外监督的情况下跨任务复用。STRONG-VLA 给出了机器人方向最清楚的硬指标。ZWM 则用有限的自然视频提出了更广的学习主张。

## Clusters

### 鲁棒 VLA 训练成为一个明确的评测目标
STRONG-VLA 将这一天的重点放在具身控制中的失效容忍度上。论文认为，鲁棒性训练应拆成两步：先在扰动下学习，再恢复干净任务上的保真度。证据很具体。在 LIBERO 上，OpenVLA 的提升达到已见场景 +12.60%、未见场景 +7.77%，OpenVLA-OFT 为 +14.48% 和 +13.81%，pi0 为 +16.49% 和 +5.58%。干净性能仍接近基线。基准也很关键。它覆盖文本和视觉上的 28 类扰动，包括语义漂移和动态视觉伪影这类留出测试。这让论文对应的是遮挡、指令污染和传感器噪声等部署问题，而不只是合成压力测试。

#### Evidence
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md): Summary gives the two-stage method, 28 perturbation benchmark, and headline gains across OpenVLA, OpenVLA-OFT, and pi0.

### 一个视觉预测器被要求支持多种零样本任务
Zero-shot World Model，简称 ZWM，让这一天有了第二个重点：从稀疏自然视频中获得广泛的视觉能力。设置很具体。模型完整看到一帧，只看到下一帧大约 10% 的内容，然后学习预测剩余部分。测试时，模型通过对输入做小改动，在不做任务特定训练的情况下读出光流、深度、分割和简单物理推理。论文声称，仅靠儿童第一视角视频就能做到这一点：BabyZWM 使用 34 个孩子共 868 小时的数据，单一儿童的 132 小时版本在多数任务上也接近完整版本。最强的结果是覆盖面。文中报告，同一个预测器在 TAP-Vid-DAVIS 光流上有竞争力，在 UniQA-3D 深度上超过 90%，在 SpelkeBench 分割上表现强，在论文的短时程物理基准上接近 100%。

#### Evidence
- [Zero-shot World Models Are Developmentally Efficient Learners](../Inbox/2026-04-11--zero-shot-world-models-are-developmentally-efficient-learners.md): Summary describes the masked two-frame predictor, zero-shot readout method, and cross-task results.
