---
source: arxiv
url: https://arxiv.org/abs/2606.02274v1
published_at: '2026-06-01T14:01:11'
authors:
- Huayi Zhou
- Wei Gao
- Dekun Lu
- Ruiji Liu
- Zhanqi Zhang
- Ziyang Zhang
- Jian Chen
- Wenlve Zhou
- Sheng Xu
- Shumin Li
- Kangyi Guo
- Shichen Xu
- Zixin Huang
- Yongyi Su
- Kui Jia
topics:
- vision-language-action
- robot-foundation-model
- dexterous-manipulation
- bev-representation
- robot-data-scaling
- cross-embodiment
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning

## Summary
## 摘要
Dex-BEV 通过 3D 对齐的视觉输入和动作来训练机器人操作策略，同时保持与 2D VLM 主干的兼容性。论文声称，它在跨机体和跨视角泛化上优于 2D VLA 基线。

## 问题
- 现有 VLA 策略常用 2D RGB 输入，因此缺少精细操作所需的显式 3D 几何信息。
- 机器人数据集使用不同的相机位姿、机器人坐标系、动作约定和执行速度，这给学习目标带来了本可避免的变化。
- 这很重要，因为通用机器人策略需要在混合机体和数据集上训练，而不用重新学习相机特定或机器人特定的坐标习惯。

## 方法
- Dex-BEV 根据相机标定和可用深度，把每个图像像素转成 3D 点，生成与 RGB 特征保持像素对齐的 aligned vertex map。
- 它把多视角视觉几何、机器人本体感知和输出动作都表达在同一个共享 3D 坐标系中。
- 这个共享坐标系是一个规范的鸟瞰图（BEV）坐标系，通常是机器人基座坐标系，或桌面工作区底部中心。
- 它通过把所有相机的聚合彩色点云投影到俯视图，构造合成 BEV 图像。
- 对于只有 RGB 的相机，它使用 vertex spectrum：每个像素采样多个深度假设，并将这些假设编码为供 VLM 使用的 3D 位置特征。

## 结果
- 在官方 LIBERO 上，Dex-BEV 用一个跨机体检查点达到 97.8% 的平均成功率；X-VLA 为 98.1%，π₀ 为 94.2%，2D 消融版为 92.8%。
- 在 RoboTwin 2.0 Clean 上，Dex-BEV 的成功率为 76.0%；X-VLA 为 70.0%，π₀ 为 46.4%，2D 消融版为 64.8%。
- 在 RoboTwin 2.0 Randomized 上，Dex-BEV 的成功率为 42.0%；X-VLA 为 39.0%，π₀ 为 16.4%，2D 消融版为 35.2%。
- 在修改后的 LIBERO 中，相机视角以及场景或机器人基座位姿发生变化时，Dex-BEV 的平均成功率为 89.9%；文中报告 X-VLA 和 2D 消融版都低于 10%。
- 在修改后的 LIBERO 任务套件上，Dex-BEV 的结果是 Spatial 92.8%、Object 89.4%、Goal 91.0%、Long 86.2%。
- 在可见的真实世界片段中，Dex-BEV 在 Agilex Fold Mailer Box 任务上完成了 23/30 次试验，即 76.7%；X-VLA 为 17/30，即 56.7%；π₀ 为 13/30，即 43.3%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02274v1](https://arxiv.org/abs/2606.02274v1)
