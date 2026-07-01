---
source: arxiv
url: https://arxiv.org/abs/2606.31723v1
published_at: '2026-06-30T14:24:00'
authors:
- Xidong Zhang
- Yichi Zhang
- Jiaxin Shi
- Fucai Zhu
- Siyu Zhu
- Michael Yu Wang
- Xiaojun Wu
- Weihao Yuan
topics:
- vision-language-action
- tactile-sensing
- dexterous-manipulation
- contact-rich-control
- robot-policy
- tactile-prediction
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# UniTacVLA: Unified Tactile Understanding and Prediction in Vision Language Action Models

## Summary
## 摘要
UniTacVLA 在面向富接触操作的视觉-语言-动作机器人策略中加入触觉推理、未来触觉预测和高频触觉校正。它报告称，在 8 个灵巧操作任务的真实机器人实验中成功率更高，在扰动条件下提升最大。

## 问题
- 视觉-语言-动作策略难以处理打滑、卡滞、接触开始和细小对齐误差等接触事件，尤其是在接触点被遮挡时。
- 许多触觉 VLA 方法把触觉信号作为额外输入送入策略，但没有训练模型理解接触阶段，也没有训练模型预测接触会如何变化。
- 这个问题很重要，因为在插入、擦拭、调整和装配任务中，低频动作块如果不能及时校正细小接触误差，任务就会失败。

## 方法
- UniTacVLA 在 VLM 内学习统一触觉 token，使策略能够把与任务相关的接触信息同视觉和语言观测一起存储。
- 它使用触觉链式思维监督，使触觉潜变量描述接触阶段、接触状态和可能的失败模式。
- 它分两步预测未来触觉潜变量：先由 MLP 预测粗略的未来接触趋势，再由 DiT 细化局部触觉细节。
- 一个轻量级 Transformer 控制器接收规划动作、预测的未来触觉潜变量和实时触觉潜变量，然后向动作加入有界残差校正。
- 训练分为两个阶段：先在干净演示上联合训练动作、语义和触觉预测，再在干净轨迹和受扰恢复轨迹上训练控制器。

## 结果
- 在 8 个真实机器人子任务中，每种设置进行 50 次试验，UniTacVLA 的平均干净条件成功率为 64.0%，平均扰动条件成功率为 53.5%。
- 复现出的最强触觉基线 pi0.5-TacVLA 的平均成功率为干净条件 45.25%、扰动条件 16.25%，因此 UniTacVLA 的平均成功率在干净条件下提高 18.75 个百分点，在扰动条件下提高 37.25 个百分点。
- 相比仅视觉的 pi0.5，UniTacVLA 将平均成功率从干净条件下的 26.0% 提高到 64.0%，从扰动条件下的 5.75% 提高到 53.5%。
- 在无扰动 USB 插入任务中，消融实验的成功率从无触觉组件时的 18% 上升到使用触觉输入时的 30%、使用 T-CoT 时的 36%、使用粗粒度预测时的 44%、使用细粒度预测时的 52%，以及使用控制器时的 62%。
- UniTacVLA 在推理时不使用真实触觉输入的情况下，平均成功率达到干净条件 48.0%、扰动条件 17.0%，这说明触觉监督训练仍能改进学到的接触先验。
- 根据所提供图中文字，USB 消融实验中报告的最佳预测窗口为 12 步。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31723v1](https://arxiv.org/abs/2606.31723v1)
