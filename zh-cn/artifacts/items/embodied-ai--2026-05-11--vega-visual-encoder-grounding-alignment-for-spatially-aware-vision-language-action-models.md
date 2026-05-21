---
source: arxiv
url: https://arxiv.org/abs/2605.10485v1
published_at: '2026-05-11T12:44:26'
authors:
- Hao Wang
- Xiaobao Wei
- Jingyang He
- Chengyu Bai
- Chun-Kai Fan
- Jiajun Cao
- Jintao Chen
- Ying Li
- Shanyu Rong
- Ming Lu
- Xiaozhu Ju
- Jian Tang
- Shanghang Zhang
topics:
- vision-language-action
- spatial-grounding
- robot-manipulation
- feature-alignment
- 3d-visual-representations
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# VEGA: Visual Encoder Grounding Alignment for Spatially-Aware Vision-Language-Action Models

## Summary
## 摘要
VEGA 在训练期间加入具备 3D 感知能力的视觉特征对齐，从而改进 OpenVLA-OFT；推理时移除额外的教师模型和投影器。

## 问题
- VLA 视觉编码器主要用 2D 图像数据训练，因此可能漏掉精确操作所需的深度、相对位置、物体高度和视角线索。
- 现有隐式空间 grounding 方法对齐 LLM 级视觉 token，并且需要搜索层；对齐目标依赖任务，还会把几何信息和语言上下文混在一起。

## 方法
- 使用冻结的 DINOv2-FiT3D 作为空间教师模型。FiT3D 是用多视角 3D Gaussian Splatting 监督调优过的 DINOv2。
- 通过 LayerNorm 加两层 MLP 投影器，将 OpenVLA-OFT 的 DINOv2 视觉编码器输出对齐到 DINOv2-FiT3D 的 patch 特征。
- 使用标准动作预测损失加余弦特征对齐损失进行训练；主要实验中 λ = 0.1。
- 推理时丢弃教师模型和投影器，因此运行时开销与基础 VLA 相同。

## 结果
- 在 RoboTwin 2.0 上，覆盖 6 个双臂任务且每个任务 100 次试验，VEGA 报告的平均成功率为 Easy 67.5%、Hard 30.7%。
- 相比 OFT + Spatial Forcing，VEGA 在 Easy 上高 3.3 个百分点（67.5% vs 64.2%），在 Hard 上高 2.9 个百分点（30.7% vs 27.8%）。
- 相比 OpenVLA-OFT，VEGA 将 Easy 平均成功率从 56.0% 提高到 67.5%，将 Hard 平均成功率从 22.7% 提高到 30.7%。
- 任务级提升包括：Move Card Away Hard 为 43%，OpenVLA-OFT 为 34%；Click Bell Hard 为 53%，OpenVLA-OFT 为 46%；Place Shoe Hard 为 25%，OpenVLA-OFT 为 9%。
- 训练效率主张：在 Move Playingcard Away Easy 上，VEGA 训练 10k 步达到的成功率约等于 OpenVLA-OFT 训练 60k 步。
- 数据效率主张：在 Move Playingcard Away Easy 上使用 25% 演示数据时，VEGA 比 OpenVLA-OFT 高 10 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10485v1](https://arxiv.org/abs/2605.10485v1)
