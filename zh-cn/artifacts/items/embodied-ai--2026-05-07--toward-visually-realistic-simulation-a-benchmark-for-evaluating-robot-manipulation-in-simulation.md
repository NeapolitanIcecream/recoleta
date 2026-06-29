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
VISER 是一个面向机器人操作的视觉真实感仿真基准，用于评估 VLA 的视觉 sim-to-real 差距。它通过加入 PBR 材料、高光线索和柔和阴影，与真实世界策略结果的一致性更高。

## 问题
- 现有机器人操作基准常常简化光照和材料，因此仿真中的 VLA 成功率可能和真实世界成功率不一致。
- 论文指出，高光反射和接触阴影是会影响几何推理和空间定位的视觉线索。
- 这很重要，因为真实机器人评估成本高，而仿真只有在能预测真实世界策略行为时才有用。

## 方法
- VISER 构建了一个 3D 资产集，包含 1,049 个对象、319 个类别和 12 个超类别，并使用干净的 PBR 材料。
- 资产流程会从每个对象的 32 个视角渲染图像，使用 MLLM 识别考虑材料的部件，检索匹配材料，使用 SAM3 生成部件掩码，然后把掩码投影到 UV 空间进行 PBR 贴图。
- 第二个 MLLM 会检查掩码质量，并在掩码遗漏对象部件时加入重新分割提示。
- 场景布局由描述或图像生成：先提取对象，构建场景图，估计二维桌面坐标，再把对象实例化到仿真中。
- 基准包含 14 个整理过的任务、8 个重建的真实世界任务、生成任务、基础技能任务（如抓取和放入）以及用 Qwen-3-VL Agent Score 评分的长时序任务。

## 结果
- VISER 报告了仿真与真实世界性能之间的平均 Pearson 相关系数为 0.92，覆盖不同策略。
- 在 sim-to-real 相关性测试中，Octo 在 VISER 中达到 r=0.9988，而在 SimplerEnv 中为 r=0.8860；OpenVLA 在 VISER 中达到 r=0.8496，而在 SimplerEnv 中为 r=-0.2712。
- 高光反射把 eggplant-in-pot 步骤的成功率从没有高光时的 10% 提高到有高光时的 90%，真实世界中为 100%；抓取 eggplant 在这三种设置下都保持 100%。
- 柔和阴影把 put-spoon-on-towel 的成功率提高到 49%，而没有阴影时为 12%，硬阴影时为 0%，真实世界中为 42%。
- 资产质量评分高于 RoboTwin 和 ManiTwin：VISER 的 VLM-S 为 55.35、CLIP-S 为 25.20，RoboTwin 为 45.66/21.35，ManiTwin 为 38.27/20.75。
- 基准表将 VISER 列为 1,049 个资产、319 个资产类别和 22 个加生成任务，并包含柔和阴影、高光渲染、干净 PBR 材料以及已验证的 sim-to-real 相关性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06311v1](https://arxiv.org/abs/2605.06311v1)
