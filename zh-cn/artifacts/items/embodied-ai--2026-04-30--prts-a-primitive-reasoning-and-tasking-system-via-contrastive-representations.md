---
source: arxiv
url: https://arxiv.org/abs/2604.27472v1
published_at: '2026-04-30T06:14:02'
authors:
- Yang Zhang
- Jiangyuan Zhao
- Chenyou Fan
- Fangzheng Yan
- Tian Li
- Haitong Tang
- Sen Fu
- Xuan'er Wu
- Qizhen Weng
- Weinan Zhang
- Xiu Li
- Chi Zhang
- Chenjia Bai
- Xuelong Li
topics:
- vision-language-action
- robot-foundation-model
- goal-conditioned-rl
- contrastive-learning
- long-horizon-manipulation
- offline-robot-data
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# PRTS: A Primitive Reasoning and Tasking System via Contrastive Representations

## Summary
## 摘要
PRTS 是一个 4B 的视觉-语言-动作机器人模型，在行为克隆预训练中加入了目标可达性学习。它只用离线轨迹训练 VLM 来判断一个状态-动作对达到语言目标的可能性。

## 问题
- 现有的 VLA 预训练主要使用行为克隆，因此模型学到的是动作预测，而不是对语言目标的任务进展进行显式估计。
- 这对长时程和接触密集型机器人任务很重要，因为策略需要判断当前状态-动作是否在接近成功。
- 摘要中提到的以往 value-augmented VLA 方法需要奖励标签、进度标签、单独的 value 网络，或者多阶段训练。

## 方法
- PRTS 把每条语言指令当作一个目标，并把对比强化学习应用到离线机器人演示数据上。
- 它学习两个嵌入：状态-动作嵌入 phi(s,a) 和目标嵌入 psi(l)。它们的内积近似对数折扣后的目标可达性，也就是 log Q_l(s,a)。
- 由于整条轨迹共享同一个语言目标，方法用 gamma^(T-t) 按到完成的时间距离给正样本加权，让更接近任务成功的状态权重更高。
- 它使用双向 InfoNCE 损失：从状态-动作到语言，用于任务区分；从语言到状态-动作，用于时间进展排序。
- 该架构向 Qwen3-VL-4B-Instruct 添加了 <CRL_action> 和 <CRL_goal> 令牌块，并用角色感知因果掩码在一次前向传播中同时输出动作 logits 和两个对比嵌入。

## 结果
- 摘要没有给出定量基准成功率，所以无法根据提供的文本对主要性能结论做数值核查。
- PRTS 在 167B token 的操作和具身推理数据上预训练。
- 训练使用 64 张 H100 GPU，持续 1 周，并使用自定义的 CuTe-FlashAttention 内核和序列打包。
- 论文声称在 4 个仿真基准家族上达到最先进性能：LIBERO、LIBERO-Pro、LIBERO-Plus 和 SimplerEnv。
- 论文还在真实世界测试集中评估了 14 个复杂操作任务，覆盖双臂 RealMan 和单臂 Flexiv 平台。
- 论文声称收益在长时程执行、接触密集型任务、零样本新指令泛化，以及在人为干预下的恢复能力上最强，但摘要没有给出成功率差值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27472v1](https://arxiv.org/abs/2604.27472v1)
