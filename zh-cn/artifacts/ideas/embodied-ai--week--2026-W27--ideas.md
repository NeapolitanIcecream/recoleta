---
kind: ideas
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- world models
- robot manipulation
- deployment systems
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/robot-manipulation
- topic/deployment-systems
language_code: zh-CN
---

# 机器人 VLA 执行可靠性

## Summary
机器人 VLA 工作正在进入执行中最先出问题的环节：跨机器人队列的模型服务延迟、长 rollout 漂移，以及策略无法跟踪接触造成的场景变化。实际工作是把调度、进度信号和与动作相关的未来变化目标加入现有机器人流水线，然后用任务完成度来测试，而不是只看请求延迟或单步预测。

## 面向多机器人工厂任务的符合 SLO 的模型服务调度器
运行 VLA、规划器、安全模型和监控模型的工厂机器人团队，在为每台机器人购买一条专用加速器路径之前，应先测试带任务级 SLO 的共享 GPU 服务池。ROSA 给出了具体工作流：用声明式任务文件记录机器人队列、模型组件、提示词、调用率、重试规则，以及停止、重发、重新规划或呼叫人工等回退动作。调度器再根据符合 SLO 的动作吞吐量，选择模型放置、请求路由、批处理和每个任务的动作率。

一种低成本验证方法是把已记录的机器人观测回放到当前服务设置和一个 Ray Serve 风格的共享池中，然后只统计在任务 SLO 内到达、且能让机器人安全继续工作的动作。ROSA 报告称，在 8 块 NVIDIA H200 GPU、最多 64 个虚拟机器人的设置下，相比每台机器人分配专用服务的基线，符合 SLO 的工厂生产率最高提升 12.06 倍；相比使用同一服务基础设施但没有 ROSA 调度器的共享服务器基线，合格的工厂动作吞吐量最高提升 2.44 倍。采用障碍很具体：降低模型延迟只有在改变安全任务进展时才有用，而工厂负载包含机器人执行物理动作时的空闲时间，专用 GPU 分配会浪费这些时间。

### Evidence
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): 描述 ROSA 的共享 GPU 池、声明式任务文件、调度器输入，以及报告的符合 SLO 的吞吐量提升。
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): 论文摘要围绕共享 GPU 池服务、多模型流水线、故障处理和工厂生产率来说明该系统。

## 面向长时程双臂装配策略的连续进度头
构建长时程操作演示的团队应为策略加入连续进度输出，并用它触发子任务切换。FurnitureVLA 为双臂装配给出了直接实现方式：把任务拆成由语言条件控制的子任务，例如抓取、对齐、插入、抬升、旋转和撤离；训练 VLA 预测 14 维双臂动作加一个标量进度值；当进度越过阈值时切换子任务。

关键测试是完整任务 rollout，而不是短子任务分数。FurnitureVLA 覆盖真实尺度家具装配，包含 4 到 7 个子任务和 650 到 1,550 个控制步。它在三种 IKEA 风格任务上的平均仿真成功率从单体微调的 0.48 提升到 0.80。消融实验也给了部署规划的实用检查项：移除后置相机设置会把平均成功率降到 0.50，离散进度预测在三个仿真家具任务上全部失败。进度监督最适合早期毫米级误差会把后续步骤推入演示数据缺失状态的场景。

### Evidence
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): 总结 FurnitureVLA 的连续进度输出、子任务触发、长时程任务设置和成功率提升。
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): 摘要说明了最多 7 个子任务、1,550 个控制步的设置，以及带进度增强的 VLA 设计。

## 面向视觉变化下操作策略的缓存未来变化目标
操作策略团队可以增加一个训练步骤，为每条演示标注预期场景结果、可能变化的像素和局部运动方向。Bridge-WA 在真实机器人轨迹上训练未来变化教师模型，缓存未来 token、变化图和运动流图，再训练一个轻量预测器，使部署后的策略无需运行 5B 教师模型，也无需生成密集未来图像。

这适合抓取、推动、倾倒和插入任务：机器人需要作用于接触后会变化的区域，同时忽略光照、背景和干扰物。第一个实验应在同一批操作任务上比较现有 VLA 与未来变化条件策略，并加入干扰物、光照变化和桌布变化。Bridge-WA 报告称，VLABench 平均成功率为 52.8%，而列出的最强成功率基线为 43.1%；在 Dobot hard-track 平均值上，它在有干扰物时为 62.8%，光照变化下为 74.0%，桌布变化下为 70.4%，相比之下 X-VLA 分别为 53.2%、65.2% 和 55.6%。

### Evidence
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): 描述未来变化教师模型、缓存目标、轻量预测器、推理设置和基准结果。
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): 摘要说明了三种紧凑先验，以及部署时移除密集未来图像生成。
