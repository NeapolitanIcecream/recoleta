---
source: arxiv
url: https://arxiv.org/abs/2606.27163v1
published_at: '2026-06-25T15:31:23'
authors:
- Ilia Larchenko
topics:
- vision-language-action
- robot-folding
- sim2real
- reinforcement-learning
- bimanual-manipulation
- deformable-objects
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Learning to Fold: prizewinning solution at LeHome Challenge 2026 (1st place online, 2nd offline)

## Summary
## 摘要
本文报告了一个在竞赛中获胜的双臂衣物折叠系统。系统以 flow-matching VLA 策略为核心，并通过强化学习、回放、人类修正和 sim-to-real 调优改进。

## 问题
- 该系统面向可变形物体操作：用两个 6-DOF 机械臂基于 RGB 摄像头折叠衬衫、上衣、长裤和短裤。
- 这项任务有难度，因为单靠行为克隆很难完成布料折叠：布料状态变化快，奖励稀疏，策略还必须泛化到未见过的衣物。
- 真实世界阶段还带来迁移问题：作者在无法接触最终评测机器人的情况下完成训练。

## 方法
- 基础策略是源自 pi_0.5 的 SigLIP + Gemma VLA，其中 Gemma-300M 动作专家通过 flow matching 输出 30 步、12 维的关节动作块。
- 同一个网络同时预测动作和值函数类信号：成功概率、完成度、衣物类型、关键点距离、未来关键点距离，以及以动作为条件的成功残差。
- 训练结合 AWR 式优势加权采样和 RECAP 式优势条件控制，因此高优势帧会被更多采样，策略也能在推理时接受引导。
- 数据采集通过 HuggingFace Hub 异步运行：一个训练器、多个 Isaac Sim rollout worker，以及一个用于修正困难状态的手动 DAgger 工作站。
- sim-to-real 使用摄像头对齐工具、大量图像和环境增强、速度对齐，以及 human-in-the-loop 真实机器人数据。

## 结果
- 在线仿真赛：在 LeHome Challenge 2026 的 62 支队伍中获得第 1 名。
- 在线得分：总体成功率 79.63%，领先第 2 名 6.1 个百分点。
- 在线评测覆盖 4 类衣物，每类 20 件：10 件已见和 10 件未见，其中包括私有未见衣物。
- 真实世界决赛：在 ICRA 2026 入围的前 8 支仿真队伍中获得第 2 名。
- 真实评测使用 4 类衣物，每类 5 件，其中每类包含 3 件已见和 2 件未见衣物。
- 论文给出的正式消融证据很少；它描述了实际提交的系统，并说明各组件没有经过受控测试。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27163v1](https://arxiv.org/abs/2606.27163v1)
