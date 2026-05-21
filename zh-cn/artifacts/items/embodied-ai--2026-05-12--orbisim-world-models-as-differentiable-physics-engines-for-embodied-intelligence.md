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
OrbiSim 将机器人世界模型训练成类似可微分物理引擎的系统：它预测显式物理状态，并从这些状态渲染像素。论文声称，这可以改进长时域机器人仿真，并支持直接基于梯度的策略训练。

## 问题
- MuJoCo、PhysX、Bullet 和 Isaac Sim 等经典仿真器能生成有用的机器人 rollout，但其接触和渲染流水线常会阻断直接策略优化或参数优化所需的梯度。
- 近期生成式世界模型可以预测视频，但许多模型不暴露闭环机器人控制所需的物理状态、场景资产、质量、摩擦或其他参数。
- 这很重要，因为机器人学习需要把资产、物理、像素和奖励连接在同一条可训练执行路径中的仿真器。

## 方法
- OrbiSim 将仿真拆成两个神经模块：OrbiSim-Dynamics 预测下一个显式物理状态，OrbiSim-Vision 从该状态渲染下一个 RGB 观测。
- 动力学模型把机器人和每个物体视为独立 token，然后用 Transformer 耦合模块来建模接触、约束和多物体交互。
- 动作、物体属性，以及质量、摩擦、几何形状和重力等世界参数，通过 Adaptive Layer Normalization 对动力学进行条件控制。
- 视觉模型使用潜在扩散，并以预测状态、近期帧和场景描述为条件生成像素，同时把物理状态作为锚点。
- 由于 rollout 可微分，OrbiSim 可以优化场景参数以进行 real-to-sim 识别，并通过动力学计算解析策略梯度。

## 结果
- 在 robosuite Push 上，OrbiSim Final 报告的 PSNR10 为 26.7105，PSNR100 为 19.9819；相比之下，Vid2World 为 22.2014 和 17.8856，AdaWorld 为 26.6647 和 12.8346。
- OrbiSim Final 报告的 LPIPS10 为 0.1078，LPIPS100 为 0.1428，优于 Vid2World 的 0.1312 和 0.2551，以及 AdaWorld 的 0.1183 和 0.3482。
- OrbiSim Final 报告的 FVD 为 533.9；Vid2World 为 1750.1，AdaWorld 为 1305.8。
- OrbiSim Final 报告的轨迹误差为 0.4468；Vid2World 为 0.6754，AdaWorld 为 1.8597。
- 去除动力学-视觉解耦的消融版本有更高的 PSNR10，为 27.9346，但长时域指标更差：FVD 为 689.1，轨迹误差为 0.8134，而 OrbiSim Final 分别为 533.9 和 0.4468。
- 论文还声称，OrbiSim 在 Isaac Lab Stack 上可以在 225 步时域内保持稳定的自回归 rollout，并在 AdaManip 中的关节物体和 Physion Drape 中的可变形布料上展现定性泛化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.16395v1](https://arxiv.org/abs/2605.16395v1)
