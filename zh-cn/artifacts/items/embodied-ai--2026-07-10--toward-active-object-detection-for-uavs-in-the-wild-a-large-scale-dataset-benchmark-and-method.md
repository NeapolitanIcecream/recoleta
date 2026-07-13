---
source: arxiv
url: https://arxiv.org/abs/2607.09078v1
published_at: '2026-07-10T03:49:45'
authors:
- Tianpeng Liu
- Xinhua Jiang
- Li Liu
- Qinmu Shen
- Siwei Tang
- Zhen Liu
- Yongxiang Liu
topics:
- active-object-detection
- uav-perception
- world-model
- policy-generalization
- robot-data-scaling
- sim2real
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# Toward Active Object Detection for UAVs in the Wild: A Large-Scale Dataset, Benchmark and Method

## Summary
## 摘要
论文介绍了 ATRNet-LUDO，这是一个面向无人机-地面主动目标检测的大型真实世界基准数据集；同时介绍了 AOD-JEPA，这是一种基于 JEPA 的世界模型，用于提升策略的泛化能力。在无人机运动成本相近的情况下，该方法的识别率高于被动感知和基于 DRL 的基线方法。

## 问题
- 当目标被遮挡、尺寸较小，或从单一位置观察角度不佳时，无人机检测器容易失效。
- 现有主动目标检测数据集主要面向室内机器人或合成无人机场景，限制了真实世界评估。
- 基于 DRL 的主动观测策略在测试环境与训练环境不一致时性能会下降。

## 方法
- 采集 121,000 张多视角全景图像和 1.21 百万个局部目标图块，覆盖 10 类车辆和 40 个室外场景。
- 根据密集的无人机视点构建 200 个多目标环境和 2,000 个单目标环境，并标注目标框、类别、遮挡情况、无人机位姿和目标位置。
- 使用 JEPA 世界模型训练主动观测策略，在执行动作后于潜在空间中预测下一次观测。
- 使用 SAM3 掩码加入面向 AOD 的场景净化，使状态表示更关注目标外观、结构和空间上下文，同时减少背景干扰。
- 设计基准数据划分，用于测试模型在目标-背景布局变化和未见采样区域上的泛化能力，并比较七种 AOD 策略方法。

## 结果
- 与被动目标感知相比，主动观测使目标识别率提高约 20 个百分点。
- 在无人机运动成本相近的测试环境中，采用 AOD-JEPA 的 WMPL 比 DRL 基线方法的目标识别率高 2 至 3 个百分点。
- ATRNet-LUDO 包含 121,000 张全景图像、1,210,000 个局部图块、10 种车辆类型、40 个场景、200 个多目标环境和 2,000 个单目标环境。
- 数据集使用尺寸为 8,000 × 6,000 的全景图像和尺寸为 300 × 300 的局部图块；对于完全遮挡目标的位置预测，平均误差为 53 像素。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09078v1](https://arxiv.org/abs/2607.09078v1)
