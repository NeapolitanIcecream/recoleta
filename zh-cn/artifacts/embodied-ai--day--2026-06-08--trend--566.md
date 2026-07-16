---
kind: trend
trend_doc_id: 566
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- failure recovery
- humanoid control
- robot data collection
run_id: materialize-outputs
aliases:
- recoleta-trend-566
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/failure-recovery
- topic/humanoid-control
- topic/robot-data-collection
language_code: zh-CN
---

# 机器人论文正在集中到时间记忆、恢复和可用控制回路上

## 概览
视觉语言动作（VLA）机器人工作的效果最好的是那些让策略保留时间状态、在出错后恢复、或接受低延迟人工输入的场景。MemoryVLA++、MotionWAM 和 YUBI 体现了当天的重点：让策略在更长时域上行动，收集更大的真实数据，并让修正尽量贴近执行。

## 研究发现

### 机器人策略的时间记忆和世界模型
一些论文把时间当作机器人控制的一级输入。MemoryVLA++ 保存过去的感知和任务 token，再把它们和潜在的未来预测结合起来生成动作。它在需要记住先前交互或预测运动的任务上提升最大，包括真实机器人上依赖记忆和依赖想象的任务组分别提升 26 和 28 个百分点。

iMaC 用机器人运动学和接触热图让动作条件视频展开在空间上更精确。它的世界模型估计与真实策略成功在 8 个长时程真实机器人任务中的 6 个上相关。Echo-Memory 还给出一个提醒：只看重放指标，可能看不出世界模型在相机离开再返回后是否保住了物体身份。

#### 资料来源
- [MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models](../Inbox/2026-06-08--memoryvla-temporal-modeling-via-memory-and-imagination-in-vision-language-action-models.md): MemoryVLA++ summary, method, and reported simulation and real-robot gains.
- [iMaC: Translating Actions into Motion and Contact Images for Embodied World Models](../Inbox/2026-06-08--imac-translating-actions-into-motion-and-contact-images-for-embodied-world-models.md): iMaC action-to-motion/contact conditioning and policy-evaluation correlations.
- [Echo-Memory: A Controlled Study of Memory in Action World Models](../Inbox/2026-06-08--echo-memory-a-controlled-study-of-memory-in-action-world-models.md): Controlled memory study showing replay quality and revisit memory can rank methods differently.

### 冻结 VLA 策略周围的失败恢复
恢复工作保持基础 VLA 不变，只在运行时或通过残差训练加入定向纠正。ReCoVLA 用视觉语言模型识别失败类型和恢复阶段，编译分阶段奖励，并在仿真中训练残差策略。它把 Fetch 任务的平均仿真成功率从 36.7% 提高到 66.7%，零样本实体成功率达到 61.7%。

B2FF 预先生成未来图像里程碑，并在执行偏离时选择一个恢复目标。在注入失败的 LIBERO 上，它把 UD-VLA 的平均成功率从 56.3% 提高到 74.0%。ProbeAct 更轻量：它读取隐藏状态探针来跟踪物体，并在多次失败后使用控制障碍区域，讓 LIBERO-plus 成功率从 69.6% 提高到 74.1%。

#### 资料来源
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](../Inbox/2026-06-08--recovla-vlm-guided-reward-compilation-for-failure-recovery-in-vision-language-action-policies.md): ReCoVLA frozen-policy residual recovery, reward compilation, and success metrics.
- [Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection](../Inbox/2026-06-08--back-to-the-familiar-future-failure-recovery-for-vla-policies-via-pre-imagined-milestone-selection.md): B2FF milestone-selection recovery and LIBERO results.
- [ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models](../Inbox/2026-06-08--probeact-probe-guided-training-free-failure-recovery-in-vision-language-action-models.md): ProbeAct runtime probing, control-barrier correction, and LIBERO-plus gains.

### 执行时调控和安全过滤器
执行循环正在加入更明确的用户和安全通道。Flow Control 用一个简单的键盘方向来修改 flow-matching 动作采样器的初始条件。在 Two-Block 任务中，调节初始条件后，左块获取在更长的调节时域内几乎达到完美，而抓取放置成功率在报告设置中保持接近 100%。

另一篇安全过滤论文读取冻结 VLA 内部的注意力头，在控制过程中识别当前目标物体。在动态 SafeLIBERO Level III 上，它把平均碰撞率从仅用初始化过滤器时的 70.75% 降到 26.88%，并把安全成功率从 25.5% 提高到 55.75%。共同点很直接：少量运行时信号可以在不重新训练的情况下约束大型策略。

#### 资料来源
- [Flow Control: Steering Vision-Language-Action Models with Simple Real-Time Inputs](../Inbox/2026-06-08--flow-control-steering-vision-language-action-models-with-simple-real-time-inputs.md): Flow Control mechanism and Two-Block steering results.
- [Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models](../Inbox/2026-06-08--your-model-already-knows-attention-guided-safety-filter-for-vision-language-action-models.md): Attention-guided safety filter, dynamic SafeLIBERO collision and safe-success results.

### 真实世界数据和全身控制正在接受具体规模测试
YUBI 用更轻的手指对齐夹爪和固定支架的 VR 跟踪来缓解数据瓶颈。报告的数据集规模对开放式 UMI 风格设置来说很大：8,434 小时、120 万个回合、680 万个视频-语言-动作三元组，以及由 179 名操作员采集的 119 个任务。一个基于 π0.5 的策略在 YUBI 的腕部数据上训练后，可以在 UR、Franka 和 Toyota ELEY 机械臂之间迁移，并使用同一个末端执行器。

MotionWAM 把 world-action 建模扩展到 Unitree G1 人形机器人的行走与操作。它使用一个第一人称摄像头和统一的全身运动潜变量，在 9 个真实任务上的平均成功率达到 76.1%，而列出的最强基线为 43.9%。TORL-VLA 为接触密集任务加入触觉在线强化学习，在真实机器人子任务试验中达到杯子 30/30、锁扣 29/30 和鸡蛋 30/30 的成功。

#### 资料来源
- [YUBI: Yielding Universal Bidigital Interface for Bimanual Dexterous Manipulation at Scale](../Inbox/2026-06-08--yubi-yielding-universal-bidigital-interface-for-bimanual-dexterous-manipulation-at-scale.md): YUBI dataset scale, interface design, and cross-robot rollout results.
- [MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation](../Inbox/2026-06-08--motionwam-towards-foundation-world-action-models-for-real-time-humanoid-loco-manipulation.md): MotionWAM whole-body humanoid action design and nine-task real-robot results.
- [TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation](../Inbox/2026-06-08--torl-vla-tactile-guided-online-reinforcement-learning-for-contact-rich-manipulation.md): TORL-VLA tactile online RL design and contact-rich real-robot results.
