---
source: arxiv
url: https://arxiv.org/abs/2605.16395v1
published_at: '2026-05-12T13:43:53'
authors:
- Jiajian Li
- Jingyuan Huang
- Junru Gong
- Qi Wang
- Xiaokang Yang
- Yunbo Wang
topics:
- robot-world-model
- differentiable-simulation
- vision-language-action
- sim2real
- robot-policy-optimization
- embodied-ai
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# OrbiSim: World Models as Differentiable Physics Engines for Embodied Intelligence

## Summary
## 摘要
OrbiSim 训练一个机器人世界模型，使其像可微分物理引擎一样工作：它预测显式物理状态，并根据这些状态渲染像素。论文声称，这样可以带来更好的长时程机器人仿真，以及直接基于梯度的策略训练。

## 问题
- MuJoCo、PhysX、Bullet 和 Isaac Sim 等经典模拟器能提供有用的机器人滚动轨迹，但它们的接触和渲染流程通常会阻断用于直接进行策略或参数优化所需的梯度。
- 近年的生成式世界模型可以预测视频，但很多模型不暴露物理状态、场景资产、质量、摩擦或其他闭环机器人控制所需的参数。
- 这很重要，因为机器人学习需要把资产、物理、像素和奖励连接到同一条可训练的执行路径上。

## 方法
- OrbiSim 将仿真拆成两个神经部分：OrbiSim-Dynamics 预测下一个显式物理状态，OrbiSim-Vision 根据该状态渲染下一帧 RGB 观测。
- 动力学模型把机器人和每个物体分别当作独立 token，再用 Transformer 耦合模块来建模接触、约束和多物体交互。
- 动作、物体属性，以及质量、摩擦、几何形状和重力等世界参数通过自适应层归一化来条件化动力学模型。
- 视觉模型使用以预测状态、最近帧和场景描述符为条件的潜变量扩散来生成像素，同时把物理状态作为锚点。
- 由于整个 rollout 可微分，OrbiSim 可以优化场景参数，用于真实到仿真的识别，并通过动力学计算解析策略梯度。

## 结果
- 在 robosuite Push 上，OrbiSim Final 的 PSNR10 为 26.7105，PSNR100 为 19.9819；Vid2World 分别为 22.2014 和 17.8856，AdaWorld 分别为 26.6647 和 12.8346。
- OrbiSim Final 的 LPIPS10 为 0.1078，LPIPS100 为 0.1428；Vid2World 分别为 0.1312 和 0.2551，AdaWorld 分别为 0.1183 和 0.3482。
- OrbiSim Final 的 FVD 为 533.9；Vid2World 为 1750.1，AdaWorld 为 1305.8。
- OrbiSim Final 的轨迹误差为 0.4468；Vid2World 为 0.6754，AdaWorld 为 1.8597。
- 去掉动力学与视觉解耦的消融版本在 PSNR10 上更高，为 27.9346，但长时程指标更差：FVD 为 689.1，轨迹误差为 0.8134；OrbiSim Final 分别为 533.9 和 0.4468。
- 论文还声称，在 Isaac Lab Stack 上，模型可以在 225 步时间范围内稳定进行自回归 rollout，并在 AdaManip 的关节物体和 Physion Drape 的可变形布料上表现出定性泛化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.16395v1](https://arxiv.org/abs/2605.16395v1)
