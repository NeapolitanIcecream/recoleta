---
source: arxiv
url: https://arxiv.org/abs/2607.00678v1
published_at: '2026-07-01T09:21:20'
authors:
- Ronghan Chen
- Yandan Yang
- Zuojin Tang
- Dongjie Huo
- Tong Lin
- Haoning Wu
- Haoyun Liu
- Yuzhi Chen
- Lulu Zheng
- Botai Yuan
- Tianlun Li
- Mingxin Wang
- Dekang Qi
- Bin Hu
- Wei Mei
- Yuze Xuan
- Haolong Yang
- Yanqing Zhu
- Mu Xu
- Zhiheng Ma
- Xinyuan Chang
topics:
- mobile-manipulation
- world-action-model
- vision-language-action
- latent-actions
- generalist-robot-policy
- robot-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ABot-M0.5: Unified Mobility-and-Manipulation World Action Model

## Summary
## 摘要
ABot-M0.5 是一个用于语言条件移动操作的世界动作模型。它面向长时程导航和精细物体交互，通过加入潜在运动意图、分离的动作头，并使用模型自己预测的视频进行训练来实现这一点。

## 问题
- 移动操作需要在长时程内同时控制底盘运动和机械臂，因此反应式 VLA 策略可能丢失任务上下文，并漏掉未来场景变化。
- 现有 World Action Models 通常先预测粗粒度视频片段，再将其映射到低层动作；这可能抹掉接触事件、抓取闭合和小幅对齐修正。
- 在真实未来观测上训练逆动力学会造成部署时的不匹配，因为部署时动作依赖模型预测的未来观测。

## 方法
- 该模型使用三级级联：未来视频潜变量 $z_{t+1}$、帧级潜在动作 $m_t$，然后是可执行机器人动作 $a_t$。
- 冻结的潜在动作编码器从连续帧中提取 $m_t$，因此中间动作信号来自视觉状态变化，而不是机器人特定的运动学标签。
- 双层 Mixture-of-Transformers 将视频、潜在动作和可执行动作的模态流分开，然后把可执行动作拆分为移动和操作两个子空间。
- Conditional Flow Matching 按照推理时使用的相同自回归顺序，训练视频、潜在动作和动作生成。
- Dream Forcing 在自预测视频上训练逆动力学，因此动作预测会看到部署时将面对的那类不完美 rollout 上下文。

## 结果
- 摘录没有提供基准表、成功率、控制误差值或数值消融结果。
- 论文声称在具有挑战性的移动操作和精细操作基准上达到 state-of-the-art 性能，覆盖长时程任务成功率和控制精度。
- 论文声称在图注所列任务上实现真实世界移动操作成功，包括 Arrange Flower 和 Find Toaster。
- 论文声称消融验证了三个主要组件的贡献：中间潜在动作、双层 Mixture-of-Transformers 和 Dream Forcing。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.00678v1](https://arxiv.org/abs/2607.00678v1)
