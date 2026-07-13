---
source: arxiv
url: https://arxiv.org/abs/2607.08751v1
published_at: '2026-07-09T17:50:47'
authors:
- Yunchao Yao
- Zhuxiu Xu
- Tianqi Zhang
- Zixian Liu
- Sikai Li
- Zhenyu Wei
- Feng Chen
- Dihong Huang
- Kechang Wan
- Chenyang Ma
- Shuqi Zhao
- Shenghua Gao
- Masayoshi Tomizuka
- Yi Ma
- Mingyu Ding
topics:
- dexterous-manipulation
- robot-benchmark
- multi-embodiment
- robot-policy-evaluation
- vision-language-action
- teleoperation-data
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation

## Summary
## 摘要
DexVerse 是一个模块化仿真基准，用于测试灵巧机器人策略在 100 项任务、3 条机器人手臂、6 种灵巧手、多种视觉条件和多类观测数据上的表现。它提供 3,180 条 VR 遥操作演示数据，结果显示，当前策略在接触密集、精密操作、工具使用和长时程任务上的成功率仍然有限。

## 问题
- 现有操作基准覆盖的灵巧技能、机器人本体、视觉条件或演示数据较少，难以对通用机器人策略进行受控评估。
- 灵巧操作需要高自由度手部控制、接触调节、物体可供性推理、双手协调和长时程执行能力。
- 统一基准有助于比较不同机器人本体、传感器输入、视觉变化和交互类型下的策略表现，因为这些条件会显著改变结果。

## 方法
- DexVerse 将 100 项任务划分为 8 类：基础操作、功能操作、铰接物体操作、非抓取操作、接触密集操作、双手操作、多目标操作和长时程操作。
- 其配置驱动的仿真器将任务逻辑与机器人本体分离，支持 3 条手臂，包括 Franka Research 3、UR10e 和 xArm 7，以及 6 种灵巧手。
- 该基准支持对纹理、光照、背景、相机视角、物体位姿和动力学进行可控调整。
- VR 遥操作系统使用 Apple Vision Pro、逆运动学和基于优化的手部重定向，采集同步的本体感觉、RGB、深度、点云和状态演示数据。
- 作者在覆盖 19 项任务的同一组 950 条回合子集上训练并比较 Diffusion Policy、3D Diffusion Policy、OpenVLA 和 pi0.5。

## 结果
- 在 19 项任务上，3D Diffusion Policy 和 pi0.5 的平均在线成功率并列最高，均为 0.34；Diffusion Policy 为 0.32，OpenVLA 为 0.19。
- 各方法没有在所有任务中保持领先：Diffusion Policy 在 Pick-and-Lift 上以 0.51 领先，3D Diffusion Policy 在 Tool Use 上以 0.35 领先，pi0.5 在 Articulated Manipulation 和 Precision Contact 上分别以 0.35 和 0.29 领先。
- Web 规模的 VLA 预训练没有带来高于最佳从零训练扩散策略的总体优势：pi0.5 得分为 0.34，与 3D Diffusion Policy 持平；OpenVLA 得分为 0.19。
- 四种策略在 PushT 上的成功率均为 0.00；InsertPen、SlideUtilityKnife 和 OpenLaptop 的成功率也接近于零，暴露出力调节和亚厘米级对齐方面的失败。
- DexVerse 提供 100 项任务、3 条手臂、6 种灵巧手、3,180 条演示数据和可配置的多模态观测数据，覆盖范围大于论文中比较的基准套件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08751v1](https://arxiv.org/abs/2607.08751v1)
