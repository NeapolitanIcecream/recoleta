---
source: arxiv
url: http://arxiv.org/abs/2603.09121v1
published_at: '2026-03-10T02:55:27'
authors:
- Yifan Han
- Zhongxi Chen
- Yuxuan Zhao
- Congsheng Xu
- Yanming Shao
- Yichuan Peng
- Yao Mu
- Wenzhao Lian
topics:
- vision-language-action
- human-in-the-loop
- dexterous-manipulation
- robot-learning
- teleoperation
relevance_score: 0.31
run_id: materialize-outputs
language_code: zh-CN
---

# DexHiL: A Human-in-the-Loop Framework for Vision-Language-Action Model Post-Training in Dexterous Manipulation

## Summary
DexHiL 是一个用于灵巧操作视觉-语言-动作模型后训练的人在回路框架，把离线示教、在线人工接管纠错和干预感知重加权训练结合起来。论文核心主张是：对高自由度机械手任务，少量高价值的人类纠错数据比单纯增加离线数据更有效。

## Problem
- 现有 VLA 在通用操作上有泛化能力，但迁移到灵巧手任务时，动作空间高维、接触复杂、误差易累积，单靠离线微调很难稳定收敛。
- 传统遥操作/示教系统存在人手到机械手的运动学不对齐，难以采集高保真、细粒度的灵巧操作数据，尤其不利于在线增量纠错。
- 机器人执行时会发生协变量偏移；没有即时恢复机制，小错误会把策略推到分布外状态并导致失败，这对真实世界高 DOF 操作尤为关键。

## Approach
- 提出一个**一体化 arm-hand HiL 系统**：手臂用 ArUco 方块的 6D 位姿做轻量遥操作，手部用动作捕捉手套 + 学习式重定向网络控制灵巧手，实现手臂和手指的统一在线接管。
- 设计**两阶段手指重定向**：先学习四指稳定运动流形，再冻结四指并单独学习拇指残差，避免五指一起学时退化成“捏夹”姿态。
- 采用**异步多线程控制**：策略推理 20Hz、人工手臂遥操作 30Hz、手部遥操作 90Hz；当系统即将失败时，人类可实时接管并给出纠正轨迹。
- 在训练上使用**干预感知重加权**：把稀疏但高价值的 intervention 样本按重要性采样提高权重，文中将目标干预比例设为 0.5，以强化错误恢复学习。
- 使用**离线 warm-up + 在线 DAgger 式迭代**，并只保留“最后一次干预到任务完成”的恢复片段，减少不一致轨迹带来的策略振荡。

## Results
- 在真实机器人两项任务上，DexHiL 相比数据量匹配的标准离线微调基线，**平均成功率提升 25%**（摘要主结果）。
- 论文还报告：经过 **3 轮** 在线迭代后，相比“等数据量离线训练”基线，两个任务的成功率分别提升 **20%** 和 **30%**。
- **Tissue Extraction**：Round 3 时 DexHiL 达到 **95%** 成功率，优于 **DAgger\*** 的 **80%** 和离线基线的 **75%**；评测为每个任务 **20 次**真实机器人独立试验。
- **Plush Toy Grasping**：Round 3 时 DexHiL 达到 **65%**，而 **DAgger\*** 为 **20%**、离线基线为 **35%**。
- 训练/数据设定：初始使用 **60 条离线轨迹**做 warm-up；之后每轮每个任务新增 **10 条轨迹**，并与相同数据预算的 Offline-40/50/60 基线比较。
- 实现细节显示其基础 VLA 为 **Being-H0.5**，初始全量训练使用 **8×NVIDIA H100**、**60k iterations**，在线交互数据微调使用 **1×H100**。

## Link
- [http://arxiv.org/abs/2603.09121v1](http://arxiv.org/abs/2603.09121v1)
