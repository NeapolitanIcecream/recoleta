---
kind: trend
trend_doc_id: 259
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
topics:
- vision-language-action
- robot manipulation
- test-time compute
- error recovery
- real-time control
run_id: materialize-outputs
aliases:
- recoleta-trend-259
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/test-time-compute
- topic/error-recovery
- topic/real-time-control
language_code: zh-CN
---

# 机器人 VLA 策略正在加入执行时判断

## Overview
本期机器人论文集中讨论 Vision-Language-Action（VLA）策略的执行时判断。VLA-ATTC 在动作不确定时投入额外推理。Sentinel-VLA 监控任务状态，并在执行出错时触发规划或恢复。两篇论文都把新增推理与仿真和真实机器人操作任务中的延迟预算联系起来。

## Clusters

### 自适应测试时动作选择
VLA-ATTC 为 VLA 机器人策略加入一个决策门。它采样两个动作片段，测量它们的动态时间规整（Dynamic Time Warping）距离，并把高距离视为动作不确定性。低不确定性步骤直接执行。高不确定性步骤在共享的视觉-语言预填充后采样候选动作片段，再由 Relative Action Critic 通过成对比较选出偏好的动作。

报告中的收益在一次错误动作会毁掉长任务的场景中最大。在 LIBERO-LONG 上，使用自适应设置时，PI0 的平均成功率从 82.8% 提高到 90.6%。PI0.5 从 90.6% 提高到 94.0%，完整审议设置将 PI0.5 的失败率降低了 51.1%。在真实 Agilex Piper 任务上，使用自适应 VLA-ATTC 时，PI0 从 46.0% 提高到 58.7%。论文还报告了 20.8 Hz 的控制频率；这一点有实际意义，因为如果候选搜索用得过广，会破坏机器人的时序。

#### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 摘要片段给出了不确定性门控、Relative Action Critic、LIBERO-LONG 结果、真实机器人结果，以及 20.8 Hz 控制频率。

### 用于操作中恢复的状态监控
Sentinel-VLA 为基于 PI0 的策略加入一个 Status Monitor 专家。一个学习得到的监控查询读取视觉-语言模型缓存，并预测机器人处于初始步骤、正常运行、进入新子任务，还是出现错误。该策略保留计划、当前子任务和错误反思的记忆。状态变化时，它更新这段记忆，再让动作专家基于图像、指令、状态和记忆生成动作。

证据显示，恢复可以作为可测量的控制功能。Sentinel-VLA 在受扰动的 RLBench 任务上达到 54.7% 的平均成功率，PI0 为 46.0%，OneTwoVLA 为 48.4%。在未见过的 RLBench 任务上，它报告 51.3%，高于 PI0 的 42.0%。在真实 Agilex Piper 任务上，它在 Stack cube、Pour water 和 Sweep rubbish 上达到 60.0% 的平均成功率。延迟数据也很具体：在 RTX4090 上每个动作 13 ms，RLBench 上的错误检测率为 97.4%，真实世界错误集上的错误检测率为 90.6%。

#### Evidence
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 摘要片段涵盖了监控状态、思维记忆、训练数据、基准结果、延迟和错误检测率。
