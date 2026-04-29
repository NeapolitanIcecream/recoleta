---
kind: ideas
granularity: day
period_start: '2026-04-23T00:00:00'
period_end: '2026-04-24T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- long-horizon manipulation
- world models
- safety evaluation
- dexterous manipulation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/long-horizon-manipulation
- topic/world-models
- topic/safety-evaluation
- topic/dexterous-manipulation
language_code: zh-CN
---

# 机器人策略的执行监督

## Summary
执行监督已经具体到可以直接围绕它做产品和流程。近期最明确的方向包括：为长时域操作构建每步重规划的监督器，为机器人策略后训练建立仿真优先的纠错闭环，以及为家庭任务基准加入安全调整后的评估路径。每个方向都对应到底层论文中报告的性能提升或明确的审查结果，而且实现细节已经足够支撑一个聚焦的原型或工作流改动。

## 用于长时域操作的闭环剩余计划监督器
做长序列家庭或仓储任务的机器人团队，现在可以构建一层监督器：基于当前相机视角在每一步后重规划，维护一份简短的“已完成 / 剩余”记忆，并向动作策略发送一个简单的 2D 轨迹，指示下一步的局部移动。LoHo-Manip 给出了这种任务管理与执行分离方式的具体做法。它的价值很直接：当抓取失手或物体发生偏移时，失败的子任务会保留在剩余计划中，轨迹也会在下一轮更新，因此恢复过程仍留在正常控制回路内。

一个实用的首版不需要新的基础模型。可以直接使用现有的短时域 VLA 或 diffusion policy，加一个规划器，在每次观测后重写剩余子任务，并把轨迹叠加渲染到执行器输入中。低成本验证方式是准备一组多步任务回放，并注入小故障，比如偏心抓取或物体被移动。观察系统能否在不手动重置的情况下恢复到原定序列。现在这样做有依据，因为 LoHo-Manip 在长时域推理和轨迹预测基准上报告了提升，包括 RoboVQA 上的 63.1 和 EgoPlan2 上的 56.7；其递进时域规划器也明确设计为在任务完成前一直把失败步骤保留在记忆中。

### Evidence
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): 摘要给出了核心机制：递进时域重规划、已完成与剩余记忆，以及 2D 轨迹提示，并附有基准提升结果。
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): 摘要正文确认了用于长时域执行的剩余计划和视觉轨迹设计。
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): 引言直接说明了操作层面的痛点：误差累积、进度跟踪，以及长序列中的恢复。

## 用于机器人后训练的世界模型介入工作区
通用机器人策略的后训练可以转向一种“仿真优先”的纠错流程：操作员在学习到的世界模型里，于接近失败的状态介入，从同一个缓存状态分叉出多个修复方案，只有在验证时才占用真实机器人时间。Hi-WM 已经给出了足够多的细节，可以把这做成一个数据采集产品，服务于已经在微调 Pi0、Diffusion Policy 或类似控制器的实验室。

用户压力主要来自成本。现实世界中的纠错循环里，每次失败 rollout 都需要重置、重搭场景和操作员看护。Hi-WM 表明，只要世界模型与动作空间及边界情况对齐得足够好，它就能承担这条流程中的一部分。在三个真实机器人任务上，论文报告相对基础策略平均提升 37.9 个百分点，相对世界模型闭环基线提升 19.0 个百分点；世界模型评估与真实性能之间的 Pearson r = 0.953。这个结果支持一条明确的部署路径：先用模拟器判断哪些失败状态值得采集人工纠错数据，再重新训练，并在硬件上做抽查验证。一个低成本验证方式是选一个经常在后期阶段失败的任务，比如可变形物体布线，对比在仿真和真实机器人上，每采集一次成功纠错分别需要多少操作员分钟。

### Evidence
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): 摘要说明了仿真优先的介入流程、成本问题，以及主要的真实性能提升。
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): 摘要正文描述了物理世界纠错的成本，以及世界模型作为可复用纠错载体的角色。
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): 引言说明了部署经济性是纠错式后训练的瓶颈。

## 用于长时域家庭任务的安全调整基准评分器
面向家庭操作的机器人评测栈需要一条执行安全审查路径，在任务完成率之外，同时记录碰撞、支撑物掉落、放置不稳和抓取失败。可以立刻构建的东西是一个面向 BEHAVIOR1K 风格运行结果的评分器和视频审查工具，使用 sQ、seQ 这类惩罚项，再加上一小套供审查员使用的标签分类。

这对选择 checkpoint 和汇报进展的团队有用。只看最终状态的分数，会掩盖真正影响部署和调试的运行质量。BEHAVIOR1K 审查了 500 段录制结果，发现抓取失败最常见，碰撞也很频繁。加入安全惩罚后，RLC 的平均分从 Q = 0.256 降到 sQ = 0.239，Comet 从 0.192 降到 0.173。一个简单的产品测试是重新给最近一批基准视频打分，同时按完成率和安全调整后分数对 checkpoint 排序。如果排序发生变化，这条审查路径就已经开始产生价值。

### Evidence
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): 摘要提供了支持安全感知指标的论据、500 次运行审查，以及 sQ 下的分数下降。
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): 摘要正文解释了为什么只按最终状态评分会漏掉长时域家务任务中的执行安全问题。
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): 正文详细说明了与进度无关的评分问题，以及它为何会掩盖与部署相关的行为。
