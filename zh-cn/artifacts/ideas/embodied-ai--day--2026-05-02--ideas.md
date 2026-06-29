---
kind: ideas
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- vision-language-action
- robot manipulation
- test-time compute
- error recovery
- real-time control
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/test-time-compute
- topic/error-recovery
- topic/real-time-control
language_code: zh-CN
---

# 机器人 VLA 的执行时控制检查

## Summary
机器人 VLA 策略正在在动作头外加上实用的控制逻辑。具体工作包括：用于昂贵动作选择的不确定性门控、用于恢复的状态监控器，以及把触发率、恢复成功率和动作延迟放在一起记录的评估。

## 适用于长时程操作的不确定性门控候选动作选择
运行 PI0 风格策略的机器人团队，可以在花额外推理算力做动作候选之前先加一个小的决策门控。VLA-ATTC 用不同随机种子采样两个动作块，测量它们的动态时间规整距离，并把较大的距离当作动作不确定性。低不确定性的步骤直接执行。高不确定性的步骤复用一次视觉-语言 prefill，采样多个动作块，再交给 Relative Action Critic，通过两两比较选出胜者。

这是一项面向长时程操作的具体部署改动，因为一次错误动作就可能毁掉整个任务。论文报告显示，在自适应设置下，PI0 在 LIBERO-LONG 上的平均成功率从 82.8% 提升到 90.6%，PI0.5 从 90.6% 提升到 94.0%。在真实的 Agilex Piper 任务上，PI0 从 46.0% 提升到 58.7%。报告中的 20.8 Hz 控制频率很关键，因为候选搜索只有在不超过机器人时序预算时才有用。

一个有用的起步测试，是在已有机器人 rollout 上记录动作块分歧，设定一个离线分位数阈值，只把分歧高的步骤重新走一遍候选采样。是否采用，应看成功率是否提升，同时控制器频率是否仍然满足要求。

### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 概括了不确定性门控、Relative Action Critic、LIBERO-LONG 和 Agilex Piper 任务上的成功率提升，以及报告的 20.8 Hz 控制频率。
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 说明了需要量化情境难度、限制多动作采样开销，并且只在不确定步骤触发测试时推理。

## 受扰动机器人 rollout 的状态监控与恢复记忆
面向操作任务的部署，应测试一个状态监控器，让它观察策略自己的执行状态，并在机器人处于故障状态时触发恢复。Sentinel-VLA 加入了一个学习得到的 `[MONITOR]` 查询，它读取 VLM 的 key-value cache，并把当前步骤分成 Initial、Normal、New-subtask 或 Error 四种状态。策略会保留计划、当前子任务和错误反思的记忆，然后把图像、指令、状态和记忆一起送入动作专家。

用户可见的问题很直接：机器人如果漏抓或抓错对象，可能还会继续执行原来的动作序列。Sentinel-VLA 在受扰动的 RLBench 任务上报告平均成功率 54.7%，高于 PI0 的 46.0% 和 OneTwoVLA 的 48.4%。在真实的 Agilex Piper 任务中，覆盖 Stack cube、Pour water 和 Sweep rubbish，它报告的平均成功率是 60.0%。监控器的延迟也足够低，适合控制环路：在 RTX4090 上是 13 ms/action，RLBench 上的错误检测率是 97.4%，真实错误集合上是 90.6%。

实际实现可以先做一个带标签的受扰动 rollout 数据集：在成功轨迹里注入夹爪、位姿和语义错误，加入恢复路标，然后把监控器和动作模型一起训练。团队应先检查 false negative，因为漏掉错误状态最容易让坏的 rollout 继续下去。

### Evidence
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 概括了 Status Monitor、thought memory、EC-Gen 受扰动轨迹生成、成功结果、延迟和错误检测率。
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 指出了运行时故障的操作失败模式：VLA 策略在抓到空壶等错误后仍可能继续动作。

## 用于执行时推理的低延迟基准
VLA 评估应该报告执行时推理何时被触发、它能多大程度上恢复受扰动的 rollout，以及每个动作要花多少成本。这两篇论文指向同一个落地障碍：额外推理可以改善操作任务，但机器人控制器仍然需要稳定的动作频率。

基准表应该包含普通任务成功率、受扰动任务成功率、不确定性或错误状态的触发率、触发后的恢复成功率，以及目标 GPU 上实测的动作延迟。VLA-ATTC 通过只把不确定步骤送去候选采样，在保持 20.8 Hz 控制的同时提升了成功率。Sentinel-VLA 在加入状态分类和恢复记忆后，报告 13 ms/action。只看成功率，不能完整反映部署效果。

对已经在收集机器人 rollout 的实验室来说，这个改动成本很低。加上不确定性分数、状态标签、触发决策、选中的动作块和实际推理时间的 trace logging。真正有用的比较，是在相同时间预算下，对比一个快速的一次前向策略和同一策略加上执行时判断后的表现。

### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 报告了 VLA-ATTC 的自适应推理、成功率提升和 20.8 Hz 控制频率。
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 报告了 Sentinel-VLA 的受扰动任务成功率、状态监控、错误检测率和 13 ms/action 延迟。
