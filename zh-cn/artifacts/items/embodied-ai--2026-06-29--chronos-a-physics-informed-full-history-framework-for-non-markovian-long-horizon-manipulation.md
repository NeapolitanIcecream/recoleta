---
source: arxiv
url: https://arxiv.org/abs/2606.30318v1
published_at: '2026-06-29T14:00:17'
authors:
- Yulin Zhou
- Yimeng Wang
- Nengyu Wang
- Shaojia Xing
- Shiyun Tu
- Xiang Li
- Jingkai Zhang
- Ningbo Jiang
- Yuankai Lin
- Hua Yang
- Xiangrui Zeng
- Zhouping Yin
topics:
- vision-language-action
- generalist-robot-policy
- long-horizon-manipulation
- robot-memory
- state-space-models
- imitation-learning
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Chronos: A Physics-Informed Full-History Framework for Non-Markovian Long-Horizon Manipulation

## Summary
## 摘要
Chronos 是一种用于长程操作的机器人模仿学习方法，适用于当前相机视图可能遮蔽任务阶段的情况。它声称，通过把完整观察历史作为策略状态，并用学习得到的加速度场细化动作块，可在依赖记忆的操作任务上取得大幅提升。

## 问题
- 只使用当前帧或短窗口的 VLA 策略，在两个相同观察来自不同历史时，可能会选择错误动作。
- 这会影响取出、检查并放回物体等任务；在关键步骤前后，场景可能看起来相同，但正确的下一步动作不同。
- 长程模仿需要在完整演示中做时间信用分配，因为决定当前动作的事件可能发生在当前步骤之前很久。

## 方法
- 在每个物理控制步骤，Chronos 将观察和本体感知融合为一个状态 token，使序列长度与轨迹长度一致。
- 一个 Mamba 风格的选择性状态空间模型以因果方式处理完整 token 序列，并在循环状态中保存任务阶段信息。
- 训练通过完整演示序列反向传播损失，因此后期错误可以更新早期记忆形成。
- IMLE 生成器从历史条件状态中采样一个粗粒度的多模态动作块。
- 一个受二阶薛定谔方程启发的桥接模型通过预测加速度场来细化该动作块，目标是生成比直接回归、扩散或一阶流头更平滑的机器人运动。

## 结果
- 在 RMBench 上，Chronos 报告的平均成功率为 73.6%，比 π_0.5 高 +62.4 个百分点，相对提升 6.6 倍，参数量为其十分之一。
- 在 RMBench 上，它比 Mem-0 高 22.8 个百分点，同时参数量不到 Mem-0 的三十分之一。
- 在使用一个 RGB 相机的真实双臂测试中，Chronos 报告 4 个任务的平均成功率为 78%。
- 在 3 个依赖记忆的真实任务上，Chronos 报告的平均成功率为 72%，而 π_0.5 在同一子集上为 0%。
- 论文评估了 16 个仿真任务和 4 个真实实验，包括精密插入、通用操作和依赖记忆的长程控制。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30318v1](https://arxiv.org/abs/2606.30318v1)
