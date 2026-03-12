---
source: arxiv
url: http://arxiv.org/abs/2603.06450v1
published_at: '2026-03-06T16:42:46'
authors:
- Jonathan Yang
- Chelsea Finn
- Dorsa Sadigh
topics:
- cross-embodiment-transfer
- robot-data-scaling
- vision-language-action
- trajectory-pairing
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
---

# Data Analogies Enable Efficient Cross-Embodiment Transfer

## Summary
本文研究跨机器人形态迁移时，哪些数据组织方式最有效。结论是：相比单纯增加异构演示数量，带有跨机器人“数据类比”的配对演示，尤其是轨迹级配对，更能提升少样本跨具身迁移效果。

## Problem
- 论文解决的是：在目标机器人只有少量示例时，如何利用其他机器人、视角和场景的数据来提升目标机器人的任务成功率。
- 这很重要，因为通用机器人策略越来越依赖大规模异构数据，但目前并不清楚真正有用的是“更多数据”还是“更有结构的数据”。
- 尤其在形态差异（不同夹爪/机械臂）下，简单堆数据可能无法学到可迁移的控制对应关系。

## Approach
- 不改模型结构或训练算法，只研究**数据组成**：在固定预算下比较 coverage（targeted vs. diverse）和 pairing（unpaired / task-paired / trajectory-paired）。
- 提出 **data analogies**：跨具身但在场景、任务实例或执行轨迹上保持对应的演示，让模型看到“不同机器人如何做同一件事”。
- 在仿真中系统控制三类分布偏移：**viewpoint、morphology、appearance**；在真实机器人上验证趋势是否成立。
- 轨迹配对通过 **DTW** 对齐同一任务实例下的跨机器人轨迹；训练时将这些“translation dataset”与目标机器人的 50-shot 数据按 50:50 共同微调到预训练 VLA（pi\_0.5-style）上。

## Results
- 在仿真中，相比大规模但无配对的开放数据集 **OXE**，作者的组合式 **OXE+Translational** 数据设计平均提升 **19% success rate**。
- 在真实世界实验中，仅改变数据组成，就比大规模无配对数据平均提升 **22.5% success rate**。
- 对 **morphology** 偏移，配对比单纯多样性更关键：论文报告 targeted-trajectory-paired 与 diverse-trajectory-paired 分别约 **62% vs. 64%**，但“paired 与 unpaired”的平均差距约 **23%**。
- 对 **viewpoint** 和 **appearance**，增加多样性更有效；随着多样性提升，成功率平均增加约 **17%**，且 trajectory pairing 仍平均比较弱配对方案高 **6%**。
- 对 **morphology scaling**，不带配对时增加多样性几乎无效，性能仅约 **42% -> 44%**；说明更多机械臂/夹爪样本本身不足以跨越控制与运动学差异。
- 实验设置上，真实世界每个迁移方向使用 **50** 个源机器人演示、每轴/场景/机器人 **50** 个 translational 演示；仿真结果基于 **100** 个随机种子，真实世界基于 **5** 个随机初始化。

## Link
- [http://arxiv.org/abs/2603.06450v1](http://arxiv.org/abs/2603.06450v1)
