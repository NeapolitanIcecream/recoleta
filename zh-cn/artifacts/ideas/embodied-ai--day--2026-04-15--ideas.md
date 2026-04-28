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

# 任务状态操作栈

## Summary
近期最明确的变化出现在执行器策略之上。一条路径是使用 grounded 规划器，把目标框和局部裁剪图交给控制器，用于杂乱环境下的多步操作。另一条路径是加入任务状态层，提供记忆、后置条件检查和恢复动作，处理那些因为一次中间步骤出错就会失败的工作流。第三条路径是一种训练方案：在 PPO 早期 rollout 中少量使用 VLA 先验，降低交互成本，同时让部署控制器继续保持为 RL 策略。

## 用于杂乱长时程操作的边界框引导规划器与动作策略
从事长时程桌面操作的机器人团队，现在可以测试一种带有明确 grounding 接口的规划器-执行器拆分方案：让 VLM 输出下一个子任务、目标物体和边界框，再把全局场景 tokens 和该边界框对应的高分辨率局部裁剪图，一起送入独立的动作策略。HiVLA 在 RoboTwin 2.0 上报告的平均成功率为 83.3%，H-RDT 为 70.6%；在更难的任务和杂乱环境中的小物体操作上，提升更大。这里有一个具体且有用的实现点：由边界框引导的局部裁剪能让控制器拿到物体细节，同时保留场景上下文，而规划器不需要介入底层电机调参。一个低成本的验证步骤是：在一个杂乱环境下的抓取放置或工具使用任务中加入规划器生成的裁剪输入，并与单流策略比较失败模式；首先要看的错误包括目标身份识别错误、抓取位置不佳，以及多步进度中断。

### Evidence
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): 摘要给出了架构拆分、基于裁剪的 grounding 接口，以及相对 H-RDT 和其他 VLA 基线的基准提升。
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): 摘要确认规划器会输出带目标边界框的结构化计划，底层 DiT 策略会消费 grounded 视觉输入。

## 用于多阶段操作恢复的结构化记忆与后置条件检查
对长时程操作来说，一个实用的支撑层是显式的步骤校验和恢复状态，而不只是更强的动作模型。Goal2Skill 保存情节历史、紧凑的工作记忆摘要和错误寄存器；每个子任务都带有前置条件、后置条件、时域、干扰区域和原语技能选择。执行失败或超时后，系统会重试、调整参数，或重建剩余计划。在五个 RMBench 任务上，它报告的平均成功率为 32.4%，最强基线为 9.8%；在记忆密集型任务上为 38.7%，对应基线为 9.0%。对已经在运行 VLA 执行器的团队，这指向一个明确的构建方向：先加入任务状态记录和后置条件检查，再去重训策略。第一个测试很简单：给一个多阶段工作流加上每一步之后的显式成功检查，并测量恢复机制是否能减少早期失误导致的整任务崩溃。

### Evidence
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): 摘要说明了结构化记忆、校验、恢复闭环，以及 RMBench 上的主要提升，包括记忆密集型任务。
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): 引言给出了一个具体的扫描并重试任务示例，说明这类任务需要持续记忆、中间校验和自适应纠错。

## 在操作任务的早期 PPO 训练中使用稀疏 VLA 引导
机器人 RL 团队可以把预训练 VLA 模型当作临时训练信号使用，而不把它变成部署时的控制器。VLAJS 在 PPO 上加入稀疏教师查询，查询步数最多占 rollout 步数的 20%；它用余弦损失对齐动作方向，然后随着奖励提升逐步衰减并移除这类引导。报告结果是，在若干 ManiSkill 任务上，环境交互次数减少超过 50%，而最终策略仍然是高频 PPO 控制器。对已经有 OpenVLA 级模型、且仿真或机器人时间成本较高的实验室，这是一个具体的流程调整：只在训练早期接入教师引导，部署时继续使用 RL 策略。最低成本的检查方式是，在一个稀疏奖励操作任务上设定固定查询预算，比较达到目标成功率阈值所需时间，并与 PPO 和直接蒸馏基线对照。

### Evidence
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): 摘要概括了稀疏查询设置、短暂引导日程，以及在 ManiSkill 任务上的样本效率提升结论。
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): 正文确认若干任务上的交互次数降幅超过 50%，并说明真实世界测试在 Franka Panda 的一个子集上使用了零样本 sim-to-real 迁移。
