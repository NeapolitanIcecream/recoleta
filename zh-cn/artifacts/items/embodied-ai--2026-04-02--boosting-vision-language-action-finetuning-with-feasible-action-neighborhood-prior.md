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
这篇论文在 vision-language-action 微调中加入了可行动作邻域先验。核心思路是训练机器人策略，让概率质量覆盖一小片相近且同样有效的动作区域，而不是收缩到一个精确动作上。

## 问题
- 标准 VLA 微调使用语言模型风格的目标，例如 one-hot 下一 token 预测或 PPO 风格更新，把某一个动作当作唯一正确的目标。
- 在机器人操作中，对于同一个状态，许多邻近动作都可能同样有效，因此强行学习单一且尖锐的动作分布会损害泛化能力，也会浪费数据。
- 论文针对两种常见失败模式：小规模演示数据下监督微调的过拟合，以及强化微调中策略必须通过探索自行发现动作容忍范围时的低样本效率。

## 方法
- 论文定义了 **feasible action neighborhood (FAN)**：对于一个状态，存在一个连通的动作集合，其中动作价值与最优动作的差距在容忍范围内。
- 它把策略分布作为 FAN 大小的一个实用代理：尖窄的峰值表示容忍度低，较宽且平滑的峰值表示鲁棒性更强。
- 该方法加入一个 KL 正则项，把动作分布拉向一个以策略当前最佳动作为中心的高斯分布。这会鼓励邻近动作上形成平滑、单峰的分布。
- 对于 **FAN-SFT**，正则项加到监督对数似然损失中，协方差取自策略当前的方差。
- 对于 **FAN-PPO**，正则项加到 PPO 中，并使用固定协方差目标，因此策略更新需要在奖励提升、trust-region 稳定性和高斯形状的局部动作先验之间权衡。

## 结果
- 在 **ManiSkill** 的 **OpenVLA** SFT 上，**FAN-SFT** 将分布内成功率从 **78.1 ± 3.1** 提高到 **89.8 ± 0.8**（**+11.7 个点**）。
- 在 ManiSkill OOD 评测中，**vision** 成功率从 **76.6 ± 1.9** 提高到 **81.7 ± 1.1**（**+5.1**），**semantic** 从 **57.4 ± 0.9** 提高到 **63.5 ± 1.5**（**+6.1**），**execution** 从 **40.4 ± 0.8** 提高到 **44.8 ± 0.5**（**+4.4**）。
- 与 OpenVLA + SFT 基线相比，ManiSkill 的平均 OOD 成功率从 **58.1** 提高到 **63.3**（**+5.2 个点**），也高于文中报告的 **RL4VLA** OOD 平均值 **60.7**。
- 论文还声称，在 **ManiSkill** 和 **LIBERO** 上，使用 **OpenVLA** 和 **OpenVLA-OFT** 时，该方法在 **SFT 和 RFT** 中都能提升**样本效率、收敛速度和 OOD 鲁棒性**。
- 当前提供的摘录不包含 RFT 的定量表格或完整的 LIBERO 数值，因此这里无法用精确指标核实这些说法。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01570v1](http://arxiv.org/abs/2604.01570v1)
