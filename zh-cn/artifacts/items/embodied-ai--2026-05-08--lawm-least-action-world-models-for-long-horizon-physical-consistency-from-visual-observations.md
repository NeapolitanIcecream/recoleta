---
source: arxiv
url: https://arxiv.org/abs/2605.08279v1
published_at: '2026-05-08T07:03:13'
authors:
- Qixin Xiao
- Maani Ghaffari
topics:
- world-model
- visual-prediction
- embodied-ai
- robot-interaction
- physics-informed-learning
- variational-integrator
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# LaWM: Least Action World Models for Long-Horizon Physical Consistency from Visual Observations

## Summary
## 摘要
LaWM 是一种视觉潜变量世界模型，它的下一状态更新来自学习到的最小作用量目标。它面向长时程视频和机器人场景预测，这类任务里，无约束的潜状态转移容易偏离物理动力学。

## 问题
- 它要解决长时程视觉滚动预测中的误差累积、能量漂移、加速度不稳定和几何误差。
- 这对具身 AI、基于模型的强化学习和机器人规划都很重要，因为规划器需要在动态上保持一致的未来，而不只是看起来合理的帧。

## 方法
- 每个观测都会编码成潜坐标 q_t；解码后的潜变量生成预测帧或状态。
- 模型学习一个离散拉格朗日量 L_d(q_k, q_{k+1}; h, eta)，其中包含可学习的正对角质量矩阵和势能网络。这里的 action 指的是拉格朗日作用量，不是机器人动作。
- 它在潜状态上构造离散作用量，并导出离散欧拉-拉格朗日残差。
- 下一潜状态由一个展开的局部求解器寻找，该求解器以恒速外推初始化，用于减小残差；论文在消融实验中报告，N=4 个求解步骤就足以得到稳定的 PIS 和能量表现。
- 训练把滚动预测损失、DEL 残差损失和正则项结合起来，推理时则递归使用同一个由 DEL 定义的转移。

## 结果
- 在 NewtonGen 风格的匀速运动上，LaWM 报告 PIS-v_x 为 0.9938±0.0045；NewtonGen 为 0.9830±0.005，Veo3 为 0.9784±0.006，Sora 为 0.6548±0.022，CogVideoX-5B 为 0.5392±0.007，Wan2.2 为 0.6395±0.029，PhyT2V 为 0.5349±0.014；参考值为 0.9972。
- 在匀速运动的背景一致性上，LaWM 报告 BC 为 0.9930±0.0021；NewtonGen 为 0.9694±0.020，Sora 为 0.9573±0.003，参考值为 1。
- 在匀速运动的运动平滑度上，LaWM 报告 MS 为 0.9993±0.0001；NewtonGen 为 0.9962±0.003，Veo3 为 0.9953±0.001，Sora 为 0.9926±0.003，参考值为 1。
- 在加速度任务上，LaWM 报告 PIS-a_x 为 0.8964±0.0275；NewtonGen 为 0.6568±0.013，Veo3 为 0.6187±0.308，Sora 为 0.3437±0.355，CogVideoX-5B 为 0.5458±0.038，Wan2.2 为 0.3077±0.261，PhyT2V 为 0.5033±0.011；参考值为 0.8489。
- 摘要还声称它在具身机器人交互指标上有提升，包括 LPIPS、PSNR、AbsRel、δ1、δ2 和 APSNR，但给出的文本没有这些数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08279v1](https://arxiv.org/abs/2605.08279v1)
