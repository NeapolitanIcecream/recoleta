---
source: arxiv
url: https://arxiv.org/abs/2607.19876v1
published_at: '2026-07-22T08:04:17'
authors:
- Zeyu Liu
- Zhangzhe Zhu
- Yang Zhang
- Chenyou Fan
- Chenjia Bai
- Xuelong Li
topics:
- embodied-world-models
- robot-foundation-models
- sim2real
- robot-benchmarking
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# KineBench: Benchmarking Embodied World Models via IDM-Free Kinematic Grounding

## Summary
## 摘要
KineBench 将生成的视频转换为机器人末端执行器的 6D 位姿，并在物理仿真器中测试这些位姿，以评估具身世界模型。其无需 IDM 的运动学落地流程减少了世界模型失效与动作提取失效之间的归因歧义，同时增加了 3D 运动学诊断指标。

## 问题
- 像素级指标和开环视频指标无法证明生成的机器人运动是否能够在物理上执行。
- 现有闭环基准依赖逆动力学模型（IDM），因此失败可能源于生成的视频不符合物理规律，也可能源于 IDM 对新轨迹的泛化能力不足。

## 方法
- 使用 YOLOv11 分割夹爪，使用微调后的 MoGeV2 估计度量深度，并通过 CAD 约束的 FoundationPose 恢复 6D 位姿。
- 在 ManiSkill3 物理仿真器中执行恢复出的位姿序列，以进行闭环任务评估。
- 使用 Spectral Arc Length（SPARC）衡量轨迹平滑度，并使用 Maruyama Manipulability Index 衡量机器人运动学可行性。
- 在四类测试套件中评估 20 项操作任务：基础执行、任务迁移、视觉分布外泛化和复杂度扩展。

## 结果
- 在未见过的轨迹上，使用 MoGeV2 深度的显式流程实现了约 1.5–3 cm 的平移误差，而 Dino3DFlowIDM 基线的误差约为 10 cm；其剩余旋转误差约为 10 度。
- 闭环成功率因模型和测试套件而有较大差异：Wan2.2 5B 在基础执行、任务迁移和未见视觉 OOD 资产上的成功率分别为 56.32%、11.90% 和 55.50%；Wan2.1 1.3B 在相同测试套件上的成功率分别为 43.96%、20.00% 和 52.83%。
- 在复杂度扩展测试套件中，Wan2.1 1.3B 的成功率从训练 1.5k 步时的 44.83% 提升至训练 15k 步时的 73.33%；在训练 7.5k 步时扩大数据规模，规模为 10、25 和 50 时的成功率分别为 53.67%、52.00% 和 51.17%。
- SPARC 和 Maruyama Manipulability Index 与仿真成功率之间的关联取决于任务和模型，因此它们提供的是互补的诊断信号，而不是具有普遍预测能力的指标。
- 该流程仍依赖分割结果、深度质量、末端执行器的可见性以及方向估计，因此它减少了评估归因歧义，但并未完全消除这种歧义。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19876v1](https://arxiv.org/abs/2607.19876v1)
