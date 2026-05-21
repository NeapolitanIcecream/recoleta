---
source: arxiv
url: https://arxiv.org/abs/2605.17556v1
published_at: '2026-05-17T17:37:34'
authors:
- Peter Schaldenbrand
- Jean Oh
topics:
- robotic-sculpting
- deformable-manipulation
- visual-planning
- dynamics-modeling
- long-horizon-planning
- sim2real
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# Visual Sculpting: Visually-Aligned Planning Representations for Long-Horizon Robot Clay Sculpting

## Summary
## 摘要
Visual Sculpting 是一种机器人黏土雕塑方法，在稠密深度图和空间深度梯度上进行规划，使机器人能够同时针对 3D 形状和可见表面细节。它从机器人生成的推压动作中学习深度变化动力学模型，并使用 MPC 执行长动作序列。

## 问题
- 以往的可变形物体方法通常需要为每个目标重新训练一个策略，或在约 300 个点的稀疏点云上规划；这些点云会漏掉影响雕塑外观的表面纹理和明暗线索。
- 黏土浮雕雕塑需要许多受控动作、材料在大面积表面上的移动，以及精细的局部细节；早期面团工作中使用的夹爪捏合会让长时域雕塑变得难以控制。
- 这个问题重要，因为只匹配粗略 3D 形状的机器人仍可能漏掉人们用来评价雕塑的视觉特征。

## 方法
- 状态是 512×512 的稠密深度图。视觉规划信号是该深度图的空间梯度，用于捕捉与光照和纹理相关的局部表面变化。
- 每个机器人动作都是一次线性推压，参数包括 x、y、方向 θ、行程长度 l 和深度 z。主系统使用单个末端执行器，并将其与夹爪捏合基线比较。
- 神经动力学模型 param2deform 根据当前深度图、其梯度，以及推压形状参数 l 和 z，预测一个动作造成的深度变化。
- 模型先在固定姿态下预测形变，再用可微的透视变换把预测结果平移和旋转到请求的 x、y 和 θ。这减少了所需的机器人数据量。
- 规划使用 MPC：贪心动作初始化、梯度下降或 CEM 优化、执行一小批动作、重新扫描，并根据 3D 损失和视觉损失重新规划。

## 结果
- 在留出形变预测上，加入视觉损失改善了泡沫材料指标：L3D 从 0.138 降至 0.130，Lviz 从 0.025 降至 0.024，Chamfer Distance 从 0.26 降至 0.22，EMD 从 0.16 降至 0.15。列出的所有指标都是越低越好。
- 在面团上，加入视觉损失使 L3D 从 0.190 降至 0.187，Lviz 从 0.029 降至 0.028，Chamfer Distance 从 0.45 降至 0.41，EMD 从 0.31 降至 0.30。
- 在沙子上，视觉损失只改善了 Lviz，从 0.012 降至 0.011；L3D 从 0.043 变差到 0.047，Chamfer Distance 和 EMD 保持在 0.40 和 0.22。
- 在泡沫材料上，单末端执行器推压比夹爪捏合更容易建模：使用 L3D+Lviz 的推压结果为 L3D 0.130、Lviz 0.024、CD 0.22、EMD 0.15；夹爪捏合结果为 L3D 0.624、Lviz 0.043、CD 0.50、EMD 0.30。
- 该动力学模型用约 100 个机器人动作学到了有用的状态转移；随着样本增加，性能进一步提高。
- 该系统生成了超过 100 个动作的长时域雕塑，包括在不重置黏土的情况下完成从 A 到 F 的字母序列，以及一个 50 个动作的 X 雕塑；执行过程中 3D 损失和视觉损失都下降了。摘录没有给出这些规划运行的最终数值损失。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17556v1](https://arxiv.org/abs/2605.17556v1)
