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
- humanoid-robotics
- whole-body-control
- flow-matching
- physics-aware-control
relevance_score: 0.34
run_id: materialize-outputs
language_code: zh-CN
---

# PhysiFlow: Physics-Aware Humanoid Whole-Body VLA via Multi-Brain Latent Flow Matching and Robust Tracking

## Summary
PhysiFlow提出了一个面向人形机器人全身控制的物理感知VLA框架，把语义理解、高频动作生成和稳定跟踪拆成三个“脑”协同完成。它主要解决现有VLA在人形全身任务中推理慢、语义引导弱、动态稳定性不足的问题，并在仿真与实机上展示了更可靠的语义驱动动作执行。

## Problem
- 现有人形机器人VLA往往难以同时兼顾**语义理解**、**高频动作生成**和**物理稳定控制**，导致复杂全身任务中容易失稳或失败。
- 传统端到端VLA推理效率偏低，难以满足人形机器人全身控制所需的高频闭环要求，尤其在边缘设备上更明显。
- 纯运动控制方法虽然能跟踪动作，但通常缺少视觉和语言层面的任务理解，难以完成“看懂场景+听懂指令+稳定执行”的家庭/服务场景任务。

## Approach
- 采用一个**bio-inspired multi-brain**架构：Neocortical Brain负责把视觉和语言压成语义-动作意图潜变量，Basal Ganglionic Brain负责根据该潜变量生成连续动作块，Cerebellar Brain负责物理约束下的稳健跟踪执行。
- 高层语义模块使用**基于SigLIP+LoRA的两阶段课程学习CVAE**，将“做什么”和“怎么做”的动作意图编码为一个潜变量；训练时使用未来动作做后验，推理时只依赖视觉和语言先验。
- 动作生成模块使用**conditional flow matching**而非自回归或扩散，输入潜变量和机器人状态，按10 Hz生成长度为10的动作序列块，通过重叠执行实现等效50 Hz控制。
- 控制执行模块使用**teacher-student RL motion tracker + PD controller**，并在训练后期把跟踪误差反传到flow-matching生成器，使生成动作更符合真实物理约束。
- 通过仿真数据回放、远程采集和场景/物体随机替换构建VLA数据集，提高视觉、语言与运动的联合泛化能力。

## Results
- 在Neocortical Brain消融中，完整模型的**Retrieval Top-1 = 0.357**；去掉VL对齐后降到**0.016**，**Retrieval (Cross Ep.)**从**0.859**降到**0.037**，说明语言-语义对齐是关键。
- 去掉课程学习后，**Future Shuffle Gap**从**1.134**几乎崩到**0.001**，同时**Recon. Prior**从**0.023**恶化到**0.081**，表明分阶段训练对潜变量有效性和重建质量很重要。
- 在动作生成基准中，flow matching平均延迟**18.65 ms**、单样本延迟**2.33 ms**，相对**DDPM快5.3倍**、相对**AR快126倍**；同时**total variation = 0.0061**、**jerk = 0.0036**，平滑性接近AR且优于DDPM。
- 系统通过10 Hz生成动作块并执行其中前5帧，实现**等效50 Hz**高频全身控制；下游PD控制器运行在**1000 Hz**。
- 在9项仿真任务中，相比LeVERB，PhysiFlow总体成功率从**65.0%**提升到**74.9%**。代表性任务上：**Nav. (Long) 31.2%→63.6%**，**Nav. & Sit 5.8%→18.1%**，**Nav. & Circle 54.5%→69.2%**，**Locomotion 97.2%→100.0%**，**raise arm 79.1%→100.0%**。
- 也有少数任务未全面领先，例如**Nav. (Short)**从**78.5%**降到**71.7%**，说明该方法更明显的优势集中在需要持续协调与稳定性的复杂全身任务上。

## Link
- [http://arxiv.org/abs/2603.05410v1](http://arxiv.org/abs/2603.05410v1)
