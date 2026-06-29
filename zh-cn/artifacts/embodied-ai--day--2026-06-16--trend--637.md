---
kind: trend
trend_doc_id: 637
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
topics:
- robot manipulation
- vision-language-action models
- world models
- robot evaluation
- multimodal sensing
- policy adaptation
run_id: materialize-outputs
aliases:
- recoleta-trend-637
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/world-models
- topic/robot-evaluation
- topic/multimodal-sensing
- topic/policy-adaptation
language_code: zh-CN
---

# 机器人VLA工作集中于真实控制条件下的泛化

## Overview
这一时期的重点是机器人操作。当前工作集中在视觉-语言-动作（VLA）策略上，目标是在不同机器人本体间扩展，在行动前推理，并在部署期间检查自身动作。Qwen-RobotManip是最明确的规模化尝试；其他工作加入潜在规划、世界模型更新、传感器选择、不确定性、记忆和更严格的诊断。

## Clusters

### 跨具身规模和传感器选择
Qwen-RobotManip把机器人形态差异处理为对齐问题。它把不同机械臂、夹爪、相机和动作空间映射到共享的状态-动作模板，然后在约38,100小时的操作数据上训练。大部分规模来自人到机器人的合成流程：该流程把第一视角人类示范渲染成15种双臂机器人配置。报告称其在RoboChallenge Table30-v1通用赛道排名第一，并报告了在AgileX ALOHA、Franka、UR和ARX平台上的真实机器人验证。

MuseVLA加入了另一类泛化压力：策略必须判断什么时候RGB不够用。它根据指令和场景选择热成像、声学、mmWave或不使用额外传感器，把选中的测量转换为有对象定位的传感器图像，再送回VLA。在真实灵巧手任务中，经过合成预训练后，模型在已见传感器引导任务上的平均成功率为80.6%，在未见任务上为66.7%。

#### Evidence
- [Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models](../Inbox/2026-06-16--qwen-robotmanip-technical-report-alignment-unlocks-scale-for-robotic-manipulation-foundation-models.md): Qwen-RobotManip的数据规模、跨具身对齐、人到机器人的合成数据，以及报告的基准结果。
- [MuseVLA: An Adaptive Multimodal Sensing Vision-Language-Action Model for Robotic Manipulation](../Inbox/2026-06-16--musevla-an-adaptive-multimodal-sensing-vision-language-action-model-for-robotic-manipulation.md): MuseVLA的自适应传感器选择、有对象定位的传感器图像设计、数据集规模和成功率。

### 潜在规划和世界模型训练
多篇论文在解码机器人动作前加入内部预测步骤。PearlVLA用冻结的潜在世界模型细化潜在计划token，然后解码连续动作块，从而让动作生成保持较快速度。它报告在LIBERO上的平均成功率为98.7%，高于本地摘要中列出的强基线。

ThinkingVLA让模型能看到中间推理：文本子目标、预测的未来图像、面向动作的理由，然后生成动作。它在RoboTwin 2.0 Easy上达到77.9%的平均成功率，并报告在五个真实ALOHA任务上的平均成功率为85%。WAM-RL从训练侧测试同一思路，在在线交互期间同时更新视频世界模型和actor。在LIBERO-Object上，成功率从基础模型的68%升至82%。

#### Evidence
- [PearlVLA: Progressive Embodied Action-Plan Refinement in Latent Space](../Inbox/2026-06-16--pearlvla-progressive-embodied-action-plan-refinement-in-latent-space.md): PearlVLA的潜在细化设计和LIBERO结果。
- [ThinkingVLA: Interleaved Vision and Language Reasoning for Robotic Manipulation](../Inbox/2026-06-16--thinkingvla-interleaved-vision-and-language-reasoning-for-robotic-manipulation.md): ThinkingVLA交错的文本-图像-动作推理，以及RoboTwin/ALOHA结果。
- [WAM-RL: World-Action Model Reinforcement Learning with Reconstruction Rewards and Online Video SFT](../Inbox/2026-06-16--wam-rl-world-action-model-reinforcement-learning-with-reconstruction-rewards-and-online-video-sft.md): WAM-RL对世界模型和actor的联合在线训练，以及LIBERO-Object和RLBench结果。

### 已部署策略的运行时检查和记忆
面向部署的论文关注策略在首个动作样本可能出错或当前图像缺少任务历史时该怎么做。VERITAS采样多个短动作块，用视觉验证器评分，执行最佳候选动作，之后用已验证成功的rollout进行微调。在三个策略和1,160个评估episode中，它报告在没有策略微调的情况下，仿真平均成功率提升12.6%，真实部署提升35%。

Uncertainty Quantification for Flow-Based VLAs通过动作头集成之间的速度场分歧加入置信度信号。同一信号驱动SAVE；SAVE是一种主动微调方法，会选择不确定案例请求专家示范。WeaveLA处理重复问题：它只在子目标完成事件写入紧凑的潜在记忆。在报告的设置中，RoboMME SwingXtimes且N=3时，使用pi_0.5骨干后成功率从0%升至47.8%。

#### Evidence
- [Visual Verification Enables Inference-time Steering and Autonomous Policy Improvement](../Inbox/2026-06-16--visual-verification-enables-inference-time-steering-and-autonomous-policy-improvement.md): VERITAS的推理时视觉验证、自生成rollout和报告的收益。
- [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](../Inbox/2026-06-16--uncertainty-quantification-for-flow-based-vision-language-action-models.md): 用于不确定性的速度场分歧和SAVE主动微调。
- [WeaveLA: Event Driven Cross-Subtask Latent Memory Weaving for Repetitive Robot Manipulation](../Inbox/2026-06-16--weavela-event-driven-cross-subtask-latent-memory-weaving-for-repetitive-robot-manipulation.md): WeaveLA的事件驱动潜在记忆和重复任务收益。

### 基准暴露隐藏失败模式
评估工作强调细粒度诊断。EBench在五个能力轴和四类泛化转移上测试26个移动、长程和灵巧仿真任务。主要结果是，π0、π0.5、XVLA和InternVLA-A1的总体测试成功率集中在24.4%到29.5%的窄区间内，但技能画像差异很大。InternVLA-A1在移动操作上表现好，但在灵巧固定基座任务上的成功率降至5.8%。

WireCraft面向电线和线缆等工业可变形线状物体。特权状态RL解决了多个仿真设置，其中State PPO在以太网连接器插入任务上的插入成功率为95.86%。基于视觉的方法仍弱得多：Vision PPO在同一以太网任务上的插入成功率为17.74%，仅用仿真训练的ACT在报告的真实UR5测试中插入结果为0/10。

#### Evidence
- [EBench: Elemental Diagnosis of Generalist Mobile Manipulation Policies](../Inbox/2026-06-16--ebench-elemental-diagnosis-of-generalist-mobile-manipulation-policies.md): EBench的任务设计、能力轴、泛化转移和策略比较结果。
- [WireCraft: A Simulation Benchmark for Industrial DLO Manipulation](../Inbox/2026-06-16--wirecraft-a-simulation-benchmark-for-industrial-dlo-manipulation.md): WireCraft工业DLO基准设计，以及状态方法与视觉方法的性能差距。
