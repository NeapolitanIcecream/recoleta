---
source: arxiv
url: http://arxiv.org/abs/2603.09391v1
published_at: '2026-03-10T09:03:35'
authors:
- Robin Doerfler
- Lonce Wyse
topics:
- neural-audio-synthesis
- physics-informed-modeling
- differentiable-dsp
- engine-sound-synthesis
- karplus-strong
relevance_score: 0.08
run_id: materialize-outputs
---

# Physics-Informed Neural Engine Sound Modeling with Differentiable Pulse-Train Synthesis

## Summary
本文提出一种面向发动机声音合成的物理先验神经架构 PTR，不再只拟合频谱结果，而是直接建模燃烧脉冲列及其在排气系统中的传播。它将可微脉冲生成与可微共振器结合，在提升重建质量的同时给出更可解释的物理参数。

## Problem
- 现有神经发动机音频方法多是拟合**听到的谐波频谱**，而不是建模真正的成因：按点火顺序发生的离散排气压力脉冲。
- 发动机声音同时具有**低基频、强非平稳、快速瞬态、加减速方向相关**等特点，传统 harmonic-plus-noise 或一般音乐音频建模假设不够贴切。
- 这个问题重要，因为更贴近物理机理的模型有望得到**更好的重建、跨工况泛化和参数可解释性**，适合声音合成与交互式引擎音频应用。

## Approach
- 提出 **Pulse-Train-Resonator (PTR)**：输入 RPM、扭矩及其一阶/二阶差分，经神经网络解码为脉冲与噪声参数，再在时域直接合成音频。
- 用**与点火周期对齐的脉冲列**表示每个气缸的排气事件，并加入物理启发的脉冲形状：谐波衰减、压力释放包络、热力学相位调制、每缸增益与时序偏移。
- 用基于扭矩符号的**节气门/减速断油(DFCO)门控**控制不同噪声源，使推进和减速两种工况下的噪声行为更符合物理规律。
- 用**可微 Karplus-Strong 共振器**模拟排气管路声学；作者把递归延迟反馈重写成适于梯度优化的 all-pole 形式，并用 Gumbel-Softmax 学习离散延迟长度。
- 训练时结合**多分辨率 STFT loss**与沿发动机阶次轨迹计算的**harmonic loss**，鼓励既匹配整体频谱，也匹配与 RPM 同步的谐波结构。

## Results
- 在 Procedural Engine Sounds Dataset 的 3 个子集（A/B/C，总计 **7.5 小时**音频）上，PTR 相比相同编码器-解码器的 **HPN baseline**，平均 **总验证损失从 1.006 降到 0.949**，即 **5.7% 降低**。
- 平均 **harmonic loss 从 0.111 降到 0.088**，作者称为 **21% 的谐波重建提升**；平均 **STFT loss 从 1.899 降到 1.807**。
- 分数据集总损失：**A: 0.944 -> 0.872（约 7.6%）**，**B: 0.943 -> 0.907（约 3.8%）**，**C: 1.132 -> 1.069（约 5.6%）**，PTR 在三种发动机类型上都优于基线。
- 在最难的 **Dataset C** 上，harmonic loss **0.166 -> 0.117**，说明直接建模脉冲而非显式谐波，仍能更好恢复谐波结构。
- 训练设置包括 **16 kHz** 音频、**100 epochs**、约 **45,000 steps**；文中称两种模型都在前 **10,000 steps** 内快速收敛，但 PTR 后续保持更优表现。
- 感知层面作者声称 PTR 能生成更真实的 RPM 相关谐波、负载相关噪声、离合/换挡过渡与 DFCO 声学行为；不过这部分主要是定性描述，没有给出主观听评数字。

## Link
- [http://arxiv.org/abs/2603.09391v1](http://arxiv.org/abs/2603.09391v1)
