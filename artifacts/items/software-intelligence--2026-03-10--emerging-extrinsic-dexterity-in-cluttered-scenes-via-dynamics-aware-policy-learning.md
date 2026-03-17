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
- robot-manipulation
- extrinsic-dexterity
- dynamics-aware-rl
- world-model
- sim-to-real
relevance_score: 0.08
run_id: materialize-outputs
---

# Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamics-aware Policy Learning

## Summary
本文提出 DAPL，通过先学习“物体接触后会怎样动”的动力学表征，再用其条件化强化学习策略，让机器人在拥挤场景中自然学会利用环境接触进行非抓取操作。该方法面向杂乱场景中的外在灵巧操作，并在仿真、零样本现实部署和杂货检索任务中展示出明显优势。

## Problem
- 目标问题：在**杂乱拥挤场景**中完成非抓取式 6D 物体重排，需要机器人有选择地利用或规避多物体接触，这类“外在灵巧性”比单纯抓取更难。
- 难点在于：成功不仅取决于几何形状，还取决于接触后物体会**滑动、翻倒、传递动量**等耦合动力学；现有方法大多只看静态几何或依赖手工接触启发式。
- 这很重要，因为真实环境里抓取常因遮挡、拥挤、缺少无碰撞路径而失败，而非抓取接触操作能补足抓取能力的局限。

## Approach
- 核心机制是两阶段学习：先训练一个**物理世界模型**，预测机器人动作下点云中各点未来的位置和速度；再把该模型学到的**动力学特征**输入强化学习策略。
- 世界模型输入不仅包含点云几何，还加入**质量与速度**等物理属性；使用基于 patch 的 Transformer 编码多物体接触耦合，再由 MLP 预测逐点未来运动。
- 为避免大多数点几乎静止导致速度预测塌缩，作者加入**方差正则项**，约束预测速度场的整体变化幅度与真实分布一致。
- 策略学习阶段将动力学表征、机器人本体状态和目标位姿共同输入 actor-critic 网络，输出连续关节控制；奖励设计保持简单，不依赖复杂 reward shaping。
- 还引入**课程式交替训练**：先用当前策略收集约 60k 步交互数据更新世界模型，再用改进后的动力学表征继续训练策略，让模型与策略共同迭代提升。

## Results
- 在新提出的 **Clutter6D** 基准上，DAPL 在未见仿真场景中显著超过所有基线。成功率分别为：Sparse **71.88%**、Moderate **51.04%**、Dense **44.56%**；对应最强表示学习基线 CORN 为 **46.63% / 45.83% / 22.22%**，在 Dense 场景约**翻倍**提升（44.56 vs. 22.22）。
- 相比抓取式基线 GraspGen + CuRobo，DAPL 在 Sparse/Moderate/Dense 上分别达到 **71.88/51.04/44.56%**，而对方仅 **26.6/15.6/3.13%**；论文摘要还概括称在未见拥挤仿真场景上对抓取、人类遥操作和先前表征策略的成功率提升**超过 25%**。
- 在环境扰动指标 M.O. 上，DAPL 在 Dense 为 **12.65**，低于 CORN 的 **17.43**，说明在更高成功率下还能减少对非目标物体的扰动；Moderate 上 DAPL 为 **2.7**，也优于 CORN 的 **5.51**。
- 训练效率上，作者称 DAPL 在前几千次迭代内即可达到约 **70%** 成功率，明显快于基于静态几何表征的方法。
- 消融实验（Sparse）显示：完整配置（point-level world model + velocity + physical features）达到 **71.88%** 成功率、M.O. **2.59**；去掉物理特征但保留速度降至 **58.25%**，再去掉速度与物理特征降至 **42.00%**；若改为简单重建预训练，仅 **11.75%** 或 **29.63%**，说明动力学建模是关键。
- 课程学习迭代中，成功率从 **61.3%** 提升到 **71.8%**（3 次迭代后）。现实世界零样本部署在 **10** 个杂乱场景上成功率约 **50%**，与人类遥操作相当，但平均执行时间更短：**42.6s vs. 55.9s**。

## Link
- [http://arxiv.org/abs/2603.09882v1](http://arxiv.org/abs/2603.09882v1)
