---
source: arxiv
url: http://arxiv.org/abs/2603.14498v1
published_at: '2026-03-15T17:30:49'
authors:
- Yuhao Zhang
- Wanxi Dong
- Yue Shi
- Yi Liang
- Jingnan Gao
- Qiaochu Yang
- Yaxing Lyu
- Zhixuan Liang
- Yibin Liu
- Congsheng Xu
- Xianda Guo
- Wei Sui
- Yaohui Jin
- Xiaokang Yang
- Yanyan Xu
- Yao Mu
topics:
- embodied-manipulation
- 3d-aware-policy
- diffusion-policy
- multi-view-fusion
- real-time-inference
- sim-benchmark
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# R3DP: Real-Time 3D-Aware Policy for Embodied Manipulation

## Summary
R3DP提出一种把大规模3D基础模型先验接入机器人操作策略、同时保持实时控制速度的方法。它面向具身操作中常见的3D空间理解与时延冲突问题，在模拟基准上同时提升成功率和推理效率。

## Problem
- 现有基于2D视觉的模仿学习策略缺少显式3D空间理解，在遮挡、接触丰富、精细对位等操作任务上容易失败。
- 直接把大型3D基础模型逐帧接入控制环路会带来过高延迟，难以满足实时机器人控制需求。
- 多视角输入常用简单拼接，未显式利用相机内外参与几何关系，跨视角融合不稳定。

## Approach
- 提出**Asynchronous Fast-Slow Collaboration (AFSC)**：慢分支仅在稀疏关键帧上调用预训练3D模型VGGT，提取高质量3D特征；快分支在中间帧上快速补全特征，从而避免每帧都跑重模型。
- 提出轻量**TFPNet**：利用历史帧和上一时刻3D特征，预测当前帧的实时3D特征；可理解为“用过去的信息猜当前的3D表示”，以低成本维持时序一致性。
- 提出**MVFF**多视角特征融合器：先融合每个视角的2D与3D特征，再通过PRoPE显式注入相机内参和外参，得到更一致的多视角3D表示。
- 将上述模块作为即插即用感知前端接入Diffusion Policy，训练时冻结VGGT和TFPNet主干，仅优化策略头，以较低计算成本引入3D先验与时序信息。

## Results
- 在RoboTwin的10个任务上，**R3DP(4)**平均成功率**69.0%**，对比**DP-single 36.1%**提升**32.9个百分点**，对比**DP-multi 17.6%**提升**51.4个百分点**。
- **R3DP(8)**平均成功率**65.7%**，仍明显高于**DP3 57.6%**、**DP3+DA2 28.2%**和**π0 59.9%**。
- 代表性任务上，R3DP(4)达到：**Block Hammer Beat 77%**（DP-single/DP-multi均**0%**，DP3 **49%**），**Block Handover 95%**（DP-single **1%**，π0 **71%**），**Put Apple Cabinet 100%**（DP3 **98%**）。
- 在透明物体相关的**Tube Insert**任务上，R3DP达到**97%**，与**DP3 97%**持平，但显著高于**DP3+DA2 32%**与**π0 68%**。
- 推理延迟方面，观察编码耗时从朴素**DP+VGGT 73.1 ms**降到**R3DP(8) 40.3 ms**，相比朴素集成减少**44.8%**；**R3DP(4)**为**50.5 ms**，下降**30.9%**。
- 论文核心主张是：通过把“重3D理解”与“快策略执行”解耦，R3DP在不依赖深度传感器的前提下，实现了更强3D感知、更高成功率和更低实时推理延迟。

## Link
- [http://arxiv.org/abs/2603.14498v1](http://arxiv.org/abs/2603.14498v1)
