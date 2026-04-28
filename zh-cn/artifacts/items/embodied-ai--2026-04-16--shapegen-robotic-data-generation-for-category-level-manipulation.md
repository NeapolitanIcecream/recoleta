---
source: arxiv
url: http://arxiv.org/abs/2604.15569v1
published_at: '2026-04-16T22:55:39'
authors:
- Yirui Wang
- Xiuwei Xu
- Angyuan Ma
- Bingyao Yu
- Jie Zhou
- Jiwen Lu
topics:
- robot-data-generation
- category-level-manipulation
- sim2real
- shape-correspondence
- pointcloud-policy
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# ShapeGen: Robotic Data Generation for Category-Level Manipulation

## Summary
## 摘要
ShapeGen 通过将操作中的物体替换为同一类别中的其他形状，同时保持交互在物理上合理、在功能上正确，来生成新的机器人操作示范。论文关注类别级操作，也就是策略必须处理从未见过的杯子、水壶和其他形状差异很大的物体。

## 问题
- 机器人策略在同一类别中遇到未见过的物体时常会失败，因为动作轨迹依赖物体几何形状，尤其是在挂杯子或用水壶倒水这类精细任务中。
- 为大量不同形状的物体收集真实示范成本很高，因为这需要许多实体物体和大量人工劳动。
- 以往的数据生成方法要么主要关注纹理、视角或配置变化，要么只能处理简单的抓取放置任务，要么依赖仿真，并且只能处理有限的形状变化，例如沿坐标轴缩放。

## 方法
- ShapeGen 为每个物体类别构建一个 **Shape Library**。这个库保存 3D 物体模型，以及从一个公共模板到各个形状的稠密空间形变。
- 核心机制是一个在形状之间学习点对点形变的模型，训练时使用 signed distance functions (SDFs) 提供的几何监督。这使系统可以把一个物体上的功能点，例如杯把内侧，对应到另一种形状上的相应功能点。
- 对于一个真实的源示范，人类每个示范只需做一次少量标注：任务相关关键点、一个对齐代价和一个夹爪关键点。论文称每个源示范大约需要 **1 分钟**。
- 利用学到的形变，ShapeGen 为新物体形状计算对齐，调整夹爪平移以保持抓取有效，并通过替换原始物体、移动分割后的机器人手臂点云，合成新的 3D 观测。
- 该系统不使用仿真器，并且是 real-to-real：它使用扫描得到的真实物体、RGB-D 观测、物体跟踪和 3D 合成，而不是在仿真中运行任务。

## 结果
- 在 **hang_mug** 上，未见过物体实例的成功率从只用源数据训练时的 **1/20 (5%)** 提升到使用 ShapeGen 数据时的 **9/20 (45%)**。
- 在 **hang_mug_hard** 上，成功率从 **1/20 (5%)** 提升到 **10/20 (50%)**。
- 在 **serve_kettle** 上，成功率从 **7/20 (35%)** 提升到 **15/20 (75%)**。
- 在 **pour_water** 上，成功率从 **11/20 (55%)** 提升到 **12/20 (60%)**。
- 主实验中的训练数据规模：作者针对 **4 个任务**，每个任务用一个物体实例收集 **5** 个遥操作源示范，并为每个源示范生成 **15** 个新示范。
- 论文的主要结论是，无需仿真的 real-to-real 形状增强能提升精细操作在未见过物体形状上的类别级泛化能力，其中报告的最大增益出现在 **hang_mug_hard**，为 **+40 个百分点**，**hang_mug** 上也是 **+40 个百分点**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15569v1](http://arxiv.org/abs/2604.15569v1)
