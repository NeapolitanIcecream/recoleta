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
## 摘要
HANDFUL 训练 LEAP Hand 在抓住一个物体的同时，为后续动作保留可用手指。它面向序贯灵巧操作，其中稳定的初始抓取可能会阻碍第二个任务。

## 问题
- 论文研究两步灵巧操作任务：先抓住一个物体，然后在仍然握住第一个物体的情况下，推、按、扭、拉或拾取另一个物体。
- 这很重要，因为只针对稳定性优化的抓取可能会占用下一个动作所需的手指或掌部空间。
- 以往的灵巧操作研究通常只研究一个物体或一种技能，因此遗漏了序列中的手指分配问题。

## 方法
- HANDFUL 将手指视为有限资源。部分手指用于第一次抓取，其他手指保持不活动，以供第二个任务使用。
- 抓取奖励加入了活动手指接触奖励和非活动手指接触力惩罚，使选定手指握住物体，未使用手指避免接触。
- 它在 4 指 LEAP Hand 上，用一指和两指组合以及两种初始手部姿态训练了 9 个抓取策略。
- 对于每个第二任务，它从终止抓取状态训练第二阶段策略，然后使用 3 阶段课程来保留最佳候选：C0 中有 9 个策略，C1 中保留 6 个，C2 中保留 3 个。
- 在真实部署中，它使用 SAM2 分割和融合点云，检索一条成功的仿真轨迹，其初始物体姿态与观测到的真实姿态最匹配。

## 结果
- 在仿真中，跨 5 个随机种子，HANDFUL 在 Push Object 上达到 69.90±5.54% 的成功率，在 Press Button 上达到 77.75±2.15%，在 Twist Knob 上达到 61.52±5.47%，在 Pull Drawer 上达到 78.94±1.77%，在 Pick Second 上达到 76.54±3.63%。
- 仅针对抓取训练时，第一阶段抓取策略达到 94.67±2.60% 的平均抓取成功率。
- 移除手指约束后，Push Object 成功率降至 66.69±5.66%，Press Button 降至 44.26±40.58%，Twist Knob 降至 49.44±5.73%，Pull Drawer 降至 58.99±17.36%，Pick Second 降至 0.00±0.00%。
- 基于阶段的单环境基线在 Push Object 上达到 32.38±6.36%，在 Press Button 上达到 10.08±19.23%，在 Twist Knob、Pull Drawer 和 Pick Second 上均为 0.00±0.00%。
- 与非课程训练相比，课程训练保持了相近的最终成功率，同时将第二阶段训练从 9000 万步减少到 5400 万步，减少 40%。
- 论文报告了真实 LEAP Hand 验证，但摘录未给出真实世界成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25126v1](https://arxiv.org/abs/2604.25126v1)
