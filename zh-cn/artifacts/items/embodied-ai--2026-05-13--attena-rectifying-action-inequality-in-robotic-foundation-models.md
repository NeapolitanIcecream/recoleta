---
source: arxiv
url: https://arxiv.org/abs/2605.13548v1
published_at: '2026-05-13T13:55:37'
authors:
- Daojie Peng
- Fulong Ma
- Jiahang Cao
- Qiang Zhang
- Xupeng Xie
- Jian Guo
- Ping Luo
- Andrew F. Luo
- Boyu Zhou
- Jun Ma
topics:
- vision-language-action
- robot-foundation-models
- world-action-models
- manipulation-policy
- loss-weighting
- robot-data-scaling
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# AttenA+: Rectifying Action Inequality in Robotic Foundation Models

## Summary
## 摘要
AttenA+ 通过给速度慢、精度要求高的动作步骤更高的损失权重，改善了机器人基础模型的训练。论文报告称，它在 Libero 和 RoboTwin 2.0 上带来了幅度不大但稳定的成功率提升，而且不需要改动模型骨干。

## 问题
- VLA 和 WAM 模型通常会给每个动作时间步相同的损失权重，尽管抓取、对齐和放置比快速接近动作更容易出错。
- 这很关键，因为即使轨迹的大部分都正确，最后几厘米的误差也可能让长时程操作任务失败。

## 方法
- 根据真实动作计算瞬时速度大小。在 Libero 上，这个方法使用连续运动维度，省略二元夹爪状态。
- 把速度转换为训练权重：低速度对应更高权重，高速度对应更低权重。
- 测试四种速度到权重的映射：反比、反比平方、指数衰减和对数。
- 将这些权重应用到现有训练损失中，例如 OpenVLA-OFT 的加权 L1 损失，以及 pi 风格生成策略的加权 flow-matching 损失。
- 对权重进行裁剪，并在需要时做归一化，避免接近静止的步骤主导梯度，同时让平均损失尺度接近基线。

## 结果
- 在 Libero 上，AttenA+OFT 的平均成功率达到 98.60%，而 OpenVLA-OFT 为 97.10%，提升 1.50 个百分点。平均错误率从 2.90% 降到 1.40%。
- AttenA+OFT 在 Libero 各项任务上的得分为：Spatial 99.0% ± 0.16，Object 100.0% ± 0.00，Goal 98.8% ± 0.28，10 任务长时程划分为 96.6% ± 0.30。
- 与 Libero 上的 OpenVLA-OFT 相比，提升分别是 Spatial +1.4 个百分点、Object +1.6、Goal +0.9、长时程任务 +2.1。
- 在 Libero 上使用生成式 pi-0.5 骨干时，AttenA+pi-0.5 的平均成功率达到 97.95%，而 pi-0.5 为 96.85%，提升 1.10 个百分点。平均错误率从 3.15% 降到 2.05%。
- 在 RoboTwin 2.0 上，AttenA+WAM 的平均成功率达到 92.46%，而 Fast-WAM 为 91.80%，LingBot-VA 为 92.20%。其中 Clean 为 93.06%，Randomized 为 91.86%。
- 论文还声称在 Franka 机械臂上做了真实世界验证，并且有跨任务泛化，但摘要没有给出具体的真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13548v1](https://arxiv.org/abs/2605.13548v1)
