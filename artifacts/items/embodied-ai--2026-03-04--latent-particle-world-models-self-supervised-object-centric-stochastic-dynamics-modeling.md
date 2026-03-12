---
source: arxiv
url: http://arxiv.org/abs/2603.04553v1
published_at: '2026-03-04T19:36:08'
authors:
- Tal Daniel
- Carl Qi
- Dan Haramati
- Amir Zadeh
- Chuan Li
- Aviv Tamar
- Deepak Pathak
- David Held
topics:
- object-centric-world-model
- latent-particles
- self-supervised-video-modeling
- stochastic-dynamics
- latent-actions
relevance_score: 0.75
run_id: materialize-outputs
---

# Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling

## Summary
LPWM提出了一种自监督、以对象为中心的世界模型，直接从视频中发现关键点、边界框和掩码，并在潜空间中预测多对象随机动态。它强调端到端训练、可扩展到真实多对象场景，并可被动作、语言或目标图像条件控制。

## Problem
- 现有高保真视频生成/世界模型通常计算昂贵、推理慢，不利于决策与机器人等应用。
- 常见patch级表示缺少显式语义对象分解，难以自然建模多对象交互，也不容易和语言对齐。
- 先前对象中心视频预测方法多局限于简单或模拟环境，且常依赖显式跟踪、两阶段训练或全局潜动作，难扩展到复杂真实世界随机动态。

## Approach
- 使用DLP风格的**latent particles**表示每帧：每个粒子显式编码位置、尺度、深度、透明度和外观特征，外加一个背景粒子，从而在无标注视频中自发现对象结构。
- 提出新的**Context模块**：一个因果时空Transformer，为**每个粒子**学习潜动作，而不是给整帧一个全局潜动作；它包含逆动力学头和潜策略头，前者从相邻帧推断潜动作，后者给出基于当前状态的潜动作先验分布。
- 用潜策略分布去正则化逆动力学分布，并在推理时直接从该先验采样，因此模型可以生成**随机、多峰**的未来轨迹，而不仅是确定性预测。
- 动力学模块同样是因果时空Transformer，通过AdaLN把每个粒子的潜动作注入到状态转移中，预测下一时刻粒子，再由解码器渲染回图像。
- 整个系统作为时序VAE**端到端**仅用视频训练，同时支持动作、语言、目标图像和多视角条件，把全局条件映射成每粒子的局部潜动作。

## Results
- 论文声称LPWM在**多种真实世界和合成多对象数据集**上达到**object-centric video prediction的SOTA**，并且可用于决策任务，如**goal-conditioned imitation learning**。
- 文中明确声称它是**首个**“仅从视频训练、支持多视角训练、并同时支持动作/语言/目标图像等多种条件”的自监督对象中心模型。
- 相比DDLP，LPWM去除了**显式粒子跟踪**要求，允许**所有帧并行编码**，并引入每粒子连续潜动作以处理遮挡、出现/消失、随机运动等随机转移。
- 提供的摘录**没有给出具体定量数字**（如PSNR/SSIM/FVD、数据集名上的提升百分比、模仿学习成功率等），因此无法报告精确指标、基线差值或统计显著性。
- 最强的具体结论是：LPWM既能做**随机视频建模**，也能做**目标条件模仿学习**，并支持**语言条件视频生成**和**潜动作条件视频预测**等多种控制形式。

## Link
- [http://arxiv.org/abs/2603.04553v1](http://arxiv.org/abs/2603.04553v1)
