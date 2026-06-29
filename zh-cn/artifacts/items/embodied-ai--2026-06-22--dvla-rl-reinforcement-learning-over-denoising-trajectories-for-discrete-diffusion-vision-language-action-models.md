---
source: arxiv
url: https://arxiv.org/abs/2606.23623v1
published_at: '2026-06-22T17:19:03'
authors:
- Yuhao Wu
- Yitian Liu
- Weijie Shen
- Mishuo Han
- Wenjie Xu
- Haotian Liang
- Zhongshan Liu
- Yinan Mao
- Lei Xu
- Xinping Guan
- Ru Ying
- Ran Zheng
- Wei Sui
- Xiaokang Yang
- Wenbo Ding
- Yao Mu
topics:
- vision-language-action
- discrete-diffusion
- reinforcement-learning
- robot-manipulation
- ppo
- bimanual-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# dVLA-RL: Reinforcement Learning over Denoising Trajectories for Discrete Diffusion Vision-Language-Action Models

## Summary
## 摘要
dVLA-RL 通过在采样得到的去噪路径上训练，将 PPO 用于离散扩散 VLA 策略。论文报告称，该方法在 LIBERO 上达到 99.7% 的平均成功率，并且在 RoboTwin 2.0 上比其 SFT MM-ACT 骨干高出 30.6 个百分点。

## 问题
- 离散扩散 VLA 通过多个掩码 token 去噪步骤生成一个动作，因此最终动作的精确概率需要对许多可能的中间路径求和。
- 标准 PPO 需要策略似然；只使用最后一个去噪步骤会忽略生成已执行动作的路径。
- 这一点很关键，因为只用 SFT 训练的机器人策略在闭环执行中可能发生漂移，而 RL 可以直接根据奖励优化任务成功率。

## 方法
- 该方法把一个环境动作内部的 K 步去噪过程视为马尔可夫链，并优化采样路径的概率。
- 它将路径似然分解为逐步的 token 生成概率，范围是每个去噪步骤中新解除掩码的 token。
- Gumbel-TopK 掩码调度器被视为不可微的系统动态，因此 PPO 梯度只应用于新生成的动作 token。
- 同一种似然形式支持 1 步、2 步和 4 步解码，使作者可以按任务分配更短或更长的去噪时域。

## 结果
- 在 LIBERO 上，dVLA-RL 报告在 Spatial、Object、Goal 和 Long 上的平均成功率为 99.7%，四个套件的成功率均高于 99%。
- 在 LIBERO 上，节选表格中报告的平均值高于 OpenVLA 的 76.5%、π0 的 94.2% 和 UniVLA 的 95.2%。
- 在 RoboTwin 2.0 上，dVLA-RL 将 MM-ACT SFT 骨干在八个选定任务上的平均成功率从 61.4% 提高到 92.0%，提升 +30.6 个百分点。
- 列出的 RoboTwin 2.0 最大增益是 Handover Mic 的 +47.9 个百分点、Move Can Pot 的 +47.5 个百分点，以及 Lift Pot 的 +43.1 个百分点。
- 报告的 dVLA-RL 分数是 RL 训练期间的最佳在线 rollout 成功率，其中每个 LIBERO 任务使用 512 个 rollout episode，每个 RoboTwin 2.0 任务使用 64 个 rollout episode。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23623v1](https://arxiv.org/abs/2606.23623v1)
