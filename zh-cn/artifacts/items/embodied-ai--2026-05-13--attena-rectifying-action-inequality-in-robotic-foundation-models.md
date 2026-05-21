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
AttenA+ 通过提高慢速、高精度动作步骤的损失权重来改进机器人基础模型训练。它报告称，在不改变模型骨干的情况下，Libero 和 RoboTwin 2.0 上的成功率有小幅但一致的提升。

## 问题
- VLA 和 WAM 模型通常给每个动作时间步相同的损失权重，但抓取、对齐和放置比快速接近动作更容易受误差影响。
- 这一点很关键，因为即使大部分轨迹正确，最后一厘米的误差也可能导致长时程操作任务失败。

## 方法
- 根据真实动作计算瞬时速度大小。在 Libero 上，该方法使用连续运动维度，并省略二值夹爪状态。
- 将速度转换为训练权重：低速度得到较大权重，高速度得到较小权重。
- 测试四种速度到权重的映射：倒数、平方倒数、指数衰减和对数映射。
- 将这些权重应用到现有训练损失上，例如用于 OpenVLA-OFT 的加权 L1 损失，以及用于 pi 风格生成式策略的加权流匹配损失。
- 对权重进行裁剪，并可选择归一化，使接近静止的步骤不会主导梯度，同时让平均损失尺度接近基线。

## 结果
- 在 Libero 上，AttenA+OFT 的平均成功率达到 98.60%，OpenVLA-OFT 为 97.10%，提升 +1.50 个百分点。平均错误率从 2.90% 降至 1.40%。
- AttenA+OFT 在 Libero 各任务上的得分为：Spatial 99.0% ± 0.16，Object 100.0% ± 0.00，Goal 98.8% ± 0.28，10 任务长时程划分 96.6% ± 0.30。
- 与 Libero 上的 OpenVLA-OFT 相比，Spatial 提升 +1.4 个百分点，Object 提升 +1.6 个百分点，Goal 提升 +0.9 个百分点，长时程任务提升 +2.1 个百分点。
- 使用 Libero 上的生成式 pi-0.5 骨干时，AttenA+pi-0.5 的平均成功率达到 97.95%，基线为 96.85%，提升 +1.10 个百分点。平均错误率从 3.15% 降至 2.05%。
- 在 RoboTwin 2.0 上，AttenA+WAM 的平均成功率达到 92.46%，Fast-WAM 为 91.80%，LingBot-VA 为 92.20%。它在 Clean 上报告 93.06%，在 Randomized 上报告 91.86%。
- 论文还声称在 Franka 机械臂上进行了真实世界验证，并具备跨任务泛化能力，但摘录没有给出具体的真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13548v1](https://arxiv.org/abs/2605.13548v1)
