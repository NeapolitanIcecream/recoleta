---
source: arxiv
url: http://arxiv.org/abs/2603.10980v1
published_at: '2026-03-11T17:10:16'
authors:
- Zixing Wang
- Devesh K. Jha
- Ahmed H. Qureshi
- Diego Romeres
topics:
- diffusion-policy
- robot-learning
- inference-time-guidance
- multiple-instance-learning
- imitation-learning
relevance_score: 0.31
run_id: materialize-outputs
---

# PPGuide: Steering Diffusion Policies with Performance Predictive Guidance

## Summary
PPGuide 是一种在推理时引导机器人扩散策略的方法：先自动找出哪些观测-动作片段最可能导致成功或失败，再用一个轻量分类器的梯度把策略从失败模式中“推开”。它的意义在于不需要密集奖励、世界模型或额外专家演示，就能提升长时程操作任务的鲁棒性。

## Problem
- 扩散策略虽然擅长学习多模态机器人操作，但生成动作中的微小误差会随时间累积，导致长时程任务失败。
- 现有改进方法通常依赖更多专家数据、密集奖励或世界模型，这些在真实场景中成本高、难获得或计算开销大。
- 难点在于：只有轨迹级的稀疏终局标签（成功/失败），却需要为每个时刻提供可操作的细粒度引导信号。

## Approach
- 提出 **PPGuide**：对一个已训练好的扩散策略做**推理时引导**，无需改动策略结构，也无需重新训练主策略。
- 先收集基础策略在不同训练阶段的 rollout，把整条轨迹当作一个 MIL“包”，其中每个观测-动作 chunk 是“实例”，仅用成功/失败二值终局标签训练注意力式 MIL 模型。
- MIL 模型通过注意力权重自动定位最关键片段，并把实例自标注为三类：**success-relevant (SR)**、**failure-relevant (FR)**、**irrelevant (IR)**；文中指出 IR 数量比 SR/FR 多 **10 倍以上**。
- 再训练一个轻量三分类 guidance classifier，输入观测-动作对，输出其属于 SR/FR/IR 的概率；推理时对动作求梯度：提高 SR 概率、降低 FR 概率，从而修改扩散去噪过程。
- 为减少开销，作者采用**alternating guidance**，只在部分去噪步上施加引导，声称性能接近每步都引导的 constant guidance，但计算更省。

## Results
- 在 **Robomimic** 与 **MimicGen** 多个任务上、且仅用原始专家演示 **10%** 训练基础策略时，PPGuide 整体上“持续优于或匹配”基础扩散策略（DP）与若干变体。
- **Square** 任务：DP 从 **62%/58%**（epoch 500/550）提升到 PPGuide **72%/66%**，分别 **+10 / +8** 个百分点；PPGuide-CG 达到 **72%/68%**，显示交替引导接近常量引导。
- **Transport** 任务：DP **60%/68%** 提升到 PPGuide **68%/76%**，分别 **+8 / +8** 个百分点；PPGuide-CG 为 **68%/74%**。
- **Mug Cleanup D1**：DP **26%/26%** 提升到 PPGuide **30%/36%**，分别 **+4 / +10** 个百分点。
- **Coffee D2**：DP **54%/46%** 提升到 PPGuide **58%/58%**，分别 **+4 / +12** 个百分点；**Kitchen D1** 从 **52%/40%** 到 **52%/44%**（**+0 / +4**）。
- 也存在非一致提升：如 **Stack Three D1** 在 epoch 550 上，DP **30%** 而 PPGuide **28%**（**-2**）；异构基策略评测中 **Transport 1500** 从 **74%** 降到 **70%**（**-4**）。最强提升出现在异构评测：**Transport 1300** 从 **56%** 到 **74%**（**+18**），**Square 1300** 从 **54%** 到 **70%**（**+16**）。

## Link
- [http://arxiv.org/abs/2603.10980v1](http://arxiv.org/abs/2603.10980v1)
