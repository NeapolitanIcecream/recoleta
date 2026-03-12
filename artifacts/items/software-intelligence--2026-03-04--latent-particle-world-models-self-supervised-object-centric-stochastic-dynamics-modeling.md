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
- world-models
- object-centric-learning
- video-prediction
- latent-actions
- self-supervised-learning
relevance_score: 0.18
run_id: materialize-outputs
---

# Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling

## Summary
LPWM提出了一种自监督、以对象为中心的世界模型，直接从视频中发现关键点、边界框和掩码，并在潜空间中建模多对象随机动力学。它强调比整帧/patch式视频模型更高效、更可解释，并可被动作、语言和目标图像条件控制。

## Problem
- 现有高保真视频生成/世界模型通常计算代价高、推理慢，难以直接用于决策与规划。
- 许多视频预测方法使用整帧patch表示，缺少显式对象分解，较难捕捉多对象交互，也不易与语言语义对齐。
- 先前对象中心方法常依赖监督、两阶段训练、显式粒子跟踪，或仅适用于简单/模拟场景，难扩展到真实世界复杂多对象视频。

## Approach
- 论文提出**Latent Particle World Model (LPWM)**：把每帧编码为一组前景“粒子”加一个背景粒子，每个粒子显式表示位置、尺度、深度、透明度和外观特征，并端到端训练为VAE式世界模型。
- 核心创新是**per-particle latent action**机制：不是用一个全局隐动作解释整帧变化，而是给每个粒子分配一个连续隐动作，用来描述该对象/局部区域的随机转移。
- 引入**Context模块**（因果时空Transformer），同时学习两个头：逆动力学头从相邻帧推断隐动作；策略头根据当前状态预测隐动作分布，并用KL把前者正则到后者上。训练时用逆动力学隐动作，推理时可从策略分布采样，从而生成随机rollout。
- **Dynamics模块**也是因果时空Transformer，用粒子状态和对应隐动作预测下一时刻粒子分布；同时取消了DDLP中的显式粒子跟踪，使所有帧可并行编码，提升可扩展性。
- 模型支持多种条件输入：外部动作、语言、目标图像和多视角输入；作者还声称该Context模块也可迁移到非对象中心的patch表示架构上。

## Results
- 摘要与引言中声称：LPWM在“diverse real-world and synthetic datasets”上实现了**object-centric video prediction的state-of-the-art**，但给定摘录**未提供具体数据集名、指标数值或基线差值**。
- 论文明确宣称LPWM是首个同时具备以下组合能力的自监督对象中心模型：**仅用视频训练、支持多视角训练、支持动作/语言/图像等多种条件、端到端训练**；这一点在相关工作表格中与SCALOR、SlotFormer、DDLP、PlaySlot等方法作了定性对比。
- 作者进一步声称模型可用于决策，特别是**goal-conditioned imitation learning**，并在**两个复杂多对象环境**中展示有效性；但摘录中**没有给出模仿学习成功率、回报或与基线比较的具体数字**。
- 最强的具体技术性主张包括：去除了显式粒子跟踪、支持并行编码全部帧、可在推理时从隐策略中采样每粒子隐动作以建模多模态随机动态（如遮挡、出现、随机移动）。

## Link
- [http://arxiv.org/abs/2603.04553v1](http://arxiv.org/abs/2603.04553v1)
