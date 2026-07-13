---
kind: ideas
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- task memory
- sample efficiency
- action control
- dexterous benchmarks
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/task-memory
- topic/sample-efficiency
- topic/action-control
- topic/dexterous-benchmarks
language_code: zh-CN
---

# 可靠的机器人操作系统

## Summary
机器人团队可以在现有策略外加入任务进度状态和重试控制，从失败轨迹中恢复监督信号，并根据完成时间、接触力和控制器上限测试动作表示。这些改动可以先在小规模任务集上评估，再决定是否投入新的数据采集或更大规模的策略训练。

## 冻结 VLA 的任务进度记忆与重试控制
部署预训练 VLA 的团队可以在其外层加入规划器，记录已完成的阶段、接触结果和重试历史。VLA 负责短时的接触密集型动作；显式原语负责目标定位、自由空间运动、重新布置和释放。Harness VLA 采用这种结构后，在不对 VLA 进行微调的情况下，将 LIBERO-Pro 的成功率从直接冻结基线的 50.0% 提高到 82.4%。TFP 还表明，回合内任务状态可以区分视觉上相似但需要不同动作的场景：真实机器人上的物体交换成功率从 3/20 提高到 15/20。

可以先选择一个在空抓取、遮挡或物体交换后经常失败的多阶段任务进行测试。记录一个紧凑状态，包括当前阶段、已用时间、最近一次接触结果和重试次数。在不同布局下，将加入外层规划器的策略与未修改的控制器进行比较，测量完整任务成功率、重复动作错误、重试次数和新增延迟。这项测试可以判断，加入执行状态是否比再收集一批任务专用微调数据更节省成本地提升可靠性。

### Evidence
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): 介绍固定原语库、任务记忆和全局记忆、可重试的 VLA 调用，以及 LIBERO-Pro 对比结果。
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): 介绍回合内连续时间信念状态的设计，以及其在依赖任务阶段的真实机器人任务中的收益。

## 失败机器人轨迹的事后重标注
机器人学习团队可以在后训练流程中加入重标注环节，让连贯的失败轨迹产生可用监督信号。VLM 观察失败轨迹，描述实际发生的行为，再根据这条新指令为轨迹评分。Learning from Hindsight 让约 70% 至 80% 的轨迹组可用于训练，在约 5 个训练步骤内达到标准 GRPO 需要近 30 个步骤才能达到的性能；使用 160 条真实机器人轨迹时，成功率达到 56%，而 GRPO 为 22%。

成本最低的检查方式是离线审查最近一批失败轨迹。抽取 100 条失败轨迹，生成事后指令，再由操作人员检查每条描述是否正确、具体且适合用于强化。如果一致性较高，可以在相同轨迹预算下进行一次短期后训练对比，并跟踪可用轨迹组比例、原任务成功率和非预期行为是否增加。这种流程适用于实体数据采集时间长、稀疏奖励占训练成本较高的场景。

### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): 报告重标注流程、可用轨迹比例、训练步数减少情况和 Franka 结果。
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): 解释如何将失败轨迹中的连贯行为转化为另一个语言条件任务的监督信号。

## 包含完成时间、力阈值和跟踪上限的动作控制测试
接触密集型操作的策略评估除了任务成功率，还应包括执行时间、力超限次数和底层跟踪误差。B-spline Policy 表明，连续动作曲线可以重新调整时间尺度，并以较高控制频率采样：清理桌面的时间从 23.57 秒降至 11.80 秒，成功率从 13/20 变为 14/20。其 4× Speed Stacking 结果也降至 0/20，暴露出控制器的速度边界。PAC-ACT 报告称，经过分块级强化学习后训练后，超过 60 N 的力读数减少了 46 倍。

可以搭建一个测试台，通过离散动作块和连续曲线，以多个速度倍率重放相同演示数据，然后记录成功率、完成时间、峰值力、超过力上限的持续时间和关节跟踪误差。测试至少应包含一个精密接触任务和一个长时域任务。DexVerse 说明，不能只依赖简单的抓取放置检查：其 19 任务子集中的最高平均成功率为 0.34，所有测试策略在 PushT 上的成功率都是零。由此得到的速度-力边界可以为部署工程师提供每个控制器和任务的明确运行上限。

### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): 报告完成时间收益、成功率、连续 B-spline 控制，以及速度过高时的失败。
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): 介绍分块级后训练方法，以及报告的超过 60 N 力读数减少结果。
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): 显示所有评估策略在灵巧操作任务上的总体成功率较低，且在 PushT 上成功率为零。
