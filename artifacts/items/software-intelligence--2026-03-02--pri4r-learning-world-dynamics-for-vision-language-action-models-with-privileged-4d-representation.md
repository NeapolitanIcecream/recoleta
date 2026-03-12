---
source: arxiv
url: http://arxiv.org/abs/2603.01549v2
published_at: '2026-03-02T07:23:53'
authors:
- Jisoo Kim
- Jungbin Cho
- Sanghyeok Chu
- Ananya Bal
- Jinhyung Kim
- Gunhee Lee
- Sihaeng Lee
- Seung Hwan Kim
- Bohyung Han
- Hyunmin Lee
- Laszlo A. Jeni
- Seungryong Kim
topics:
- vision-language-action
- robot-learning
- world-dynamics
- 3d-point-tracking
- privileged-supervision
relevance_score: 0.35
run_id: materialize-outputs
---

# Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation

## Summary
Pri4R让视觉-语言-动作（VLA）模型在训练时额外学习“动作会怎样改变世界”，而不仅是模仿动作本身。它用3D点轨迹作为特权4D监督，提升机器人在复杂操控中的物理感知与控制精度，同时推理阶段不增加任何开销。

## Problem
- 现有VLA主要用动作标签训练，学到的是“怎么动”，但缺少“动了之后世界会怎么变化”的动力学理解。
- 这种缺失会导致语义上看似合理、物理上却不准确的操作，例如忽略门铰链、抽屉约束等，从而造成交互脆弱和任务失败。
- 以语言、图像、特征或目标状态作为辅助监督时，常与真实控制所处的时空度量空间不对齐，且不少方法还会增加推理时延迟与复杂度。

## Approach
- 作者提出Pri4R：在训练阶段给VLA加一个轻量级point track head，预测未来一段时间内场景中3D点的位移/轨迹。
- 核心机制很简单：把VLA内部用于动作预测的表征喂给这个辅助头，让模型同时学“动作”和“未来3D几何如何演化”，从而把世界动力学压进共享表示里。
- 监督信号使用预先构建的3D点轨迹（4D几何：3D随时间变化），并以逐步3D位移作为学习目标；仿真中用真值网格生成，真实场景中用现成3D点跟踪模型生成伪标签。
- 该方法兼容两类主流VLA架构（如OpenVLA-OFT与π系列），训练后直接丢弃辅助头，因此测试时原始VLA架构、输入输出接口和计算量都不变。

## Results
- **LIBERO**：OpenVLA-OFT平均成功率从**92.7%**提升到**96.3%**（+**3.6**）；其中**LIBERO-Long**从**85.5%**提升到**95.3%**，约+**10**个百分点。
- **LIBERO**：π0从**87.4% ± 0.2**提升到**90.6% ± 0.2**；π0.5从**92.6% ± 0.4**提升到**94.0% ± 0.2**。OpenVLA-OFT + Pri4R在四个子集上分别达到**93.2 / 98.6 / 98.1 / 95.3**。
- **RoboCasa**：OpenVLA-OFT平均成功率从**33.1%**提升到**46.3%**，提升**13.2**点，约相对+**40%**；作者摘要中也明确强调了在RoboCasa上的“**+40% gain**”。
- **RoboCasa**：π0从**38.8%**到**42.2%**（+**3.4**），π0.5从**52.9%**到**57.0%**（+**4.1**）。OpenVLA-OFT在多个类别上大幅提升，如Turning levers **36.0→66.7**（+**30.7**）、Pressing buttons **56.0→79.3**（+**23.3**）、Open/Close drawers **59.0→80.0**（+**21.0**）。
- 作者还声称：3D点轨迹比其他辅助监督目标更适合学习动作-世界动力学，并通过系统消融验证了关键设计选择；但在给定摘录中未提供这些消融的完整数值表。

## Link
- [http://arxiv.org/abs/2603.01549v2](http://arxiv.org/abs/2603.01549v2)
