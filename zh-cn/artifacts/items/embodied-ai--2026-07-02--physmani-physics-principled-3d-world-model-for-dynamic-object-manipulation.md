---
source: arxiv
url: https://arxiv.org/abs/2607.01938v1
published_at: '2026-07-02T09:32:39'
authors:
- Peng Yun
- Shouwang Huang
- Hao Li
- Jinxi Li
- Jianan Wang
- Bo Yang
topics:
- robot-world-model
- dynamic-manipulation
- 3d-gaussian-splatting
- vision-language-action
- imitation-learning
- physics-based-prediction
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# PhysMani: Physics-principled 3D World Model for Dynamic Object Manipulation

## Summary
## 摘要
PhysMani 是一个面向机器人的 3D Gaussian 世界模型系统，用于操作移动目标。它在线预测受物理约束的场景运动，并将该运动输入 3D 动作策略。

## 问题
- 当目标移动速度接近机器人末端执行器极限时，机器人需要快速的 3D 运动预测来抓取、放置、推动或插入物体。
- 现有 VLA 和视频世界模型常会预测出偏 2D 观感的未来状态，缺少可靠的 3D 几何和物理运动，这会影响对时间敏感的操作。
- 论文还通过引入基于 RLBench 的 PhysMani-Bench 填补基准缺口，其中包含 16 个动态操作任务。

## 方法
- 世界模型用 30,000 个 3D Gaussians 表示场景，这些高斯由 4 个固定相机的 RGB-D 视图初始化。
- 一个速度 MLP 为每个 Gaussian 预测 6 个运动分量：3 个线性分量和 3 个角分量。基函数构造使速度场满足无散度约束。
- 模型使用 RGB-D 监督在线更新，损失函数包括 L1 和 SSIM。报告的设置为每步进行 50 次速度更新迭代和 7 次细化迭代。
- 策略基于 3D FlowMatch Actor。它将 RGB-D 观测提升为 4,096 个 3D 视觉 token，用 KNN 检索附近的 Gaussians，并通过注意力 token 注入局部预测速度。
- 策略使用 rectified flow 预测未来末端执行器关键位姿，然后通过逆运动学将其转换为机器人关节命令。

## 结果
- 在 PhysMani-Bench 上，PhysMani 报告了最高的平均仿真成功率：45.9±0.8%，相比之下 3DFA 为 37.8±0.9%，3DFA-OF 为 37.5±1.0%，3DDA 为 35.1±1.7%，Act3D 为 27.1±2.7%，ManiGaussian 为 22.5±0.8%，pi0.5 为 8.3±0.2%。
- 列出的最大任务增益来自 Drop to Hoop：PhysMani 为 71.7±3.1%，3DFA 为 30.8±3.1%，3DFA-OF 为 27.5±5.4%。
- Pick Cube 中，PhysMani 达到 84.2±3.1%，3DFA 为 70.0±6.1%，3DDA 为 63.3±6.6%。
- Push Button 中，PhysMani 达到 57.5±3.5%，3DFA 为 55.8±4.2%，3DFA-OF 为 54.2±3.1%。
- PhysMani 在可见表格中的并非每个任务都领先：Beat Buzz 中 PhysMani 为 78.3±4.2%，3DFA 为 82.5±2.0%；Insert Peg 中 PhysMani 为 37.5±6.1%，3DDA 为 68.3±6.6%。
- 在线世界模型优化报告为在一块 RTX 4090 GPU 上每次更新约 200 ms，基准设置中的移动目标速度最高为 2 m/s。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01938v1](https://arxiv.org/abs/2607.01938v1)
