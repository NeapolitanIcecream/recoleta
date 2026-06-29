---
kind: ideas
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world-models
- cross-embodiment
- tactile-sensing
- medical-robotics
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/cross-embodiment
- topic/tactile-sensing
- topic/medical-robotics
language_code: zh-CN
---

# Robot Policy Transfer and Execution Reliability

## Summary
近期最明确的工作集中在迁移接口、跨平台医疗后训练，以及机器人执行的置信度层。证据最强的是这些论文把变化和具体系统及可测增益绑在一起：JoyAI-RA 对跨实体共享动作空间迁移，Open-H-Embodiment 对跨平台手术后训练，Temporal Difference Calibration 对现有 VLA 策略上的失败预测和动作选择。

## Shared action-space retargeting for multi-robot manipulation training
持续为每个新手臂或新手爪重训策略的机器人团队，现在有了一个更清晰的中间目标：先做一个动作重定向层，再测试混合的人类、仿真和机器人数据能否减少针对不同实体的专用数据需求。JoyAI-RA 报告称，把网页数据、第一视角人类视频、仿真和机器人轨迹放进同一个动作表示后，在 RoboTwin Easy 和 Hard 上分别达到 90.48% 和 89.28%，在 RoboCasa GR1 Tabletop 上达到 63.2%，在 AgiBot 真实世界基准上的平均成功率为 0.74，而 π0.5 为 0.62。实际上的改进方向是，不再把跨实体迁移当成一个宽泛的预训练愿望，而是把它变成一个明确的训练接口：相机坐标系下的末端执行器动作、对缺失自由度做掩码处理，以及在目标机器人上做一个较小的后训练阶段。

最便宜的检查方式，是在你已经控制的两个实体之间做一次窄范围迁移试验，比如实验室机械臂和移动操作臂，或者两种夹爪。选一个长时程家务任务和一个杂乱场景下的抓取任务。测量共享动作空间加上几小时面向实体的后训练，是否能超过只在目标机器人上训练的同规模模型。如果在搭建时间和试验次数上差距缩小，对一直为硬件变化反复付出同样数据采集成本的实验室和产品团队来说，这个结果已经有直接价值。

### Evidence
- [JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy](../Inbox/2026-04-22--joyai-ra-0-1-a-foundation-model-for-robotic-autonomy.md): Reports the unified action space design and concrete gains across RoboTwin, RoboCasa, and a real humanoid benchmark.

## Cross-platform post-training workflow for surgical robot policies
医疗机器人团队现在已经有足够多的公开配对视频和运动学数据，可以把跨平台后训练当成一条实际流程，而不是一次性的定制数据项目。Open-H-Embodiment 汇集了 770 小时、124,019 个 episode、20 个机器人平台和 33 个任务家族，然后用这批语料把 GR00T-N1.6 后训练成 GR00T-H。 在 SutureBot 上，GR00T-H 完成了 20 次端到端缝合试验中的 5 次，而 ACT、GR00T-N1.6 和 LingBot-VA 都是 0/20。论文还报告了在 dVRK-Si、Versius 和 MIRA 上的提升，包括总体平均成功率的统计显著改善。

由此可以直接做一个跨平台手术适配基准，适合那些已经有多个系统少量日志的机构。把配对视频和运动学统一格式，跨平台微调同一个策略，并跟踪短时的站点级适配运行是否足以恢复有用的子任务表现，尤其是抓取、递交、投掷和取出。一个低成本验证步骤，是在同一实验室网络里复现论文的低数据条件：留出一个平台，只用几小时做微调，再和只用该平台本地数据训练的策略比较。如果共享模型能在完整端到端自主还没准备好之前，就提升早期子任务完成率，这对训练、辅助和模拟器冷启动都已经有用。

### Evidence
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): Provides the dataset scale, platform coverage, suturing results, and cross-platform evaluation figures.

## Black-box rollout success prediction for VLA execution gating
部署 VLA 策略的团队可以在黑盒动作输出之上加一个成功预测器，用它做提前停止、回退和动作排序。Temporal Difference Calibration 把置信度定义在整个 episode 上，用时序差分目标训练这个预测器，并报告在 OpenVLA、π0、π0-FAST 和 UniVLA 上更好的校准和更早的失败检测。论文还报告称，当学习到的价值预测器对采样动作进行排序时，OpenVLA 在 LIBERO 上的成功率提升了 15%。

这给通过 API 或冻结检查点使用基础机器人策略的人提供了一层直接可用的支持模块。记录随时间变化的动作概率，用最终任务结果训练一个 rollout-success head，并暴露一个阈值，在预测成功率下降时暂停执行或把控制权交回遥操作。低成本测试也很简单：选一个已有的基准或一个已知会出现恢复失败的真实机器人流程，对比不中断执行和置信度门控执行，测量任务完成率、无效运动和操作员介入次数。论文的黑盒结果很关键，因为很多部署团队即使能记录策略输出，也拿不到内部隐藏状态。

### Evidence
- [Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models](../Inbox/2026-04-22--temporal-difference-calibration-in-sequential-tasks-application-to-vision-language-action-models.md): Describes the sequential calibration method, black-box applicability, early failure detection, and the 15% OpenVLA improvement on LIBERO.
