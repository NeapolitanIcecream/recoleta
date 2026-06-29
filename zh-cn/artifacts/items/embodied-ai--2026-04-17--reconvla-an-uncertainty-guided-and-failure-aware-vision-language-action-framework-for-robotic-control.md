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
## 总结
ReconVLA 为冻结的视觉-语言-动作策略加入了校准后的不确定性估计和运行时故障检查。它通过给机器人控制动作打分并在执行失败前标记不安全状态，来提高控制安全性。

## 问题
- 视觉-语言-动作模型可以根据图像和语言生成机器人动作，但通常不会为这些动作输出经过校准的置信度。
- 在真实机器人控制中，这一点很重要，因为分布偏移、含糊的观测和随机的动作生成都可能在没有预警信号的情况下导致失败。
- 论文关注两类不确定性来源：把机器人推入陌生状态的输入不确定性，以及来自随机生成式动作采样的噪声不确定性。

## 方法
- 该方法在预训练且冻结的 VLA 策略外面加一层包装，而不是重新训练它或修改其权重。
- 对于动作不确定性，它在不同噪声采样下从生成式策略中抽取多个候选动作，并将 conformal 分位数回归应用到动作 token 上，构建校准后的预测区间。
- 它把这些区间当作置信度信号，并选择预测不确定性更低的动作候选来执行。
- 对于状态故障检测，它在学习到的特征空间中跟踪机器人状态，并用基于马氏距离的检测器，将运行时状态与训练时的安全状态统计量作偏离度比较。
- 如果运行时状态超过安全阈值，系统会标记为可能的分布外或不安全状态，并可以触发停止或回退。

## 结果
- 摘要称，该方法在多个任务上的仿真和真实机器人操作实验中都进行了测试。
- 摘要称，它对动作预测给出了与执行质量和任务成功相关的校准不确定性估计。
- 摘要称，与没有不确定性引导的底层 VLA 相比，它能更好地提前发现失败、减少灾难性错误，并提高部署时的可靠性。
- 所给摘录没有包含成功率、校准误差、数据集或基线差距的定量表格或具体数值，因此无法仅凭这段文本报告可核实的数值提升。
- 它还称，这些提升无需重新训练或修改基础 VLA 策略。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16677v1](http://arxiv.org/abs/2604.16677v1)
