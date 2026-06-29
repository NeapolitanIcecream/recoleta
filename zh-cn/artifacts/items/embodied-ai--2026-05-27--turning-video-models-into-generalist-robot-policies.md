---
source: arxiv
url: https://arxiv.org/abs/2605.27817v1
published_at: '2026-05-27T01:21:58'
authors:
- Sizhe Lester Li
- Evan Kim
- Xingjian Bai
- Tong Zhao
- Tao Pang
- Max Simchowitz
- Vincent Sitzmann
topics:
- video-world-models
- inverse-dynamics
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Turning Video Models into Generalist Robot Policies

## Summary
## 总结
VERA 通过保留视频空间中的规划，并加入一个针对机器人本体的 Jacobian 逆动力学模型，把一个 14B 视频生成模型变成了闭环机器人策略。论文声称，这样可以减少配对的视频-动作-文本训练数据需求，同时支持 Panda 机械臂操作和 16 自由度 Allegro 手指立方体重定向。

## 问题
- 通用机器人策略通常需要和每种机器人本体绑定的动作标注数据，而网络规模的机器人动作数据并不存在。
- 视频模型可以预测任务成功时应该是什么样子，但机器人需要关节或末端执行器指令，因此缺失的一步是可靠的视频到动作转换。
- 直接的逆动力学模型在动作数据有限时可能失败，而且随着动作维度增加会变不准，这会影响高自由度机器人，比如灵巧手。

## 方法
- 使用一个不依赖动作的视频规划器，根据观测历史和目标，通常是文本，预测未来的机器人视频帧。
- 为每种机器人本体单独训练一个 Jacobian 逆动力学模型。
- J-IDM 预测一个稠密的图像空间 Jacobian：对每个像素，它估计每个动作维度会怎样移动这个像素。
- 在测试时，把生成帧之间的光流通过学习到的 Jacobian 反解，恢复机器人的动作。
- 只执行生成计划的短前缀，观察新状态，然后在闭环中重新规划。

## 结果
- 在仿真中，J-IDM 的闭环成功率在所有报告任务上都超过了 UniPi 风格的直接 IDM：Allegro-Sim 为 70.0% 对 0.0%，Panda-Sim 为 94.0% 对 0.0%，PushT-Sim 为 92.5% 对 74.4%。
- 在报告的 4 种设置里，J-IDM 的动作重建 MSE 有 3 种更低：Allegro-Sim 为 0.031 对 0.044/0.063，PushT-Sim 为 0.046 对 0.059/0.071，5 关节手指为 0.017 对 0.030/0.047；Panda-Sim 为 0.19，对最好的基线 0.09。
- 在一个受控的 2D 手指研究里，5 自由度下，论文报告 J-IDM 的数据效率大约比直接 IDM 基线高 2 倍。
- 在真实 Panda 基础指令任务上，DreamZero 的成功率为 90%，VERA 为 60%，π0.5 为 30%。
- 论文声称，在真实 Panda 机械臂的未见场景中，使用不同相机和提示词可以零样本部署；还声称可以仅用 RGB 在真实 Allegro 手上完成 16 自由度立方体重定向。
- 同一个视频规划器分别配合 Panda 和 Allegro 机器人对应的本体特定 J-IDM，支持跨本体的说法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27817v1](https://arxiv.org/abs/2605.27817v1)
