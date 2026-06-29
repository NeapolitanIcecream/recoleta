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
## 总结
VEGA 在训练阶段为 OpenVLA-OFT 加入了具备 3D 感知的视觉特征对齐，并在推理时移除额外的教师模型和投影器。

## 问题
- VLA 的视觉编码器主要用 2D 图像数据训练，因此可能缺少精确操作所需的深度、相对位置、物体高度和视角线索。
- 现有的隐式空间 grounding 方法对齐的是 LLM 层级的视觉 token，还需要做层搜索；对齐目标依赖任务，而且会把几何信息和语言上下文混在一起。

## 方法
- 使用冻结的 DINOv2-FiT3D 作为空间教师。FiT3D 是经过多视角一致的 3D Gaussian Splatting 监督微调的 DINOv2。
- 通过 LayerNorm 加两层 MLP 投影器，把 OpenVLA-OFT 的 DINOv2 视觉编码器输出对齐到 DINOv2-FiT3D 的 patch 特征。
- 训练时同时使用标准动作预测损失和余弦特征对齐损失，主实验中 λ = 0.1。
- 在推理时丢弃教师和投影器，因此运行时开销与基础 VLA 相同。

## 结果
- 在 RoboTwin 2.0 上，覆盖 6 个双臂任务，每个任务 100 次试验，VEGA 在 Easy 上的平均成功率为 67.5%，在 Hard 上为 30.7%。
- 与 OFT + Spatial Forcing 相比，VEGA 在 Easy 上高 3.3 个百分点（67.5% 对 64.2%），在 Hard 上高 2.9 个百分点（30.7% 对 27.8%）。
- 与 OpenVLA-OFT 相比，VEGA 将 Easy 的平均成功率从 56.0% 提升到 67.5%，将 Hard 从 22.7% 提升到 30.7%。
- 任务级提升包括 Move Card Away Hard：43% 对 34%（OpenVLA-OFT），Click Bell Hard：53% 对 46%，Place Shoe Hard：25% 对 9%。
- 训练效率方面：在 Move Playingcard Away Easy 上，VEGA 训练到 10k 步时达到的成功率与 OpenVLA-OFT 训练到 60k 步时大致相同。
- 数据效率方面：在 Move Playingcard Away Easy 上只使用 25% 的示范时，VEGA 比 OpenVLA-OFT 高 10 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10485v1](https://arxiv.org/abs/2605.10485v1)
