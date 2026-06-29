---
source: arxiv
url: https://arxiv.org/abs/2605.21800v1
published_at: '2026-05-20T22:58:15'
authors:
- Lucas Maes
- Quentin Le Lidec
- Luiz Facury
- Nassim Massaudi
- Ayush Chaurasia
- Francesco Capuano
- Richard Gao
- Taj Gillin
- Dan Haramati
- Damien Scieur
- Yann LeCun
- Randall Balestriero
topics:
- world-model
- robotics-benchmark
- reproducibility
- mpc-planning
- data-loading
- ood-evaluation
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation

## Summary
## 总结
stable-worldmodel 是一个用于可复现世界模型研究的开源平台，覆盖数据加载、基线训练、MPC 规划和受控评估。论文贡献的是共享基础设施和基准覆盖，没有提出新的世界模型架构。

## 问题
- 世界模型论文常常使用彼此独立的代码库、数据管道、规划器和评估设置，这让结果难以比较。
- 以视频为主的世界模型训练需要快速访问由帧、动作和传感器流组成的时间块；MP4 和 HDF5 等常见格式会拖慢训练。
- 标准模拟器基准通常测试与训练分布接近的设置，因此可能漏掉外观、几何或物理变化下的失效。

## 方法
- swm 使用基于 Lance 的数据层，并支持 MP4、HDF5 和 LeRobot 数据集的转换。
- 它定义了三个主要接口：World 用于 Gymnasium 风格的环境和扰动，Policy 用于动作选择，Solver 用于 MPC 规划。
- 它包含经过测试的世界模型基线实现，如 DINO-WM、LeWorldModel、PLDM 和 TD-MPC2，也包含 CEM、iCEM、MPPI、梯度下降、投影梯度下降和 GRASP 等规划求解器。
- 其基准套件覆盖 Classic Control、MuJoCo、Atari、机器人任务、OGBench、Push-T 和 Craftax，并带有可控的视觉、几何和物理变化因素。

## 结果
- 在 Push-T 数据加载上，Lance 本地在不使用缓存时达到 4,815 个样本/秒，而 HDF5 本地为 1,416 个样本/秒，视频本地为 1,331 个样本/秒。
- 对于 Push-T 的 S3 流式传输，Lance 在不使用缓存时达到 3,184 个样本/秒，使用缓存时为 3,253 个样本/秒；HDF5 通过 S3 在不使用缓存时为 9 个样本/秒，使用缓存时为 757 个样本/秒。
- 在基线比较中，Push-T 的成功率分别是 TD-MPC2 12%、GCBC 75%、LeWM 94%、PLDM 78% 和 DINO-WM 92%。
- 在 OGB-Cube 上，成功率分别是 TD-MPC2 4%、GCBC 84%、LeWM 72%、PLDM 62% 和 DINO-WM 86%。
- 论文报告了零样本和域外评估工具，但给出的摘录没有完整的定量 OOD 表；具体结论是，在每种设置下的 256 条轨迹中，成功和失败的 Push-T 规划运行之间，预测 MSE 有重叠，因此原始预测误差对规划成功的指示作用较弱。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21800v1](https://arxiv.org/abs/2605.21800v1)
