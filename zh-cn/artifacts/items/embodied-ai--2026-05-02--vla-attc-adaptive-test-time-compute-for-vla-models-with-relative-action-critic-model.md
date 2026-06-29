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
VLA-ATTC 为视觉-语言-动作机器人策略加入了自适应测试时计算：只有当基础策略看起来不确定时才增加额外推理，然后用 Relative Action Critic 在采样到的动作块中做选择。论文报告，在 LIBERO-LONG 和真实机器人任务上，它提升了成功率，同时不需要对基础 VLA 模型再微调。

## 问题
- PI0 和 PI0.5 这类 VLA 策略通常在一次快速前向中直接输出动作，这在长时序或含糊的操作任务上会失败。
- 每个时间步都做昂贵的候选搜索对机器人控制来说太慢，而动作块的绝对动作价值评分又很难训练。
- 这个问题很重要，因为一次错误动作就可能让长任务中断，而真实机器人仍然需要较高的控制频率。

## 方法
- 该方法用不同随机种子采样两个动作块，并计算它们的动态时间规整距离。距离越大，说明动作不确定性越高。
- 如果不确定性低于离线分位数设定的阈值，机器人就执行第一个动作。如果不确定性高于阈值，就进入测试时推理步骤。
- 在推理阶段，动作头会采样 N 个候选动作块，同时复用同一次 VLM 预填充过程，所以昂贵的视觉-语言编码只运行一次。
- Relative Action Critic 在 VLM 特征、查询特征、动作差异和本体感觉状态的条件下比较动作对。锦标赛式选择会保留更优动作，直到只剩一个动作。
- 这个 critic 由自动生成的偏好对训练：专家动作或高步数 flow-matching 动作被标记为优于低步数生成动作，并加入对称的样本增强。

## 结果
- 在 LIBERO-LONG 上，PI0 的平均成功率从 82.8% 升至 90.6%（自适应 VLA-ATTC，+7.8 个百分点），在完整推理下升至 92.2%（+9.4 个百分点）。
- 在 LIBERO-LONG 上，PI0.5 的成功率从 90.6% 升至 94.0%（自适应 VLA-ATTC，+3.4 个百分点），在完整推理下升至 95.4%（+4.8 个百分点）。完整设置把 PI0.5 的失败率从 9.4% 降到 4.6%，下降 51.1%。
- 在真实世界的 Agilex Piper 任务上，PI0 的平均成功率从 46.0% 升至 58.7%（自适应 VLA-ATTC，+12.7 个百分点），在完整推理下升至 63.3%（+17.3 个百分点）。
- 在同样的真实世界任务上，PI0.5 的成功率从 52.0% 升至 62.0%（自适应 VLA-ATTC，+10.0 个百分点），在完整推理下升至 62.7%（+10.7 个百分点）。
- 论文报告了 20.8 Hz 的实用控制频率，并指出 PI0 的动作解码在 86 ms 的推理过程中占 27 ms，这支持在一次共享预填充后批量采样候选动作。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01194v1](https://arxiv.org/abs/2605.01194v1)
