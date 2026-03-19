---
source: arxiv
url: http://arxiv.org/abs/2603.08519v1
published_at: '2026-03-09T15:52:48'
authors:
- Xiaoquan Sun
- Zetian Xu
- Chen Cao
- Zonghe Liu
- Yihan Sun
- Jingrui Pang
- Ruijian Zhang
- Zhen Yang
- Kang Pang
- Dingxin He
- Mingqi Yuan
- Jiayu Chen
topics:
- vision-language-action
- world-model
- offline-rl
- robot-manipulation
- long-horizon
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# AtomVLA: Scalable Post-Training for Robotic Manipulation via Predictive Latent World Models

## Summary
AtomVLA提出一种面向机器人操作的两阶段后训练框架，用原子级子任务指令和潜在世界模型奖励来提升长时程任务的稳定性与泛化。它重点解决仅靠模仿学习时指令落地不足、误差累积严重、且在线RL代价过高的问题。

## Problem
- 现有VLA通常只用粗粒度高层指令做监督微调，缺少中间步骤引导，导致长时程多步操作中容易产生误差累积。
- 机器人在线RL在真实系统上成本高、风险大、难扩展，因此很难用交互式方式继续优化策略。
- 像素级生成世界模型常出现长序列预测误差和视觉幻觉，难以为离线策略优化提供稳定可靠的奖励。

## Approach
- 采用两阶段训练：**Stage I**先用GPT-4o把高层任务分解成2-5个原子子任务，并把高层指令与子任务指令一起用于SFT，增强指令落地与阶段性引导。
- 主干使用Qwen3-VL-4B-Instruct作为VLM，配合cross-attention Diffusion Transformer动作头，直接生成动作chunk而不是单步动作。
- **Stage II**使用基于V-JEPA2的动作条件潜在世界模型：给定当前观测和候选动作chunk，预测未来潜在状态，并与当前子任务边界帧、最终目标帧的潜在表示做距离比较来打分。
- 奖励由三部分组成：子目标能量、最终目标能量、与专家动作的偏差约束；然后用离线GRPO在候选动作组内做相对优化，并加KL约束保持接近SFT参考策略。
- 核心机制可简单理解为：先把复杂任务拆成小步骤教会模型“现在该做什么”，再让世界模型在潜在空间里评估“这串动作会不会更接近当前子目标和最终目标”，据此离线强化更好的动作。

## Results
- 在**LIBERO**上，AtomVLA达到**97.0%**平均成功率；分项为Spatial **96.4%**、Object **99.6%**、Goal **97.6%**、Long **94.4%**。对比：NORA-1.5为**94.5%**平均，π0为**94.2%**，CoT-VLA为**83.9%**。
- 在更难的**LIBERO-PRO**上，AtomVLA平均成功率为**0.48（48%）**，优于π0的**0.45**、X-VLA的**0.46**、MolmoAct的**0.41**、NORA的**0.39**。
- 作者称**后训练持续带来提升**：相对SFT基线（LIBERO平均**93.0%**），仅用子目标奖励可到**96.0%**，仅用最终目标奖励可到**96.1%**，完整奖励可到**97.0%**，即整体提升约**4.0%**；在Long子集上从**90.0%**提升到**94.4%**，增幅**4.4%**。
- 子任务指令确实重要：在LIBERO-Long上，仅图像输入为**80.4%**；图像+高层任务指令为**90.0%**；再加入原子子任务指令后达到**92.2%**。
- 动作chunk大小消融显示**4步**最好：平均**97.0%**，优于8步和16步的**96.6%**以及32步的**96.3%**；Long子集上4步为**94.4%**，明显高于32步的**91.2%**。
- 真实世界Galaxea R1 Lite六项任务中，标准设置下AtomVLA平均**66.7%**，与π0的**65.8%**接近；但在泛化设置下AtomVLA达到**47.5%**，显著高于π0的**29.2%**，绝对提升**18.3%**。例如Fold T-shirt从**5%**提升到**25%**，Fold towel从**20%**到**35%**。

## Link
- [http://arxiv.org/abs/2603.08519v1](http://arxiv.org/abs/2603.08519v1)
