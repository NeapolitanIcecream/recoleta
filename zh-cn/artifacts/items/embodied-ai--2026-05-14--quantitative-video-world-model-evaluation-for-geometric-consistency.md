---
source: arxiv
url: https://arxiv.org/abs/2605.15185v1
published_at: '2026-05-14T17:59:04'
authors:
- Jiaxin Wu
- Yihao Pi
- Yinling Zhang
- Yuheng Li
- Xueyan Zou
topics:
- video-world-models
- geometric-consistency
- benchmarking
- 3d-reconstruction
- physical-evaluation
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# Quantitative Video World Model Evaluation for Geometric-Consistency

## Summary
## 摘要
PDI-Bench 为生成视频提供了一个衡量三维几何一致性的数值测试。它结合分割、单目三维重建和点跟踪，对尺度-深度对齐、三维运动和物体刚性进行评分。

## 问题
- 论文处理的是视频世界模型评估中的一个缺口：画面看起来可信的片段，仍然可能在三维几何上出错，比如尺度漂移、滑移、物体变形或透视关系断裂。
- 常见指标如 FVD 和基于 CLIP 的评分主要衡量视觉分布或语义匹配，因此可能漏掉物理几何错误。
- 这个问题重要，因为视频生成器正在被当作隐式世界模型来使用，而世界模型应当随时间保持基本的投影几何和物体结构。

## 方法
- 该方法定义了 Perspective Distortion Index（PDI），这是一个对三个残差加权的分数：尺度-深度对齐、三维轨迹一致性和结构刚性。
- 它先用 Florence-2 和 SAM 2 分离目标物体，再随时间测量物体掩码和像素高度。
- 它用 MegaSaM 重建深度、相机位姿和世界空间点图，这样就能在三维中而不是屏幕坐标中测量物体运动。
- 它用 CoTracker3 跟踪物体锚点，把这些二维轨迹提升到三维坐标，并检查两两距离是否保持稳定。
- 最终的 PDI 权重为：尺度 0.4、轨迹 0.4、刚性 0.2；PDI 越低，几何一致性越好。

## 结果
- 该基准包含 28 个文本提示下的 183 个视频：15 个真实 ground-truth 视频和 168 个来自 6 个模型的生成视频，覆盖 5 种场景。
- ground truth 的表现最好，PDI 为 0.1206，尺度残差 0.0660，轨迹残差 0.1764，刚性残差 0.1182，离群率 0.0%，MathPass 为 86.7%。
- Seedance 2.0 是整体表现最好的生成模型，PDI 为 0.2422，离群率 0.0%，MathPass 为 89.3%；CogVideoX-3 紧随其后，PDI 为 0.2480，并且在生成模型中轨迹和刚性分数最好，分别为 0.2033 和 0.2065。
- Veo 3.1、Wan 2.2、Sora 和 HunyuanVideo 的总体得分更差，PDI 分别为 0.4521、0.5595、0.8255 和 0.8825。
- Sora 和 HunyuanVideo 的尺度误差很大：尺度残差分别为 1.6753 和 1.8469，是 ground truth 尺度残差 0.0660 的 25 倍以上，两者的离群率都是 14.3%。
- 场景结果显示了具体失败案例：Sora 在曲线运动场景上的 PDI 达到 2.1277，尺度误差为 4.8660；HunyuanVideo 在部分遮挡场景上的 PDI 达到 2.4104，尺度误差为 5.3793。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15185v1](https://arxiv.org/abs/2605.15185v1)
