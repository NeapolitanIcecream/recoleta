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
- 3d-awareness
- real-time-inference
- diffusion-policy
- multi-view-fusion
relevance_score: 0.21
run_id: materialize-outputs
language_code: zh-CN
---

# R3DP: Real-Time 3D-Aware Policy for Embodied Manipulation

## Summary
R3DP提出一种面向具身操作的实时3D感知策略，把高质量3D基础模型先验接入扩散策略，同时尽量避免实时控制中的高延迟。核心是“慢而准”的3D模型与“快而轻”的时序特征预测协同工作，再结合显式多视角几何融合来提升操作成功率。

## Problem
- 具身操作需要稳定的3D空间理解与时序一致性，但常见2D模仿学习策略主要依赖RGB特征，难以处理深度、遮挡和接触丰富的任务。
- 直接把大型3D基础模型逐帧用于机器人控制会带来过高推理延迟，尤其在多视角场景下很难满足实时性。
- 依赖深度/点云传感器虽可增强3D感知，但会增加硬件复杂度，并在透明、反光、无纹理物体上不稳定。

## Approach
- 提出R3DP：把VGGT这类大型3D视觉基础模型的中间3D特征接入Diffusion Policy，作为可插拔的3D感知模块。
- 设计异步快慢协同模块（AFSC）：仅在稀疏关键帧上运行慢速VGGT，其他中间帧由轻量Temporal Feature Prediction Network（TFPNet）根据历史特征和当前RGB预测3D特征。
- TFPNet通过蒸馏VGGT预训练，利用时序相关性在实时条件下保持特征连续性与稳定性，同时显式引入时间上下文。
- 设计Multi-View Feature Fuser（MVFF）：先融合每个视角的2D与3D特征，再借助PRoPE显式注入相机内参与外参，做几何一致的多视角融合。
- 训练时扩展时间窗口：每个训练样本使用8帧、步长8，总覆盖64帧；视觉骨干冻结，仅训练扩散策略头，以控制计算成本。

## Results
- 在RoboTwin的10个任务上，R3DP平均成功率达到**69.0%**（τ=4）和**65.7%**（τ=8），明显高于**DP-single 36.1%**、**DP-multi 17.6%**、**DP3 57.6%**、**DP3+DA2 28.2%**，也高于**π0 59.9%**。
- 论文摘要声称：R3DP相对单视角和多视角Diffusion Policy的平均成功率分别提升**32.9%**和**51.4%**。
- 观测编码延迟方面，朴素的**DP+VGGT**为**73.1 ms**，加入MVFF后为**78.3 ms**；而**R3DP(τ=4)**降至**50.5 ms**，**R3DP(τ=8)**降至**40.3 ms**，相对朴素集成最多减少**44.8%**。
- 任务级结果显示，R3DP(τ=4)在多个难任务上领先，例如**Block Handover 95%**（vs DP-single **1%**, DP3 **48%**, π0 **71%**）、**Blocks Stack Easy 69%**（vs DP-single **6%**, DP3 **26%**, π0 **79%**）、**Block Hammer Beat 77%**（vs DP-single **0%**, DP3 **49%**, π0 **47%**）。
- 在透明物体相关任务**Tube Insert**上，R3DP达到**97%**（τ=4/8），与**DP3 97%**持平，但明显高于**DP3+DA2 32%**、**π0 68%**和**DP-multi 64%**，支持其对RGB-only 3D先验整合的鲁棒性主张。

## Link
- [http://arxiv.org/abs/2603.14498v1](http://arxiv.org/abs/2603.14498v1)
