---
kind: ideas
granularity: day
period_start: '2026-07-02T00:00:00'
period_end: '2026-07-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action policies
- world models
- test-time control
- robot data
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-policies
- topic/world-models
- topic/test-time-control
- topic/robot-data
language_code: zh-CN
---

# 自适应机器人操作的数据与控制

## Summary
机器人团队可以基于现有证据测试三项具体改变：在推理期间中断过期动作块，在静态视角之外采集移动摄像头 episode，并在任务特定示范前用无标签机器人运动预训练 VLA 策略。每项改变都针对操作中的一个可测量失败模式：开环执行期间的漂移、摄像头或物体位置捷径，以及专家遥操作数据不足。

## 用于动作块 VLA 策略的视觉潜变量漂移监控器
采用动作块的 VLA 部署应加入一个小型推理时监控器，检查摄像头流的变化是否符合当前动作块的预测。实际触发条件很简单：如果观测到的视觉潜变量变化持续偏离预期变化，就停止执行队列中剩余的动作，并让策略生成一个修正后的动作块。

VLA-Corrector 给出了一个具体模板。它冻结 VLA 主干，在示范数据上训练一个 40M 的潜在动力学 MLP，比较预期和实际的视觉潜变量变化，并用中位数和 MAD 阈值检测持续不匹配。发生中断后，它把下一次 flow-matching 去噪步骤引向修正方向。在 MetaWorld 上，pi0.5 的平均成功率从 48.70% 升至 64.35%；SmolVLA 在 horizon 10 下从 61.90% 提升到 73.00%，同时平均策略调用次数从 19.27 降至 15.64。

低成本测试是在涉及接触、打滑或位姿漂移的任务上做一次动作块审计。记录预期视觉潜变量变化、观测变化、中断率、成功率，以及每个 episode 的策略调用次数。如果中断集中出现在真实执行错误附近，并减少失败的长动作块，这个监控器就可以成为固定 horizon VLA 控制器的部署防护机制。

### Evidence
- [VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon](../Inbox/2026-07-02--vla-corrector-lightweight-detect-and-correct-inference-for-adaptive-action-horizon.md): 概述了 VLA-Corrector 的冻结主干监控器、漂移检测、修正式重规划，以及报告的成功率和策略调用收益。
- [VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon](../Inbox/2026-07-02--vla-corrector-lightweight-detect-and-correct-inference-for-adaptive-action-horizon.md): 描述了在线偏差检测、截断过期动作和修正式重规划机制。

## VLA 数据采集中的移动摄像头和物体偏移 episode
当机器人会遇到摄像头移动、装置差异或工作单元布局变化时，VLA 数据采集应包含移动环境摄像头 episode 和物体布局偏移。固定视角下的成功率可能掩盖摄像头位姿、机器人基座和物体位置之间的捷径。

The Moving Eye 给出了一个可执行的采集模式：一条机械臂执行操作，另一条机械臂移动环境摄像头，然后在训练集中混合移动摄像头 episode 和静态多视角 episode。在笔任务中，固定视角训练在固定的同分布测试上达到 85.0% 成功率，在移动摄像头评估中为 43.0%。混合数据分别达到 86.0% 和 83.0%。在物体位置测试中，将支架移动一个直径后，多固定视角基线从 95.0% 降至 71.9%，而混合 1:3 设置得到 91.9% 和 90.6%。

一个小的采用步骤是在现有 VLA 评估中加入摄像头运动划分和一个直径的物体偏移划分。团队随后可以采集一批有边界的移动摄像头 episode，在 Gr00t 风格训练中尝试接近 1:3 的 Moving:Multi-Fixed 比例，并检查分布外成功率是否提升且不损害固定视角表现。

### Evidence
- [The Moving Eye: Enhancing VLA Spatial Generalization via Hybrid Dynamic Data Collection](../Inbox/2026-07-02--the-moving-eye-enhancing-vla-spatial-generalization-via-hybrid-dynamic-data-collection.md): 报告了双臂移动摄像头设置、混合数据比例、固定视角与移动摄像头结果，以及物体位置偏移结果。
- [The Moving Eye: Enhancing VLA Spatial Generalization via Hybrid Dynamic Data Collection](../Inbox/2026-07-02--the-moving-eye-enhancing-vla-spatial-generalization-via-hybrid-dynamic-data-collection.md): 详述了在摄像头和布局变化部署中会产生影响的摄像头-物体和物体位置捷径机制。

## 在语言条件行为克隆前进行无标签随机探索预训练
拥有闲置硬件的机器人团队可以采集无标签运动轨迹，并在语言条件行为克隆前使用逆动力学预训练。目标用户是受专家遥操作和任务标签成本限制的团队，尤其是在小型机械臂上，安全随机探索可以在有限监督下运行数小时。

TAP 展示了这个流程。它通过预测连续观测之间的 7D 位姿增量动作，在任务无关轨迹上预训练 VLA，然后用带语言标签的专家示范微调同一个模型。真实世界流程会构建安全位姿库，采样可达路点，加入接触启发式规则，注入有界高斯噪声，并记录轨迹。在 SIMPLER 中，TAP-20k 达到 33.32% Avg-All 成功率；相同架构用标准行为克隆训练时为 23.15%。在真实 WidowX 推南瓜任务上，TAP 平均成功率为 61%，从头训练为 21%；在背景和视角变化下，从头训练模型得分为 0%，TAP 仍保留了一部分成功率。

实际检查方式是运行 20 到 30 小时安全随机探索，用逆动力学目标做预训练，然后在已用于行为克隆的同一示范预算上微调。评估应集中在接触、推动和视角变化会暴露基线缺口的任务上。

### Evidence
- [Learning to Move Before Learning to Do: Task-Agnostic pretraining for VLAs](../Inbox/2026-07-02--learning-to-move-before-learning-to-do-task-agnostic-pretraining-for-vlas.md): 概述了 TAP 的任务无关轨迹来源、逆动力学预训练、随机探索流程，以及报告的 SIMPLER 和 WidowX 结果。
- [Learning to Move Before Learning to Do: Task-Agnostic pretraining for VLAs](../Inbox/2026-07-02--learning-to-move-before-learning-to-do-task-agnostic-pretraining-for-vlas.md): 解释了使用无标签自主交互轨迹的动机，这类轨迹常被当前 VLA 流程丢弃。
