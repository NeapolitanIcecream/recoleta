---
source: arxiv
url: https://arxiv.org/abs/2605.06311v1
published_at: '2026-05-07T14:13:05'
authors:
- Yixin Zhu
- Zixiong Wang
- Jian Yang
- Jin Xie
- Jingyi Yu
- Jiayuan Gu
- Beibei Wang
topics:
- robot-manipulation
- simulation-benchmark
- sim2real
- vision-language-action
- pbr-assets
- visual-realism
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Toward Visually Realistic Simulation: A Benchmark for Evaluating Robot Manipulation in Simulation

## Summary
## 摘要
VISER 是一个面向机器人操作的视觉真实仿真基准，针对 VLA 评估中的视觉仿真到现实差距。它通过加入 PBR 材质、镜面反射线索和柔和阴影，报告了与真实世界策略结果更高的一致性。

## 问题
- 现有机器人操作基准常常简化光照和材质，因此仿真中的 VLA 成功率可能与真实世界成功率不一致。
- 论文指出，镜面高光和接触阴影是影响几何推理和空间定位的视觉线索。
- 这一点很关键，因为真实机器人评估成本高，只有在仿真能够预测真实世界策略行为时才有用。

## 方法
- VISER 构建了一个 3D 资产集，包含 319 个类别、12 个超类中的 1,049 个对象，并使用干净的 PBR 材质。
- 资产流水线从 32 个视角渲染每个对象，使用 MLLM 识别具备材质信息的部件，检索匹配材质，使用 SAM3 生成部件掩码，然后将掩码投影到 UV 空间用于 PBR 纹理贴图。
- 第二个 MLLM 检查掩码质量，并在掩码遗漏对象部件时添加重新分割提示。
- 场景布局根据描述或图像生成：提取对象，构建场景图，估计 2D 桌面坐标，并在仿真中实例化对象。
- 该基准包含 14 个人工整理任务、8 个重建的真实世界任务、生成任务、拿起和放入等基础技能，以及使用 Qwen-3-VL Agent Score 评分的长程任务。

## 结果
- VISER 报告称，在不同策略上，仿真性能与真实世界性能之间的平均 Pearson 相关系数为 0.92。
- 在仿真到现实相关性测试中，Octo 在 VISER 中达到 r=0.9988，而在 SimplerEnv 中为 r=0.8860；OpenVLA 在 VISER 中达到 r=0.8496，而在 SimplerEnv 中为 r=-0.2712。
- 镜面高光将 eggplant-in-pot 步骤的成功率从无镜面高光时的 10% 提高到有镜面高光时的 90%，真实世界为 100%；抓取茄子在三种设置下都保持 100%。
- 柔和阴影将 put-spoon-on-towel 成功率提高到 49%，相比之下，无阴影为 12%，硬阴影为 0%，真实世界为 42%。
- 资产质量分数高于 RoboTwin 和 ManiTwin：VISER 的 VLM-S 为 55.35、CLIP-S 为 25.20，RoboTwin 为 45.66/21.35，ManiTwin 为 38.27/20.75。
- 基准表报告 VISER 拥有 1,049 个资产、319 个资产类别，以及 22 个加生成任务，并包含柔和阴影、镜面渲染、干净 PBR 材质和经过验证的仿真到现实相关性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06311v1](https://arxiv.org/abs/2605.06311v1)
