---
source: arxiv
url: https://arxiv.org/abs/2605.01194v1
published_at: '2026-05-02T02:13:11'
authors:
- Wenhao Li
- Xiu Su
- Dan Niu
- Yichao Cao
- Hongyan Xu
- Zhe Qu
- Lei Fan
- Shan You
- Chang Xu
topics:
- vision-language-action
- test-time-compute
- robot-manipulation
- action-critic
- preference-learning
- libero-long
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model

## Summary
## 摘要
VLA-ATTC 为视觉-语言-动作机器人策略加入自适应测试时计算：只有在基础策略看起来不确定时才增加推理开销，然后用 Relative Action Critic 从采样得到的动作片段中选择。论文报告称，在不微调基础 VLA 模型的情况下，该方法提高了 LIBERO-LONG 和真实机器人任务的成功率。

## 问题
- PI0 和 PI0.5 等 VLA 策略通常通过一次快速前向计算输出动作，这在长时程或含糊的操作任务中可能失败。
- 在每个时间步运行开销高的候选搜索对机器人控制来说太慢，而针对动作片段训练绝对动作价值评分也很难。
- 这个问题很重要，因为一次错误动作就可能让长任务失败，同时真实机器人仍需要较高的控制频率。

## 方法
- 该方法用不同随机种子采样两个动作片段，并测量它们的 Dynamic Time Warping 距离。距离高表示动作不确定性高。
- 如果不确定性低于由离线百分位数设定的阈值，机器人执行第一个动作。如果不确定性高于阈值，则进入测试时审议步骤。
- 在审议期间，动作头采样 N 个候选动作片段，同时复用同一次 VLM 预填充，因此开销高的视觉-语言编码只运行一次。
- Relative Action Critic 在 VLM 特征、查询特征、动作差异和本体感知状态的条件下比较动作对。锦标赛选择会保留更受偏好的动作，直到只剩一个动作。
- 该 critic 使用自动生成的偏好对训练：专家动作或高步数 flow-matching 动作被标注为优于低步数生成动作，并使用对称配对增强。

## 结果
- 在 LIBERO-LONG 上，PI0 的平均成功率从 82.8% 提升到使用自适应 VLA-ATTC 时的 90.6%（+7.8 个百分点），使用完整审议时达到 92.2%（+9.4 个百分点）。
- 在 LIBERO-LONG 上，PI0.5 的成功率从 90.6% 提升到使用自适应 VLA-ATTC 时的 94.0%（+3.4 个百分点），使用完整审议时达到 95.4%（+4.8 个百分点）。完整设置将 PI0.5 的失败率从 9.4% 降至 4.6%，降幅为 51.1%。
- 在真实世界 Agilex Piper 任务上，PI0 的平均成功率从 46.0% 提升到使用自适应 VLA-ATTC 时的 58.7%（+12.7 个百分点），使用完整审议时达到 63.3%（+17.3 个百分点）。
- 在同一组真实世界任务上，PI0.5 的成功率从 52.0% 提升到使用自适应 VLA-ATTC 时的 62.0%（+10.0 个百分点），使用完整审议时达到 62.7%（+10.7 个百分点）。
- 论文报告了可用的 20.8 Hz 控制频率，并指出 PI0 动作解码在一次 86 ms 推理中耗时 27 ms，这支持在一次共享预填充后进行批量候选采样。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01194v1](https://arxiv.org/abs/2605.01194v1)
