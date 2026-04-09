---
source: arxiv
url: http://arxiv.org/abs/2604.04161v1
published_at: '2026-04-05T16:03:32'
authors:
- Yuanchang Liang
- Xiaobo Wang
- Kai Wang
- Shuo Wang
- Xiaojiang Peng
- Haoyu Chen
- David Kim Huat Chua
- Prahlad Vadakkepat
topics:
- vision-language-action
- robot-policy-inference
- action-chunking
- robot-manipulation
- uncertainty-estimation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Adaptive Action Chunking at Inference-time for Vision-Language-Action Models

## Summary
## 摘要
AAC 是一种用于视觉-语言-动作模型的推理时方法。它会在执行过程中动态选择动作块大小，而不是在整个 episode 中使用一个固定值。它利用采样得到的候选轨迹的动作熵，在预测不确定时选择更短的动作块，在预测稳定时选择更长的动作块。

## 问题
- VLA 策略通常会执行动作块：先规划若干个未来动作，然后在每一步都不重新规划的情况下连续执行。
- 固定的动作块大小会带来权衡。较大的动作块会降低对新观测的响应速度，较小的动作块则可能导致块之间不连续、运动抖动，以及重规划之间更频繁的模式跳变。
- 最优动作块大小会随任务变化，甚至会在同一任务的不同阶段变化，因此手动调一个固定值会限制性能和可扩展性。

## 方法
- AAC 只在推理时运行，不改变训练过程或模型架构。
- 模型会并行采样 **N** 个候选动作块，然后用熵来估计每个未来时间步的不确定性：对连续的平移/旋转动作使用高斯微分熵，对离散的夹爪动作使用标准熵。
- 对于每个可能的执行长度 **h**，AAC 会计算预测动作块前 **h** 步的平均动作熵。
- 它会在平均熵随动作块长度变化幅度最大的点选择动作块大小，并设置一个下界 **ξ**，以保证机器人在重新规划前至少执行一定数量的动作。
- 在实际运行中，高熵会对应更短的执行长度和更频繁的重规划；低熵会对应更长的执行长度，从而让动作更平滑，并减少模型调用次数。

## 结果
- 在 **RoboCasa** 上，使用默认固定动作块大小 **h=16** 的 GR00T 平均成功率为 **59.7%**，而 **GR00T + AAC** 达到 **62.0%**，在 **24 个任务** 上提升 **2.3 个百分点**。
- 在 RoboCasa 的 **Rotation** 任务中，AAC 将成功率从 **57.6%** 提高到 **61.4%**。在 **Container** 任务中，从 **80.3%** 提高到 **82.2%**。在 **Relocation** 任务中，从 **42.1%** 提高到 **44.4%**。
- 在 **LIBERO** 上，使用固定 **h=16** 的 GR00T 平均成功率为 **94.1%**，而 **AAC** 达到 **95.0%**。在更难的 **LIBERO-Long** 基准上，性能从 **88.8%** 提高到 **92.8%**，提升 **4.0 个百分点**。
- 在 RoboCasa 上与其他固定动作块大小相比，AAC 的平均成功率 **62.0%** 高于 **h=2: 47.0%**、**h=4: 56.2%**、**h=8: 61.2%**、**h=12: 60.2%** 和 **h=16: 59.7%**。
- 使用另一种骨干模型时，**pi-0.5** 在 LIBERO 上的平均成功率从 **97.0%** 提高到使用 AAC 后的 **97.9%**；列出的最大提升出现在 **Long** 任务上，从 **92.5%** 提高到 **95.2%**。
- 在 **LIBERO-Pro** 的 OOD 扰动测试中，**GR00T** 的平均成功率从 **3.9%** 提高到使用 AAC 后的 **6.3%**，**pi-0.5** 则从 **30.9%** 提高到 **34.8%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04161v1](http://arxiv.org/abs/2604.04161v1)
