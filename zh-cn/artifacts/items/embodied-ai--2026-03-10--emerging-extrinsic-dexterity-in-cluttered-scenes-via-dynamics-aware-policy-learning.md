---
source: arxiv
url: http://arxiv.org/abs/2603.09882v1
published_at: '2026-03-10T16:40:30'
authors:
- Yixin Zheng
- Jiangran Lyu
- Yifan Zhang
- Jiayi Chen
- Mi Yan
- Yuntian Deng
- Xuesong Shi
- Xiaoguang Zhao
- Yizhou Wang
- Zhizheng Zhang
- He Wang
topics:
- extrinsic-dexterity
- non-prehensile-manipulation
- world-model
- sim2real
- cluttered-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamics-aware Policy Learning

## Summary
本文提出 DAPL，通过先学习“接触后物体会如何运动”的动力学表示，再用其条件化强化学习策略，使机器人在拥挤杂乱场景中自然学会借助环境接触进行非抓取操作。该方法面向外在灵巧性（extrinsic dexterity），并在仿真、零样本真实世界和实际杂货取物部署中展示了优于几何表征与抓取式基线的性能。

## Problem
- 要解决的是**杂乱场景中的非抓取式 6D 物体重排**：机器人不仅要移动目标物体，还要在多物体耦合接触中选择性地利用或避免碰撞。
- 这很重要，因为在拥挤、遮挡、难以抓取的真实环境里，单靠抓取和无碰规划常常失败；成功往往依赖推、滑、翻等外在灵巧动作。
- 现有方法大多只看静态几何、缺少显式动力学建模，因此在高密度杂乱中难以推断接触后的滑动、翻倒和动量传递结果。

## Approach
- 核心方法是 **Dynamics-Aware Policy Learning (DAPL)**：先训练一个物理世界模型，输入目标物体、周围场景和末端执行器的点云，并附加**质量与速度**等物理属性，预测动作后下一时刻各点的位置和速度。
- 这个世界模型用 **patch-based Transformer/ViT + MLP 解码器** 学习“接触会带来什么后果”的潜在动力学特征；这些特征再作为条件输入给 Actor-Critic 强化学习策略。
- 为避免大多数静止点导致速度预测塌缩到接近 0，作者加入了**速度方差正则项**，让模型保留动态区域的运动幅度与空间变化。
- 训练采用**交替课程学习**：先用当前策略收集约 **60k** 步交互数据，再更新世界模型，再用更新后的动力学表示继续训练策略，循环迭代直到收敛。
- 作者还构建了 **Clutter6D** 基准：基于 IsaacLab/PhysX，含 **10K** 归一化物体资产，按稀疏/中等/稠密三档分别测试 **4/8/12** 个物体杂乱度下的 6D 重排。

## Results
- 在 **Clutter6D** 未见仿真场景上，DAPL 成功率分别达到：**Sparse 71.88% / Moderate 51.04% / Dense 44.56%**。强基线 **CORN** 为 **46.63% / 45.83% / 22.22%**，说明在稠密场景中 DAPL 约提升 **22.34 个百分点**，相对最强基线接近翻倍；相对论文摘要中的概括，超过各类基线 **25%+** 成功率提升。
- 与抓取式 **GraspGen + CuRobo** 相比，DAPL 在 **Sparse/Moderate/Dense** 上分别为 **71.88 vs 26.6 / 51.04 vs 15.6 / 44.56 vs 3.13**，显示非抓取外在灵巧在密集杂乱中明显更有效。
- 与人类遥操作相比，DAPL 在仿真中也更强：人类为 **50.0% / 40.0% / 20.0%**，DAPL 为 **71.88% / 51.04% / 44.56%**；同时 Dense 下非目标物扰动（M.O.）**12.65 cm**，低于 CORN 的 **17.43 cm**。
- 训练效率上，作者称方法在前期训练中即可达到约 **70%** 成功率，而几何表征基线收敛更慢，说明动力学表示提升了样本效率。
- 消融实验（Sparse）显示：完整**点级世界模型 + 速度 + 物理属性**最好，达到 **71.88%** 成功率、**2.59 cm** 扰动；去掉物理属性降至 **58.25%**，改为对象级世界模型仅 **16.88%**，简单重建预训练仅 **29.63%** 或 **11.75%**，说明点级动力学监督最关键。
- 课程学习有效：成功率随迭代从 **61.3%** 提升到 **71.8%**（3 轮后）。真实世界零样本部署在 **10** 个杂乱场景中成功率约 **50%**，与人类遥操作相当，但平均执行时间更短：**42.6s vs 55.9s**。此外论文还声称完成了实际**杂货取物**部署，但摘录未给出更多量化数字。

## Link
- [http://arxiv.org/abs/2603.09882v1](http://arxiv.org/abs/2603.09882v1)
