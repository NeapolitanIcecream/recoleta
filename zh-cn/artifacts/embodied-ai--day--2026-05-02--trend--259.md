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

# 机器人 VLA 策略正在增加执行时判断

## 概览
这一时期的机器人论文集中在 Vision-Language-Action（VLA）策略的执行时判断上。VLA-ATTC 在动作不确定时增加额外推理。Sentinel-VLA 监控任务状态，并在执行出错时触发规划或恢复。两篇论文都把额外推理和仿真及真实机器人操作任务中的延迟预算联系起来。

## 研究发现

### 自适应测试时动作选择
VLA-ATTC 为 VLA 机器人策略加了一个决策门。它采样两个动作块，测量它们的动态时间规整距离，并把高距离当作动作不确定性。低不确定性的步骤直接执行。高不确定性的步骤在共享的视觉-语言预填充后采样候选动作块，然后由 Relative Action Critic 通过成对比较选出首选动作。

报告中的提升最大，出现在一个错误动作就可能毁掉长任务的场景。在 LIBERO-LONG 上，PI0 在自适应设置下的平均成功率从 82.8% 提升到 90.6%。PI0.5 从 90.6% 提升到 94.0%，完整 deliberation 设置把 PI0.5 的失败率降低了 51.1%。在真实的 Agilex Piper 任务上，PI0 在自适应 VLA-ATTC 下从 46.0% 提升到 58.7%。论文还报告了 20.8 Hz 的控制频率，这很重要，因为候选搜索如果用得太广，会打乱机器人的时序。

#### 资料来源
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): Summary chunk gives the uncertainty gate, Relative Action Critic, LIBERO-LONG results, real-robot results, and 20.8 Hz control figure.

### 操作中恢复的状态监控
Sentinel-VLA 为基于 PI0 的策略加入了一个 Status Monitor 专家。一个学习到的监控查询读取视觉-语言模型缓存，并预测机器人是在初始步骤、正常运行、进入新子任务，还是处于错误状态。策略保存计划、当前子任务和错误反思的记忆。状态变化时，它会更新这段记忆，然后让动作专家根据图像、指令、状态和记忆来生成动作。

证据表明，恢复能力是一个可测量的控制特征。Sentinel-VLA 在受扰动的 RLBench 任务上达到 54.7% 的平均成功率，高于 PI0 的 46.0% 和 OneTwoVLA 的 48.4%。在未见过的 RLBench 任务上，它报告 51.3%，高于 PI0 的 42.0%。在真实的 Agilex Piper 任务上，它在 Stack cube、Pour water 和 Sweep rubbish 三项任务上的平均成功率达到 60.0%。延迟数据也很明确：在 RTX4090 上每个动作 13 ms；在 RLBench 上的错误检测率为 97.4%，在真实世界错误集上为 90.6%。

#### 资料来源
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): Summary chunk covers the monitor states, thought memory, training data, benchmark results, latency, and error-detection rates.
