---
source: arxiv
url: http://arxiv.org/abs/2603.06450v1
published_at: '2026-03-06T16:42:46'
authors:
- Jonathan Yang
- Chelsea Finn
- Dorsa Sadigh
topics:
- robot-learning
- cross-embodiment-transfer
- data-centric-learning
- trajectory-pairing
- vision-language-action
relevance_score: 0.16
run_id: materialize-outputs
---

# Data Analogies Enable Efficient Cross-Embodiment Transfer

## Summary
本文研究在机器人跨形态迁移中，什么样的数据组织方式最有效。核心结论是：相比单纯扩大异构演示数据规模，具有跨机器人对应关系的“数据类比”（尤其是轨迹级配对）更能提升少样本目标机器人上的迁移效果。

## Problem
- 论文要解决的是：当目标机器人只有少量演示数据时，如何利用其他机器人、视角和场景的数据实现高效跨 embodiment 迁移。
- 这很重要，因为当前通用机器人策略常依赖大规模异构数据，但并不清楚真正起作用的是“数据量/多样性”还是“跨机器人可对应的结构”。
- 特别是形态差异（如夹爪、运动学）比视觉差异更难迁移；若只做无结构的数据堆叠，策略可能无法学到可复用的动作对应关系。

## Approach
- 作者只改变**数据组成方式**，不改模型结构或训练算法：从预训练的 VLA/π0.5 风格策略出发，与目标机器人 50-shot few-shot 数据共同微调。
- 将跨 embodiment 差异分成三条轴：**viewpoint、morphology、appearance**，并在固定预算下系统比较两类因素：**coverage**（targeted vs. diverse）与 **pairing**（unpaired / task-paired / trajectory-paired）。
- 所谓**data analogies**，就是不同机器人之间在相同场景、任务甚至相似轨迹上的配对演示；其中 trajectory-paired 通过对同一任务实例的轨迹做 DTW 对齐，尽量让不同机器人执行“同一种动作策略”。
- 论文提出组合式数据配方：对感知类偏移（viewpoint、appearance）强调更广覆盖；对 morphology 强调更强配对，再把这些子数据集按固定预算混合成 compositional dataset。
- 在与开源数据结合时，作者还对 OXE 做覆盖重加权，并注入 40% trajectory-paired 数据，形成 **OXE+Translational**。

## Results
- 在真实世界实验中，仅通过改变数据组成，**跨 embodiment 迁移成功率平均比大规模未配对数据高 22.5%**。
- 在仿真中，作者报告其 compositional / translational 数据策略相对大规模开源未配对数据（如 OXE）**平均提升 19% 成功率**，且在两个目标机器人、四个 RoboCasa 任务上持续占优。
- 对 morphology 轴，**paired vs. unpaired 的平均差距约为 23%**；而 targeted vs. diverse 在 trajectory-paired 条件下只相差不大（文中示例 **62% vs. 64%**），说明形态迁移的关键不是盲目增广，而是跨机器人对应关系。
- 对 viewpoint 与 appearance，随着多样性增加，性能**平均提升约 17%**；同时 trajectory pairing 相比较弱配对方式仍保持**平均约 6%**优势。
- 仅增加 morphology 多样性几乎无效：文中给出的曲线示例从**42% 仅升到 44%**，表明如果没有显式配对，更多机械臂/夹爪并不能自动带来动作迁移。
- 论文还给出具体训练设定：目标 few-shot 与 translational data 通常各 **50 demonstrations**，真实机器人实验涉及 **Franka、WidowX、PiperX**，仿真统计基于 **100 个随机种子**，真实实验基于 **5 个随机初始化**。

## Link
- [http://arxiv.org/abs/2603.06450v1](http://arxiv.org/abs/2603.06450v1)
