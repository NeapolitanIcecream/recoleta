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
## 摘要
VGA 认为，机器人操作应使用原生 3D 几何特征，而不是语言模型或视频模型特征。它在一个预训练 3D 世界模型之上构建策略，并报告了当前最优的 LIBERO 表现，以及在真实机器人上更强的零样本跨视角迁移能力。

## 问题
- 论文关注当前机器人基础模型中的一个错配：操作依赖 3D 位置、旋转和空间关系，但许多 Vision-Language-Action 和视频动作模型预训练于 2D 图文或像素预测数据。
- 这个错配会带来问题，因为策略可能学会视觉模式或语义信息，却没有学到精确抓取、伸手和物体放置所需的几何结构，从而损害鲁棒性和视角泛化能力。
- 此前尝试加入 3D 线索的方法，仍然保留以 2D 为中心的骨干网络，或需要额外的深度传感器。作者认为，这会造成 3D 到 2D 的瓶颈，或增加硬件复杂度。

## 方法
- 核心方法是 VGA，即 **Vision-Geometry-Action** 模型。它用 **VGGT** 替代常见的 VLM 或视频骨干网络。VGGT 是一个预训练 3D 世界模型，可将多视角 RGB 直接映射为原生 3D 场景表示。
- 输入包括多视角 RGB、语言指令和机器人本体感觉。这些 token 经过 VGGT transformer，并采用局部与全局注意力交替的方式，生成用于控制的共享 3D 感知 token。
- 动作预测使用一个 chunk size 为 **C=8** 的动作解码器。新的 **Progressive Volumetric Modulation (PVM)** 模块通过分阶段交叉注意力，逐层将几何信息注入动作解码器。
- 训练采用多任务方式：共享骨干网络通过联合损失同时预测 **actions + camera parameters + depth maps**。测试时会移除相机和深度分支，因此推理时只解码动作。
- 根据摘要内容，该模型使用 **LoRA rank 64** 训练，系统中约有 **500M trainable parameters**。

## 结果
- 在 **LIBERO** 上，VGA 在 Spatial 上报告 **99.0%**，Object 上 **99.6%**，Goal 上 **98.6%**，Long 上 **95.0%**，平均 **98.1%**。
- 与 LIBERO 上的主要 VLA 基线相比，VGA 比 **pi_0.5**（**96.9% avg**）高 **+1.2 个点**，比 **OpenVLA-oft**（**97.1% avg**）高 **+1.0**，比 **VLA-Thinker**（**97.5% avg**）高 **+0.6**。
- 与 3D-VLA 基线相比，VGA 比 **SpatialVLA**（**78.1% avg**）高 **+20.0 个点**，比 **GeoAwareVLA**（**96.8% avg**）高 **+1.3**，比 **GeoVLA**（**97.7% avg**）高 **+0.4**。
- 与 world-action/video 风格基线相比，VGA 比 **Motus**（**97.7% avg**）高 **+0.4 个点**，比 **mimic-video**（**93.9% avg**）高 **+4.2**。
- 对于真实机器人，摘要称其在未见过的相机视角上具有更好的 **zero-shot generalization**，且成功率高于 **pi_0.5**，但提供的文本中没有给出真实世界实验的具体数值。
- 摘要还称，定量结果确认 VGA 能以高保真度预测 3D 属性，但提供的文本中未包含具体的相机或深度指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12908v1](http://arxiv.org/abs/2604.12908v1)
