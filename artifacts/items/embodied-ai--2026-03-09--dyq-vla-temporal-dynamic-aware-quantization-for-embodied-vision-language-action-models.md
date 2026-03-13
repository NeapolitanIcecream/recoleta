---
source: arxiv
url: http://arxiv.org/abs/2603.07904v1
published_at: '2026-03-09T02:52:57'
authors:
- Zihao Zheng
- Hangyu Cao
- Sicheng Tian
- Jiayu Chen
- Maoliang Li
- Xinhao Sun
- Hailong Zou
- Zhaobo Zhang
- Xuanzhe Liu
- Donggang Cao
- Hong Mei
- Xiang Chen
topics:
- vision-language-action
- dynamic-quantization
- edge-inference
- embodied-ai
- robot-deployment
relevance_score: 0.94
run_id: materialize-outputs
---

# DyQ-VLA: Temporal-Dynamic-Aware Quantization for Embodied Vision-Language-Action Models

## Summary
本文提出 DyQ-VLA，一种面向具身视觉-语言-动作模型的时序动态感知量化框架，根据机器人当前运动阶段动态切换激活比特宽度。它试图在几乎不损失控制性能的前提下，显著降低内存占用并加速仿真与真实机器人推理。

## Problem
- VLA 模型虽然强大，但推理开销高，难以在边缘设备上实时部署，这直接限制了具身智能系统的实用性。
- 现有静态量化对整个任务使用固定精度，忽略了机器人执行过程中“粗运动”和“精细操作”对误差容忍度的巨大差异，因此要么浪费算力，要么在关键阶段失效。
- 更难的是，系统缺少一种足够轻量、可实时计算的“敏感度代理”，来决定当前时刻应该用多少比特最合适。

## Approach
- 核心思路很简单：机器人在“动作粗放、误差不敏感”时用更低比特加速；在“动作精细、误差敏感”时切回更高比特甚至 BF16，以减少关键操作失败。
- 方法分成两部分：一是 sensitivity-aware switching，用实时运动学信号决定何时切换精度；二是 kinematic-guided bit allocation，用这些信号决定当前该分配 2/4/8/16 bit 中的哪一种。
- 作者发现 VLA 量化敏感度具有明显时间动态性，并用两类运动学代理来跟踪它：Motion Fineness 反映平移动作是否细腻，Angular Jerk 反映旋转变化是否突然；二者与真实敏感度相关性分别达到 **r=0.90** 和 **r=0.87**。
- 系统采用 **静态 W4 + 动态 A-bit** 范式：权重固定为 INT4，激活按步骤在 **2/4/8 bit** 与 **BF16** 间切换，避免动态换权重带来的带宽开销。
- 为防止频繁抖动切换，框架引入滞回/延迟窗口机制；同时通过离线校准，把连续敏感度映射成在线常数时间查表的离散比特选择。

## Results
- 论文摘要声称：DyQ-VLA 仅使用原模型 **30.9%** 的内存占用，同时保持 **99.5%** 的原始性能。
- 在速度上，方法实现了 **1.49×** 的仿真加速，以及最高 **1.43×** 的真实世界加速。
- 在敏感度建模上，运动学代理与量化敏感度呈强相关：**Motion Fineness r=0.90**，**Angular Jerk r=0.87**，支撑了“用实时运动状态指导量化”的关键假设。
- 论文还通过逐步扰动分析说明：即使局部量化误差在某些粗运动阶段达到峰值，任务成功率仍可保持较高，说明“局部误差大小”与“最终任务是否失败”并非线性对应，这正是动态量化优于静态量化的依据。
- 摘录中未给出更细的完整实验表格信息，例如具体数据集分项分数、与 GPTQ/AWQ/QVLA/SQAP-VLA 的逐项数值对比、误差条或显著性检验。

## Link
- [http://arxiv.org/abs/2603.07904v1](http://arxiv.org/abs/2603.07904v1)
