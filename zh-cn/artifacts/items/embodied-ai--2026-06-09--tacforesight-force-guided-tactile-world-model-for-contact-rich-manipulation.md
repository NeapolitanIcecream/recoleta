---
source: arxiv
url: https://arxiv.org/abs/2606.11184v1
published_at: '2026-06-09T17:59:03'
authors:
- Yujie Zang
- Yuhang Zheng
- Xian Nie
- Yupeng Zheng
- Shuai Tian
- Songen Gu
- Chen Gao
- Zining Wang
- Shuicheng Yan
- Wenchao Ding
topics:
- robot-world-model
- tactile-sensing
- force-feedback
- contact-rich-manipulation
- visuo-tactile-policy
- real-robot-evaluation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation

## Summary
## 摘要
TacForeSight 是一个受力条件化的触觉世界模型和策略，用于真实机器人中的接触丰富操作。它先根据腕部力/力矩和当前触觉输入预测短时域的触觉潜变量，再用这些预测引导动作生成。

## 问题
- 当机器人只能在触觉反馈里看到打滑、错位或接触丢失之后才反应时，接触丰富任务就会失败。
- 腕部力/力矩的变化通常早于指尖触觉形变变得明显，所以策略需要把力作为未来接触状态的早期信号。
- 这个问题会影响擦拭、滑动、插入、锁定，以及任务中途受扰后的恢复，因为很小的接触误差就可能让任务停下来。

## 方法
- TacForceWM 将双指触觉场编码成紧凑潜变量，并在高频 6 轴腕部力/力矩条件下预测未来的触觉潜变量块。
- 一个时间力编码器用因果 1D 卷积和下采样，把 120 Hz 的力/力矩数据与 30 Hz 的触觉观测对齐。
- 潜变量动态预测器使用带 AdaLN 力条件化的 Transformer，在未来触觉潜变量上用 MSE 训练，同时加入时间差损失和 SIGReg 正则化。
- 策略通过交叉注意力比较当前触觉潜变量和预测的未来触觉潜变量，再用触觉引导的通道门控融合视觉和触觉特征。
- 一个条件流匹配动作头从视觉、触觉、力派生特征和本体感知特征中预测未来动作块。

## 结果
- 在五个真实机器人接触丰富任务上，TacForeSight 的平均完成分数为 79.0%，高于列出的最强基线 RDP 的 43.0%。
- TacForeSight 在 Vase Wiping 上得分 100%，在 Card Swiping 上得分 85%，在 Tube Adjustment and Insertion 上得分 70%，在 Bulb Insertion and Locking 上得分 80%，在 Wire Insertion 上得分 60%。
- 在任务进行中的扰动下，TacForeSight 的平均分数为 86.7%，高于列出的最强扰动基线 RDP 的 33.3%。
- TacForeSight 在 Wiping-P 上得分 90%，在 Swiping-P 上得分 85%，在 Adjustment-P 上得分 85%。
- 该系统在 RTX 4090D GPU 上以 20 Hz 运行，并且每种方法和任务都用 20 次独立试验进行评估。
- TacForceWM 有 1180 万个参数，训练数据来自 2700 个力-触觉交互 episode；下游流匹配策略有 6890 万个参数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11184v1](https://arxiv.org/abs/2606.11184v1)
