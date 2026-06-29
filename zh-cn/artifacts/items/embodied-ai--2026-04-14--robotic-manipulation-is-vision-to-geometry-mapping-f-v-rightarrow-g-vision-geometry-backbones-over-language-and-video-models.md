---
source: arxiv
url: http://arxiv.org/abs/2604.12908v1
published_at: '2026-04-14T15:57:16'
authors:
- Zijian Song
- Qichang Li
- Jiawei Zhou
- Zhenlong Yuan
- Tianshui Chen
- Liang Lin
- Guangrun Wang
topics:
- vision-language-action
- robot-manipulation
- 3d-world-model
- geometry-aware-policy
- zero-shot-generalization
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models

## Summary
## 总结
VGA 认为，机器人操作应该使用原生 3D 几何特征，而不是语言模型或视频模型特征。它在一个预训练的 3D 世界模型之上构建策略，并报告了在 LIBERO 上的最佳水平表现，以及在真实机器人上更强的零样本跨视角迁移能力。

## 问题
- 这篇论文针对当前机器人基础模型中的一个不匹配：操作依赖 3D 位置、旋转和空间关系，但许多视觉-语言-动作和视频动作模型是在 2D 图文数据或像素预测数据上预训练的。
- 这个不匹配会带来问题，因为策略可能学到视觉模式或语义，却没有学到精确抓取、伸手和放置物体所需的几何信息，这会削弱鲁棒性和视角泛化能力。
- 现有加入 3D 线索的方法仍然保留以 2D 为中心的骨干网络，或者需要额外的深度传感器。作者认为，这会造成 3D 到 2D 的瓶颈，或者增加硬件复杂度。

## 方法
- 核心方法是 VGA，一个 **Vision-Geometry-Action** 模型。它用 **VGGT** 替换常见的 VLM 或视频骨干网络。VGGT 是一个预训练的 3D 世界模型，可将多视角 RGB 直接映射为原生 3D 场景表示。
- 输入包括多视角 RGB、语言指令和机器人的本体感觉信息。这些 token 经过 VGGT transformer，交替使用局部和全局注意力，生成共享的、具备 3D 感知能力的控制 token。
- 动作预测使用动作解码器，chunk size 为 **C=8**。新的 **Progressive Volumetric Modulation (PVM)** 模块通过分阶段交叉注意力，逐层把几何信息注入动作解码器。
- 训练是多任务的：共享骨干同时预测 **动作 + 相机参数 + 深度图**，并使用联合损失。测试时去掉相机和深度分支，因此推理只解码动作。
- 根据摘录，该模型使用 **LoRA rank 64** 训练，可训练参数大约是 **5 亿**。

## 结果
- 在 **LIBERO** 上，VGA 在 Spatial 上为 **99.0%**，Object 上为 **99.6%**，Goal 上为 **98.6%**，Long 上为 **95.0%**，平均为 **98.1%**。
- 与 LIBERO 上的主要 VLA 基线相比，VGA 比 **pi_0.5**（平均 **96.9%**）高 **1.2** 个百分点，比 **OpenVLA-oft**（平均 **97.1%**）高 **1.0** 个百分点，比 **VLA-Thinker**（平均 **97.5%**）高 **0.6** 个百分点。
- 与 3D-VLA 基线相比，VGA 比 **SpatialVLA**（平均 **78.1%**）高 **20.0** 个百分点，比 **GeoAwareVLA**（平均 **96.8%**）高 **1.3** 个百分点，比 **GeoVLA**（平均 **97.7%**）高 **0.4** 个百分点。
- 与 world-action / video 风格基线相比，VGA 比 **Motus**（平均 **97.7%**）高 **0.4** 个百分点，并且比 **mimic-video**（平均 **93.9%**）高 **4.2** 个百分点。
- 在真实机器人上，摘录声称它在未见过的相机视角上有更好的 **zero-shot generalization**，成功率也高于 **pi_0.5**，但提供的文本没有给出真实世界的具体数值。
- 摘录还声称，定量结果确认 VGA 能高保真地预测 3D 属性，但提供的文本没有包含具体的相机/深度指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12908v1](http://arxiv.org/abs/2604.12908v1)
