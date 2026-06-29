---
source: arxiv
url: https://arxiv.org/abs/2605.26638v1
published_at: '2026-05-26T07:19:04'
authors:
- Junyi Dong
- Haotian Luo
- Ziwei Xu
- Shengwei Bian
- Heng Zhang
- Sitong Mao
- Jingyi Guo
- Yang Xu
- Wenhao Chen
- Qiuyu Feng
- Yao Mu
- Ping Luo
- Shunbo Zhou
- Xiaodong Wu
topics:
- sim2real
- robot-manipulation
- synthetic-data
- vision-language-action
- robot-data-scaling
- gaussian-splatting
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation

## Summary
## 总结
HyperSim 是一个面向机器人操控的 sim-to-real 流程，结合了高保真场景渲染、对抗式合成轨迹和 sim-real 联合训练。它的目标是在尽量少采集真实数据的情况下，扩大机器人策略的数据规模。

## 问题
- 机器人策略需要成对的观测-动作数据，而在硬件上采集这些数据速度慢、成本高，也难以扩展。
- 标准仿真数据往往迁移效果较差，因为场景过于干净、物体和位姿覆盖范围较窄，而且接触动力学与真实硬件不同。
- 这会迫使团队采集更多真实示范，或针对每个部署环境重新调参。

## 方法
- HyperSim 将场景拆成可交互前景和重建背景。前景使用基于约束的物体布局和 18 个空间求解器；背景使用结合几何信息的 3D Gaussian Splatting，并融合 LiDAR、RGB 和 IMU 数据。
- 它把操控过程拆成运动原语和交互原语，并围绕目标物体附近的瓶颈位姿生成轨迹。
- 在合成轨迹生成过程中，它会在瓶颈位姿处扰动目标位置和朝向，然后记录恢复动作。这样可以给策略提供纠正行为的示例。
- 它在仅仿真数据上用行为克隆训练 ACT 和 pi0，用于零样本部署，然后把仿真数据与 35 个真实示范混合，用于少样本联合训练。

## 结果
- 该研究报告了在 Galaxea R1 机器人上完成的 400 多次真实任务执行，任务是深桶分拣，并使用 20 次固定评测试验。
- 在零样本迁移中，3DGS-ADSim 用 ACT 达到 25% 的总体成功率（SR3），BaseSim 为 5%。使用 pi0 时，3DGS-ADSim 达到 75% 的 SR3，BaseSim 为 55%。
- 在包含 35 个真实示范的少样本联合训练中，Real35&3DGS-ADSim 用 ACT 达到 80% 的 SR3，用 pi0 达到 95% 的 SR3。
- 同一少样本设置下，ACT 的目标对齐率为 85%，pi0 的目标对齐率为 95%。
- 仅使用真实数据、且包含 35 个示范的基线结果中，ACT 的 SR3 为 60%，pi0 的 SR3 为 70%，低于混合 sim-real 的 HyperSim 结果。
- 论文声称，对抗式轨迹让在物理扰动下的完成率提高了 35%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26638v1](https://arxiv.org/abs/2605.26638v1)
