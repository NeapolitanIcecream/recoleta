---
source: arxiv
url: https://arxiv.org/abs/2606.17463v1
published_at: '2026-06-16T03:25:34'
authors:
- Shoujing Zhu
- Zhenyang Liu
- Fungmiu Wang
- Jiafeng Wang
- Bo Yue
- Guiliang Liu
- Simo Wu
- Xiangyang Xue
- Taiping Zeng
topics:
- vision-language-action
- robot-memory
- repetitive-manipulation
- cross-subtask-conditioning
- robot-foundation-model
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# WeaveLA: Event Driven Cross-Subtask Latent Memory Weaving for Repetitive Robot Manipulation

## Summary
## 摘要
WeaveLA 在冻结的 VLA 策略上加入事件驱动的潜在记忆通道，让重复机器人任务能把一个已完成子任务的信息带入下一个动作片段。最强的结果来自 RoboMME SwingXtimes 的 N=3 设置：在 pi_0.5 骨干上，成功率从 0% 提升到 47.8%。

## 问题
- 短窗口 VLA 策略可以执行单个操作原语，但在 swing three times、place N objects、press stop after a count 等重复任务中，它们会在子任务边界丢失所需状态。
- 这一点很关键，因为当前观测可能有歧义：在 SwingXtimes 和 StopCube 中，正确的下一步动作取决于此前完成了多少个子目标，不能只看可见场景。
- 以往的记忆方法通常逐帧写入、检索演示阶段，或在事件处触发，但没有把紧凑的已完成子任务摘要传给动作专家。

## 方法
- WeaveLA 只在 rollout 期间的子目标完成事件写入记忆。在报告的仿真实验中，模拟器提供这些边界，因此论文把记忆机制与边界检测分开考察。
- Query-driven Memory Weaver 使用一次注意力池化，在冻结 VLA 的视觉、文本和本体感知特征上，把刚完成的片段压缩成 8 个宽度为 2048 的潜在 token。
- 这些潜在 token 通过动作生成路径为下一个子任务提供条件，在 pi_0.5 的 Gemma 动作专家内部使用记忆交叉注意力和 AdaRMS 调制。
- 基础 VLA 大部分保持冻结；可训练部分约为 46M 参数，叠加在约 3.4B 参数的基础策略上，约为基础规模的 1.4%。
- 训练使用分阶段动作 grounding、记忆 warmup，随后使用语义对齐和对比辅助损失，权重分别为 0.05 和 0.02；子目标文本只在训练期间使用。

## 结果
- 在使用 pi_0.5 加注意力池化的六个已训练 RoboMME 任务上，平均成功率从 Weaver 关闭时的 19.0% 提升到 Weaver 开启时的 24.7%。
- 在 16 任务训练规模下，平均成功率从 17.3% 提升到 23.3%。
- 在 SwingXtimes 的 N=3 设置，也就是报告中最难的重复切片上，成功率从 0% 提升到 47.8%；在 16 任务规模下，同一切片从 4% 提升到 30%。
- 在 6 任务规模下，N>=2 的合并重复任务成功率从 7.2% 提升到 24.6%，相对增益为 3.4 倍；在 16 任务规模下，从 5.8% 提升到 17.4%，相对增益为 3.0 倍。
- N=1 的单次执行 episode 在 Weaver 开启和关闭设置下都接近 100%，这支持论文关于增益来源的说法：提升来自跨子任务记忆，一般容量增加不是主要原因。
- 论文还报告了额外的定位结果：StopCube 从 8% 提升到 22%，Hard episode 从 1.4% 提升到 12.5%；在配对匹配 episode 中，Weaver 开启独有地解决了 13 个 SwingXtimes episode，相比之下 Weaver 关闭为 1 个，StopCube 为 8 个对 1 个。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17463v1](https://arxiv.org/abs/2606.17463v1)
