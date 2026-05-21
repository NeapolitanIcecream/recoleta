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
PDI-Bench 为生成视频提供一项 3D 几何一致性的数值测试。它使用分割、单目 3D 重建和点跟踪，对尺度-深度对齐、3D 运动和物体刚性进行评分。

## 问题
- 论文处理的是视频世界模型评估中的一个缺口：视觉上可信的片段仍可能通过尺度漂移、滑动、物体形变或透视错误违反 3D 几何。
- FVD 和基于 CLIP 的分数等常用指标主要衡量视觉分布或语义匹配，因此可能漏掉物理几何错误。
- 这个问题很重要，因为视频生成器正被当作隐式世界模型使用，但世界模型应在时间维度上保持基本的投影几何和物体结构。

## 方法
- 该方法定义了透视畸变指数（Perspective Distortion Index，PDI），这是一个基于三类残差的加权分数：尺度-深度对齐、3D 轨迹一致性和结构刚性。
- 它先用 Florence-2 和 SAM 2 分离目标物体，然后测量物体掩码和像素高度随时间的变化。
- 它用 MegaSaM 重建深度、相机位姿和世界空间点图，因此可以在 3D 中测量物体运动，而不是在屏幕坐标中测量。
- 它用 CoTracker3 跟踪物体锚点，将这些 2D 轨迹提升到 3D 坐标，并检查成对距离是否保持稳定。
- 最终 PDI 对尺度、轨迹和刚性分别使用 0.4、0.4 和 0.2 的权重；PDI 越低表示几何一致性越好。

## 结果
- 该基准包含来自 28 个文本提示的 183 个视频：15 个真实基准视频，以及来自 6 个模型、覆盖 5 个场景的 168 个生成视频。
- 真实基准得分最好：PDI 为 0.1206，尺度残差为 0.0660，轨迹残差为 0.1764，刚性残差为 0.1182，离群值为 0.0%，MathPass 为 86.7%。
- Seedance 2.0 是整体最佳生成模型，PDI 为 0.2422，离群值为 0.0%，MathPass 为 89.3%；CogVideoX-3 随后，PDI 为 0.2480，并取得生成模型中最佳的轨迹和刚性分数，分别为 0.2033 和 0.2065。
- Veo 3.1、Wan 2.2、Sora 和 HunyuanVideo 的整体得分更差，PDI 分别为 0.4521、0.5595、0.8255 和 0.8825。
- Sora 和 HunyuanVideo 显示出较大的尺度错误：尺度残差分别为 1.6753 和 1.8469，是真实基准尺度残差 0.0660 的 25 倍以上，二者的离群值均为 14.3%。
- 场景结果显示了具体失败案例：Sora 在曲线运动场景中达到 PDI 2.1277，尺度错误为 4.8660；HunyuanVideo 在部分遮挡场景中达到 PDI 2.4104，尺度错误为 5.3793。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15185v1](https://arxiv.org/abs/2605.15185v1)
