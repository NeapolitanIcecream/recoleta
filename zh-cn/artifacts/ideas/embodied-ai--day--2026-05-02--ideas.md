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

# 面向 VLA 机器人的执行时控制检查

## Summary
机器人 VLA 策略正在动作头周围加入实用控制逻辑。具体工作包括用于高成本动作选择的不确定性门、用于恢复的状态监控器，以及同时记录触发率、恢复成功率和动作延迟的评估。

## 用于长时程操作任务的不确定性门控候选动作选择
运行 PI0 风格策略的机器人团队，可以在为候选动作投入额外推理之前加入一个小型决策门。VLA-ATTC 用不同随机种子采样两个动作块，测量它们的 Dynamic Time Warping 距离，并把高距离视为动作不确定性。低不确定性步骤直接执行。高不确定性步骤复用一次视觉-语言预填充，采样多个动作块，再交给 Relative Action Critic；该 critic 通过成对比较选出胜者。

这是面向长时程操作的具体部署改动，因为一个错误动作可能毁掉整次运行。论文报告，在自适应设置下，LIBERO-LONG 上的 PI0 平均成功率从 82.8% 升至 90.6%，PI0.5 从 90.6% 升至 94.0%。在真实 Agilex Piper 任务中，PI0 从 46.0% 升至 58.7%。报告的 20.8 Hz 控制率很关键，因为候选搜索只有保持在机器人的时序预算内才有用。

一个有用的初始测试，是在现有机器人 rollout 上记录动作块分歧，设置离线百分位阈值，并只对高分歧步骤用候选采样重放。是否采用应取决于成功率是否提高，同时控制器频率是否仍不低于要求。

### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 总结了不确定性门、Relative Action Critic、LIBERO-LONG 和 Agilex Piper 任务上的成功率提升，以及报告的 20.8 Hz 控制率。
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 描述了量化情境难度、限制多动作采样开销，并只在不确定步骤触发测试时思考的需求。

## 用于受扰动机器人 rollout 的状态监控和恢复记忆
操作部署应测试一个状态监控器，用来观察策略自身的执行状态，并在机器人处于故障状态时触发恢复。Sentinel-VLA 加入了一个学习得到的 `[MONITOR]` 查询，它读取 VLM 键值缓存，并将当前步骤分类为 Initial、Normal、New-subtask 或 Error。该策略保留计划、当前子任务和错误反思的记忆，然后让动作专家以图像、指令、状态和记忆为条件生成动作。

用户能直接感受到的问题很简单：机器人抓取失败或抓错物体后，可能继续执行原来的动作序列。Sentinel-VLA 报告，在受扰动的 RLBench 任务上平均成功率为 54.7%，相比之下 PI0 为 46.0%，OneTwoVLA 为 48.4%。在真实 Agilex Piper 任务中，覆盖 Stack cube、Pour water 和 Sweep rubbish，它报告的平均成功率为 60.0%。监控器的延迟声明也足够小，可用于控制环：在 RTX4090 上为 13 ms/action，错误检测率在 RLBench 上为 97.4%，在真实世界错误集上为 90.6%。

实际构建方式是制作一个带标签的受扰动 rollout 集：向成功轨迹注入夹爪、位姿和语义错误，加入恢复路点，并把监控器与动作模型一起训练。团队应先检查假阴性，因为漏检错误状态最可能让糟糕的 rollout 继续下去。

### Evidence
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 总结了 Status Monitor、思维记忆、EC-Gen 受扰动轨迹生成、成功率结果、延迟和错误检测率。
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 指出了运行中的故障模式：VLA 策略在抓住空水壶等运行时错误后，仍可能继续动作。

## 面向 VLA 策略执行时推理的延迟感知基准
VLA 评估应报告执行时推理何时触发、它多常能恢复受扰动 rollout，以及每个动作的成本。两篇论文指向同一个采用障碍：额外推理可以提升操作表现，但机器人控制器仍需要稳定的动作速率。

基准表应包含普通任务成功率、受扰动任务成功率、不确定或错误状态的触发率、触发后的恢复成功率，以及目标 GPU 上测得的动作延迟。VLA-ATTC 只把不确定步骤路由到候选采样，在保持 20.8 Hz 控制的同时报告了成功率提升。Sentinel-VLA 在加入状态分类和恢复记忆的同时报告 13 ms/action。这些测量说明，仅看成功率不足以评估部署。

对已经收集机器人 rollout 的实验室来说，这项改动成本不高。加入轨迹日志，记录不确定性分数、状态标签、触发决策、选中的动作块和墙钟推理时间。有用的比较是在相同时序预算下，对比快速单遍策略和加入执行时判断的同一策略。

### Evidence
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](../Inbox/2026-05-02--vla-attc-adaptive-test-time-compute-for-vla-models-with-relative-action-critic-model.md): 报告了 VLA-ATTC 的自适应思考、成功率提升和 20.8 Hz 控制频率。
- [Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery](../Inbox/2026-05-02--sentinel-vla-a-metacognitive-vla-model-with-active-status-monitoring-for-dynamic-reasoning-and-error-recovery.md): 报告了 Sentinel-VLA 的受扰动任务成功率、状态监控、错误检测率和 13 ms/action 延迟。
