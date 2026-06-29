---
source: arxiv
url: http://arxiv.org/abs/2604.01618v1
published_at: '2026-04-02T04:55:34'
authors:
- Jiawei Chen
- Simin Huang
- Jiawei Du
- Shuaihang Chen
- Yu Tian
- Mingjie Wei
- Chao Yu
- Zhaoxia Yin
topics:
- vision-language-action
- adversarial-robustness
- robot-manipulation
- 3d-texture-attacks
- sim2real
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models

## Summary
## 摘要
Tex3D 通过在模拟器中的物体表面优化对抗性 3D 纹理来攻击视觉-语言-动作模型。论文称，这是首个面向 VLA 系统的、可直接在端到端方式下优化的物理约束 3D 纹理攻击方法，并在仿真和真实机器人测试中显示出很大的失败率上升。

## 问题
- 用于机器人操作的 VLA 模型会在对抗输入下失效，但以往攻击主要使用文本扰动或 2D 图像补丁。
- 这些攻击面不太适合真实部署：语言攻击依赖指令通道，2D 补丁又依赖视角，而且很显眼。
- 3D 物体纹理对机器人来说是更强的物理攻击面，但标准模拟器，如 MuJoCo，不允许梯度从 VLA 损失回传到物体外观；长时程操作也让单帧攻击不稳定。

## 方法
- Tex3D 通过 **前景-背景解耦（Foreground-Background Decoupling, FBD）** 建立可微分攻击路径：MuJoCo 渲染完整场景背景，Nvdiffrast 渲染带可学习纹理的目标物体，再把两者合成为冻结的 VLA 策略使用的观测。
- FBD 对齐 MuJoCo 和 Nvdiffrast 中的物体位姿、相机矩阵和光照，让插入的物体与模拟器视图一致，同时仍然可以用梯度更新纹理。
- Tex3D 加入 **轨迹感知对抗优化（Trajectory-Aware Adversarial Optimization, TAAO）**，通过给行为上关键的帧更高权重来保持长回合中的攻击效果。关键帧由预训练视觉编码器中的潜在速度和加速度估计得到。
- TAAO 还使用逐顶点颜色参数化，让优化后的纹理更平滑，并减少对少数视角或帧的过拟合。
- 该框架支持无目标攻击，把动作推离干净行为；也支持有目标攻击，把策略推向攻击者指定的行为。它还使用变换期望来增强物理迁移性。

## 结果
- 最强结果是在 Tex3D 下，**任务失败率最高达到 96.7%**。
- 在 **OpenVLA** 上，无攻击时平均失败率为 **24.1%**，在无目标 Tex3D 下升至 **88.1%**，在有目标 Tex3D 下升至 **90.5%**。高斯噪声达到 **31.1%**，在完整 Tex3D 之前最强的消融版本达到无目标 **82.9%**、有目标 **86.6%**。
- 在 **OpenVLA-OFT** 上，无攻击时平均失败率为 **4.7%**，无目标 Tex3D 下升至 **76.0%**，有目标 Tex3D 下升至 **79.3%**。高斯噪声达到 **6.5%**。
- 在 **pi0** 上，无攻击时平均失败率为 **4.6%**，无目标 Tex3D 下升至 **71.8%**，有目标 Tex3D 下升至 **73.3%**。高斯噪声达到 **10.7%**。
- 对于 **OpenVLA 空间任务**，无目标失败率达到 **95.8%**，有目标失败率达到 **96.7%**，而无攻击时为 **15.6%**。
- 摘要说明实验覆盖了仿真和真实机器人环境中的多个操作任务套件，但提供的文本里没有真实机器人的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01618v1](http://arxiv.org/abs/2604.01618v1)
