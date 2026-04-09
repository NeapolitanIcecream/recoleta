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
Tex3D 通过在模拟器内优化物体表面的对抗性 3D 纹理来攻击视觉-语言-动作模型。论文称，这是首个针对 VLA 系统、端到端优化且具备物理可实现性的 3D 纹理攻击方法，并在仿真和真实机器人测试中显示出明显更高的任务失败率。

## 问题
- 用于机器人操作的 VLA 模型会在对抗性输入下失效，但以往攻击主要依赖文本扰动或 2D 图像贴片。
- 这些攻击面不太符合真实部署：语言攻击依赖指令通道，2D 贴片依赖视角且视觉上很显眼。
- 对机器人来说，3D 物体纹理是更强的物理攻击面，但 MuJoCo 等标准模拟器无法让梯度从 VLA 损失回传到物体外观，而长时程操作也会让单帧攻击不稳定。

## 方法
- Tex3D 用 **Foreground-Background Decoupling (FBD)** 构建可微的攻击路径：MuJoCo 渲染完整场景背景，Nvdiffrast 渲染带有可学习纹理的目标物体，再将两者合成为冻结 VLA 策略使用的观测。
- FBD 在 MuJoCo 和 Nvdiffrast 之间对齐物体位姿、相机矩阵和光照，使插入的物体与模拟器视图一致，同时仍允许通过梯度更新纹理。
- Tex3D 还加入 **Trajectory-Aware Adversarial Optimization (TAAO)**，通过对行为上关键的帧赋予更高权重，使攻击在长回合中保持有效；这些关键帧由预训练视觉编码器中的潜在速度和加速度估计得到。
- TAAO 还使用基于每个顶点颜色的参数化，让优化后的纹理更平滑，并减少对少量视角或帧的过拟合。
- 该框架同时支持无目标攻击和有目标攻击：前者让动作偏离干净行为，后者让策略朝攻击者指定的行为偏移；它还使用 expectation over transformations 来增强物理迁移性。

## 结果
- 最强的结论是：在 Tex3D 攻击下，**任务失败率最高达到 96.7%**。
- 在 **OpenVLA** 上，平均失败率从无攻击时的 **24.1%** 上升到 Tex3D 无目标攻击下的 **88.1%**，有目标攻击下为 **90.5%**。高斯噪声可达到 **31.1%**，而完整 Tex3D 之前最强的消融版本在无目标攻击下达到 **82.9%**，有目标攻击下达到 **86.6%**。
- 在 **OpenVLA-OFT** 上，平均失败率从 **4.7%** 上升到 Tex3D 无目标攻击下的 **76.0%**，有目标攻击下的 **79.3%**。高斯噪声达到 **6.5%**。
- 在 **pi0** 上，平均失败率从 **4.6%** 上升到 Tex3D 无目标攻击下的 **71.8%**，有目标攻击下的 **73.3%**。高斯噪声达到 **10.7%**。
- 对于 **OpenVLA 空间任务**，失败率在无目标攻击下达到 **95.8%**，在有目标攻击下达到 **96.7%**，而无攻击时为 **15.6%**。
- 摘要称实验覆盖了仿真和真实机器人环境中的多组操作任务，但提供的文本没有给出真实机器人的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01618v1](http://arxiv.org/abs/2604.01618v1)
