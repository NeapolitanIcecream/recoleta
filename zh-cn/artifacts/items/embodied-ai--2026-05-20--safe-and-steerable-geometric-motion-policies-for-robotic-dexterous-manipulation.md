---
source: arxiv
url: https://arxiv.org/abs/2605.21811v1
published_at: '2026-05-20T23:16:01'
authors:
- Albert Wu
- Riccardo Bonalli
- Thomas Lew
- C. Karen Liu
topics:
- dexterous-manipulation
- control-barrier-functions
- geometric-control
- motion-policy
- in-hand-reorientation
- robot-safety
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# Safe and Steerable Geometric Motion Policies for Robotic Dexterous Manipulation

## Summary
## 摘要
SafePBDS 通过把任务空间目标和定义在不同流形上的硬安全约束结合起来，生成灵巧机器人运动。它面向多指手的实时抓取和手内重定向，高层动作可以引导运动，同时安全约束始终生效。

## 问题
- 灵巧操作把目标和约束混在关节空间、末端执行器位姿空间、接触几何、距离边界和力闭合条件里。控制器必须在控制频率下协调这些要求。
- 先前的 PBDS 方法把流形任务按几何一致性组合起来，但安全通常以软代价进入，在目标冲突时可能被违反。
- 学习型灵巧策略往往需要大量任务专用数据，并且在训练分布之外会失效，因此对硬件手来说，显式的在线安全很重要。

## 方法
- SafePBDS 通过平滑任务映射，把任务流形上的目标和安全条件映回机器人配置流形，然后求解一个二次规划，输出一个配置空间加速度指令。
- Pullback 控制屏障函数把任意任务流形上的安全函数转换为配置加速度上的线性约束。
- 论文为这个设置推导了两种高阶 CBF 形式：指数 CBF 和 backstepping CBF。
- 自主 PBDS 行为保留在加权最小二乘目标里，安全约束作为 QP 中的硬约束执行。
- 任务流形动作接口允许高层策略加入低维残差指令；零输入会恢复自主行为，而任意输入都会被同一组安全约束过滤。

## 结果
- 在 23 自由度的 Franka Panda 加 Allegro Hand 硬件灵巧抓取实验中，SafePBDS 在 20 个家用物体和 120 次试验中报告了 92.5% 的成功率，即 111 次成功试验。
- 通过动作接口，系统可以在抓取时用一维动作排除四根手指中的任意一根。
- 在三指抓取测试中，系统在 3 个物体和 36 次试验中报告了 94.4% 的成功率，即 34 次成功试验。
- 在手内重定向中，该方法在完全驱动的掌朝下 Allegro Hand 设置下，在不同物体重量和手腕运动条件下，报告了两个方向都超过 360° 的 yaw 旋转。
- 摘要称，针对 S² 双积分器和 7 自由度机械臂的仿真测试验证了图表不变性、度量效应、从不安全状态恢复以及动作接口，但所示文本没有给出仿真的数值指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21811v1](https://arxiv.org/abs/2605.21811v1)
