---
kind: ideas
granularity: week
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- embodied-ai
- vla
- evaluation
- long-horizon-control
- memory
- safety
- geometry
tags:
- recoleta/ideas
- topic/robotics
- topic/embodied-ai
- topic/vla
- topic/evaluation
- topic/long-horizon-control
- topic/memory
- topic/safety
- topic/geometry
language_code: zh-CN
---

# 状态感知的机器人执行

## Summary
本周的材料指向了机器人系统构建和测试方式上的几项具体变化。评测正在变得更有诊断性：分阶段进度指标和危险前提条件指标，能暴露汇总成功率看不见的失败模式。控制栈也在转向显式规划器状态，让子任务、grounding、记忆和验证以运行数据的形式穿过整个回路。在实验室自动化里，基于进度的子任务切换现在已经有了足够证据，可以把它当作多步流程中的实用运行时组件。

## 带危险 commit 跟踪的长时程分阶段评测
长时程操作的基准测试需要失败日志，不能只看一个成功率数字。LongBench 给出了一个具体模板：按失败机制拆分任务，按阶段给进度打分，并把完全可观测的任务与需要记住早期上下文的任务分开。对已经在做桌面或实验室操作的机器人团队，实际可做的是搭建一套评测工具。它应当给每个 episode 标注机制标签，例如 phase dependence、error accumulation、temporal windows 和各类 ambiguity，然后报告策略在哪一步停滞或漂移。相比单一任务完成率，这对模型选型更有用，因为 LongBench 显示，即使所有模型都使用同样的 16-step open-loop interface，不同失败机制上的差距仍然很大。这种打分方式也适合做安全审查。HazardArena 说明了为什么终点成功率会掩盖风险：一个策略可能已经到达危险前提条件，或几乎完成了一个不安全动作，但最后没有做完。因此，面向部署的测试平台应为常见任务的不安全 twin 添加动作级别的 `attempt`、`commit` 和 `success` 计数。向家庭、实验室或仓库交付 VLA 系统的团队，可以先用现有的 teleoperation 和 replay 栈搭起这套评测，再考虑增加新的模型复杂度。一个成本很低的第一步，是用分阶段指标和危险前提条件指标，重新给当前某个 benchmark 或内部任务集打分，看看候选策略的排序会不会变化。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench 定义了按机制区分的长时程评测、分阶段打分，并展示了与执行稳定性和时间窗口难度相关的明显性能差异。
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): HazardArena 加入了安全/不安全 twin 任务以及 `attempt`、`commit`、`success` 指标，能暴露终点成功率掩盖的危险进展。

## 用于长时程操作的规划器状态日志与控制器接口
规划器状态记录正在变成一种具体的控制接口，而不只是可解释性的附加项。HiVLA 和 Goal2Skill 都通过显式写出中间控制状态来提升操作表现：子任务指令、目标对象、局部视觉 grounding、过往结果的记忆、后置条件检查，以及恢复决策。对机器人团队，一个有用的实现是定义一套 planner-state schema，让每次 rollout 都写入，让每个控制器都读取。这个 schema 可以很窄：当前子任务、目标区域、预期后置条件、超时、错误码，以及验证失败时的下一步动作。这样一来，多步任务偏离轨道时，操作员就有了可检查的内容；同时，低层策略拿到的输入也比“原始指令加最近几帧”更好。Goal2Skill 报告称，在五个 RMBench 任务上，平均成功率提升到 32.4%，而最强基线是 9.8%；在记忆密集型任务上，提升更大。HiVLA 在 RoboTwin 2.0 上报告了 83.3% 的平均成功率，并且通过把 grounded plan 和目标裁剪区域送入独立动作专家，在困难、杂乱场景任务上明显领先。近期可落地的路径是改日志层和控制层，而不是先换一个全新的基础模型。一个低成本测试，是先在一个现有的长时程任务里加入这份状态记录，再看失败复盘是否足够具体，能把规划错误和电机控制错误区分开。

### Evidence
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Goal2Skill 使用结构化记忆、后置条件验证和反思机制来提高长时程任务成功率，尤其是在记忆密集型任务上。
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): HiVLA 显式输出结构化子任务计划和 grounded target boxes，并将其送入独立控制器，在杂乱场景和长时程操作上取得了明显提升。

## 用于多步实验室自动化的基于进度的子任务切换
对子任务切换使用 progress head，看起来已经可以用于阶段边界清晰、重启代价高的实验室自动化。ChemBot 使用带进度感知的 Skill-VLA，在 0 到 1 的尺度上预测子任务完成度，并在超过阈值后把控制权交还给规划器。它还结合了短期场景记忆、对历史成功轨迹的长期检索，以及供规划器使用的结构化场景描述。直接可做成的产品形态，是一种实验室机器人运行时：某个 skill 结束，是因为任务状态表明这一步已经完成，而不是因为固定动作时长已经耗尽。这在化学流程里很重要，因为搅拌、倾倒、加热和转移动作的持续时间会变化，而且错误会在整个流程中累积。论文报告称，在三个多步 UR3 实验中，它的真实世界任务成功表现优于 full-trajectory baselines；其消融实验还表明，场景描述和子任务链贡献了大部分分解收益，而记忆减少了上下文负担。最早的用户会是那些用有限技能库自动化重复性湿实验流程的研究实验室。一个低成本检查方法，是给现有某个脚本式或 VLA 驱动的流程加上一个标量进度估计器，然后比较重复运行中不必要的额外动作、过早切换，以及重启频率。

### Evidence
- [Long-Term Memory for VLA-based Agents in Open-World Task Execution](../Inbox/2026-04-17--long-term-memory-for-vla-based-agents-in-open-world-task-execution.md): ChemBot 结合了基于进度的子任务切换、结构化场景描述和双层记忆，并报告了在多步真实世界化学任务上的提升。
