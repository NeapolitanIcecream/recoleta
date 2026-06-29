---
source: arxiv
url: https://arxiv.org/abs/2605.28527v1
published_at: '2026-05-27T14:23:29'
authors:
- Jiachen Zhang
- Junnan Nie
- Junyi Lao
- Wei Cheng
- Chenghao Liu
- Jiaxin Jiang
- Songfang Huang
topics:
- vision-language-action
- robot-foundation-models
- value-probing
- test-time-action-selection
- libero-goal
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies

## Summary
## 摘要
冻结的 VLA 和视觉表征里包含一种类似价值的成功信号，线性探针可以直接读出它，不需要重新训练策略。论文表明，这个信号在任务/时间步控制下仍然存在，并且能在一些较难的 LIBERO-Goal 任务上改善 Pi0.5 的动作选择。

## 问题
- VLA 策略训练的目标是模仿动作，而不是估计奖励、进展或未来任务成功。
- 如果冻结的 VLA 特征已经编码了成功信息，机器人就可以在测试时对候选动作排序，而不用重新训练策略，也不用单独训练奖励模型。
- 简单的探针结果可能会误导，因为任务身份、时间步和数据集伪特征都可能和成功相关。

## 方法
- 作者从完整轨迹中构建 Monte Carlo 结果目标：成功状态取 \(\gamma^{T-1-t}\)，其中 \(\gamma=0.99\)，失败状态取 0。
- 他们提取了 Pi0.5、OpenVLA、OpenVLA-OFT、SmolVLA、DINOv2、CLIP、随机投影、本体感知和标量干扰特征的冻结表示。
- 他们训练标准化的线性岭回归探针来预测这种类似价值的目标，然后比较 demo-split 和 task-split 的表现。
- 他们用同任务、同时间步配对的样本测试是否依赖捷径，这些样本的标签差至少为 0.20，并加入标签打乱的对照组。
- 他们把训练好的探针用作测试时选择器，在 \(K=16\) 个采样的 Pi0.5 动作片段中做选择，在仿真中展开五步动作前缀，并在不改变策略权重的情况下执行被选中的前缀。

## 结果
- 在 LIBERO-Goal 上，探针使用了来自 1,400 条混合成功和失败轨迹的 311,719 行帧级数据。
- 最好的 task-split \(R^2\) 分数分别是：Pi0.5 为 0.5510，OpenVLA-OFT 为 0.5505，OpenVLA 为 0.5493，SmolVLA 为 0.5257，DINOv2 为 0.5104，CLIP 为 0.5095。
- 标量捷径弱得多：进展和剩余时间都只有大约 \(R^2=0.03\)，任务 one-hot 接近 0，本体感知在 task split 上达到 0.1107。
- 主要的 Pi0.5 同任务、同时间步对照组在 4,605 对样本上的成对排序准确率为 94.22%，而标签打乱对照组为 50.05%。
- 在 10 次同步骤运行中，平均成对准确率为 92.16%，打乱准确率为 49.67%；没有一次探针运行低于 89.58%。
- 在在线 Pi0.5 选择中，合并后的 hard-3 成功率是：价值引导选择 42.44%，随机选择 36.89%，贪心解码 31.11%；在 push-plate 上，成功率从贪心解码的 26.7% 提升到探针引导选择器的 44.3%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28527v1](https://arxiv.org/abs/2605.28527v1)
