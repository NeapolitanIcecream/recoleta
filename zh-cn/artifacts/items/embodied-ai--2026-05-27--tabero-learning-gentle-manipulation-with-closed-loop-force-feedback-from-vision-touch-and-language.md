---
source: arxiv
url: https://arxiv.org/abs/2605.27886v1
published_at: '2026-05-27T03:08:21'
authors:
- Qiwei Wu
- Rui Zhang
- Xin Xiang
- Tao Li
- Weihua Zhang
- Junjie Lai
- Renjing Xu
topics:
- vision-language-action
- tactile-sensing
- force-control
- gentle-manipulation
- robot-data-scaling
- robot-benchmark
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language

## Summary
## 总结
Tabero 为类似 VLA 的机器人策略加入触觉和闭环力控制，用于温和操作。摘要称，在温和指令下，平均抓握力降低超过 70%，同时在基准上保持较高任务成功率。

## 问题
- VLA 策略通常使用图像和语言，但缺少触觉反馈，因此它们可以完成任务，却可能挤压、撞击或损坏物体。
- 对齐的视觉-触觉-语言机器人数据很少，因为真实触觉数据采集需要专用硬件和缓慢的维护。
- 标准机器人基准只测成功率，忽略接触质量，例如峰值抓握力和施加力。

## 方法
- Tabero 在 Isaac Lab 中重放开源操作轨迹，包括 LIBERO 风格任务，并配合带触觉的夹爪，生成同步的视觉、触觉、力、本体感觉、动作和语言数据。
- 模拟器记录腕部和第三人称 RGB-D 视图、320 × 240 的模拟 GelSight 触觉图像、11 × 9 的标记位移网格，以及 20 Hz 的指尖接触力。
- 数据流程调整夹爪刚度和阻尼，例如 Kp = 2000、500、200 N/m 以及 Kd = 100、25、10 N·s/m，然后把低力试验配上“gently”，把高力试验配上“firmly”。
- Tabero-VTLA 将触觉标记运动或触觉图像编码为 token，同时预测位姿和力目标，并把它们送入固定的混合控制器。
- 控制器把抓握力和施加到物体上的力分开，然后用力反馈在执行过程中调整夹爪宽度和末端执行器位置。

## 结果
- 摘要称，在温和指令下平均抓握力降低超过 70%，同时保持较高任务成功率；摘要片段没有给出这项对比的具体成功率。
- 跨平台重放让平均任务成功率接近源设置：MuJoCo 在四个 LIBERO 子任务上的平均值为 0.85，而使用相同机器人设置的 Isaac 重放平均值为 0.76。
- 使用带触觉的 Franka 夹爪时，随着力降低，平均数据保留率下降：T-100 为 0.60，T-25 为 0.50，T-10 为 0.36。
- 表 1 中的空间任务对力最敏感：成功率从 Isaac 重放的 0.83 降到 T-100 的 0.42、T-25 的 0.24 和 T-10 的 0.07。
- 物体任务在降低力时更稳定：Isaac 重放为 0.77，T-100 为 0.84，T-25 为 0.87，T-10 为 0.73。
- 该基准用四个力指标评估接触质量：最大瞬时抓握力、平均抓握力、最大瞬时施加力和平均施加力。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27886v1](https://arxiv.org/abs/2605.27886v1)
