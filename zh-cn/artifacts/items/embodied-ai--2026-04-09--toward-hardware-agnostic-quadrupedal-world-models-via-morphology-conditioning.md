---
source: arxiv
url: http://arxiv.org/abs/2604.08780v1
published_at: '2026-04-09T21:31:24'
authors:
- Mohamad H. Danesh
- Chenhao Li
- Amin Abyaneh
- Anas Houssaini
- Kirsty Ellis
- Glen Berseth
- Marco Hutter
- Hsiu-Chin Lin
topics:
- world-model
- quadruped-locomotion
- morphology-conditioning
- zero-shot-transfer
- sim-to-real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning

## Summary
## 摘要
这篇论文提出了一种四足世界模型，在动力学建模中显式加入从机器人 USD 描述中提取的形态信息。目标是在不同四足机器人机体之间实现零样本迁移，无需在线适应、预热或重新训练。

## 问题
- 标准机器人世界模型通常绑定于单一硬件配置，因此在一种四足机器人上训练的模型，换到另一种具有不同肢段长度、质量分布或执行器限制的机器人上时可能会失效。
- 许多迁移方法把形态当作需要从运动历史中推断的隐藏变量。这会在部署开始时带来适应延迟，并损害安全性和控制质量。
- 为每台机器人分别训练一个模型成本很高，也无法扩展到由异构机器人组成的集群。

## 方法
- 该方法基于 DreamerV3，并在世界模型中加入显式形态条件，将整个系统称为 Quadrupedal World Model (QWM)。
- 一个 Physical Morphology Encoder 从机器人的 USD 文件中提取归一化特征向量。这些特征包括腿部各段长度、膝关节配置、站姿几何、总质量、躯干质量比例以及执行器扭矩密度。
- 模型采用双塔编码器：一塔处理本体感觉观测，另一塔处理静态形态向量，然后在潜在状态推断前将两者融合。
- 循环动力学模型在每一步也以形态作为条件，因此潜在状态不需要再从交互历史中推断静态机体属性。
- 一个 Adaptive Reward Normalization 模块使用 EMA 跟踪的第 5 和第 95 回报百分位数，按机器人对奖励进行重缩放，避免奖励幅度较大的机器人在训练中占主导。

## 结果
- 论文称，这是首个能在四足机器人家族内部对未见过的四足形态实现零样本泛化的运动控制世界模型。
- 论文称，该方法可以在仿真和真实机器人环境中，直接部署到完全未见过的四足机器人上，无需微调、适应或预热。
- 摘录中没有给出基准表或最终任务指标，因此这里没有直接的成功率、回报值或与基线比较的数字。
- 文中给出了具体的奖励尺度示例，说明归一化的必要性：Spot 的平均奖励收敛在约 350，ANYmal 各变体约 25，Unitree A1/Go1/Go2 约 40，Unitree B2 约 15。
- 该方法被描述为有分布边界：它是在已训练的四足形态家族内部做插值，而不是一个通用物理引擎。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08780v1](http://arxiv.org/abs/2604.08780v1)
