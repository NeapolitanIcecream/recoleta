---
source: arxiv
url: http://arxiv.org/abs/2603.10451v1
published_at: '2026-03-11T06:10:03'
authors:
- Yushan Bai
- Fulin Chen
- Hongzheng Sun
- Yuchuang Tong
- En Li
- Zhengtao Zhang
topics:
- dexterous-manipulation
- few-shot-learning
- data-augmentation
- residual-policy-learning
- sim-to-real
relevance_score: 0.28
run_id: materialize-outputs
---

# FAR-Dex: Few-shot Data Augmentation and Adaptive Residual Policy Refinement for Dexterous Manipulation

## Summary
FAR-Dex面向少样本条件下的灵巧操作学习，把“从少量演示扩增高质量数据”和“在线自适应残差纠错”结合起来，用于多指手与机械臂的协同控制。它试图同时解决示教稀缺、高维动作难控、以及长时程任务中精度和鲁棒性不足的问题。

## Problem
- 灵巧操作需要机械臂与多指手协同，但联合动作空间维度高，长时程任务中容易积累误差，难以稳定控制。
- 真实高质量示教很少，且缺少细粒度手-物体3D交互信息，导致模仿学习数据不足、泛化差、难落地。
- 现有数据增强方法常有仿真到现实落差，现有残差策略又缺乏显式时空建模，难以做阶段敏感的精细修正。

## Approach
- 提出分层框架 FAR-Dex：先用 **FAR-DexGen** 从每个任务仅少量演示中生成大规模、物理可行的合成轨迹，再用 **FAR-DexRes** 对基础策略做在线残差细化。
- 数据生成的核心思路很简单：把演示轨迹切成“接近物体的运动段”和“接触/操作的技能段”，改变物体初始位姿后，重新计算机械臂轨迹并在 IsaacLab 中回放采集，从而得到更多带细粒度接触信息的数据；文中真实系统每个任务仅采集 **2 条专家演示**，采样频率 **20 Hz**。
- 基础策略基于 DP3，但用一致性模型把原来多步去噪推理蒸馏成单步预测，以降低高维点云条件下的推理延迟；点云编码器换成四阶段递归 PointNet，输出 **128 维**嵌入。
- 残差细化模块的机制是：基础动作先给出一个“主动作”，再用跨注意力读取最近 **H=8** 步观察和轨迹片段，生成与动作维度对齐的自适应权重 sigma，对残差动作逐维缩放后加回去；残差策略通过 PPO 训练，实现按任务阶段动态纠错。

## Results
- **数据生成质量**（Insert Cylinder，上游统一用 DP3 评估）：FAR-DexGen 为 **87.9%**，优于 DemoGen 的 **74.5%** 和 MimicGen 的 **68.3%**；相对 DemoGen 提升 **13.4 个百分点**，相对 MimicGen 提升 **19.6 个百分点**。
- **数据生成时间**：FAR-DexGen 为 **10.3 ms/trajectory**，略慢于 DemoGen 的 **9.1 ms** 和 MimicGen 的 **8.3 ms**，但文中强调与最快方法差距仅约 **2 ms**。
- **仿真任务成功率**（FAR-DexRes）：Insert Cylinder **93%**、Pinch Pen **83%**、Grasp Handle **88%**、Move Card **95%**。对应最强基线中，ResiP 在前三项分别为 **85%/79%/80%**，IDP3 在 Move Card 为 **86%**，因此 FAR-DexRes 分别高出 **8/4/8/9 个百分点**。
- **单步推理时间**（FAR-DexRes）：Insert Cylinder **3.0 ms**、Pinch Pen **4.3 ms**、Grasp Handle **3.8 ms**、Move Card **4.3 ms**；相比 DP3 的 **29.1/31.5/29.8/29.6 ms** 明显更快，也略快于或接近 ACT+3D、ManiCM、Flow Policy 等快速基线。
- **总体声明结果**：摘要称 FAR-Dex 相比现有最优方法，任务成功率提升 **7%**，真实任务成功率超过 **80%**，并具备较强的位置泛化能力。摘录未给出更完整真实世界分任务明细。

## Link
- [http://arxiv.org/abs/2603.10451v1](http://arxiv.org/abs/2603.10451v1)
