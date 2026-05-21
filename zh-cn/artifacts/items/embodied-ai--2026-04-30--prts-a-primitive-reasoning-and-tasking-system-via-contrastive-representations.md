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
PRTS 是一个 4B 视觉-语言-动作机器人模型，在行为克隆预训练中加入目标可达性学习。它只使用离线轨迹来训练 VLM，让模型为某个状态-动作对到达语言目标的可能性打分。

## 问题
- 现有 VLA 预训练主要使用行为克隆，因此模型学习动作预测时，没有显式估计任务朝语言目标推进的进度。
- 这会影响长时程和接触密集型机器人任务，因为策略需要判断当前状态-动作是否让任务更接近成功。
- 摘录中引用的既有价值增强 VLA 方法需要奖励标签、进度标签、独立价值网络或多阶段训练。

## 方法
- PRTS 将每条语言指令视为一个目标，并将对比强化学习应用于离线机器人示范。
- 它学习两个嵌入：状态-动作嵌入 phi(s,a) 和目标嵌入 psi(l)。二者内积近似于对数折扣目标可达性，即 log Q_l(s,a)。
- 由于语言目标在一条轨迹中共享，该方法用 gamma^(T-t) 按距离完成的时间间隔为正样本加权，给更接近任务成功的状态更高权重。
- 它使用双向 InfoNCE 损失：从状态-动作到语言用于任务区分，从语言到状态-动作用于时间进度排序。
- 架构在 Qwen3-VL-4B-Instruct 中加入 <CRL_action> 和 <CRL_goal> token 块，并使用角色感知因果掩码，在一次前向传播中产生动作 logits 和两个对比嵌入。

## 结果
- 摘录没有给出定量基准成功率，因此无法从所提供文本中用数字核查主要性能主张。
- PRTS 在 167B token 的操作和具身推理数据上预训练。
- 训练使用 64 块 H100 GPU，耗时 1 周，并使用自定义 CuTe-FlashAttention kernel 和序列打包。
- 论文声称在 4 个仿真基准系列上达到当前最佳性能：LIBERO、LIBERO-Pro、LIBERO-Plus 和 SimplerEnv。
- 论文还在一个真实世界套件上评估，覆盖双臂 RealMan 和单臂 Flexiv 平台上的 14 个复杂操作任务。
- 论文声称，在长时程执行、接触密集型任务、零样本新指令泛化以及人在干预后的恢复方面，增益最强，但摘录没有提供成功率差值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27472v1](https://arxiv.org/abs/2604.27472v1)
