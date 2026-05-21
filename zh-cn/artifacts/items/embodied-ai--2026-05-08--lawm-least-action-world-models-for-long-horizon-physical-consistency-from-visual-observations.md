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
LaWM 是一种视觉潜在世界模型，其下一状态更新来自学习得到的最小作用量目标。它面向长时域视频和机器人场景预测，在这类任务中，不受约束的潜在转移可能偏离物理动力学。

## 问题
- 它处理长时域视觉 rollout 中的累积误差、能量漂移、不稳定加速度和几何错误。
- 这对具身 AI、基于模型的强化学习和机器人规划很重要，因为规划器需要在动力学上保持一致的未来状态，不能只依赖看起来合理的画面。

## 方法
- 每个观测被编码为潜在坐标 q_t；解码后的潜变量生成预测帧或状态。
- 模型学习离散拉格朗日量 L_d(q_k, q_{k+1}; h, eta)，其中包含学习得到的正对角质量矩阵和势能网络。这里的 action 指拉格朗日作用量，不指机器人命令。
- 它在潜在状态上形成离散作用量，并推导离散 Euler-Lagrange 残差。
- 下一潜在状态由展开的局部求解器得到，该求解器降低该残差，并用恒速外推初始化；论文在消融实验中报告，N=4 个求解步骤足以获得稳定的 PIS 和能量行为。
- 训练结合 rollout 预测损失、DEL 残差损失和正则化；推理时递归使用同一个由 DEL 定义的转移。

## 结果
- 在 NewtonGen 风格的匀速运动上，LaWM 报告的 PIS-v_x 为 0.9938±0.0045，对比 NewtonGen 0.9830±0.005、Veo3 0.9784±0.006、Sora 0.6548±0.022、CogVideoX-5B 0.5392±0.007、Wan2.2 0.6395±0.029 和 PhyT2V 0.5349±0.014；参考值为 0.9972。
- 在匀速运动的背景一致性上，LaWM 报告的 BC 为 0.9930±0.0021，对比 NewtonGen 0.9694±0.020 和 Sora 0.9573±0.003，参考值为 1。
- 在匀速运动的运动平滑度上，LaWM 报告的 MS 为 0.9993±0.0001，对比 NewtonGen 0.9962±0.003、Veo3 0.9953±0.001 和 Sora 0.9926±0.003，参考值为 1。
- 在加速度上，LaWM 报告的 PIS-a_x 为 0.8964±0.0275，对比 NewtonGen 0.6568±0.013、Veo3 0.6187±0.308、Sora 0.3437±0.355、CogVideoX-5B 0.5458±0.038、Wan2.2 0.3077±0.261 和 PhyT2V 0.5033±0.011；参考值为 0.8489。
- 摘录还声称它在具身机器人交互指标上有提升，包括 LPIPS、PSNR、AbsRel、δ1、δ2 和 APSNR，但提供的文本没有包含这些数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08279v1](https://arxiv.org/abs/2605.08279v1)
