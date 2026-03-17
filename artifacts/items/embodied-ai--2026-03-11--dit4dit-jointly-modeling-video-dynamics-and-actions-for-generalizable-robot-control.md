---
source: arxiv
url: http://arxiv.org/abs/2603.10448v1
published_at: '2026-03-11T06:03:53'
authors:
- Teli Ma
- Jia Zheng
- Zifan Wang
- Chuili Jiang
- Andy Cui
- Junwei Liang
- Shuo Yang
topics:
- vision-language-action
- video-diffusion
- robot-control
- generalist-robot-policy
- world-model
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
---

# DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control

## Summary
DiT4DiT提出把视频生成模型与动作生成模型端到端联合训练，用视频扩散过程中的中间时空特征来指导机器人动作预测。核心观点是：学习“未来会如何变化”的视频动力学，比只靠静态视觉语义更适合作为通用机器人控制的基础。

## Problem
- 现有VLA/机器人基础模型大多继承静态图文预训练表征，缺少对**时序变化和物理动力学**的原生建模，因此控制能力强依赖昂贵的动作标注数据。
- 以往把视频模型用于机器人控制的方法，常是**多阶段**流程：先做视频/表征学习，再单独训练动作模型，导致信息传递间接、训练不统一。
- 论文要解决的是：**如何把视频生成真正变成机器人策略学习的核心骨干**，并证明它为什么能提升泛化、数据效率和真实部署表现。

## Approach
- 使用一个统一的**双DiT架构**：一个Video Diffusion Transformer预测未来视频动力学，另一个Action Diffusion Transformer预测动作轨迹。
- 关键机制不是用最终重建出的未来帧，而是从**视频去噪过程中的中间隐藏状态**提取特征，把这些 temporally grounded 的表征作为动作模型的条件输入。
- 提出**dual flow-matching**联合目标，同时训练视频生成与动作生成；两者共享一个统一框架，但各自有独立噪声与流时间步。
- 采用**tri-timestep / decoupled timestep**设计：视频模块用均匀采样时间步学习完整去噪轨迹；特征提取用固定时间步保证稳定条件；动作模块用Beta分布时间步强调关键控制阶段。
- 初始化上，视频骨干来自Cosmos-Predict2.5-2B，动作头基于GR00T系Action DiT，并冻结文本编码器与VAE，仅联合微调两个DiT模块。

## Results
- 在**LIBERO**仿真基准上，DiT4DiT达到**98.6%平均成功率**，文中称为新的SOTA，并指出在长时程任务上优于**π0.5**与**CogVLA**等强VLA基线。
- 在**RoboCasa GR1** 24个桌面任务上，达到**50.8%平均成功率**，文中称显著超过**GR00T**系列等预训练策略。
- 作为“视频生成是更好缩放代理任务”的验证，在RoboCasa GR1上相较于Grounding和FLARE-style语义中心基线，**样本效率提升超过10×**，**收敛速度最高提升7×**。
- 在真实**Unitree G1**机器人上，论文声称优于预训练基线**GR00T-N1.5**和参数量匹配基线，并且仅用**单个第一视角相机**即可完成高精度任务；但摘录中**未提供具体真实世界数值指标**。
- 论文还声称具备强**zero-shot泛化**，能适应未见物体、类别变化和数量变化，覆盖仿真与真实环境；摘录中同样**未给出量化泛化分数**。

## Link
- [http://arxiv.org/abs/2603.10448v1](http://arxiv.org/abs/2603.10448v1)
