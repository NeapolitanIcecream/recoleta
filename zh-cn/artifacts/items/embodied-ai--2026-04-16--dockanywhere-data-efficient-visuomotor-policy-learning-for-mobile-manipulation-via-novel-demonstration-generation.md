---
source: arxiv
url: http://arxiv.org/abs/2604.15023v1
published_at: '2026-04-16T13:53:01'
authors:
- Ziyu Shan
- Yuheng Zhou
- Gaoyuan Wu
- Ziheng Ji
- Zhenyu Wu
- Ziwei Wang
topics:
- mobile-manipulation
- imitation-learning
- data-augmentation
- point-clouds
- sim2real
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation

## Summary
## 总结
DockAnywhere 是一种用于移动操作的数据增强方法，它把少量位于一个停靠位姿的示范，转成多个在新停靠位姿下仍保持一致的示范。它针对的是导航误差带来的失效，这类误差会改变机器人底盘位置，并改变操作策略看到的视角。

## 问题
- 两阶段移动操作系统通常先导航到一个停靠位姿，再运行固定底座的操作策略，但轻微的停靠误差会改变机器人的视角，并使策略失效。
- 为许多停靠位姿采集示范成本很高，而先前面向静态操作的数据增强方法无法很好处理底盘重定位。
- 这在家庭和工厂里都很重要，因为真实导航有噪声，操作策略需要在机器人停在未见过的位置时继续工作。

## 方法
- 该方法把策略输入从第一人称视角改为固定的第三人称 RGB-D 视角，这样停靠位置变化就变成了底盘位姿上的几何问题，而不是外观的大幅变化。
- 它把一条示范拆成两部分：自由空间运动片段和接触丰富的技能片段。运动片段是低精度的接近动作；技能片段是与物体交互的阶段，应保持不变。
- 对于一个新的可行停靠点，它保留技能片段，只在可见性、可达性和无碰撞约束下，使用任务与运动规划重规划运动片段，并复用夹爪指令。
- 然后，它直接在三维点云空间里合成新观测，对机器人和物体点进行编辑，并使用与动作相同的空间变换，使观测和动作对齐。
- 生成的示范用于训练行为克隆的视觉运动策略，论文报告的实验中使用 DP3 作为策略头。

## 结果
- 在 ManiSkill 中，使用 5 个停靠点时，DockAnywhere 的总体成功率达到 **78.9%**，高于 **DP3+DemoGen** 的 **74.2%**、**DP3** 的 **17.8%** 和 **DP** 的 **15.8%**。
- 使用 5 个停靠点时的 ManiSkill 任务级结果为：**Pick Banana 97.0%**、**Pick Mug 89.4%**、**Place Can 87.2%**、**Cabinet Door 60.2%**、**Cabinet Drawer 60.6%**。与 **DP3+DemoGen** 相比，除 Pick Banana 外，其余四项任务分别提高 **0.8**、**3.0**、**12.0** 和 **8.6** 个百分点；Pick Banana 低 **1.0** 个百分点。
- 只有 1 个停靠点时，普通 DP3 在 ManiSkill 中的总体成功率为 **88.6%**；但在 5 个停靠点且没有面向移动的增强时，它降到 **17.8%**，这说明了论文要解决的停靠位置变化问题。
- 在增强数量的消融实验中，测试未见过的停靠点时，总体成功率从 **1** 个停靠点时的 **35.5%** 提升到 **2** 个时的 **48.5%**、**4** 个时的 **61.9%**（本文方法）以及 **6** 个时的 **63.9%**。这说明大部分收益在 4 个增强停靠点时就已经出现。
- 论文报告了在一台带单个第三人称相机的移动操作机器人上的真实部署，并声称在源示范数量有限的情况下，平均成功率为 **43.3%**，每条源轨迹的增强开销约为 **0.1 s**。
- 摘要没有给出完整的真实世界表格，因此这里无法提供按任务划分的真实世界基线对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15023v1](http://arxiv.org/abs/2604.15023v1)
