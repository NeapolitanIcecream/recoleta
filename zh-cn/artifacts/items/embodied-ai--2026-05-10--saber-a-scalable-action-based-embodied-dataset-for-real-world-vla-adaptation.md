---
source: arxiv
url: https://arxiv.org/abs/2605.09613v1
published_at: '2026-05-10T15:51:01'
authors:
- Narsimha Menga
- Parikshit Sakurikar
- Amirreza Rouhi
- Satya Sai Reddy
- Anirudh Govil
- Sri Harsha Chittajallu
- Rajat Aggarwal
- Anoop Namboodiri
- Sashi Reddi
topics:
- vision-language-action
- robot-data-scaling
- human-video-retargeting
- retail-robotics
- dexterous-manipulation
- humanoid-robotics
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation

## Summary
## 总结
SABER 是一个零售机器人数据集，基于真实门店中的人类视频构建，用于将 VLA 策略适配到杂货店操作任务。论文声称，领域特定的动作数据把 GR00T N1.6 在 RoboBenchMart 零售任务上的表现从 13.4% 的平均成功率提高到 29.3%。

## 问题
- 通用机器人 VLA 模型对零售任务的覆盖很弱，例如货架取放、打开冰箱、装篮、地面取物，以及处理不同包装。
- 在运营中的门店里收集机器人遥操作数据成本高、会干扰经营，也很难扩展。
- 这个差距很重要，因为在广泛机器人数据上训练出的策略，遇到与预训练数据不同的门店布局、物体、光照、遮挡和动作顺序时，可能失效。

## 方法
- SABER 通过头戴式 GoPro 和固定的 DreamVu ALIA 360° 摄像机，在真实杂货店中记录了大约 100 小时的自然活动。
- 数据集把视频转成三条动作流：来自第一人称视频的 25K LAPA 潜在动作片段、重定向到机器人关节空间的 18.6K 灵巧手姿轨迹，以及重定向到 Unitree G1 类人机器人的 1.2K 全身运动片段。
- 人工标注者检查并修正手部和身体姿态估计，然后通过重定向把人类动作转换成机器人可用的动作目标。
- 作者用共享主干的多任务方案对 GR00T N1.6 做后训练，输入是这三条 SABER 数据流，再加少量机器人原生锚点数据和与任务对齐的种子数据。

## 结果
- SABER 包含来自约 100 小时真实门店采集的 44.8K 个训练样本。
- 数据集组成：25K 潜在动作序列、18.6K 手姿轨迹和 1.2K 全身同步运动序列。
- SABER-MM 后训练在 10 个 RoboBenchMart 零售操作任务上的平均成功率达到 29.3%。
- 对比基线是仅用仿真进行微调，在同一任务集上的平均成功率为 13.4%。
- 论文声称，相比微调基线，提升超过 2.19 倍。
- 论文公开发布了一个 10K 样本的 SABER 子集，许可为 CC BY-NC 4.0。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09613v1](https://arxiv.org/abs/2605.09613v1)
