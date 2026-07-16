---
kind: ideas
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- online adaptation
- reinforcement learning
- world action models
- humanoid locomotion
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/online-adaptation
- topic/reinforcement-learning
- topic/world-action-models
- topic/humanoid-locomotion
language_code: zh-CN
---

# VLA 部署加固

## 摘要
VLA 机器人团队现在有了具体测试目标，用来处理实验室训练后出现的故障：摄像头移动、演示质量弱，以及动作块延迟。最实用的改动是在现有策略周围加入小型部署流程：任务执行前的短探测、模仿学习后的评论器校准在线微调循环，以及用于异步控制的延迟条件适配器。

## 用于摄像头和机器人设置漂移的安全任务前探测
使用 VLA 策略的操作单元，可以在摄像头移动、夹爪更换或安装位置调整后，在第一个任务前加入一次短校准。机器人采样安全目标位姿，记录起始图像、动作和结束图像片段，然后在任务执行期间把这些片段作为上下文前置给策略。ICWM 在主设置中使用 Qwen2.5-VL-3B、FAST 动作分词、长度为 5 的动作块，以及 5 个上下文片段来报告这种模式。

一种低成本验证方式是跨视角验收测试：把摄像头移动到留出角度，在有探测上下文和无探测上下文两种条件下运行相同任务，并跟踪成功率、末端执行器偏移和夹爪过早闭合。ICWM 的 LIBERO 跨视角结果给出了一个有用目标：平均分布外成功率比 Multi-View BC 高 13.0 个百分点，比显式摄像头角度基线高 9.5 个百分点。消融结果让运行检查更明确：移除图像后平均成功率下降 56.4 个百分点，错误上下文的表现低于无上下文。

### 资料来源
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): 总结了 ICWM 的探测流程、部署失败模式、LIBERO 跨视角收益、延迟和消融结果。
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): 描述了如何把与任务无关的随机运动作为上下文，用于在仿真和真实机器人中进行隐式系统识别。

## 行为克隆后的评论器校准在线微调
使用模仿训练 VLA 策略的团队，可以测试一种在线微调任务：先做评论器校准，再更新执行器。FORCE 在演示数据上使用离线 Cal-QL，把一小批当前策略 rollout 混入预热阶段，然后在在线训练期间分别保留专家缓冲区和 rollout 缓冲区。它的自蒸馏步骤会采样候选动作，用评论器打分，并把策略训练到状态级平均 Q 基线以上的动作。

这适合已有演示但机器人因动作不一致或完成速度慢而停滞的重复工位任务。FORCE 报告称，使用 Octo 骨干时，在六个 ManiSkill 任务上的平均成功率为 82.3%；在线微调后，在六个真实 Franka 任务上的平均成功率为 98.3%，高于行为克隆的 45.0%。小规模试点应把成功率、执行步数和早期训练下降与当前行为克隆策略对比，并设置保守的 rollout 限制和停止条件。

### 资料来源
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): 给出了 FORCE 的训练阶段、评论器预热机制、缓冲区设计、自蒸馏方法，以及报告的 ManiSkill 和 Franka 结果。
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): 描述了在线执行器更新前需要做评论器校准的原因，包括初始遗忘和低质量探索问题。

## 用于异步分块 VLA 控制的延迟条件动作适配器
运行分块 VLA 策略的机器人，可以测试一个小型适配器：它根据推理运行期间已经执行的运动来调节下一个动作块。ACNet 编码上一动作块中已经执行的后缀，将其填充到动作时域长度，并作为残差注入到基本冻结的动作头中。感知-语言骨干保持冻结，使改动集中在动作块交接处。

这对接触密集或高精度任务最相关：异步执行消除了空闲等待，但会在动作块边界产生动作跳变。ACNet 在延迟 Kinetix 设置上的平均成功率为 0.79，Naïve Async 为 0.61；在 Meta-World MT50 上以 0.74 的平均成功率匹配完整延迟条件重训练，同时在 Kinetix 上只训练约 20% 的参数。部署测试应在决定完整策略重训练前记录交接不连续、任务成功率、控制频率和接触失败。

### 资料来源
- [Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models](../Inbox/2026-06-24--action-controlnet-a-lightweight-delay-aware-adapter-for-smooth-asynchronous-control-in-vision-language-action-models.md): 总结了 ACNet 适配器设计、异步控制失败模式、参数效率主张，以及 Kinetix、Meta-World 和真实 SO-ARM101 结果。
- [Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models](../Inbox/2026-06-24--action-controlnet-a-lightweight-delay-aware-adapter-for-smooth-asynchronous-control-in-vision-language-action-models.md): 解释了重叠推理期间的过时观测如何在动作块边界导致不连续、抖动和失败。
