---
kind: ideas
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- reinforcement learning
- robot safety
- world models
- human demonstrations
- shared autonomy
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/robot-safety
- topic/world-models
- topic/human-demonstrations
- topic/shared-autonomy
language_code: zh-CN
---

# 闭环 VLA 部署控制

## Summary
机器人 VLA 团队在扩大部署前已有更明确的近期工作：把安全专项 rollout 加入发布测试，通过共享自主控制处理精细接触步骤，并在已部署策略不确定的状态收集恢复演示。共同压力来自模型离开离线模仿训练后的闭环行为。

## 面向 VLA 操作策略的安全专项发布测试
VLA 操作团队应在发布测试中加入安全测试阶段，把不安全接触和不安全指令遵循行为与任务完成率分开衡量。LIBERO-Safety 给出了可用模板：75 个任务覆盖可供性感知抓取、人机交互、桌面空间避让、自由空间手-物避让和语义安全推理，难度级别为 L0-L2。该基准还包含 19,664 条经过人工筛查的无碰撞演示，这些演示由稀疏关键位姿和 CuRobo 碰撞检查生成。

操作原因很直接：一个策略可以完成简单的操作任务，却仍会在杂物、人手或手持物体附近失败。在 LIBERO-Safety 中，OpenVLA-OFT 在高难度可供性感知抓取上的成功率降至 1.3%，π0.5 在同一级别上也只有 35.3%。实用的发布准入检查应让同一个策略同时跑标准任务套件和安全套件，记录成功、碰撞、拒绝和恢复行为，并在 L2 安全案例反复失败的任务上阻止部署。

### Evidence
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety 定义了安全套件、数据集规模、数据生成方法，以及基线在高难度物理安全设置下的失败情况。
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): 论文摘要描述了参数化安全基准和 19,664 条无碰撞演示。

## 辅助 VLA 机器人的抓取和释放步骤操纵杆交接
辅助机器人团队可以先用接触感知共享控制层测试冻结的 VLA，再收集大型微调数据集。Assistron 展示了这种工作流的形式：VLA 处理语言条件下的宏观移动，腕部相机检测器监测接触密集阶段和预测到的夹爪状态变化，用户在抓取、插入或释放时通过操纵杆输入。操纵杆命令会融合进 VLA 的流匹配去噪过程，随后控制权回到自主模式。

这是针对家庭操作中常见失败模式的具体修复方法。冻结的 VLA 可以理解宽泛意图，但在精确接触点上可靠性会下降。在一个新手用户场景恢复基准中，Assistron 达到 91.3% 的部分成功率，而自主 VLA 只有 13.7% 且超时。该系统仍需要用户在 56.5% 的运行时间内主动输入，因此首个采用测试应关注：这种交接是否能降低操纵杆能力较弱用户的工作负担，同时不引入新的信任问题。

### Evidence
- [Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models](../Inbox/2026-06-22--assistron-bayesian-shared-autonomy-with-off-the-shelf-vision-language-action-models.md): Assistron 保持 VLA 冻结，在接触密集步骤附近触发用户介入，并报告部分成功率、自主运行时间、工作负担和用户研究结果。
- [Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models](../Inbox/2026-06-22--assistron-bayesian-shared-autonomy-with-off-the-shelf-vision-language-action-models.md): 论文说明了在辅助场景中直接使用 VLA 的动机，并描述了零样本可靠性问题。

## VLA 微调期间由不确定性触发并配合回放的恢复演示
机器人学习团队可以在 rollout 期间记录高不确定性状态，并要求从这些状态开始提供恢复演示，从而缩短部署后的适应周期。RECALL 使用 INSIGHT 标记 token 级决策中的不确定性，在线收集恢复样例，然后用回放数据进行微调以保留已有技能。

有用的工作流变化是把示教时间转向策略不确定的子步骤，而不是每个失败任务都要求从起始状态开始的完整演示。示教者可以把时间花在策略不确定的子步骤上，训练时再回放旧任务。在 RECALL 中，strong INSIGHT 在线恢复结合完整回放达到 72.4% 的 LIBERO-10 总体成功率，高于匹配的被动收集的 60.2%。只用新的恢复数据训练会破坏已保留行为；最佳 new-only 设置的总体成功率为 28.4%，收集任务成功率为 0.4%。因此，回放混合是工作流的一部分，不能当作可选的收尾步骤。

### Evidence
- [RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models](../Inbox/2026-06-22--recall-recovery-experience-collection-for-active-lifelong-learning-in-vision-language-action-models.md): RECALL 报告了不确定性引导的恢复收集、主动收集与被动收集的比较，以及没有回放时 new-only 微调的失败。
- [RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models](../Inbox/2026-06-22--recall-recovery-experience-collection-for-active-lifelong-learning-in-vision-language-action-models.md): 论文解释了为什么被动的起始状态演示会浪费精力，以及为什么不确定的中间状态适合作为新监督的目标。
