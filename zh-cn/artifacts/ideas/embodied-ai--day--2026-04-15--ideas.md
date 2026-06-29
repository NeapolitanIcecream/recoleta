---
kind: ideas
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- long-horizon manipulation
- hierarchical control
- reinforcement learning
- uav navigation
tags:
- recoleta/ideas
- topic/robotics
- topic/long-horizon-manipulation
- topic/hierarchical-control
- topic/reinforcement-learning
- topic/uav-navigation
language_code: zh-CN
---

# Task-state manipulation stack

## Summary
最直接的短期变化发生在执行器策略上方。一条路是用带定位的规划器，把目标边界框和局部裁剪图交给控制器，处理杂乱场景里的多步操作。另一条路是加上任务状态层，包含记忆、后置条件检查和恢复动作，用来应对在某个中间步骤出错后失败的流程。第三条路是在早期 PPO rollout 中少量使用 VLA 先验，降低交互成本，同时让部署控制器继续保持在 RL 中。

## Bounding-box-guided planner and action policy for cluttered long-horizon manipulation
做长时程桌面操作的机器人团队现在可以测试一种规划器-执行器拆分，并配上明确的定位接口：让 VLM 生成下一步子任务、目标物体和边界框，然后把全局场景 token 和该边界框的高分辨率裁剪同时送入独立的动作策略。HiVLA 在 RoboTwin 2.0 上的平均成功率为 83.3%，高于 H-RDT 的 70.6%，在更难任务和杂乱场景中的小物体操作上提升更大。这个做法的操作意义很明确：边界框引导的局部裁剪让控制器保留物体细节，同时不丢场景上下文，而规划器不再介入低层电机调参。一个成本较低的验证办法，是在一个杂乱的抓取放置或工具使用任务里加入规划器生成的裁剪图，再和单流策略比较失败模式：目标识别错误、抓取位置不准、以及多步进展丢失，这三类错误最先看。

### Evidence
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): Summary gives the architecture split, crop-based grounding interface, and benchmark gains over H-RDT and other VLA baselines.
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): Abstract confirms the planner outputs structured plans with target bounding boxes and the low-level DiT policy consumes grounded visual inputs.

## Structured memory and post-condition checks for multi-stage manipulation recovery
长时程操作需要的支撑层，是明确的步骤验证和恢复状态，而不只是更强的动作模型。Goal2Skill 会保存情节历史、紧凑的工作记忆摘要和错误记录；每个子任务都带有前置条件、后置条件、执行时长、干扰区域和一个原始技能选择。执行失败或超时后，系统会重试、调整参数，或重建剩余计划。在五个 RMBench 任务上，它报告的平均成功率为 32.4%，高于最强基线的 9.8%；在记忆密集型任务上则是 38.7% 对 9.0%。对已经在跑 VLA 执行器的团队，这给出一个具体改动：在重新训练策略前，先加上任务状态记录和后置条件检查。第一个测试很直接：给一个多阶段流程加上每一步后的明确成功检查，看看恢复机制是否能在早期出错后减少整单崩溃。

### Evidence
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Summary states the structured memory, verification, recovery loop, and the headline RMBench improvements including memory-intensive tasks.
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Introduction gives a concrete example of a scan-and-retry task that needs sustained memory, intermediate verification, and adaptive correction.

## Sparse VLA guidance during early PPO training for manipulation
机器人强化学习团队可以把预训练 VLA 模型当作临时训练信号，而不是部署控制器。VLAJS 在 PPO 上加入稀疏教师查询，查询只占 rollout 步数的最多 20%，再用余弦损失对齐动作方向，随着回报提升逐步衰减并移除这类引导。文中报告的结果是，在多个 ManiSkill 任务上，环境交互次数减少了 50% 以上，而最终策略仍然是一个高频 PPO 控制器。对已经有 OpenVLA 级模型、且仿真或机器人时间成本很高的实验室，这是一条明确的流程改动：只在训练早期接入教师引导，部署时继续用 RL 策略。最便宜的检查方法，是在一个稀疏奖励操作任务上设置固定查询预算，比较达到阈值成功率所需时间，并对照 PPO 和直接蒸馏基线。

### Evidence
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): Summary captures the sparse-query setup, transient guidance schedule, and the sample-efficiency claim on ManiSkill tasks.
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): Main text confirms over-50% interaction reduction on several tasks and states that real-world tests use zero-shot sim-to-real transfer on a Franka Panda subset.
