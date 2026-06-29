---
kind: ideas
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- robotics
- VLA
- world models
- long-horizon planning
- video evaluation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robotics
- topic/vla
- topic/world-models
- topic/long-horizon-planning
- topic/video-evaluation
language_code: zh-CN
---

# 面向长时间机器人工作流的定向可靠性修复

## Summary
机器人团队可以针对长时间执行中的失败做小范围改动：为灵巧轨迹加入相对介入，在家务规划测试中把目标进展和整项完成分开评分，以及为以放置为主的 VLA 任务加入 RGB 派生的深度特征。

## Relative correction mode for dexterous VLA rollouts
灵巧机器人实验室应该增加一种校正模式，让操作者在 VLA 策略继续运行时，基于当前策略状态调整手和臂的指令。实际问题是接管跳变：在人手姿态和机器人手姿态在介入时刻很少一致，绝对式遥操作切换会破坏稳定抓握。

HandITL 提供了一个可以直接照搬的做法。它在介入时刻固定手部状态，把操作者的相对指尖运动映射到机器人手上，并把腕部控制器的残差速度扭量加到策略的手臂指令上。系统还会记录执行过的校正轨迹，供后续微调使用。一个小规模落地测试，是在改基础策略架构之前，先在两到三个接触密集任务上记录接管时的指令变化、物体掉落或重试次数，以及微调后的任务成功率。

### Evidence
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): Summarizes HandITL’s relative correction method, takeover discontinuity results, task retry reductions, and fine-tuning gains from correction data.
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): Describes the gesture-jump problem at the takeover boundary and the proposed relative intervention design.

## Long-horizon household planner tests with separate progress and completion scores
评估家务机器人智能体的团队，应该在仿真里运行自由形式的多目标家务任务，并把目标进展和整项任务完成情况分开报告。LongAct 说明了原因：规划器可以完成很多子目标，但只要失去依赖关系、忘记物体状态，或者跨房间恢复失败，整项家务还是会失败。

一个可用的测试框架可以包含书桌整理、厨房重置和清洁序列这类任务，设置步数上限、物体状态记录，以及 Success Rate、Goal-Condition Success、step count 和 Improvement Rate 的评分。智能体应当暴露依赖图、空间记忆更新和 Critic 的决策，这样失败就能追到规划、记忆或执行恢复环节。LongAct 报告的差距足够大，值得做这类评测：纯 Qwen3-VL-32B 的 Goal-Condition Success 只有 6.14%，Success Rate 为 0%；而加入 HoloMind 后，Qwen3-VL-32B 的 Goal-Condition Success 提高到 51.2%，Success Rate 提高到 15.0%。

### Evidence
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): Provides LongAct’s benchmark setup, metrics, HoloMind components, and reported Goal-Condition Success and Success Rate numbers.
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): Explains that LongAct tests instruction interpretation, state maintenance, dependency handling, and plan adaptation over thousands of steps.

## RGB-derived depth modulation for spatially precise VLA manipulation
使用多视角 RGB 相机的机器人团队，可以先测试一个紧凑的深度特征模块，再决定要不要加深度硬件或更大的 3D 模型。目标任务是抓取、放置和物体间交互，这些任务里只看 2D 视觉 token 会丢掉相对位置和深度线索。

Evo-Depth 给出了一条具体实现路径：用 IDEM 从多视角 RGB 中提取紧凑的潜在深度特征，再用 SEM 把它们变成 FiLM 风格的 scale 和 shift 项，最后调制动作专家使用的视觉语言 token。一个低成本试验应该把现有 VLA 策略和深度调制版本放在以放置为主的任务上对比，同时记录成功率、GPU 内存和推理频率。论文报告，0.9B 参数模型在三个真实任务上的平均成功率是 90%，GPU 内存占用 3.2 GB，推理频率 12.3 Hz。

### Evidence
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Summarizes Evo-Depth’s RGB-derived depth features, compact model size, benchmark results, and real-world deployment numbers.
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Describes the spatial weakness of 2D-only VLA policies on localization, placement, and spatially consistent manipulation.
