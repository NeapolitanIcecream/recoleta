---
source: arxiv
url: https://arxiv.org/abs/2604.25126v1
published_at: '2026-04-28T02:04:50'
authors:
- Ethan Foong
- Yunshuang Li
- Hao Jiang
- Gaurav S. Sukhatme
- Daniel Seita
topics:
- dexterous-manipulation
- sequential-manipulation
- resource-aware-grasping
- sim2real
- robot-benchmark
- reinforcement-learning
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness

## Summary
## 总结
HANDFUL 训练一只 LEAP Hand 在抓住一个物体的同时，给后续动作保留可用手指。它面向顺序灵巧操作，其中稳定的第一次抓取可能会阻碍第二个任务。

## 问题
- 这篇论文处理两步灵巧任务：先抓住一个物体，再在仍握住第一个物体的同时推动、按压、旋转、拉动，或抓取另一个物体。
- 之所以重要，是因为只针对稳定性优化的抓取，可能会占用后续动作需要的手指或掌部空间。
- 以往的灵巧操作研究往往只看一个物体或一种技能，因此没有处理一串动作中的手指分配。

## 方法
- HANDFUL 把手指当作有限资源。部分手指用于第一次抓取，另一部分手指为第二个任务保留。
- 抓取奖励加入了有源手指接触奖励和无源手指接触力惩罚，这样被选中的手指负责 удерж住物体，未使用的手指尽量不接触物体。
- 它在一只 4 指 LEAP Hand 上，用单指和双指组合训练了 9 个抓取策略，初始手部姿态有两种。
- 对每个第二任务，它从最终抓取状态训练第二阶段策略，再用 3 阶段课程保留最佳候选：C0 中 9 个策略，C1 中剩 6 个，C2 中剩 3 个。
- 面向真实部署时，它用 SAM2 分割和融合点云，检索一个成功的仿真轨迹，其初始物体姿态与观察到的真实姿态最接近。

## 结果
- 在 5 个随机种子下的仿真中，HANDFUL 在推物体、按按钮、旋钮、拉抽屉和抓第二个物体任务上的成功率分别为 69.90±5.54%、77.75±2.15%、61.52±5.47%、78.94±1.77% 和 76.54±3.63%。
- 只为抓取训练时，第一阶段抓取策略的平均抓取成功率达到 94.67±2.60%。
- 去掉手指约束后，成功率降到推物体 66.69±5.66%、按按钮 44.26±40.58%、旋钮 49.44±5.73%、拉抽屉 58.99±17.36%、抓第二个物体 0.00±0.00%。
- 基于阶段的单环境基线在推物体上达到 32.38±6.36%，在按按钮上达到 10.08±19.23%，在旋钮、拉抽屉和抓第二个物体上都为 0.00±0.00%。
- 课程训练在保持与非课程训练相近的最终成功率的同时，把第二阶段训练从 9000 万步降到 5400 万步，减少了 40%。
- 论文报告了真实 LEAP Hand 验证，但摘要片段没有给出真实世界成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25126v1](https://arxiv.org/abs/2604.25126v1)
