---
source: arxiv
url: http://arxiv.org/abs/2603.08124v1
published_at: '2026-03-09T09:03:25'
authors:
- Xiang Shi
- Wenlong Huang
- Menglin Zou
- Xinhai Sun
topics:
- vision-language-action
- robot-foundation-model
- compute-aware-control
- hierarchical-policy
- feature-caching
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
---

# SaiVLA-0: Cerebrum--Pons--Cerebellum Tripartite Architecture for Compute-Aware Vision-Language-Action

## Summary
本文提出 SaiVLA-0，一种面向机器人 Vision-Language-Action 的“大小脑分工”三部件架构，把高层语义理解与高速低层控制解耦，并显式围绕算力与时延进行设计。该工作更像概念与协议论文，但给出了初步 LIBERO 证据，显示特征缓存与模块化控制在训练效率和成功率上有潜在收益。

## Problem
- 现有 VLA 往往把语义理解和高频控制耦合在一个大模型里，导致**时延高、控制不稳定、算力成本高**，在小数据场景下尤其容易过拟合。
- 只依赖大模型最后一层表征，往往难以同时兼顾**全局语义**与**局部几何/接触细节**；这对精细操作和灵巧控制很关键。
- 训练与评测常缺少统一的缓存、提示词、校准和算力报告协议，导致**复现困难、比较不公平**。

## Approach
- 提出三部件架构：**Cerebrum** 是冻结的大型 VLM，低频运行，提供稳定的多层语义先验；**Pons Adapter** 把这些高层特征与当前本体状态结合，压缩成可执行上下文 token；**Cerebellum** 用 ParaCAT 高频输出动作。
- ParaCAT 将每个动作维度离散成 **-1/0/+1** 三类，并且**一次前向并行预测 K=20 步**，而不是逐步连续回归；可把它理解为“每个关节只决定下一小步朝正向、停住还是反向”。
- 采用**双频调度**：Cerebrum 每 **N=5** 个控制 chunk 才调用一次，低层控制复用高层语义；这样在尽量不损失任务表现的前提下摊薄大模型成本。
- 采用**两阶段特征缓存训练**：Stage A 离线跑冻结 VLM 并缓存多层特征；Stage B 只训练 Pons + Cerebellum。这样减少重复大模型前向，提高训练速度和可复现性。
- 引入与末端执行器几何绑定的**腕部 ROI**，从主视角中裁出随手部运动稳定变化的高分辨率局部区域，以补充全局视图中的接触与细粒度姿态信息。

## Results
- 论文明确定位为**concept-and-protocol paper with preliminary evidence**，因此完整结论性实验仍未覆盖；作者强调会在匹配 GPU/分辨率/batch 的条件下报告 success、latency、`SR_cn` 等指标。
- 在 **LIBERO** 的初步证据中，**split feature caching** 将训练时间从 **7.5h 降到 4.5h**，同时把平均成功率从 **86.5% 提升到 92.5%**；文中说明该比较是在 **official N1.5 head-only training** 设置下得到的。
- 文中还声称 **SaiVLA-0 在 LIBERO 上达到 99.0% mean success**，但摘录中未给出更细的子集拆分、方差、基线对照表或完整实验条件。
- 体系默认关键配置包括：**Cerebrum 调用频率 N=5**、**单次前向复用 K=20 步**、双臂系统动作维度 **D=16**、主视图 **1028×800→256²**、双腕部 ROI 各 **256²**。
- 论文提出了算力归一化指标 **`SR_cn = SuccessRate / ComputeBudget`**，并主张未来比较应同时报告冷启动 Cerebrum 时延、Cerebellum 单步/单前向时延、前向频率 `f_fwd` 与有效动作频率 `f_eff`；但摘录中**尚无完整定量基准表**。

## Link
- [http://arxiv.org/abs/2603.08124v1](http://arxiv.org/abs/2603.08124v1)
