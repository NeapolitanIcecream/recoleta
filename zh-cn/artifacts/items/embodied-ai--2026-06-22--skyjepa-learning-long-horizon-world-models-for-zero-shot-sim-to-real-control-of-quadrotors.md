---
source: arxiv
url: https://arxiv.org/abs/2606.23444v1
published_at: '2026-06-22T15:00:59'
authors:
- Pratyaksh Rao
- Wancong Zhang
- Randall Balestriero
- Yann LeCun
- Giuseppe Loianno
topics:
- quadrotor-control
- world-models
- sim2real
- latent-dynamics
- model-based-control
- jepa
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# SkyJEPA: Learning Long-Horizon World Models for Zero-Shot Sim-to-Real Control of Quadrotors

## Summary
## 摘要
SkyJEPA 为四旋翼控制训练一个 JEPA 风格的潜在世界模型，并把它用于基于采样的控制器，实现零样本仿真到现实飞行。论文的目标是在不逐步重建状态的情况下进行长时域预测。

## 问题
- 学习式四旋翼动力学模型通常以自回归方式预测下一状态，因此很小的单步误差会在较长控制时域中累积。
- 控制器需要位置、速度、姿态和角速度等物理状态变量中的预测结果，不能只依赖抽象嵌入。
- 真实四旋翼数据采集成本高，并且可能损坏硬件，尤其是在激进机动和平台变更场景中。

## 方法
- 模型把一段历史状态和动作窗口编码为潜在向量，然后在预测时域内预测未来潜在状态，而不是重建完整的未来状态。
- 训练使用多步潜在预测损失加 SIGReg。SIGReg 是一种防塌缩正则项，通过随机 1D 投影推动潜在嵌入接近各向同性高斯分布。
- 第二阶段的物理启发式探测器冻结潜在模型，并通过带残差校正的运动学把预测潜变量映射到度量状态。
- 探测器预测 R^3 中的残差平动加速度，以及一个与 4 个旋翼力相关的 3x4 残差角加速度映射。
- 学习到的模型被放入基于采样的最优控制器，并在域随机化仿真数据上训练，用于零样本户外部署。

## 结果
- 给定摘录没有提供准确的指标值、数据集规模、基线分数或闭环成功率。
- 文中声称的评估包括开环预测测试和户外闭环飞行实验。
- 文中声称的比较包括当前动力学学习基线，以及围绕关键设计选择的消融实验，但摘录没有给出数值差异。
- 文中声称的效果包括更好的长时域预测、在嵌入式硬件上的实时执行，以及跨轨迹和平台变化的零样本仿真到现实迁移。
- 方法中的具体数值细节包括一个含 4 个电机力的四旋翼动作向量，状态项包括 3D 位置、3D 速度、SO(3) 姿态和 3D 角速度，以及探测器中的一个 3x4 残差角映射。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23444v1](https://arxiv.org/abs/2606.23444v1)
