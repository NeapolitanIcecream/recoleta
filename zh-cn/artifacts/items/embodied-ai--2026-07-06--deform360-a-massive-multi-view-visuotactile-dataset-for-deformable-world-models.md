---
source: arxiv
url: https://arxiv.org/abs/2607.05390v1
published_at: '2026-07-06T17:59:18'
authors:
- Hongyu Li
- Wanjia Fu
- Xiaoyan Cong
- Zekun Li
- Binghao Huang
- Hanxiao Jiang
- Xintong He
- Yiqing Liang
- Rao Fu
- Tao Lu
- Srinath Sridhar
- Kevin A. Smith
- George Konidaris
- Yunzhu Li
topics:
- deformable-world-models
- visuotactile-dataset
- robot-data-scaling
- multi-view-3d-tracking
- dexterous-manipulation
- model-predictive-control
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models

## Summary
## 摘要
Deform360 是一个大型真实世界视觉-触觉数据集，用于学习可变形物体世界模型。它为可变形物体操作配套提供 360 度多视角视频、触觉感知、密集 3D 跟踪和机器人交互数据。

## 问题
- 机器人很难预测可变形物体的运动，因为布料、绳子、泡沫和毛绒物体有大量形状状态，接触效应也常被夹爪或自遮挡遮住。
- 现有可变形物体数据集往往是合成的、规模小、物体类型窄，缺少触觉数据，或缺少密集 3D 标注。
- 这个缺口会影响可变形物体操作，因为规划、接触推理，以及 2D 视频方法和 3D 粒子方法之间的模型比较，都需要基于动作条件的未来预测。

## 方法
- 作者使用 41 台同步的 720p、30 FPS 摄像机和两个带触觉传感的 UMI 夹爪，采集了 198 个日常可变形物体，覆盖 1,980 个交互序列。
- 数据集包含 28 个 1D 物体、98 个 2D 物体和 72 个 3D 体积型可变形物体，涵盖 17 个类别中的 13 种操作基元类型。
- 标注流程使用 3D Gaussian Splatting 重建逐帧几何，用 CoTracker3 在每个视角跟踪最多 1,600 个 2D 点，通过渲染深度把这些轨迹提升到 3D，并用 RANSAC 融合多视角结果。
- 跟踪通过表面对齐、局部刚性、速度平滑和触觉接触一致性损失进行细化。简单说，这种方法把多个摄像机视角和触觉读数转换为物体表面上运动的 3D 粒子。
- 该数据集用于接触预测、2D 视频模型基准测试、3D 粒子模型基准测试，以及早期的基于 MPC 的机器人规划测试。

## 结果
- 数据集规模：198 个物体、1,980 个序列、41 个摄像机视角、74,850 段原始视频、约 2,330 万帧、累计 215.7 小时多视角数据，平均每个片段 10.34 秒。
- 与表中列出的真实世界可变形物体数据集相比，Deform360 的物体数量最多：198 个物体；HCOS 为 27 个，DOT 为 22 个，PokeFlex 为 18 个，Robo360 为 17 个，PhysTwin 为 11 个。
- 在留出视角上的重建质量达到全局平均 27.66 PSNR、0.96 SSIM 和 0.0708 LPIPS。最佳类别 PSNR 是 3D 体积型可变形物体的 30.00 dB。
- 视觉-触觉跟踪的 Chamfer 距离误差为 2.71×10^-5 m^2；仅视觉跟踪为 1.41×10^-4 m^2，误差约降低 5 倍。
- 视觉到接触预测在 36 个经过同步筛选的视角上达到 88.67% 的平均准确率；随机猜测为 50.31%，F1 分数为 0.8909。
- 摘录报告了一项定性基准发现：3D 粒子模型由于具有物理结构，在低数据设置中表现更好；2D 视频模型在使用更多数据训练时泛化更好。摘录没有包含最终的世界模型基准数值表，也没有包含机器人规划成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05390v1](https://arxiv.org/abs/2607.05390v1)
