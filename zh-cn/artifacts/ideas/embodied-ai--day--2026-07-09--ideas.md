---
kind: ideas
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- policy adaptation
- temporal memory
- dexterous benchmarks
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/policy-adaptation
- topic/temporal-memory
- topic/dexterous-benchmarks
language_code: zh-CN
---

# 可靠的机器人策略部署

## Summary
冻结的机器人策略可以通过规划器控制的重试、事件敏感的任务记忆，以及使用操作员纠正训练的小型适配模块提高可靠性。部署团队还应将灵巧接触任务加入验收测试，因为标准操作套件中的高分很少检验力调节和精细对齐能力。

## 面向冻结 VLA 策略的规划器控制重试与任务状态记忆
机器人团队可以在冻结的 VLA 外包一层规划器：由解析原语负责自由空间运动、目标定位、暂存和释放，再由 VLA 执行短时的接触密集型动作。每次调用都应记录子目标、耗时、接触或夹爪事件、观测结果和重试次数。规划器可以利用这些回合状态，在空抓后重新暂存，重复局部动作，或推进到下一个子目标。

Harness VLA 在 LIBERO-Pro 上的成功率达到 82.4%，直接使用同一冻结基线时为 50.0%。TFP 提供了将进度存储在策略内部的另一项证据：其事件敏感记忆将真实机器人上的物体交换成功率从 3/20 提高到 15/20。可以先用一个包含物体位置变化和间歇性遮挡的多阶段任务开展小规模试验，再比较直接执行与包装器方案的完成率、无效重复动作次数、恢复率和额外延迟。

### Evidence
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): 介绍固定原语库、可重试的 VLA 调用、任务记忆，以及相对于直接执行冻结策略，LIBERO-Pro 上的性能提升。
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): 介绍连续时间的任务进度记忆，以及物体交换和计数抓取放置任务在真实机器人上的性能提升。

## 基于少量操作员纠正的潜在空间适配
操作员纠正生成式机器人策略时，可以为一个小型的观测到噪声适配器提供训练数据，同时保持基础流匹配策略或扩散策略冻结。适配流程应在每次干预时记录观测和纠正动作，将动作反演为潜在噪声目标，并在训练时将这些目标与成功的自主运行数据混合。这样可以将更新限制在紧凑模块内，为部署团队处理反复出现的物体、动力学或机器人本体失败提供可行方法。

FlowDAgger 在 12 个 MetaWorld 任务上的平均成功率经过 50 次 rollout 后从 0.53 提高到 0.78，其小型噪声策略的训练显存约为 8 GB。它在 Hammer 任务上的测试也说明了必要的安全检查：适配任务成功率从 0.40 提高到 0.84，但五个留出任务上的表现从 0.96 降至 0.88。因此，初步部署测试应同时包含一个已知失败案例和一组留出技能，并拒绝使回归幅度超过预设上限的更新。

### Evidence
- [FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](../Inbox/2026-07-09--flowdagger-human-in-the-loop-adaptation-of-generative-robot-policies-in-latent-space.md): 提供动作反演方法、50 次 rollout 的结果、计算资源要求，以及留出技能的回归测量结果。
- [FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](../Inbox/2026-07-09--flowdagger-human-in-the-loop-adaptation-of-generative-robot-policies-in-latent-space.md): 解释如何在不改变基础策略权重的情况下，将纠正动作映射为小型策略使用的潜在噪声向量。

## 机器人策略验收测试中的灵巧接触任务
机器人策略评估应包含插入、推动、工具滑动、关节物体开启和多阶段手部操作，并在受控条件下改变相机姿态、光照、物体姿态和动力学。结果应按交互类型和机器人本体分别报告，并单独测量接触获取、力调节、亚厘米对齐和完整任务完成情况。这种测试结构可以发现夹爪式测试套件的单一平均分所掩盖的部署障碍。

DexVerse 在相同的 19 个任务、950 个回合子集上评估了四种代表性策略。3D Diffusion Policy 和 pi0.5 共同取得最高平均成功率 0.34；所有方法在 PushT 上的成功率均为零，InsertPen、SlideUtilityKnife 和 OpenLaptop 的成功率也保持在接近零的水平。实际的第一轮测试可以为目标策略复现这 19 个任务，并要求每种关键交互类型都取得非零成功率后，再进行硬件测试。

### Evidence
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): 报告共同的 19 任务评估、0.34 的最高平均成功率，以及力调节和对齐敏感任务上的接近零结果。
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): 介绍该基准的任务覆盖范围、机器人本体、同步观测数据和演示数据集。
