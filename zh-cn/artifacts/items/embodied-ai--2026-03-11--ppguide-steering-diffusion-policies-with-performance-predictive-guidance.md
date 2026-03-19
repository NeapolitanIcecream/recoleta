---
source: arxiv
url: http://arxiv.org/abs/2603.10980v1
published_at: '2026-03-11T17:10:16'
authors:
- Zixing Wang
- Devesh K. Jha
- Ahmed H. Qureshi
- Diego Romeres
topics:
- diffusion-policy
- inference-time-guidance
- multiple-instance-learning
- robot-manipulation
- imitation-learning
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# PPGuide: Steering Diffusion Policies with Performance Predictive Guidance

## Summary
PPGuide提出一种在**推理时**引导扩散机器人策略的方法，用稀疏的成功/失败终局信号而不是密集奖励或世界模型来提升鲁棒性。核心思想是先自动找出轨迹里“哪些观测-动作片段最影响成败”，再用这个信号对采样过程施加梯度引导。

## Problem
- 扩散策略虽然能学习复杂、多峰的操作行为，但生成动作序列中的小误差会随时间累积，导致长时程操作失败。
- 现有增强鲁棒性的办法通常依赖**更多专家数据/纠错示范**、**密集奖励**或**世界模型**，这些在机器人场景里往往代价高或难获得。
- 难点在于：只有整条轨迹的二值成败标签，如何把这种稀疏监督变成每个时刻都可用的、可微的动作引导信号。

## Approach
- 先收集预训练扩散策略在不同训练阶段checkpoint上的rollout，得到既有成功也有失败的多样化轨迹。
- 把一整条轨迹看作一个MIL bag，把每个观测-动作chunk看作instance；用**注意力式Multiple Instance Learning**从仅有的轨迹级成功/失败标签中，自动找出最相关的chunk。
- 根据MIL注意力权重做伪标签，把instance分成**Success-Relevant (SR)**、**Failure-Relevant (FR)** 和 **Irrelevant (IR)** 三类；文中称IR数量比SR/FR多**10倍以上**。
- 用这些伪标签训练一个轻量级三分类指导器；推理时对动作求分类器对SR/FR对数概率的梯度，**增强SR、抑制FR**，并把该梯度注入扩散去噪过程。
- 为减少推理开销，提出**alternating guidance**：不在每个去噪步都加引导，而是隔步引导，声称性能接近恒定引导但计算更省。

## Results
- 在Robomimic与MimicGen的8个任务上评估，基座扩散策略只用原始专家示范的**10%数据**训练；PPGuide训练数据来自epoch **250/300/350/400/450**的rollout，测试于epoch **500/550** checkpoint。
- 相比基础Diffusion Policy (DP)，PPGuide在多项任务上提升明显：例如 **Square** 从 **62%→72%(+10)**@500、**58%→66%(+8)**@550；**Transport** 从 **60%→68%(+8)**@500、**68%→76%(+8)**@550；**Mug Cleanup D1** 从 **26%→36%(+10)**@550。
- 在更难或长时程任务上也有增益：**Coffee D2** 从 **54%→58%(+4)**@500、**46%→58%(+12)**@550；**Kitchen D1** 从 **40%→44%(+4)**@550；**Coffee Preparation D1** 从 **18%→22%(+4)**@550。
- 与其变体相比，**PPGuide-CG**（每步恒定引导）与**PPGuide**（交替引导）整体都优于**PPGuide-SS/DP-SS**随机采样式方法；作者称交替引导“几乎达到”恒定引导效果，同时显著减少额外前向计算。
- 异构基座策略评估（Table III）显示一定泛化：**Square** 在epoch **1300**上 **54%→70%(+16)**，**Transport** 在epoch **1300**上 **56%→74%(+18)**，但也出现个别下降，如 **Transport 1500** 从 **74%→70%(-4)**。
- 论文的核心实证主张是：在**无需世界模型、无需密集奖励、无需重新训练主策略**的前提下，PPGuide能在多任务上稳定提升预训练扩散策略的成功率。

## Link
- [http://arxiv.org/abs/2603.10980v1](http://arxiv.org/abs/2603.10980v1)
