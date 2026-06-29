---
source: arxiv
url: https://arxiv.org/abs/2605.30226v1
published_at: '2026-05-28T16:57:47'
authors:
- Zhongxi Chen
- Yifan Han
- Yanming Shao
- Huanming Liu
- Congsheng Xu
- Xiaoyu Chen
- Yao Mu
- Wenzhao Lian
topics:
- vision-language-action
- dexterous-manipulation
- offline-to-online-rl
- residual-adaptation
- human-in-the-loop
- robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models

## Summary
## 摘要
BORA 是一个面向精细 VLA 机器人策略的离线到在线 RL 训练流程。它先离线训练一个动作条件 critic，再在在线阶段加入一个小型的人类引导残差策略，从而提升了带有 Franka 机械臂和 12 自由度手的五项真实任务的成功率。

## 问题
- 精细 VLA 策略比更简单的夹爪策略更容易失败，因为手部控制自由度高，接触结果难以预测，细小的执行误差会在时间上不断累积。
- 离线模仿数据可能包含冗余或次优的手部动作，因此纯模仿学习给出的物理意图较弱，对未见过的物体泛化也较差。
- 直接对精细手进行在线 RL 会浪费真实机器人样本，带来不安全的探索，并且在全模型更新时可能损伤预训练 VLM 特征。

## 方法
- BORA 先用一致性策略动作头离线训练 VLA 策略。该动作头在 1 到 3 步去噪中生成连续动作块，相比较长的扩散链，这样能缩短 RL 的信用分配路径。
- 它的 critic 同时读取 VLM 认知 token 和生成的动作块，然后对块内每一步打分。这样价值学习评估的是所提议的手部动作，而不只是摄像头图像。
- 离线策略更新结合了 IQL 风格的价值学习、块内优势估计、裁剪的 PPO 风格更新，以及行为克隆正则项，用来限制分布外动作。
- 在线部署时，BORA 冻结基础 VLA，只训练一个小型 MLP 残差 actor，用块级修正来调整动作：A_final = A_base + lambda * A_res。
- 当策略进入风险状态时，人工干预会带来惩罚；在纠正动作后，会得到恢复奖励。在线阶段复用离线 critic，并以 1:1 的比例混合离线和在线数据。

## 结果
- 在五项标准真实任务上，每项 20 次试验，BORA-Full 的平均成功率达到 86.0%。CP Base 为 53.0%，VITRA 为 54.0%，CP + Decoupled Critic 为 45.0%，BORA-Offline 为 67.0%。
- 相比 CP Base，标准设置下提升了 33 个百分点，与论文主张一致。BORA-Full 在各任务上的成功数分别是：抓取毛绒玩具 20/20、抓取并放置 18/20、打开盒子 15/20、拉纸巾 16/20、按按钮 17/20。
- 在未见过物体的试验中，BORA-Full 的平均成功率达到 70.0%。CP Base 为 27.0%，VITRA 为 33.0%，CP + Decoupled Critic 为 41.0%，BORA-Offline 为 52.0%。
- 相比 CP Base，未见过物体设置下提升了 43 个百分点。BORA-Full 在五项任务上的成功数分别为 17/20、14/20、10/20、14/20 和 15/20。
- 仅使用 BORA-Offline 时，标准设置下的平均成功率比 CP Base 提高了 14 个百分点，未见过物体设置下提高了 25 个百分点。
- 论文报告称，在线自适应在 2 轮在线 RL 内收敛，每项任务需要 1 到 2 次人工干预，在线轨迹执行时间中大约 20% 处于人工控制下。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30226v1](https://arxiv.org/abs/2605.30226v1)
