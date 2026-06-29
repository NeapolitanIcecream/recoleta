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
$M^2$-VLA 用一个层选择模块和一个基于记忆的 meta-skill 模块，把冻结的视觉语言模型用于机器人操作。论文报告，它在 LIBERO 上的成功率高于微调版和冻结 VLM 基线，同时只用 0.3B 参数。

## 问题
- 现有 VLA 模型常常微调 VLM 主干，这会抹掉新指令和新物体所需的语言与视觉推理能力。
- 机器人控制需要精细的空间信息和轨迹信息，而 VLM 特征主要为高层图文任务设计。
- 体量较小的动作头在有限机器人数据上学习多种操作轨迹时，容量可能不够。

## 方法
- 模型保持 VLM 冻结，并把感知和动作生成分开，这样主干可以保留原有的视觉语言能力。
- 它用 DINOv2 和 SigLIP 编码全局相机和腕部相机图像，加入语言 token 和可学习的 query token，再送入 VLM。
- Mixture of Layers 从 VLM 各层读取隐藏状态，并通过独立注意力路径筛选 query/proprioception 特征、视觉 token 和动作潜变量。
- 动作头通过去噪 transformer 预测动作。
- Meta Skill Module 保存感知特征键值和成功的未来动作片段，用 L1 距离检索最近的 4 个 skill，再通过交叉注意力注入这些信息，细化动作潜变量。

## 结果
- 在同义改写后的 LIBERO Spatial 指令上，$M^2$-VLA 的成功率为 66.2%，性能下降 29.4%；OpenVLA 为 20.0% 和 64.7%，VLA-Adapter 为 52.8% 和 45.4%。
- 在 LIBERO 的新物体取放测试上，$M^2$-VLA 的成功率为 34.4%，下降 30.4%；OpenVLA 为 8.2% 和 80.2%，VLA-Adapter 为 8.0% 和 91.6%。
- 在 LIBERO 仿真中，$M^2$-VLA 在每个套件训练 15,000 步后，500 次测试的成功率分别为：Spatial 97.8%、Object 99.0%、Goal 97.2%、Long 87.0%，平均 95.3%。
- 列出的最佳基线平均值是 VLA-Adapter Frozen，89.4%，参数量 0.5B；SmolVLA 为 88.8%，参数量 2.2B；FlowVLA 为 88.1%，参数量 7.0B。
- 论文报告使用 4 张 NVIDIA A800 GPU 训练，并称这种参数高效设计可以在 1 张 RTX 3090 GPU 上用 8 小时完成训练。
- 真实世界设置使用带夹爪的 AgileX PiPer 6 自由度机械臂、2 个 RGB 相机、每个任务 50 条遥操作示范、5,000 个训练步和每个任务 20 次 rollout；给出的摘录在完整的 $M^2$-VLA 真实世界结果表之前截断。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24182v1](https://arxiv.org/abs/2604.24182v1)
