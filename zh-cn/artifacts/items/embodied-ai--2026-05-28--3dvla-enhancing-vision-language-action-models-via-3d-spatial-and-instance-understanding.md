---
source: arxiv
url: https://arxiv.org/abs/2605.29416v1
published_at: '2026-05-28T06:07:57'
authors:
- Zhongyu Xia
- Yousen Tang
- Bingqing Wei
- Yongtao Wang
topics:
- vision-language-action
- 3d-scene-understanding
- robot-manipulation
- occlusion-reasoning
- instance-understanding
- spatial-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# 3DVLA: Enhancing Vision-Language-Action Models via 3D Spatial and Instance Understanding

## Summary
## 总结
3DVLA 为预训练的 Vision-Language-Action 模型加入 3D 空间、实例和遮挡推理，用于机器人操作。论文声称，在保持基础 VLA 架构基本不变的前提下，它在 LIBERO-Plus 和 RoboTwin 2.0 上提高了成功率。

## 问题
- 大多数 VLA 使用 2D 视觉 token，因此很难推理度量 3D 位置、6-DoF 关系、物体范围和被遮挡的部分。
- 直接加入 3D 感知模型会破坏与 VLM 预训练的兼容性，而且通常需要昂贵的实例级 3D 标注。
- 这个问题很重要，因为当相机视角变化、物体重叠，或任务相关部分被遮住时，操作策略会失败。

## 方法
- 多视角空间融合利用相机几何、3D 坐标嵌入和 3D RoPE，把多相机 2D 特征提升到共享的 3D 记忆中，得到视角一致的空间特征。
- 面向物体的 3D 实例模块使用 3D probe 估计物体实例，在 3D 中进行匹配，并用冻结感知模型生成的伪框和伪掩码训练，而不是使用人工 3D 标注。
- 坐标驱动的 3D 自监督预测器保留预训练后的 masked-token predictor，并在推理时用它填补被遮挡 3D 位置上的视觉 token。
- 空间条件几何聚合为实例 token 和补全 token 加入相对于末端执行器的 3D 偏移，然后把这些 token 输入下游动作专家。
- 不确定性引导路由在 2D 实例预测不确定时，更频繁地注入补全后的 3D 几何信息。

## 结果
- 在 LIBERO-Plus 上，$\pi_{0.5}$+3DVLA 的平均成功率达到 86.0%，高于 $\pi_{0.5}$ 的 84.2%、OpenVLA-OFT 的 69.6% 和 RIPT-VLA 的 68.4%。
- 在 LIBERO-Plus 的类别分数上，$\pi_{0.5}$+3DVLA 相比 $\pi_{0.5}$ 在相机变化上更好（75.6% 对 71.2%）、光照变化上更好（97.4% 对 94.7%）、背景变化上更好（97.7% 对 94.0%）、噪声上更好（85.3% 对 84.2%）以及布局变化上更好（86.6% 对 84.3%）；在语言扰动上更低（88.6% 对 89.9%）。
- 在 RoboTwin 2.0 上，$\pi_{0}$+3DVLA 将 Easy 成功率从 46.4% 提高到 54.5%，将 Hard 成功率从 16.3% 提高到 23.2%。
- 在 RoboTwin 2.0 上，X-VLA+3DVLA 将 Easy 成功率从 70.0% 提高到 72.6%，将 Hard 成功率从 39.0% 提高到 42.1%。
- RoboTwin 2.0 上的消融实验显示，$\pi_{0}$ 的增益是累加的：仅加入 3D 实例时，Easy 达到 50.1%，Hard 达到 18.9%；再加入预测器后达到 53.4% 和 21.8%；再加入路由后达到 54.5% 和 23.2%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29416v1](https://arxiv.org/abs/2605.29416v1)
