---
source: arxiv
url: http://arxiv.org/abs/2604.01570v1
published_at: '2026-04-02T03:30:43'
authors:
- Haochen Niu
- Kanyu Zhang
- Shuyu Yin
- Qinghai Guo
- Peilin Liu
- Fei Wen
topics:
- vision-language-action
- robot-finetuning
- ood-generalization
- sample-efficiency
- manipulation-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior

## Summary
## 摘要
本文为 vision-language-action 微调加入了可行动作邻域先验。核心想法是训练机器人策略在一小片相似且有效的动作区域上保留概率质量，而不是收缩到某一个精确动作上。

## 问题
- 传统 VLA 微调使用语言模型式目标，例如 one-hot 的下一个 token 预测或 PPO 式更新，把一个动作当成唯一正确目标。
- 在机器人操作中，同一状态下很多相近动作都能产生同样好的效果，所以强行逼近单一尖锐的动作分布会损害泛化，也会浪费数据。
- 论文关注两类常见失效模式：小规模示范集上的监督微调过拟合，以及强化微调中策略需要通过探索自己发现动作容忍度时的低样本效率。

## 方法
- 论文定义了 **feasible action neighborhood (FAN)**：对某个状态而言，一组连通动作，它们的价值与最优动作相比都在某个容差范围内。
- 论文把策略分布当作 FAN 大小的实际代理：窄尖峰表示容忍度低，更宽且平滑的峰表示更稳健。
- 该方法加入一个 KL 正则项，把动作分布拉向以策略当前最佳动作为中心的高斯分布。这会鼓励邻近动作上的平滑、单峰分布。
- 对 **FAN-SFT**，正则项加入监督对数似然损失，协方差取自策略当前方差。
- 对 **FAN-PPO**，正则项加入 PPO，使用固定协方差目标，这样策略更新会在奖励提升、信赖域稳定性和高斯形状的局部动作先验之间做权衡。

## 结果
- 在 **ManiSkill** 上用 **OpenVLA** 做 SFT 时，**FAN-SFT** 将域内成功率从 **78.1 ± 3.1** 提升到 **89.8 ± 0.8**（**+11.7** 个百分点）。
- 在 ManiSkill 的 OOD 评估中，**视觉** 成功率从 **76.6 ± 1.9** 提升到 **81.7 ± 1.1**（**+5.1**），**语义** 从 **57.4 ± 0.9** 提升到 **63.5 ± 1.5**（**+6.1**），**执行** 从 **40.4 ± 0.8** 提升到 **44.8 ± 0.5**（**+4.4**）。
- ManiSkill 上的平均 OOD 成功率从 **58.1** 提升到 **63.3**（**+5.2** 个百分点），基线是 OpenVLA + SFT，并且高于文中报告的 **RL4VLA** OOD 平均值 **60.7**。
- 论文还声称，在 **SFT 和 RFT** 上，使用 **OpenVLA** 和 **OpenVLA-OFT** 在 **ManiSkill** 和 **LIBERO** 上都带来了 **样本效率、收敛速度和 OOD 鲁棒性** 的提升。
- 给出的摘录不包含 RFT 的量化表格，也没有完整的 LIBERO 数字，所以这里无法用精确指标核实这些结论。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01570v1](http://arxiv.org/abs/2604.01570v1)
