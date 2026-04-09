---
kind: trend
trend_doc_id: 43
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
topics:
- robot-learning
- safety
- data-generation
- medical-robotics
- vla
run_id: materialize-outputs
aliases:
- recoleta-trend-43
tags:
- recoleta/trend
- topic/robot-learning
- topic/safety
- topic/data-generation
- topic/medical-robotics
- topic/vla
language_code: zh-CN
---

# 机器人学习工作正更接近控制闭环

## Overview
4 月 4 日的机器人方向论文不多，但主题很一致。最强的几项工作都在收紧观测、动作和安全之间的闭环：保留动作标签的合成演示数据，满足控制时序约束的行为切换检测，以及为闭环学习记录对齐多模态数据的结肠镜平台。

## Clusters

### 用于机器人迁移的带动作标签合成数据
当前的机器人学习论文更关注更好的动作落地，而不是更大的通用模型。CRAFT是最清楚的例子。它用模拟器 rollout 和 Canny 引导的视频扩散流水线生成保留配对动作标签的逼真演示数据。这在双臂任务里很关键，因为接触和协同上的误差会很快破坏迁移效果。跨本体测试中的提升很大：从 UR5 到 Franka，CRAFT 在没有目标机器人演示的情况下，在 Lift Pot、Place Cans 和 Stack Bowls 上分别达到 82.6%、89.3% 和 86.0%。在从 xArm7 到 Franka 的真实测试中，它在三个任务上分别达到 17/20、15/20 和 16/20 次成功。这个方法还在同一条流水线中支持视角、光照、背景和机器人本体的变化。

#### Evidence
- [CRAFT: Video Diffusion for Bimanual Robot Data Generation](../Inbox/2026-04-04--craft-video-diffusion-for-bimanual-robot-data-generation.md): 包含方法和完整结果的摘要。

### 更快的行为变化检测，让共享操作更安全
安全方向的工作开始更具体地界定控制器必须在什么时候作出反应。UA-ToM 在冻结的 7B vision-language-action 模型上加入一个 992K 的 belief 模块，用来跟踪协作者是否在任务中途改变了行为。论文指出，宽松的检测窗口会掩盖运行风险。它更有说服力的结果出现在更严格的 ±3 步窗口下；在 50 ms 控制循环中，这大约是 150 ms，UA-ToM 在 1,200 个 episode 上达到 85.7% 的 hard detection。对部署更重要的是，切换检测将切换后的碰撞次数从每个 episode 的 2.34 降到 1.11，减少 52%，新增推理开销为 7.4 ms。

#### Evidence
- [Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation](../Inbox/2026-04-04--belief-dynamics-for-detecting-behavioral-shifts-in-safe-collaborative-manipulation.md): 包含检测窗口分析、碰撞下降和开销的摘要。

### 闭环数据集的仪器化程度已足以支撑医疗自主系统
医疗机器人这组工作提供的是基础设施，而不是新的策略结果。OpenRC 打包了一个低成本机器人结肠镜系统，记录同步视频、操作者指令、执行状态和 6-DoF 镜头末端位姿。实际重点是为闭环学习做好数据对齐。除去 EM 跟踪器，这套系统的组装成本低于 5,000 美元；数据集覆盖 10 种任务变化，包含 1,894 个 episode、约 19 小时的数据。它还包含 142 个失败 episode 和 141 个恢复 episode，为后续工作提供了导航错误、碰壁和视腔丢失等具体案例。完成对齐后，动作与执行之间的残余时延为 55.6 ms，执行到末端位姿的时延以 0.0 ms 为中心。

#### Evidence
- [OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research](../Inbox/2026-04-04--openrc-an-open-source-robotic-colonoscopy-framework-for-multimodal-data-acquisition-and-autonomy-research.md): 包含数据集规模、模态对齐和延迟指标的摘要。
