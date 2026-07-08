---
source: arxiv
url: https://arxiv.org/abs/2607.06323v1
published_at: '2026-07-07T14:22:31'
authors:
- Xinye Yang
- Zhiyuan Ma
- Hongze Yu
- Yuanpei Chen
- Yaodong Yang
- Xiaojie Chai
- Xinlei Chen
- Chao Yu
topics:
- dexterous-manipulation
- latent-action-space
- residual-rl
- imitation-learning
- real-world-robot-learning
- motion-prior
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# LAMP: Latent Motion Prior-Guided Real-World Learning for Dexterous Hand Manipulation

## Summary
## 摘要
LAMP 在模仿学习和残差 RL 中都使用学习得到的二维手部控制潜在运动空间，从而改进真实世界中的灵巧手学习。它在四个真实机器人任务上报告，在线 RL 后的平均最终成功率为 98.75%。

## 问题
- 灵巧手的动作维度很高，因此很小的模仿误差也可能累积成接触丢失、物体掉落或执行停滞。
- 在原始手指关节空间中进行在线 RL 会探索不安全或无用的手部动作，浪费真实机器人试验，并可能损坏硬件或物体。
- 这个问题很重要，因为接触丰富的操作需要在示范之后进行可靠修正，尤其是在只有小规模任务专用数据集时。

## 方法
- LMPM 在近期手部动作历史上训练编码器，并将 8 步手部目标历史映射到二维潜在空间中的高斯先验。
- 解码器将每个潜在命令映射回 6 维可执行 Ruiyan 手目标，因此策略仍向机器人发送常规手部命令。
- 行为克隆在原生机械臂空间中预测 6 维机械臂命令，并围绕当前 LMPM 先验中心预测潜在手部偏移。
- 在线残差 RL 从克隆策略开始，添加原生机械臂残差，并在同一潜在空间中添加手部残差，然后解码最终手部目标。
- 该方法使用来自 Franka Research 3 机械臂、Ruiyan 灵巧手、两个 RGB 相机和任务专用示范的真实机器人数据。

## 结果
- 在 Grasp & Place、Open Drawer、Pull Tissue 和 Assemble Box 上，完整 LMPM 达到 56.25% 的平均模仿学习成功率和 98.75% 的平均最终 RL 成功率。
- 最终 RL 成功率在 Grasp & Place 上为 100%，在 Open Drawer 上为 100%，在 Pull Tissue 上为 95%，在 Assemble Box 上为 100%。
- 该方法从小规模示范集开始：Grasp & Place 为 50 个示范，Open Drawer 为 20 个，Pull Tissue 为 20 个，Assemble Box 为 30 个。
- 移除低维瓶颈后，平均最终 RL 成功率降至 55.0%，各任务分数为 35%、85%、80% 和 20%。
- 移除基于历史条件的编码器后，平均最终 RL 成功率降至 73.75%，各任务分数为 95%、90%、60% 和 50%。
- 不使用 LMPM 的原始 BC 表现很差：平均 IL 成功率为 5.0%，平均最终 RL 成功率为 3.75%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06323v1](https://arxiv.org/abs/2607.06323v1)
