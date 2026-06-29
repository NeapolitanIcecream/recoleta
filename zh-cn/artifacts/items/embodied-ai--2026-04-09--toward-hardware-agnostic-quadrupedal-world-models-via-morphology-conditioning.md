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
本文提出一种四足世界模型，它根据机器人 USD 描述中的形态信息来条件化动力学。目标是在不同四足机体之间实现零样本迁移，无需在线适应、预热或重新训练。

## 问题
- 标准机器人世界模型绑定在单一硬件配置上，因此在一台四足机器人上训练出的模型，遇到腿长、质量分布或执行器限制不同的另一台机器人时可能失效。
- 许多迁移方法把形态当作从运动历史中推断的隐变量。这会在部署开始时带来适应延迟，并可能影响安全性和控制质量。
- 为每台机器人单独训练一个模型成本很高，也限制了异构机器人车队的扩展。

## 方法
- 该方法以 DreamerV3 为基础，为世界模型加入显式的形态条件化，并把系统称为四足世界模型（QWM）。
- 物理形态编码器从机器人的 USD 文件中提取一个归一化特征向量。特征包括腿段长度、膝关节构型、站姿几何、总质量、躯干质量比和执行器扭矩密度。
- 模型使用双塔编码器：一塔处理本体感觉观测，另一塔处理静态形态向量，然后在潜状态推断前融合两者。
- 循环动力学也在每一步都按形态条件化，因此潜状态不需要从交互历史中推断静态身体属性。
- 自适应奖励归一化模块使用 EMA 跟踪的第 5 和第 95 百分位回报，对每台机器人分别缩放奖励，避免奖励幅度更大的机器人在训练中占主导。

## 结果
- 论文声称，这是首个用于运动控制、能在四足机器人家族内对未见过的四足形态实现零样本泛化的世界模型。
- 论文声称，它可以在仿真和真实机器人环境中，把模型部署到完全未见过的四足机器人上，而无需微调、适应或预热。
- 摘要片段没有给出基准表或最终任务指标，因此这里无法提供直接的成功率、回报或基线对比数字。
- 文中给出了一些具体的奖励尺度例子，用来说明归一化的动机：Spot 的平均奖励收敛到约 350，ANYmal 变体约为 25，Unitree A1/Go1/Go2 约为 40，Unitree B2 约为 15。
- 文中把该方法描述为分布有界的：它只在训练过的四足形态家族内部进行插值，而不是充当通用物理引擎。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08780v1](http://arxiv.org/abs/2604.08780v1)
