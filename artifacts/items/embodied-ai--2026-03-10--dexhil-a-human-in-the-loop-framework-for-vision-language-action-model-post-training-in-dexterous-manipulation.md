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
- dexterous-manipulation
- human-in-the-loop
- robot-post-training
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
---

# DexHiL: A Human-in-the-Loop Framework for Vision-Language-Action Model Post-Training in Dexterous Manipulation

## Summary
DexHiL提出了一个面向灵巧操作视觉-语言-动作模型的人在回路后训练框架，把离线示教、在线人工接管和干预感知重加权训练整合到同一套臂手系统中。其目标是在高维、多接触的灵巧手任务上，比纯离线微调更高效地提升真实机器人成功率与鲁棒性。

## Problem
- 现有VLA在通用操作上有潜力，但迁移到灵巧手下游任务时，**高维手部控制、密集接触、协变量偏移**使纯离线后训练很难稳定收敛。
- 传统HiL/DAgger式纠错大多只覆盖机械臂或平行夹爪，**无法对机械臂与灵巧手进行统一、连续、细粒度接管**，导致纠错数据质量和协调性不足。
- 这很重要，因为灵巧操作中的小误差会快速累积并进入OOD状态，直接影响真实机器人在复杂抓取、抽取等任务上的可靠部署。

## Approach
- 提出**集成式臂-手HiL遥操作系统**：机械臂用ArUco立方体进行6D位姿映射，手部用手套关键点驱动学习式关节重定向，从而支持在线即时人工接管。
- 设计**两阶段手部重定向**：先学习四指稳定运动流形，再冻结四指并优化拇指残差与手指间几何约束，避免五指统一学习退化成“捏夹式”抓取。
- 采用**异步多线程控制**：策略20Hz自主执行，人工臂控30Hz、手控90Hz，在检测到即将失败时由人类接管并生成纠错轨迹。
- 在训练上使用**干预感知重加权**：把稀缺但高价值的人工纠错片段在损失中提高权重，目标将干预样本占比提升到0.5，以更快学习恢复与避错行为。
- 结合**离线预热 + 在线迭代聚合**的数据管线，并过滤为“最后一次干预到任务完成”的恢复片段，减少前序错误动作带来的分布冲突与策略振荡。

## Results
- 在**Tissue Extraction**任务上，DexHiL第3轮达到**95%**成功率，优于**DAgger\***的**80%**和离线基线的**75%**。
- 在**Plush Toy Grasping**任务上，DexHiL第3轮达到**65%**成功率，而**DAgger\***仅**20%**，离线基线为**35%**。
- 摘要声明：相对标准**offline-only finetuning**基线，DexHiL在不同任务上的成功率**平均提升25%**。
- 引言还声明：经过**3轮在线优化**，相对相同数据量的离线训练基线，两项任务分别获得**20%**和**30%**成功率提升。
- 实验设置显示：初始使用**60条离线轨迹**做预热；之后每轮每任务新增**10条轨迹**，并与等数据预算的Offline-40/50/60基线比较；每个任务在真实机器人上进行**20次**独立试验。
- 论文还声称消融结果表明，**干预感知重加权机制**是突破样本效率瓶颈的关键驱动，但摘录中未提供更完整的消融数表。

## Link
- [http://arxiv.org/abs/2603.09121v1](http://arxiv.org/abs/2603.09121v1)
