---
source: arxiv
url: https://arxiv.org/abs/2606.10614v1
published_at: '2026-06-09T09:13:36'
authors:
- Beomjun Kim
- Seong Hyeon Park
- Seunghoon Sim
- Seungjun Moon
- Sanghyeok Lee
- Jinwoo Shin
topics:
- dexterous-manipulation
- human-video-learning
- keypoint-policy
- robot-data-scaling
- vision-language-action
- robot-foundation-models
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations

## Summary
## 摘要
Dexterous Point Policy 只用人类视频训练灵巧机械手策略，不需要机器人示范。它用共享的 3D 关键点表示人手、机器人手和任务物体，再加入指尖接触预测来处理抓握力。

## 问题
- 用人类视频训练的机器人策略在真实机器人上常常失效，因为像素、关节和手的形态在不同具身之间不能直接迁移。
- 机器人示范采集成本高，灵巧手遥操作更难，因为多手指控制的动作维度很高。
- 这篇论文要解决零机器人数据的灵巧操作，这对把机器人数据规模做大很重要，因为人工遥操作速度太慢。

## 方法
- 该方法把人手和机器人手都表示成 6 个 3D 关键点：手腕加 5 个指尖。
- 它用 VLM 识别物体名称、用 SAM3 生成掩码，再结合深度估计或双目深度，从视频中提取任务物体点。
- 它训练一个自回归 Transformer，根据语言、物体点、当前手部关键点和相机位姿预测未来的手部关键点。
- 它先在 VITRA 上约 100 万个第一视角人类视频 episode 上预训练，VITRA 汇总了 Ego4D、Ego-Exo4D、Something-Something v2 和 EPIC-KITCHENS。
- 在任务微调时，它使用带有指尖接触标签的人类视频。部署时，逆运动学把预测的关键点映射到机器人关节，预测到的接触标志再为指尖施加很小的闭合偏移，用来提供抓握力。

## 结果
- 在 8 个真实机器人灵巧任务上，DPP 的平均成功率是 75.0%，Point Policy 为 3.7%，VITRA 为 1.0%。
- 在搬运任务上，DPP 的平均成功率是 81.7%：瓶子 95.8%，盒子 75.0%，球 70.8%，毛巾 87.5%，泰迪熊 79.2%。
- 在操作和工具使用任务上，DPP 的平均成功率是 63.9%：打开 87.5%，刷子 62.5%，喷雾 41.7%。
- 按论文结果，接触预测比只用关键点的基线提升了 71.3 个百分点。
- 互联网规模的人类视频预训练把搬运任务成功率从 67.5% 提高到 81.7%，提升了 14.2 个百分点。
- 泛化表现接近训练物体设置：多物体场景下成功率是 80.0%，新物体上是 76.7%，标准搬运任务上是 81.7%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10614v1](https://arxiv.org/abs/2606.10614v1)
