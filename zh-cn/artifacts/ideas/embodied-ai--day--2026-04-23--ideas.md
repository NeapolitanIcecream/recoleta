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

## 摘要
执行监督已经具体到可以围绕它做产品和工作流。最清楚的近期方向，是给长周期操作做每步重规划的监督器、给机器人后训练做先仿真后纠正的回路，以及给家庭任务基准做安全调整后的评测路径。每个方向都对应底层论文里的报告提升或具体审计结果，而且实现细节已经足够支撑一个聚焦的原型或流程改动。

## 面向长周期操作的闭环剩余计划监督器
机器人团队在长周期的家庭或仓库任务中，现在可以搭一个监督层：它根据当前相机视角在每一步后重新规划，保留一段简短的已完成和待完成记忆，并把一个简单的二维轨迹发给动作策略，作为下一步局部移动的指引。LoHo-Manip 给出了这种任务管理和执行拆分的具体做法。它的实际价值在于：当抓取失败或物体位置偏移时，失败的子任务会留在剩余计划里，下一轮轨迹会更新，所以恢复过程仍然在正常控制回路内完成。

第一个可落地版本不需要新的基础模型。可以直接拿现有的短视野 VLA 或扩散策略，加一个在每次观测后改写剩余子任务的规划器，再把轨迹叠加渲染到执行器输入里。一个低成本检验办法是做一组多步任务回放，并注入轻微失败，比如抓偏或物体移动。观察系统能否在不手动重置的情况下继续原本的任务序列。LoHo-Manip 在长程推理和轨迹预测基准上报出了提升，包括 RoboVQA 上的 63.1 和 EgoPlan2 上的 56.7，而且它的回溯式规划器明确会把失败步骤保留在记忆里，直到完成为止。

### 资料来源
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): Summary gives the main mechanism: receding-horizon replanning, done-and-remaining memory, and 2D trace prompting, plus benchmark gains.
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): Abstract text confirms the remaining-plan and visual-trace design for long-horizon execution.
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): Introduction states the operational pain directly: compounding errors, progress tracking, and recovery during long sequences.

## 用于机器人后训练的世界模型介入工作区
通用机器人策略在后训练阶段，可以转到一种先仿真后纠正的工作流：操作者在学到的世界模型里、靠近失败状态的位置介入，从同一个缓存状态分叉出几种修正方案，只把真实机器人时间花在验证运行上。Hi-WM 提供了足够的细节，可以把这做成一个数据采集产品，给已经在微调 Pi0、Diffusion Policy 或类似控制器的实验室使用。

用户压力来自成本。真实世界里的纠正循环，每次出错都要重置、布置场景，还要有操作者监督。Hi-WM 说明，只要世界模型和动作空间及边缘情况足够对齐，它就能承担这条回路中的一部分。在三个真实机器人任务上，论文报告平均成功率比基础策略高 37.9 个百分点，比世界模型闭环基线高 19.0 个百分点，而且世界模型评估和真实表现之间的 Pearson r = 0.953。这支持一条很窄的部署路径：先用仿真决定哪些失败状态值得采集人工纠正数据，再到硬件上重训并抽查。一个低成本验证方式，是选一个后期失败频繁的任务，比如可变形物体路径规划，对比在仿真和机器人上收集一次成功纠正所需的操作者分钟数。

### 资料来源
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): Summary states the simulator-first intervention workflow, cost problem, and main real-world gains.
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): Abstract text describes physical-world correction cost and the world model as a reusable corrective substrate.
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): Introduction explains deployment economics as the bottleneck for corrective post-training.

## 面向长周期家庭任务的安全调整基准评分器
家庭操作的机器人评测栈需要一条执行安全审查路径，把碰撞、掉落的支撑物、不稳定放置和抓取失败，和任务完成结果一起记录下来。最直接的实现，是给 BEHAVIOR1K 风格的运行做一个评分器和视频审查工具，配上 sQ、seQ 这类惩罚项，再加一个简短的审查标签分类。

这对挑选检查点和汇报进展很有用。只看最终状态分数，会掩盖部署和调试真正关心的运行质量。BEHAVIOR1K 审查了 500 条录制，发现抓取失败是最常见错误，碰撞也很频繁。加入安全惩罚后，RLC 平均分从 Q = 0.256 降到 sQ = 0.239，Comet 从 0.192 降到 0.173。一个简单的产品测试，是把最近一批基准视频重新评分，同时按完成度和安全调整后的分数给检查点排序。如果排序变了，这条审查路径就已经开始产生价值。

### 资料来源
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): Summary provides the argument for safety-aware metrics, the 500-run audit, and score drops under sQ.
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): Abstract text explains why final-state-only scoring misses execution safety in long-horizon chores.
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): Main text details the progress-agnostic scoring problem and why it obscures deployment-relevant behavior.
