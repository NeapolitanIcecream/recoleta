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
- robot-safety
- control-barrier-functions
- multimodal-robotics
relevance_score: 0.45
run_id: materialize-outputs
language_code: zh-CN
---

# Safe-Night VLA: Seeing the Unseen via Thermal-Perceptive Vision-Language-Action Models for Safety-Critical Manipulation

## Summary
Safe-Night VLA把热红外感知和运行时安全约束接入视觉-语言-动作机器人模型，使机器人能利用RGB看不到的温度信息完成更稳健的操作。它重点解决夜间、遮挡、镜像欺骗和分布外场景下的语义感知与安全执行问题。

## Problem
- 现有VLA主要依赖RGB，无法直接感知温度、埋藏目标等**不可见物理状态**，因此在安全关键操作中容易误判。
- 端到端生成式策略缺少**显式运行时安全保证**，在分布外场景、障碍物或工作空间边界附近可能产生碰撞性动作。
- 这很重要，因为真实机器人部署到非结构化环境时，既要理解像“拿热的瓶子”这样的物理语义，也要避免因幻觉或噪声导致危险执行。

## Approach
- 在预训练GR00T-N1.5-3B/冻结VLM骨干上加入**LWIR热成像、RGB和深度**三模态输入，把热图和深度图转成伪彩色图像，直接送入原视觉编码器。
- 只训练**动作头**（投影层和DiT策略头），不改动冻结的视觉语言骨干，用参数高效方式把热语义对齐到已有基础模型表征中。
- 通过**非对称增强**仅强扰动RGB，迫使策略更多依赖在弱光下更稳定的热/深度线索，而不是脆弱的可见光纹理。
- 在执行时加入**基于控制障碍函数（CBF）的QP安全滤波器**：把VLA给出的末端位姿增量转换成满足碰撞约束和关节限位的安全关节动作，简单说就是“模型提议动作，安全层实时拦截危险部分”。
- 设计三个诊断场景评测该机制：温度条件操控、埋藏热目标定位、镜面反射消歧，并在真实Franka机械臂上验证。

## Results
- **温度条件操控（50次）**：正常光、无安全滤波时，RGB-T最好为**78%**，Safe-Night VLA为**72%**，均显著高于RGB-Only **32%**和RGB-D **24%**；正常光+安全滤波后，RGB-T **86%**、Safe-Night VLA **82%**。
- **温度条件操控（弱光/夜间，50次）**：无安全滤波时，Safe-Night VLA达**56%**，明显优于RGB-Only **0%**、RGB-D **10%**、RGB-T **10%**；加安全滤波后升至**64%**，对比RGB-Only **0%**、RGB-D **12%**、RGB-T **22%**。
- **埋藏热目标定位（50次）**：正常光+安全滤波下，Safe-Night VLA取得**78%**，高于RGB-T **66%**、RGB-D **24%**、RGB-Only **16%**；弱光/夜间+安全滤波下为**72%**，仍高于RGB-T **48%**、RGB-D **2%**、RGB-Only **0%**。
- **镜像/反射消歧（单箱成功，20次）**：弱光/夜间+安全滤波下，Safe-Night VLA为**18/20**，RGB-T **17/20**，RGB-Only与RGB-D均为**9/20**。
- **镜像拒识成功（20次）**：正常光+安全滤波下，RGB-T最高为**19/20**，Safe-Night VLA **15/20**，明显优于RGB-Only **12/20**和RGB-D **11/20**；弱光/夜间+安全滤波下，Safe-Night VLA最高为**17/20**，超过RGB-T **15/20**、RGB-Only **13/20**、RGB-D **11/20**。
- 论文的核心突破主张是：**热感知显著提升语义定位能力，CBF安全层提升执行可靠性，二者结合在弱光和分布外条件下最稳健**；同时证明冻结的RGB预训练基础模型也能有效利用非可见光模态。

## Link
- [http://arxiv.org/abs/2603.05754v1](http://arxiv.org/abs/2603.05754v1)
