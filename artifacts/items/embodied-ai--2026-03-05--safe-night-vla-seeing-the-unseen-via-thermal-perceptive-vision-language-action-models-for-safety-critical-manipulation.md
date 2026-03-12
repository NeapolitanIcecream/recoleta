---
source: arxiv
url: http://arxiv.org/abs/2603.05754v1
published_at: '2026-03-05T23:26:44'
authors:
- Dian Yu
- Qingchuan Zhou
- Bingkun Huang
- Majid Khadiv
- Zewen Yang
topics:
- vision-language-action
- thermal-perception
- safe-robotics
- multimodal-manipulation
- control-barrier-functions
relevance_score: 0.93
run_id: materialize-outputs
---

# Safe-Night VLA: Seeing the Unseen via Thermal-Perceptive Vision-Language-Action Models for Safety-Critical Manipulation

## Summary
本文提出 Safe-Night VLA，把热红外感知接入预训练视觉-语言-动作模型，并在执行时加入控制屏障函数安全过滤器，用于安全关键的操作任务。它的核心价值是在弱光、遮挡、镜像欺骗和分布外场景下，让机器人利用“看不见”的热信息进行更稳健且受约束的操控。

## Problem
- 现有 VLA 主要依赖 RGB，无法直接感知温度、埋藏目标等**不可见物理状态**，因此在热相关或遮挡任务中容易失败。
- 端到端生成式策略缺少**运行时安全约束**，在 OOD 场景、障碍物或工作空间边界附近可能输出危险动作。
- 这很重要，因为真实机器人部署常处于**弱光、非结构化、存在光学假象和未知干扰**的环境，既要看懂任务，也要避免碰撞。

## Approach
- 基于 **GR00T-N1.5-3B** 搭建框架，把 **RGB、LWIR thermal、depth** 三种视角作为独立图像 token 输入冻结的视觉-语言主干；热图和深度图都转成 3 通道伪彩色，从而复用 RGB 预训练编码器。
- 采用**参数高效适配**：冻结视觉编码器和语言模型，只训练动作头（VLM projector + 16-layer DiT），让模型在保留原有语义能力的同时学会热感知操控。
- 用**非对称数据增强**削弱对 RGB 的依赖：训练时仅对 RGB 加强亮度、颜色抖动、噪声和裁剪扰动，鼓励策略更多依赖热和深度等更稳健模态。
- 在执行层把高层动作意图与低层安全解耦：VLA 先输出 6DoF 末端位姿增量和夹爪命令，再由 **CBF-QP 安全过滤器**在关节空间求解最接近期望、但满足碰撞约束和关节限位的安全动作。
- 通过三个物理评测场景验证：**温度条件操作**、**埋藏热目标定位**、**镜像反射消歧**，同时测试正常光照与 dim/night 条件，以及是否启用安全过滤器。

## Results
- 数据与设置：作者在 **Franka Panda** 上采集 **600** 条示教，每条约 **200** 个 state-action 对；训练 **5,000 steps**；比较 **RGB-Only / RGB-D / RGB-T / Ours(RGB-T-D)** 四个独立训练模型。
- **温度条件操作（50 次试验）**：正常光、无安全过滤时，RGB-Only **32%**，RGB-D **24%**，RGB-T **78%**，Ours **72%**；正常光、有过滤时，RGB-T **86%**、Ours **82%**。在 **dim/night + safety** 下，Ours 达 **64%**，优于 RGB-T **22%**、RGB-D **12%**、RGB-Only **0%**。
- **埋藏热目标定位（50 次试验）**：正常光、有过滤时，Ours **78%**，高于 RGB-T **66%**、RGB-D **24%**、RGB-Only **16%**；在 **dim/night + safety** 下，Ours **72%**，高于 RGB-T **48%**，而 RGB-D 与 RGB-Only 几乎失效（**2%** / **0%**）。
- **镜像反射消歧（每子任务 20 次）**：在正常光、有过滤时，Mirror Rejection Success 分别为 RGB-Only **12/20**、RGB-D **11/20**、RGB-T **19/20**、Ours **15/20**；在 **dim/night + safety** 下，Ours 达 **17/20**，高于 RGB-T **15/20**、RGB-Only **13/20**、RGB-D **11/20**。
- **单箱体子任务**在 **dim/night + safety** 下，Ours 为 **18/20**，略高于 RGB-T **17/20**，明显高于 RGB-Only / RGB-D 的 **9/20 / 9/20**，说明深度在弱光下提供了额外几何稳定性。
- 总体主张：热模态对“热/冷区分”和“埋藏目标定位”是关键，CBF 安全过滤器能进一步减少执行级失败；作者据此声称 foundation model 可以有效利用**非可见物理模态**完成更稳健的安全关键操控。

## Link
- [http://arxiv.org/abs/2603.05754v1](http://arxiv.org/abs/2603.05754v1)
