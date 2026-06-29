---
source: arxiv
url: https://arxiv.org/abs/2606.23296v1
published_at: '2026-06-22T13:09:34'
authors:
- Chengyu Bai
- Peidong Jia
- Tiecheng Guo
- Yukai Wang
- Rui Ma
- Fangyuan Zhao
- Chunkai Fan
- Xiaobao Wei
- Jintao Chen
- Hao Wang
- Ying Li
- Xiaozhu Ju
- Jian Tang
- Shanghang Zhang
topics:
- interactive-world-model
- robot-world-model
- vision-language-action
- robot-data-scaling
- sim2real
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# IOI: Decoupling Kinematics and Physics for Interactive World Models

## Summary
## 摘要
IOI 是一个交互式机器人世界模型，用精确的机器人运动学来指导视频生成，从而减轻模型仅从像素学习机器人运动的负担。它面向用于机器人策略训练和评估的动作条件 rollout。

## 问题
- 机器人策略需要模拟环境：环境要能根据动作返回真实感视频，并给出合理的接触动力学。
- 完全学习式的动作到视频世界模型可能偏离指令指定的机器人运动，也可能生成不可能的物体状态，例如穿透、变形或物体永久性丢失。
- 这会影响策略学习，因为质量差的 rollout 可能误导训练，并让模拟中的策略评估不可靠。

## 方法
- IOI 接收机器人 URDF 和未来动作序列，通过积分或逆运动学把动作转换为关节状态，再用正向运动学计算连杆位姿。
- 它把计算得到的机器人几何渲染为正面、侧面和俯视三个正交视图，从而避免为对齐渲染运动和观测场景而进行外参相机标定。
- Multi-view Kinematic Aggregation and Injection 模块把三个渲染视图融合为运动学 token，将其与视频 token 对齐，并通过可训练的运动学块注入到冻结的扩散 Transformer 中。
- 视频生成器在潜空间中使用 flow matching：历史帧提供场景条件，运动学 token 提供机器人运动条件，生成器预测未来帧和场景交互。

## 结果
- 在 RoboTwin 表格摘录中，IOI 报告的总体 SSIM 最好：0.8637；IRASim 为 0.8198，Ctrl-World 为 0.8192。
- IOI 报告的总体 LPIPS 最好：0.0695；IRASim 为 0.0803，Ctrl-World 为 0.0867。该指标越低越好。
- IOI 报告的总体 FVD 最好：41.23；IRASim 为 126.20，Ctrl-World 为 64.90。该指标越低越好。
- 总体 PSNR 结果不一致：IOI 报告为 25.73，低于 IRASim 的 26.81，高于 Ctrl-World 的 25.50。
- 在 Move Can Pot 上，IOI 报告 30.41 PSNR、0.9288 SSIM、0.0310 LPIPS 和 89.43 FVD，在该任务的四个指标上都超过列出的两个基线。
- 摘录还声称具备 zero-shot OOD 泛化能力，策略评估接近真实物理模拟器，并且用 IOI 合成数据训练的真实世界策略与用遥操作数据训练的策略相当，但所示文本没有为这些说法提供定量数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23296v1](https://arxiv.org/abs/2606.23296v1)
