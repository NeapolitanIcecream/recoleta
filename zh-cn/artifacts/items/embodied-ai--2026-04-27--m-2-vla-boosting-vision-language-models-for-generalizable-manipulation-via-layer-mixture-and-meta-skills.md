---
source: arxiv
url: https://arxiv.org/abs/2604.24182v1
published_at: '2026-04-27T08:44:12'
authors:
- Siyao Xiao
- Yuhong Zhang
- Zhifang Liu
- Zihan Gao
- Jingye Zhang
- Sinwai Choo
- Dake Zhong
- Mengzhe Wang
- Xiao Lin
- Xianfeng Zhou
- Jia Jia
- Haoqian Wang
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-manipulation
- parameter-efficient-adaptation
- robot-generalization
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# $M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills

## Summary
## 摘要
$M^2$-VLA 用层选择模块和基于记忆的元技能模块，把一个冻结的视觉语言模型适配到机器人操作任务。论文报告称，该模型使用 0.3B 参数，在 LIBERO 上的成功率高于微调基线和冻结 VLM 基线。

## 问题
- 当前 VLA 模型常常微调 VLM 骨干，这可能抹除处理新指令和新物体所需的语言与视觉推理能力。
- 机器人控制需要精细的空间信息和轨迹信息，而 VLM 特征面向高层图像-文本任务。
- 小型动作头容量有限，可能难以从有限的机器人数据中学习大量操作轨迹。

## 方法
- 模型保持 VLM 冻结，并将感知与动作生成分开，使骨干保留原有的视觉语言能力。
- 它用 DINOv2 和 SigLIP 编码全局相机图像和腕部相机图像，加入语言 token 和可学习查询 token，并将它们输入 VLM。
- Mixture of Layers 读取 VLM 各层的隐藏状态，并通过独立的注意力路径筛选查询/本体感受特征、视觉 token 和动作潜变量。
- 动作头通过去噪 transformer 预测动作。
- Meta Skill Module 存储感知特征键和成功的未来动作块，用 L1 距离检索最近的 4 个技能，并通过交叉注意力注入这些技能以细化动作潜变量。

## 结果
- 在同义改写的 LIBERO Spatial 指令上，$M^2$-VLA 达到 66.2% 成功率，性能下降 29.4%；OpenVLA 为 20.0%，下降 64.7%；VLA-Adapter 为 52.8%，下降 45.4%。
- 在 LIBERO 新物体 pick-and-place 测试上，$M^2$-VLA 达到 34.4% 成功率，下降 30.4%；OpenVLA 为 8.2%，下降 80.2%；VLA-Adapter 为 8.0%，下降 91.6%。
- 在 LIBERO 仿真中，$M^2$-VLA 在训练 15,000 步后、每个套件 500 次测试下报告了 97.8% Spatial、99.0% Object、97.2% Goal、87.0% Long，以及 95.3% 平均成功率。
- 表中最好的基线平均值是 VLA-Adapter Frozen，使用 0.5B 参数达到 89.4%；SmolVLA 使用 2.2B 参数报告 88.8%，FlowVLA 使用 7.0B 参数报告 88.1%。
- 论文报告使用 4 块 NVIDIA A800 GPU 训练，并称这种参数高效设计可在一块 RTX 3090 GPU 上用 8 小时完成训练。
- 真实世界设置使用带夹爪的 AgileX PiPer 6-DoF 机械臂、2 个 RGB 相机、每个任务 50 条遥操作示范、5,000 个训练步，以及每个任务 20 次 rollout；提供的摘录在完整的 $M^2$-VLA 真实世界结果表之前被截断。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24182v1](https://arxiv.org/abs/2604.24182v1)
