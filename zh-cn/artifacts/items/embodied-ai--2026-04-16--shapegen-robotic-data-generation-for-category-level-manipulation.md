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
ShapeGen 通过把被操作物体替换成同一类别中的其他形状，生成新的机器人操作演示，同时保持交互在物理上合理、功能上正确。论文针对的是类别级操作，也就是策略必须处理未见过的杯子、壶和其他形状差异很大的物体。

## 问题
- 机器人策略在未见过的同类物体上经常失效，因为动作轨迹依赖物体几何形状，尤其是在挂杯子、从水壶倒水这类细粒度任务中。
- 要覆盖很多物体形状并收集真实演示，成本很高，因为需要大量实体物体和大量人工劳动。
- 之前的数据生成方法要么只关注纹理、视角或配置变化，要么只处理简单的抓取放置任务，要么依赖仿真和有限的形状变化，例如轴对齐缩放。

## 方法
- ShapeGen 为每个物体类别构建一个 **Shape Library**。这个库保存 3D 物体模型，以及从公共模板到每个形状的学习得到的稠密空间变形。
- 核心机制是学习形状之间的点到点变形，并用来自有符号距离函数（SDF）的几何监督训练。这样系统可以把一个物体上的功能点，例如杯柄内侧，对应到另一种形状上的功能点。
- 对于真实的源演示，人工每个演示只需做一次最少标注：任务相关关键点、对齐代价和夹爪关键点。论文说这一步大约每个源演示需要 **1 分钟**。
- 利用学到的变形，ShapeGen 为新的物体形状计算对齐结果，调整夹爪平移量以保持抓取有效，并通过替换原始物体、移动分割后的机器人手臂点云来合成新的 3D 观测。
- 这个系统不依赖仿真，走的是 real-to-real 路线：使用扫描得到的真实物体、RGB-D 观测、物体跟踪和 3D 合成，而不是在仿真里执行任务。

## 结果
- 在 **hang_mug** 上，未见过的物体实例成功率从仅用源数据训练时的 **1/20（5%）** 提升到使用 ShapeGen 数据后的 **9/20（45%）**。
- 在 **hang_mug_hard** 上，成功率从 **1/20（5%）** 提升到 **10/20（50%）**。
- 在 **serve_kettle** 上，成功率从 **7/20（35%）** 提升到 **15/20（75%）**。
- 在 **pour_water** 上，成功率从 **11/20（55%）** 提升到 **12/20（60%）**。
- 主实验中的训练数据规模是：对 **4** 个任务中的每个任务，作者收集 **5** 条远程操作的源演示，每条都来自一个物体实例，并且每条源演示生成 **15** 条新演示。
- 论文的主要结论是，免仿真的 real-to-real 形状增强能提升细粒度操作在未见物体形状上的类别级泛化，其中最大报告提升出现在 **hang_mug_hard** 和 **hang_mug**，都是 **+40** 个百分点。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15569v1](http://arxiv.org/abs/2604.15569v1)
