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

# 长时间运行机器人工作流的定向可靠性修复

## Summary
机器人团队可以针对长时间执行中的失败采用小范围改动：用于灵巧 rollout 的相对干预、把目标进度和完整完成率分开评分的家用规划器测试，以及用于放置密集型 VLA 任务的 RGB 派生深度特征。

## 用于灵巧 VLA rollout 的相对纠正模式
灵巧机器人实验室应增加一种纠正模式：VLA 策略继续运行，操作员相对于当前策略状态修改手部和手臂命令。实际问题是接管跳变：人在干预时的手部姿态很少与机器人手部姿态匹配，切换到绝对遥操作可能破坏已经稳定的抓握。

HandITL 给出了可复制的具体做法。它在干预时锚定手部状态，把操作员的相对指尖运动映射到机器人手部，并把腕部控制器的残差速度扭量加入策略的手臂命令。系统还会记录已执行的纠正 rollout，用于后续微调。一个小规模采用测试可以先在两三个接触密集任务上记录接管命令变化、物体掉落或重试次数，以及微调后的任务成功率，再决定是否修改基础策略架构。

### Evidence
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): 总结了 HandITL 的相对纠正方法、接管不连续性结果、任务重试减少情况，以及纠正数据带来的微调收益。
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): 描述了接管边界处的手势跳变问题，以及提出的相对干预设计。

## 长时程家用规划器测试，分别评分进度和完成率
评估家用机器人智能体的团队应在模拟中运行自由形式的多目标家务任务，并把目标进度和完整任务完成率分开报告。LongAct 说明了原因：规划器可能完成许多子目标，但在丢失依赖关系、遗忘物体状态或无法跨房间恢复后，仍然无法完成整项家务。

一个实用测试环境可以使用桌面布置、厨房复位和清洁序列等家务任务，并设置步数上限、物体状态日志，以及 Success Rate、Goal-Condition Success、步数和 Improvement Rate 评分。智能体应暴露其依赖图、空间记忆更新和 Critic 决策，这样失败可以追溯到规划、记忆或执行恢复。LongAct 报告的差距足以支持这类评估工作：纯 Qwen3-VL-32B 达到 6.14% Goal-Condition Success 和 0% Success Rate，而使用 HoloMind 的 Qwen3-VL-32B 达到 51.2% Goal-Condition Success 和 15.0% Success Rate。

### Evidence
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): 提供了 LongAct 的基准设置、指标、HoloMind 组件，以及报告的 Goal-Condition Success 和 Success Rate 数值。
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): 说明 LongAct 会在数千步执行中测试指令理解、状态维护、依赖处理和计划调整。

## 用于空间精确 VLA 操作的 RGB 派生深度调制
使用多视角 RGB 摄像头的机器人团队可以先测试一个紧凑的深度特征模块，再增加深度硬件或大型 3D 模型。目标流程包括抓取、放置和物体间交互任务，在这些任务中，纯 2D 视觉 token 会丢失相对位置和深度线索。

Evo-Depth 给出了一条具体实现路径：用 IDEM 从多视角 RGB 中提取紧凑的潜在深度特征，用 SEM 将其转换为 FiLM 风格的缩放和偏移项，再调制动作专家使用的视觉语言 token。低成本试验应在放置密集任务上比较当前 VLA 策略和深度调制变体，并记录成功率、GPU 内存和推理频率。论文报告称，一个 0.9B 参数模型在三个真实世界任务上的平均成功率为 90%，GPU 内存使用量为 3.2 GB，推理频率为 12.3 Hz。

### Evidence
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): 总结了 Evo-Depth 的 RGB 派生深度特征、紧凑模型规模、基准结果和真实世界部署数值。
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): 描述了纯 2D VLA 策略在定位、放置和空间一致操作上的空间能力弱点。
