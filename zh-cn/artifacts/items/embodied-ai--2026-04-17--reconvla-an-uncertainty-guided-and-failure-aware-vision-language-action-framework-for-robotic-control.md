---
source: arxiv
url: http://arxiv.org/abs/2604.16677v1
published_at: '2026-04-17T20:20:43'
authors:
- Lingling Chen
- Zongyao Lyu
- William J. Beksi
topics:
- vision-language-action
- robot-reliability
- uncertainty-estimation
- conformal-prediction
- failure-detection
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ReconVLA: An Uncertainty-Guided and Failure-Aware Vision-Language-Action Framework for Robotic Control

## Summary
## 摘要
ReconVLA 在冻结的视觉-语言-动作策略上加入了校准过的不确定性估计和运行时失效检查。它的目标是通过评估动作可靠性、并在执行失败前标记不安全状态，提升机器人控制的安全性。

## 问题
- 视觉-语言-动作模型可以根据图像和语言生成机器人动作，但通常不会为这些动作给出经过校准的置信度。
- 这在真实机器人控制中很关键，因为分布偏移、观测含糊以及带随机性的动作生成都可能导致失败，而且事先没有预警信号。
- 论文针对两类不确定性来源：把机器人推入陌生状态的输入不确定性，以及由随机生成式动作采样带来的噪声不确定性。

## 方法
- 该方法封装一个预训练且冻结的 VLA 策略，而不是重新训练它或修改其权重。
- 在动作不确定性方面，它从生成式策略中在不同噪声采样下抽取多个候选动作，并对动作 token 应用 conformal quantile regression，以构建经过校准的预测区间。
- 系统将这些区间作为置信号，并选择预测不确定性更低的候选动作来执行。
- 在状态失效检测方面，它在一个学习得到的特征空间中跟踪机器人的状态，并用基于 Mahalanobis 距离的检测器衡量当前状态相对训练期安全状态统计量的偏离程度。
- 如果运行时状态超过安全阈值，系统会标记可能的分布外或不安全条件，并可触发停止或回退。

## 结果
- 摘要称，该方法已在仿真和真实机器人操作实验中、跨多种任务进行了测试。
- 文中称，它为动作预测提供了经过校准的不确定性估计，并且这些估计与执行质量和任务成功率相关。
- 文中称，与没有不确定性引导的底层 VLA 相比，它在部署中能更早预判失败、减少灾难性错误并提升可靠性。
- 提供的摘录不包含定量表格，也没有给出成功率、校准误差、数据集或基线差距的具体数值，因此仅凭这段文本无法报告经过核实的数值提升。
- 文中还称，这些收益是在不重新训练或修改基础 VLA 策略的情况下获得的。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16677v1](http://arxiv.org/abs/2604.16677v1)
