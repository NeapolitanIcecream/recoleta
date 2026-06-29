---
source: arxiv
url: https://arxiv.org/abs/2606.05773v1
published_at: '2026-06-04T06:57:25'
authors:
- Chong Ma
- Taiyi Su
- Jian Zhu
- Jianjun Zhang
- Zitai Huang
- Yi Xu
- Hanli Wang
topics:
- vision-language-action
- world-model
- policy-in-the-loop
- robot-evaluation
- dual-arm-manipulation
- closed-loop-rollout
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation

## Summary
## 总结
PiL-World 用闭环的想象 rollout 来评估 VLA 策略，而不是在真实机器人上执行每个动作块。它根据每个 VLA 动作块预测下一段多视角观测，把生成的最后一帧观测再送回策略中，并且比 Ctrl-World 更接近真实机器人的成功率。

## 问题
- VLA 策略在反馈回路中运行：观察场景，执行一个动作块，再根据新观测决定下一步动作。很多机器人世界模型只沿着固定的、预先收集好的动作轨迹做预测。
- 真实机器人评估速度慢，成本高，因为它需要安全的硬件执行、场景重置和反复试验。
- 如果想象出来的观测质量差，下一步策略动作也会被带偏，所以闭环评估需要过程一致的多视角 rollout，而不只是看起来合理的短视频。

## 方法
- PiL-World 在冻结的 VLA 策略和世界模型之间交替工作：策略预测一个动作块，世界模型预测下一段观测。
- 它用运动学和相机投影，把双臂的绝对关节指令转换成头视角下的夹爪标记控制帧。
- 它使用当前帧、任务指令、视觉控制，以及来自最近多视角帧的潜在历史记忆，生成同步的多视角未来观测。
- 每次预测生成 K=15 帧未来画面，步长为 Δ=3；最后生成的观测会成为下一步策略输入。
- 训练时先用 Wan2.1-14B 初始化，在 RealSource World 上预训练。该数据集包含 35 个任务、11,428 个 episode、超过 1400 万帧，然后再用目标任务中的成功和失败轨迹做 LoRA 微调。

## 结果
- 在三个真实双臂操作任务上，PiL-World 把真实成功率和想象成功率之间的平均差距从 Ctrl-World 的 63.2% 降到 12.0%。
- 对于 40k 步的 VLA checkpoint，Sort Cubes 的真实成功率是 83.3%；PiL-World 估计为 68.3%，差距 15.0 个百分点，而 Ctrl-World 估计为 11.5%，差距 71.8 个百分点。
- 对于 Stack Bowls，真实成功率是 96.7%；PiL-World 估计为 92.5%，差距 4.2 个百分点，而 Ctrl-World 估计为 24.1%，差距 72.6 个百分点。
- 对于 Stack Blocks，真实成功率是 50.0%；PiL-World 估计为 33.3%，差距 16.7 个百分点，而 Ctrl-World 估计为 4.9%，差距 45.1 个百分点。
- 平均无幻觉比例从 Ctrl-World 的 41.5% 升到 PiL-World 的 70.1%。
- PiL-World 报告，在各个任务和 checkpoint 设置下，真实成功率和想象成功率之间的 Pearson 相关系数为 0.94；同时，相比 Ctrl-World，它把 Sort Cubes 的整体 LPIPS 从 0.1454 降到 0.0965，把 Stack Bowls 从 0.1366 降到 0.1100，把 Stack Blocks 从 0.1277 降到 0.1208。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05773v1](https://arxiv.org/abs/2606.05773v1)
