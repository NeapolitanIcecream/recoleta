---
source: arxiv
url: https://arxiv.org/abs/2607.13017v1
published_at: '2026-07-14T17:57:12'
authors:
- Yixiang Chen
- Peiyan Li
- Yuan Xu
- Qisen Ma
- Jiabing Yang
- Kai Wang
- Jianhua Yang
- Dong An
- He Guan
- Gaoteng Liu
- Jianlou Si
- Jun Huang
- Jing Liu
- Nianfeng Liu
- Yan Huang
- Liang Wang
topics:
- robot-foundation-model
- world-action-model
- optical-flow-actions
- action-conditioned-world-model
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# FlowWAM: Optical Flow as a Unified Action Representation for World Action Models

## Summary
## 摘要
FlowWAM 将光流用作视频原生的动作表示，同时用于机器人策略学习和动作条件世界建模。该方法在 RoboTwin 2.0 Clean 设置下取得 92.94% 的成功率，在 Random 设置下取得 92.14% 的成功率，并在 WorldArena 上达到 63.71 的 EWMScore。

## 问题
- 世界动作模型需要一种既能匹配预训练视频生成器、又能保留精确机器人控制所需稠密时间运动信息的动作表示。
- 数值动作依赖具体的机器人实体，而掩码、射线图等已有视觉动作信号提供的时间运动信息有限。
- 这一问题很重要，因为较弱的动作表示可能同时降低可执行策略的性能，以及动作条件未来视频预测的保真度。

## 方法
- 将逐像素光流编码为类似 HSV RGB 的光流视频，在兼容视频生成模型的格式中保留运动方向和幅度。
- 使用具有共享 VAE 和 Transformer 组件的双流扩散 Transformer，对 RGB 视频和光流视频进行联合建模。
- 在策略模式下生成未来光流，并通过动作专家将模型的 RGB-光流特征解码为低层机器人动作块。
- 在世界模型模式下提供目标光流序列，生成遵循指定运动的 RGB 未来帧。
- 使用提取出的光流在无动作标注的视频上预训练视频生成器，然后在带标注的机器人示范上微调动作专家；运动感知重加权机制会强调运动区域。

## 结果
- 在 RoboTwin 2.0 的 50 个双臂任务上，每个任务进行 100 次 rollout 评估时，FlowWAM 在 Clean 设置下取得 92.94% 的成功率，在 Random 设置下取得 92.14% 的成功率；报告中的 Fast-WAM 基线分别为 91.88% 和 91.78%。
- 使用无动作标注的 EgoDex 进行预训练后，FlowWAM 在 Clean 设置下的表现从 82.40% 提升至 92.94%，在 Random 设置下从 80.80% 提升至 92.14%。
- 在 WorldArena 的 121 帧、24 fps rollout 上，FlowWAM 取得报告中最高的 63.71 EWMScore，Trajectory Accuracy 为 64.26；表中 GigaWorld-1 的 Trajectory Accuracy 为 54.27，EWMScore 为 62.34。
- 摘要报告称，FlowWAM 在 WorldArena 上将 Trajectory Accuracy 相对提升了 18.4%，并表示其优于 VLA 和 WAM 基线。
- 摘录未提供完整的消融实验、真实机器人结果或完整的统计处理，因此这些增益主要证明了其基准测试性能，尚不足以说明它在所有部署条件下的稳健性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13017v1](https://arxiv.org/abs/2607.13017v1)
