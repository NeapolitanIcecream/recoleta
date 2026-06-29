---
source: arxiv
url: https://arxiv.org/abs/2605.19678v1
published_at: '2026-05-19T11:10:20'
authors:
- Jingzhou Luo
- Yifan Wen
- Yongjie Bai
- Xinshuai Song
- Yang Liu
- Liang Lin
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RoVLA: Multi-Consistency Constraints for Robust Vision-Language-Action Models

## Summary
## 摘要
RoVLA 训练一个视觉-语言-动作策略，让它在改写后的指令、去噪阶段变化和受扰动的观测下保持动作预测稳定。摘录声称它在 LIBERO-Plus、RoboTwin 2.0 和真实机器人任务上表现更强，但没有给出成功率表或具体提升幅度。

## 问题
- 当摄像头视角、光照、背景、机器人状态或表述变化，而任务本身没有变化时，VLA 策略会失效。
- 这对操作任务很重要，因为只在训练和测试条件一致时才可用的机器人，在家庭、实验室和工厂里都不可靠。
- 以往工作通常通过更多数据、后训练或世界模型来改进 VLA 行为，而 RoVLA 把对任务保持不变的变化保持一致，作为训练的一部分。

## 方法
- RoVLA 使用双系统 VLA 策略：InternVL3.5-2B 提取语言和视觉 token，32 层 DiT 动作生成器通过条件流匹配预测连续动作块。
- 指令一致性在训练中采样语义等价的改写版本。在 LIBERO 和真实任务中，Qwen3-8B 每条轨迹生成约 15 个改写；RoboTwin 2.0 已经为每个任务提供 100 条等价指令。
- 演化一致性采样两个流匹配时间步 τ1 和 τ2，并对同一动作目标下它们预测的速度场之间的不一致进行惩罚。
- 观测一致性沿着会增加一致性损失的梯度方向，对视觉语义特征和机器人状态施加扰动，然后用停止梯度目标训练扰动分支去匹配干净分支。
- 总损失把干净输入和受扰动输入上的监督流匹配损失，与 EC 和 OC 一致性损失结合起来，并使用基于干净监督损失 EMA 的自适应权重。

## 结果
- 提供的摘录没有给出定量成功率、错误率、置信区间或精确的基线差距。
- 论文声称 RoVLA 在 LIBERO-Plus、RoboTwin 2.0 和真实世界操作任务上优于强基线，并且在鲁棒性和泛化上更好。
- LIBERO-Plus 评估覆盖 7 个扰动维度：布局、摄像头、机器人初始化、语言、光照、背景和传感器噪声。
- LIBERO 训练使用 1,693 个基础示范和 15,874 个经 LIBERO-Plus 扰动增强的示范。
- RoboTwin 2.0 评估覆盖 50 个双臂操作任务，训练时收集了 2,500 个干净示范和 25,000 个随机环境示范。
- 真实世界测试使用一台 Franka Research 3 机器人、5 个桌面任务，以及共 125 个示范。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19678v1](https://arxiv.org/abs/2605.19678v1)
