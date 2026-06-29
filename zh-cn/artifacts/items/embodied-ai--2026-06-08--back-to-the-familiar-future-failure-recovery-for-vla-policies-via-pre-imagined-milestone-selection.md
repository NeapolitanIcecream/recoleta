---
source: arxiv
url: https://arxiv.org/abs/2606.09258v1
published_at: '2026-06-08T09:30:38'
authors:
- Suyeon Shin
- Juwon Kim
- Hyeonbin Park
- Hyunseo Kim
- Hyundo Lee
- Hyung-Sin Kim
- Byoung-Tak Zhang
topics:
- vision-language-action
- failure-recovery
- robot-manipulation
- future-image-goals
- milestone-selection
- libero
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection

## Summary
## 摘要
B2FF 通过选择一个预生成的未来图像作为恢复目标，提升了冻结的、面向前瞻的 vision-language-action 策略的故障恢复能力。在注入故障的 LIBERO 上，在与扰动对齐的恢复时机下，它把 UD-VLA 的平均成功率从 56.3% 提高到 74.0%。

## 问题
- VLA 机器人策略在操作过程中会因为动作误差、接触变化或外部扰动偏离演示式状态。
- 一旦机器人偏离轨迹，从当前图像直接重新规划会产生不稳定动作，即使任务仍然可行也是如此。
- 这会影响机器人部署，因为像夹爪偏移或物体位移这类本来可以恢复的小失误，可能会直接导致整个任务失败。

## 方法
- 在执行前，B2FF 让冻结的 VLA 根据干净的初始观测生成一个包含 12 个未来图像里程碑的库。这个想象步骤中不会执行任何动作。
- 在恢复时，它以恢复索引为中心，用偏移 {-1, 0, +1, +2, +4} 从里程碑库中构造一个局部候选集。
- 一个学习到的选择器使用失败观测、最近的观测历史和候选图像，对每个候选里程碑打分。
- 被选中的里程碑会固定为未来图像目标，冻结的 VLA 只生成朝向该图像的动作片段。
- 选择器先用反事实滚动轨迹离线训练，这些轨迹会标记每个候选里程碑是否会带来任务成功，然后再用一步 actor-critic 风格目标继续优化。

## 结果
- 在注入故障的 LIBERO 上，B2FF 把 UD-VLA 的平均成功率从 56.3% 提高到 74.0%，提升了 17.7 个百分点。
- 在同一基准上，B2FF 在 Object 上达到 69.3%，在 Spatial 上达到 66.0%，在 Goal 上达到 73.3%，在 Long 上达到 87.3%。
- 在线触发版本在注入故障的 LIBERO 上达到 64.5% 的平均成功率，而 UD-VLA 为 56.3%。
- 在没有注入故障的标准 LIBERO 上，B2FF 将 UD-VLA 的平均成功率从 91.3% 提高到 93.7%。
- 在注入故障的 LIBERO-Object 上做选择器消融时，完整 B2FF 的成功率为 69.3%，而从头监督训练为 63.3%，只用观测打分为 50.8%。
- 在 90 次恢复试验的真实世界测试中，B2FF 在对 35 组真实世界恢复样本完成选择器调优后，整体成功率达到 61.1%；摘录中说它优于 UD-VLA 和固定锚点基线，但没有给出这些基线的具体分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09258v1](https://arxiv.org/abs/2606.09258v1)
