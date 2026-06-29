---
source: arxiv
url: https://arxiv.org/abs/2605.19600v1
published_at: '2026-05-19T09:41:04'
authors:
- Jinhan Li
- Xijie Huang
- Zhaoqi Wang
- Yijin Wang
- Weiqi Ge
- Qiyi He
- Mo Zhu
- Fei Gao
- Yuze Wu
- Xin Zhou
topics:
- aerial-vln
- uav-data-generation
- generative-world-model
- 3d-gaussian-splatting
- robot-data-scaling
- sim2real
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model

## Summary
## 总结
FlyMirage 通过结合 LLM 的场景设计、Marble 世界生成、自动 3DGS 标注和 UAV 轨迹规划来生成空中视觉-语言导航数据。论文声称它生成了一个包含 500 个场景、5 万条轨迹的数据集，数据带有 6-DoF、满足动力学约束的飞行数据。

## 问题
- 空中 VLN 数据很难扩展，因为真实 UAV 飞行需要熟练操作员，而许多仿真数据集仍依赖人工扫描或手工搭建场景。
- 现有的仿真 UAV 数据集常用有限资产或预先搭建的场景，很多还使用忽略 UAV 动力学的规划器。
- 更好的数据很重要，因为空中导航模型需要多样场景、目标指代，以及符合 UAV 运动限制的飞行路径。

## 方法
- 系统先从分类体系中采样场景类型，再让 GPT-5.4 或 Gemini 3.1 生成详细的场景描述，接着用 GPT Images 2.0 生成匹配图片，并把文本-图像对交给 Marble 1.1 Plus 生成 3D Gaussian Splatting 场景。
- 它用 GSplat 渲染 RGB 和深度视图，然后用 Boxer 做开放词汇目标检测和 3D 边界框标注。
- 它在场景中心和远处目标附近做迭代式相机探索，然后用距离剪枝重新运行 Boxer，以减少远距离的差框。
- 它根据可见性、安全性和 2.0 m 到 10.0 m 的行程距离检查，从语义框中选择导航目标。
- 它运行 EGO-Planner 生成满足动力学约束的 UAV 轨迹，渲染 RGB/深度观测，并用 Qwen-3.5-Flash 过滤质量差的轨迹并生成提示词变体。

## 结果
- FlyMirage 包含 500 个生成的 3DGS 场景，覆盖 6 类：交通、工作场所、商业空间、工业设施、休闲场所和住宅空间。
- 该数据集包含约 50,000 条导航轨迹，使用 6-DoF 动作空间和运动学约束。表 I 将它与 OpenFly 对比，后者有 100K 条轨迹、18 个场景、4-DoF 动作空间、A* 规划，而且没有运动学约束。
- 论文声称，FlyMirage 是对比表中第一个能生成真实 6-DoF 轨迹的自动空中轨迹生成流水线；先前的 6-DoF 数据集，如 UAV-Flow，使用的是人工控制。
- 生成的场景包含 5,000 多个唯一目标标签，单个场景通常有 60 到 100 个目标实例。论文把这点与 InteriorGS 对比，后者大约有 700 个唯一目标类别。
- 平均轨迹长度为 4.33 m，中位长度为 4.06 m。连续运行最多可以串联 5 个导航任务，用于约 20 m 的长时程任务。
- 论文报告的生成成本约为每个场景 2 美元，每个场景约 1 小时，渲染在消费级 NVIDIA RTX 4070 GPU 上完成。论文把这点与 Matterport Pro2 扫描硬件约 3,000 美元，以及 UAV-Flow 每小时约 100 美元的人工飞行成本进行对比。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19600v1](https://arxiv.org/abs/2605.19600v1)
