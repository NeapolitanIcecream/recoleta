---
kind: ideas
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot-learning
- safety
- data-generation
- medical-robotics
- vla
tags:
- recoleta/ideas
- topic/robot-learning
- topic/safety
- topic/data-generation
- topic/medical-robotics
- topic/vla
language_code: zh-CN
---

# 面向机器人学习的动作-状态对齐

## Summary
这一天的机器人学习工作指向三个明确方向：保留动作标签、用于跨机器人迁移的合成示范；能放进控制时序安全预算的行为切换检测；以及终于把视频、指令、执行状态和镜头位姿对齐起来、可用于闭环训练的结肠镜数据采集。共同模式是把观测、动作和与安全相关的状态连接得更紧，而且给出的数字已经足以支撑小范围构建和评估流程调整。

## 用于跨构型双臂迁移的带动作标签合成示范管线
双臂操作团队现在可以测试一条明确的跨机器人迁移数据管线：生成模拟器轨迹回放，把它们转换成照片级真实感视频，并保留配对的动作标签用于策略训练。CRAFT把这套方法做成了可执行流程。它从一个小规模真实数据集出发，构建数字孪生，在仿真中重放轨迹，并使用 Canny 引导的视频扩散，让生成视频保留仍与动作匹配的运动结构。

实际使用场景很直接：实验室已经在一套双臂系统上收集了示范，希望策略能在另一套系统上工作，同时避免重新为目标机器人采集一套新数据。论文报告的迁移结果已经足以支持把这条流程当作工程项目来做，而不只是数据增强实验。在仿真中，从双臂 UR5 迁移到双臂 Franka，在没有目标机器人示范的情况下，Lift Pot 达到 82.6%，Place Cans 达到 89.3%，Stack Bowls 达到 86.0%。在从 xArm7 到 Franka 的真实测试中，三个任务分别达到 17/20、15/20 和 16/20 的成功次数。这些结果超过了简单的 shadow 基线，也超过了一个使用 100 条目标机器人采集示范的目标数据基线。

一个具体的下一步是，围绕取放或容器操作这类单一任务族，搭建内部数据增强作业，把模拟器轨迹、渲染得到的控制视频、生成的照片级真实感视频和原始动作序列一起存成一条训练记录。一个低成本检查方法是，看用源机器人数据加上生成的目标风格示范训练出的策略，是否能减少在一种新构型或新相机设置上所需的目标端遥操作数据量。

### Evidence
- [CRAFT: Video Diffusion for Bimanual Robot Data Generation](../Inbox/2026-04-04--craft-video-diffusion-for-bimanual-robot-data-generation.md): 摘要给出了方法、动作标签保留方式，以及仿真和真实测试中的跨构型结果。
- [CRAFT: Video Diffusion for Bimanual Robot Data Generation](../Inbox/2026-04-04--craft-video-diffusion-for-bimanual-robot-data-generation.md): 摘要确认了这条统一的数据增强流程可覆盖视角、光照、背景和机器人构型，并通过模拟器生成的轨迹保留动作标签。

## 用于共享工作空间操作安全的行为切换检测模块
共享工作空间机器人团队可以在冻结的 VLA 策略前面加入一个行为切换检测器，作为控制时序内的安全层。UA-ToM 是这种设计的一个具体例子。它在冻结的 7B 主干上增加了一个 992K 的信念模块，用来跟踪协作者是否在任务中途改变了行为，并把额外推理时间控制在 7.4 ms，仍处于 50 ms 的控制预算内。

这个运行问题很明确：当人类或协作机器人改变策略后，如果机器人还沿用旧假设，就会持续进入错误的空间。论文把检测器和部署时真正重要的时延目标连在一起。在更严格的 ±3 步窗口下，也就是 50 ms 控制循环中的约 150 ms，UA-ToM 在 1,200 个 episode 上达到 85.7% 的硬检测率。安全效果也很直接：启用切换检测后，切换后的碰撞次数从每个 episode 的 2.34 降到 1.11，下降了 52%。

最近可以调整的工作流是：评估协作操作控制器时，要看更窄的切换窗口和切换后的碰撞次数，而不只看宽松容差下的平均检测分数。一个具体试点方案是，在现有共享操作策略旁边放一个小型信念跟踪器，在切换概率高时触发保守回退模式或重新规划模式，并记录切换后的碰撞次数和近距离停留时间。做 handover、co-carry 或共享装配的团队无需重训基础控制器就能测试这套方法。

### Evidence
- [Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation](../Inbox/2026-04-04--belief-dynamics-for-detecting-behavioral-shifts-in-safe-collaborative-manipulation.md): 摘要报告了冻结 7B VLA 上的 992K 信念模块、±3 步检测结果、碰撞下降幅度，以及 7.4 ms 的额外开销。
- [Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation](../Inbox/2026-04-04--belief-dynamics-for-detecting-behavioral-shifts-in-safe-collaborative-manipulation.md): 摘要说明了共享工作空间中的安全问题，以及任务执行期间可靠检测行为阶段切换的需求。

## 面向失败恢复自主研究的对齐多模态结肠镜记录
医疗机器人团队现在有了一种明确的方法，可以构建适合自主系统研究的闭环结肠镜数据集，而不只是做回顾性视频分析。OpenRC 把低成本机器人改造方案与视频、操作者指令、执行状态和 6-DoF 远端镜头位姿的同步记录结合起来。数据在共享栈上完成对齐，并以 LeRobot 2.1 格式发布。

这改变了做机器人结肠镜研究的实验室首先值得建设的东西。现在，数据集可以包含导航、失败和恢复 episode，并具备足够紧的动作与状态对齐，用于策略学习和面向控制的评估。OpenRC 报告了 1,894 个 episode、约 19 小时数据，覆盖 10 种任务变化，其中包括 142 个失败 episode 和 141 个恢复 episode。对齐后，操作者动作与执行状态之间的残余时延为 55.6 ms，执行状态到镜头位姿的时延以 0.0 ms 为中心。不含 EM 跟踪器时，硬件成本低于 5,000 美元，这降低了复现门槛。

一个实用的下一步是，基于视野丢失、镜壁接触和皱襞卡滞 episode 建一个失败恢复基准，其中一个基线策略预测下一条控制指令，另一个恢复策略只在救援片段上训练。近期最适合使用这套资源的人群，是已经有结肠镜视频、但缺少用于闭环实验的同步动作和状态日志的研究团队。

### Evidence
- [OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research](../Inbox/2026-04-04--openrc-an-open-source-robotic-colonoscopy-framework-for-multimodal-data-acquisition-and-autonomy-research.md): 摘要给出了平台范围、硬件成本、同步记录的模态、数据集规模、失败和恢复数量，以及对齐后的残余时延。
- [OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research](../Inbox/2026-04-04--openrc-an-open-source-robotic-colonoscopy-framework-for-multimodal-data-acquisition-and-autonomy-research.md): 摘要确认了闭环研究目标，以及视频、指令、执行状态和远端镜头位姿的同步记录。
