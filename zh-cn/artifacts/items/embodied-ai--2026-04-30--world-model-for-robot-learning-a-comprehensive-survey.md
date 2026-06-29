---
source: arxiv
url: https://arxiv.org/abs/2605.00080v1
published_at: '2026-04-30T14:35:31'
authors:
- Bohan Hou
- Gen Li
- Jindou Jia
- Tuo An
- Xinying Guo
- Sicong Leng
- Haoran Geng
- Yanjie Ze
- Tatsuya Harada
- Philip Torr
- Oier Mees
- Marc Pollefeys
- Zhuang Liu
- Jiajun Wu
- Pieter Abbeel
- Jitendra Malik
- Yilun Du
- Jianfei Yang
topics:
- world-models
- robot-learning
- vision-language-action
- video-generation
- learned-simulators
- policy-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# World Model for Robot Learning: A Comprehensive Survey

## Summary
## 摘要
这篇综述围绕一个核心判断组织机器人学习中的世界模型：机器人需要带动作条件的预测，才能在物理任务中进行规划、训练、评估和改进策略。

## 问题
- RT-2、OpenVLA 和 π0 这类机器人策略可以把视觉和语言映射到动作，但摘录说，反应式 VLA 策略在长时程推理、时间信用分配和误差累积上仍然吃力。
- 机器人世界模型的文献分散在策略学习、学习型仿真、视频生成、导航、自动驾驶、数据集和基准测试之间，比较起来很困难。
- 这个问题很重要，因为操作、导航和驾驶都要求机器人在动作之前先预测接触、运动和动作后果。

## 方法
- 这篇综述把机器人世界模型定义为代理-环境动力学的预测模型：给定当前状态或观测、动作序列和可选的语言目标，它预测未来状态或观测。
- 它把视频生成模型视为世界模型的一种常见视觉形式，尤其是在它们以机器人动作或语言指令为条件时。
- 它把策略模型、被动世界模型、可控世界模型和逆动力学模型联系起来，视为对同一预测-控制分布的不同条件查询。
- 它回顾三种主要用途：与机器人策略结合的世界模型、作为学习型仿真的世界模型，以及用于可控未来生成和数据生成的机器人视频世界模型。
- 它还覆盖更广泛的具身领域，包括导航和自动驾驶，并总结了数据集、基准测试和评估协议。

## 结果
- 摘录没有给出新的定量实验结果、基准分数或宣称的性能提升；这是一篇综述论文，不是方法论文。
- 它用公式 1 给出了世界模型的形式化状态转移视图：p(x_{t+1:t+H} | x_t, a_{t:t+H-1}, l)，其中 H 是预测时域。
- 它用公式 2 定义了具身视频世界模型：p(v_{t+1:t+H} | o_t, a_{t:t+H-1}, l)，把未来视觉预测放进带动作条件的机器人学习中。
- 它为可执行的世界模型列出 3 项核心能力：前瞻、由想象驱动的规划、数据放大。
- 它把综述分成 8 个部分，其中第 3 部分讲策略中的世界模型，第 4 部分讲作为仿真的世界模型，第 5 部分讲机器人视频世界模型，第 6 部分讲导航和自动驾驶，第 7 部分讲基准、数据集和结果。
- 可见的分类表至少列出 10 种 IDM 风格方法和 8 种单主干方法，显示出从解耦的视频滚动管线转向更紧密的策略-世界模型耦合。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00080v1](https://arxiv.org/abs/2605.00080v1)
