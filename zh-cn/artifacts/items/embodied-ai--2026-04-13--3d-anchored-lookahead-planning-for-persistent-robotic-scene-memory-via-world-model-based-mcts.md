---
source: arxiv
url: http://arxiv.org/abs/2604.11302v1
published_at: '2026-04-13T11:01:30'
authors:
- Bronislav Sidik
- Dror Mizrahi
topics:
- world-model-planning
- monte-carlo-tree-search
- robot-scene-memory
- vision-language-action
- embodied-ai
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# 3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS

## Summary
## 摘要
本文提出 3D-ALP，一种在测试时用于机器人操作的规划方法。它保留持续的 3D 相机位姿记忆，并结合世界模型和 MCTS 做展开。核心观点是，这个持续的 3D 锚点可以修复反应式 vision-language-action 策略在目标物体离开视野时的失效。

## 问题
- 反应式 VLA 风格的机器人策略把当前图像直接映射为动作，所以一旦物体被遮挡或移出画面，就会丢失对这些物体的跟踪。
- 这个问题在多步操作中很重要，因为机器人可能需要回到之前看过的位置，或者在一串动作之后对已经不可见的物体做操作。
- 论文认为这主要是架构层面的记忆问题，而不只是模型容量问题：没有显式的场景记忆状态，策略就只能猜。

## 方法
- 3D-ALP 保存持续的 camera-to-world 位姿 `c2w ∈ SE(3)`，并在每次真实动作后用正向运动学更新它，这样即使发生遮挡，访问过的位置仍然可以被再次定位。
- 它使用 3D 一致的世界模型 InSpatio-WorldFM，从候选未来 `c2w` 位姿渲染预测视图，然后在这些想象状态上运行 Monte Carlo Tree Search。
- 每执行一次动作后，MCTS 树会重新以新的根节点为起点，而不是直接丢弃，这样之前探索过的空间状态就保留下来，充当记忆。
- 一个混合评分器把语义图像分数和几何距离惩罚结合起来，避免规划器在三维空间里机械臂还离得很远时，仅凭二维视觉重叠就过度相信结果。
- 该方法还为机器人控制加入了四个实用的 MCTS 修正：去掉零动作陷阱、在重新设根后重置节点深度、用最大值而不是均值做回传，以及把 UCB 探索常数设得更小（`c = 0.02`）。

## 结果
- 在带 Franka Panda 的 MuJoCo E3 多步一致性任务上，3D-ALP 的记忆任务成功率是 `0.650 ± 0.109`，贪心反应式基线是 `0.006 ± 0.008`，提升 `+0.645`。
- 在最难的链式记忆步骤（第 5 步）上，贪心成功率为 `0.000`，深度 `D=1` 的 MCTS 达到 `0.622`，而 `D=2` 的 3D-ALP 达到 `0.822`，说明更深的前瞻在这一步带来 `+0.200`。
- 论文指出，在需要记忆的步骤上，反应式基线的成功率降到约 `0.6%`，而 3D-ALP 维持在约 `65%`；图 1 也报告第 5 步性能为 `82.2%`，贪心为 `0.0%`。
- 消融实验表明，持续的树记忆是提升的主要来源：`D=1` 的 MCTS 在记忆任务上的成功率为 `0.539 ± 0.064`，已经远高于贪心的 `0.006 ± 0.008`。
- 在不需要记忆的步骤上，表中显示贪心比浅层 MCTS 更强：贪心为 `0.748 ± 0.029`，`D=1` MCTS 为 `0.389 ± 0.024`，这支持了论文的判断，即收益主要集中在由遮挡触发的记忆步骤上。
- 组件检查在仿真中报告了完全的几何一致性：`SSIM = 1.000`，`ORB = 1.000`，5 条轨迹中匹配了 `391/391` 个关键点，还包括运动学桥接角误差 `0.00°`、在 `≤5°` 阈值下 `100%` 通过率，以及桥接延迟 `0.5 ms`。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11302v1](http://arxiv.org/abs/2604.11302v1)
