---
source: arxiv
url: http://arxiv.org/abs/2603.05410v1
published_at: '2026-03-05T17:33:20'
authors:
- Weikai Qin
- Sichen Wu
- Ci Chen
- Mengfan Liu
- Linxi Feng
- Xinru Cui
- Haoqi Han
- Hesheng Wang
topics:
- vision-language-action
- humanoid-control
- flow-matching
- whole-body-control
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# PhysiFlow: Physics-Aware Humanoid Whole-Body VLA via Multi-Brain Latent Flow Matching and Robust Tracking

## Summary
PhysiFlow提出了一个面向人形机器人全身控制的物理感知型VLA框架，把视觉-语言语义理解、高频动作生成和稳定跟踪控制拆成三个“脑”协同工作。其目标是在实时推理下实现语义引导的全身协调动作，并提升复杂动态任务中的稳定性与成功率。

## Problem
- 现有人形机器人VLA通常难以同时满足**语义理解、实时高频控制、物理稳定性**三者，导致复杂全身任务中容易失稳或失败。
- 纯VLA方法常有推理慢、边缘部署困难的问题；而纯全身控制/跟踪方法又缺少视觉与语言的高层语义指导。
- 这很重要，因为家庭/服务场景中的人形机器人需要根据图像和语言，自主完成需要上下肢协同与平衡维护的任务，而不只是桌面操作或遥操作跟踪。

## Approach
- 提出一个**multi-brain**分层架构：Neocortical Brain负责“做什么+怎么做”的语义-动作意图对齐，Basal Ganglionic Brain负责高频动作块生成，Cerebellar Brain负责物理约束下的稳健跟踪执行。
- Neocortical Brain使用基于**SigLIP + LoRA**的两阶段课程式CVAE，把第一/第三人称视觉和文本压缩为一个**256维语义-动作潜变量**，训练时借助未来动作，推理时只靠视觉和语言生成意图向量。
- Basal Ganglionic Brain用**conditional flow matching**替代自回归或扩散式逐步生成：以潜变量和机器人状态为条件，10 Hz生成长度为10的动作块，并通过重叠执行实现**50 Hz**有效控制。
- Cerebellar Brain采用**teacher-student RL + BC**的运动跟踪器，并在后期把跟踪误差反传到flow model进行联合微调，使生成动作更符合真实动力学与跟踪约束。
- 数据方面，作者在Isaac Lab中结合远程采集、运动回放、场景/物体随机替换，构建用于全身VLA训练的多视角、多任务数据集。

## Results
- 在Neocortical Brain消融中，完整模型优于各删减版本；例如去掉VL对齐后，**Retrieval Top-1从0.357降到0.016**，**Cross-Episode Retrieval从0.859降到0.037**，说明语言-潜变量对齐是关键。
- 去掉课程学习后，**Future Shuffle Gap从1.134降到0.001**，同时重建指标恶化（如**Recon. Prior从0.023变为0.081**），表明分阶段训练对学到有效意图表示非常重要。
- 在动作生成模块基准中，flow matching达到**18.65 ms mean latency**、**2.33 ms per-sample latency**，相对**DDPM快5.3×**、相对**AR快126×**；同时平滑性指标为**total variation 0.0061**、**jerk 0.0036**，接近AR且明显优于DDPM。
- 在Unitree G1仿真九项任务上，相比LeVERB，PhysiFlow总体成功率从**65.0%提升到74.9%**。
- 具体任务上，复杂任务提升明显：**Nav. (Long) 31.2→63.6**，**Nav. & Sit 5.8→18.1**，**Nav. & Circle 54.5→69.2**；常规任务中也有增益，如**Stand up 88.6→90.9**、**Locomotion 97.2→100.0**、**raise arm 79.1→100.0**。
- 论文还声称在真实Unitree G1上完成了视觉-语言引导的全身协调任务并表现出较强可靠性，但给定摘录中**未提供真实机器人定量指标**。

## Link
- [http://arxiv.org/abs/2603.05410v1](http://arxiv.org/abs/2603.05410v1)
