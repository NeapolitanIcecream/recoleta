---
source: arxiv
url: http://arxiv.org/abs/2603.09391v1
published_at: '2026-03-10T09:03:35'
authors:
- Robin Doerfler
- Lonce Wyse
topics:
- neural-audio-synthesis
- physics-informed-learning
- differentiable-dsp
- engine-sound-modeling
- karplus-strong
relevance_score: 0.14
run_id: materialize-outputs
language_code: zh-CN
---

# Physics-Informed Neural Engine Sound Modeling with Differentiable Pulse-Train Synthesis

## Summary
这篇论文提出 PTR（Pulse-Train-Resonator）模型，用可微分、物理先验驱动的方式直接合成发动机声的“脉冲成因”而不是只拟合频谱结果。相较 harmonic-plus-noise 基线，它在 3 个发动机数据子集上取得更好的重建质量，同时提供可解释的物理参数。

## Problem
- 现有神经发动机声音合成方法大多拟合**听到的频谱**，而不是建模声音真正的物理来源：按点火顺序发生的离散排气压力脉冲。
- 发动机声具有低基频、强非平稳、毫秒级瞬态和加减速方向相关等特性，传统谐波/噪声建模难以同时处理定时精度与音色演化。
- 这很重要，因为更符合物理机理的模型不仅可能提升重建质量，还能产出与机械现象对应的可解释控制参数，利于合成与分析。

## Approach
- 提出端到端可微的 **PTR** 架构：输入 RPM、扭矩及其一二阶差分，先解码出脉冲与噪声参数，再在音频率上合成波形。
- 用**参数化脉冲列**代替直接谐波建模：每个气缸按点火节奏生成双极性压力脉冲，并加入谐波衰减、阀门/压力释放包络、热力学相位调制等物理先验。
- 用显式门控建模工况：正扭矩时激活节气门相关燃烧噪声，负扭矩时激活减速断油（DFCO）下的气流噪声，而不是完全依赖网络隐式学习。
- 将多缸脉冲送入**可微 Karplus-Strong 共振器**模拟排气系统；通过把递归反馈改写为可优化的 all-pole 形式，并用 Gumbel-Softmax 学习离散延迟，实现梯度训练。
- 训练时结合多分辨率 STFT 损失与基于发动机阶次谐波轨迹的 harmonic loss，约束频谱整体与转速同步谐波结构。

## Results
- 在 Procedural Engine Sounds Dataset 的 3 个子集（A/B/C）上验证，总时长约 **7.5 小时**，每个子集约 **2.5 小时**，90/10 训练验证划分。
- 相比结构相同的 **HPN baseline**，PTR 的平均 **harmonic loss** 从 **0.111** 降到 **0.088**，论文称为 **21% improvement in harmonic reconstruction**。
- 平均 **STFT loss** 从 **1.899** 降到 **1.807**；平均 **total loss** 从 **1.006** 降到 **0.949**，即 **5.7%** 降低。
- 分数据集总损失：A 从 **0.944 → 0.872**（约 **7.6%** 改善），B 从 **0.943 → 0.907**（约 **3.8%**），C 从 **1.132 → 1.069**（约 **5.6%**）。
- 论文还声称模型能产生更真实的感知行为，如随 RPM 变化的谐波结构、换挡/离合导致的过渡、节气门与 DFCO 的不同噪声形态，但这部分主要是定性描述，没有给出主观听感评分数字。
- 额外声称即使架构带有 V8 点火顺序先验，仍能泛化到数据集 A 的直列四缸特性，显示一定鲁棒性。

## Link
- [http://arxiv.org/abs/2603.09391v1](http://arxiv.org/abs/2603.09391v1)
