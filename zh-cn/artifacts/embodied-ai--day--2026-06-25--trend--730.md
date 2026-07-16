---
kind: trend
trend_doc_id: 730
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
topics:
- robotics
- vision-language-action models
- behavior cloning
- test-time scaling
- robot safety
- contact-rich manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-730
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/behavior-cloning
- topic/test-time-scaling
- topic/robot-safety
- topic/contact-rich-manipulation
language_code: zh-CN
---

# 机器人 VLA 论文正在转向基于 rollout 的可靠性

## 概览
机器人视觉-语言-动作（VLA）研究正聚焦于真实操作证据：开放 rollout、部署检查和安全指标。ABC 让行为克隆更容易复现。E-TTS 加入推理时候选打分。ForesightSafety-VLA 在完整轨迹中评估不安全成功。

## 研究发现

### 开放操作数据和更密集的动作监督
ABC 通过发布数据、代码、硬件细节、模型权重、仿真资产和真实 rollout 分数，提高了行为克隆的可复现性标准。它的 ABC-130K 数据集包含 3,553 小时、134,806 个 episode 和 195 个任务，ABC-Eval 中还有超过 100 小时的真实策略 rollout。论文还报告，仿真和部分离线诊断指标与真实世界成功率相符，为研究人员选择模型提供了成本更低的信号。

LA4VLA 处理的是 VLA 预训练中的另一类数据问题。长演示通常把一条高层指令配给许多图像-动作帧，因此语言信号稀疏。LA4VLA 将演示切成短的语言-动作片段，保留 33,116 个经过人工验证的 episode，并在 VLA 训练前，用不含图像的语言、本体感知和动作轨迹训练一个 1B 模型。它的混合语言-动作和 VLA 预训练在真实世界操作任务上报告了 83.3% 的成功率，比无预训练在真实任务上高 45.0 个点。

#### 资料来源
- [Scalable Behavior Cloning with Open Data, Training, and Evaluation](../Inbox/2026-06-25--scalable-behavior-cloning-with-open-data-training-and-evaluation.md): ABC dataset scale, released stack, rollout evaluation, and diagnostic correlations.
- [LA4VLA: Learning to Act without Seeing via Language-Action Pretraining](../Inbox/2026-06-25--la4vla-learning-to-act-without-seeing-via-language-action-pretraining.md): LA4VLA language-action dataset construction and reported simulation and real-world gains.

### 已部署策略的推理时检查
多篇论文把冻结或已训练的 VLA 策略作为受监控执行循环中的一个组件。E-TTS 采样推理-动作对，用视觉-语言验证器打分，保存近期历史，并在候选失败时请求反馈。在其报告的设置中，它带来平均 13.52 个点、最高 33.14 个点的仿真成功率提升。

PhysReflect-VLA 在动作执行前加入物理可行性评分，并在执行后比较预测的下一状态和观测到的下一状态。如果差异较大，反思器会生成纠正指导。在五个真实机器人任务上，Phys-OVLA 的平均成功率比 OVLA-FT 高 5.4 个点，Phys-OFT 比 OVLA-OFT 高 3.0 个点。

RouterVLA 表明，部署前的冒烟测试也可以指导策略选择。在 LIBERO-Plus 上，一条简单的探测成功规则在冻结专家之间做选择，达到 0.6149 的留出成功率；全局最佳专家为 0.4686。

#### 资料来源
- [E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation](../Inbox/2026-06-25--e-tts-a-new-embodied-test-time-scaling-framework-for-robotic-manipulation.md): E-TTS reasoning-action sampling, verifier scoring, history buffer, and success gains.
- [PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies](../Inbox/2026-06-25--physreflect-vla-physical-feasibility-and-self-reflective-regulation-for-reliable-vision-language-action-policies.md): PhysReflect-VLA feasibility checks, reflection mechanism, and real-robot gains.
- [RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection](../Inbox/2026-06-25--routervla-turning-smoke-tests-into-supervision-for-heterogeneous-vla-selection.md): RouterVLA smoke-test routing protocol and held-out success improvement.

### 动作模块开始感知阶段和接触
PAMAE 用阶段感知的专家混合动作头修改流匹配 VLA 策略。路由器使用夹爪状态、夹爪变化、上一动作范数和进度等执行线索。在五个仿真多阶段任务上，PAMAE 将 π0 的平均成功率提高 9.2 个点，将 π0.5 提高 5.6 个点。

VibeAct 为灵巧控制加入了一个紧凑的触觉通道。压电指尖麦克风向接触和滑移估计器提供输入，估计器再向 MuJoCo 中训练的策略提供一个 12 维触觉向量。在硬件上，它在 Box Climb、Can Climb 和 Nut Rotation 上的成功率高于本体感知加点云基线。

LeHome 衣物折叠系统给出了一个面向比赛规模的可变形物体示例。它结合了流匹配 VLA 策略、强化学习、回放、人工纠正和 sim-to-real 调优，在在线仿真轮中获得第一名，在真实世界决赛中获得第二名。

#### 资料来源
- [PAMAE: Phase-Aware-MoE Action Experts Towards Reliable Flow-Matching Vision-Language-Action Policies](../Inbox/2026-06-25--pamae-phase-aware-moe-action-experts-towards-reliable-flow-matching-vision-language-action-policies.md): PAMAE phase-aware expert routing and simulated multi-stage task gains.
- [VibeAct: Vibration to Actions for Contact-Rich Reactive Robot Dexterity](../Inbox/2026-06-25--vibeact-vibration-to-actions-for-contact-rich-reactive-robot-dexterity.md): VibeAct tactile sensing setup and simulation and hardware results.
- [Learning to Fold: prizewinning solution at LeHome Challenge 2026 (1st place online, 2nd offline)](../Inbox/2026-06-25--learning-to-fold-prizewinning-solution-at-lehome-challenge-2026-1st-place-online-2nd-offline.md): LeHome folding system components and competition outcomes.

### 安全评估同时跟踪不安全成功和任务成功
ForesightSafety-VLA 将安全作为 VLA 策略的主要测量目标。它在物理交互、指令处理和感知三个方面定义了 13 个安全类别。该基准在五种机器人形态上构建了 66 个加入安全因素的 RoboTwin 场景，然后区分安全成功、不安全成功、安全失败和不安全失败。

报告的基线都显示仍有风险。OpenVLA-oft 的安全调整成功率在列出的结果中最高，为 0.35，但不安全成功仍为 0.06。在成功 episode 中，不安全占比在 OpenVLA-oft 上为 12.5%，在 ACT 上为 37.5%。这种评分选择很重要，因为机器人可能在完成指令的同时碰撞物体、进入高温区域或违反间隙限制。

#### 资料来源
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA safety taxonomy, benchmark design, and baseline safety metrics.
