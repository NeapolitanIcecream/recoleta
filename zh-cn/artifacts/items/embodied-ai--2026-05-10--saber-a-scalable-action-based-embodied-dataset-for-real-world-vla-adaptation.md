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
## 摘要
SABER 是一个零售机器人数据集，基于真实店内人类视频构建，用于让 VLA 策略适应杂货店操作任务。论文称，领域特定动作数据将 GR00T N1.6 在 RoboBenchMart 零售任务上的平均成功率从 13.4% 提高到 29.3%。

## 问题
- 通用机器人 VLA 模型对货架拣取、打开冷柜、装篮、从地面拾取物品以及处理不同包装等零售任务覆盖不足。
- 在营业中的门店内采集机器人遥操作数据成本高、干扰大，且难以扩展。
- 这个差距会带来实际影响：当门店布局、物体、光照、遮挡和动作序列不同于预训练数据时，基于广泛机器人数据训练的策略可能失败。

## 方法
- SABER 使用头戴式 GoPro 和固定式 DreamVu ALIA 360° 摄像头，在真实杂货店中记录约 100 小时的自然活动。
- 该数据集将视频转换为三类动作流：来自第一视角视频的 25K 个 LAPA 潜在动作片段、重定向到机器人关节空间的 18.6K 个灵巧手姿态片段，以及重定向到 Unitree G1 人形机器人的 1.2K 个全身运动片段。
- 人类标注员审核并校正手部和身体姿态估计，然后通过重定向将人类动作转换为机器人兼容的动作目标。
- 作者使用共享骨干的多任务配方，在三个 SABER 数据流上对 GR00T N1.6 进行后训练，并加入少量机器人原生锚定数据和与任务对齐的种子数据。

## 结果
- SABER 包含 44.8K 个训练样本，来自约 100 小时的真实店内采集。
- 数据集组成：25K 个潜在动作序列、18.6K 条手部姿态轨迹，以及 1.2K 条全身同步运动序列。
- SABER-MM 后训练在 10 个 RoboBenchMart 零售操作任务上的平均成功率达到 29.3%。
- 对比基线是在同一任务集上仅使用仿真进行微调，平均成功率为 13.4%。
- 论文声称，相比微调基线，提升超过 2.19 倍。
- 一个包含 10K 个样本的 SABER 子集已按 CC BY-NC 4.0 公开发布。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09613v1](https://arxiv.org/abs/2605.09613v1)
