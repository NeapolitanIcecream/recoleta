---
kind: trend
trend_doc_id: 692
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
topics:
- robotics
- vision-language-action models
- reinforcement learning
- robot safety
- world models
- human demonstrations
- shared autonomy
run_id: materialize-outputs
aliases:
- recoleta-trend-692
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/robot-safety
- topic/world-models
- topic/human-demonstrations
- topic/shared-autonomy
language_code: zh-CN
---

# 机器人 VLA 研究正在面向接触、安全限制和演示稀缺条件下的闭环可靠性

## 概览
这一时期的机器人视觉-语言-动作（VLA）研究集中在部署后的可靠性。dVLA-RL、LIBERO-Safety 和 LaST-HD 显示出主要压力点：任务奖励优化、受安全约束的评估，以及用于接触密集操控的更低成本人类来源数据。

## 研究发现

### 闭环 VLA 训练
多篇论文把监督模仿视为机器人策略的不完整训练信号。dVLA-RL 将近端策略优化（PPO）用于离散扩散 VLA 的采样去噪路径，让策略在多步动作生成中得到可用的似然。论文报告 LIBERO 平均成功率为 99.7%，并把 RoboTwin 2.0 上的 MM-ACT 骨干平均成功率从 61.4% 提高到 92.0%。

Flatness Preserves Instruction Following 处理另一类失效：小规模机器人数据集会让 VLA 忽略变更后的语言指令。在微调中加入 sharpness-aware minimization（SAM）后，无需新数据即可改善反事实指令跟随；其中 LIBERO-CF 成功率为 47.8%，默认 π0.5 微调为 13.2%。RECALL 加入部署循环：在高不确定性状态收集恢复演示，再用回放训练以避免遗忘。它的最强设置达到 72.4% 的 LIBERO-10 总体成功率，匹配的被动收集为 60.2%。

#### 资料来源
- [dVLA-RL: Reinforcement Learning over Denoising Trajectories for Discrete Diffusion Vision-Language-Action Models](../Inbox/2026-06-22--dvla-rl-reinforcement-learning-over-denoising-trajectories-for-discrete-diffusion-vision-language-action-models.md): dVLA-RL 方法和报告的 LIBERO/RoboTwin 提升
- [Flatness Preserves Instruction Following in Vision-Language-Action Models](../Inbox/2026-06-22--flatness-preserves-instruction-following-in-vision-language-action-models.md): 用于指令跟随的 SAM 微调结果
- [RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models](../Inbox/2026-06-22--recall-recovery-experience-collection-for-active-lifelong-learning-in-vision-language-action-models.md): 不确定性引导的恢复数据和回放结果

### 用于接触密集操控的人类数据
这些机器人论文中，数据收集是主要瓶颈，因此多个系统以更有选择性的方式把人重新纳入循环。LaST-HD 使用人手演示、动作捕捉手套和潜在动力学对齐，训练可跨夹爪和灵巧手使用的机器人策略。它报告六个真实世界任务的平均成功率为 0.73，并称该手套的数据收集速度比机器人遥操作快 4–5 倍。

Assistron 保持 VLA 冻结，并在抓取、释放等接触密集时刻请求摇杆协助。在新手用户辅助操控基准中，它达到 91.3% 的部分成功率，任务时间中有 43.5% 由系统自主运行。CoorDex 展示了同一接触问题在人形机器人仿真侧的版本：分离的身体和手部先验让移动中的抓取任务可以训练；报告的 WalkGrab 消融中，直接在关节空间使用 PPO 失败。

#### 资料来源
- [LaST-HD: Learning Latent Physical Reasoning from Scalable Human Data for Robot Manipulation](../Inbox/2026-06-22--last-hd-learning-latent-physical-reasoning-from-scalable-human-data-for-robot-manipulation.md): LaST-HD 的人手数据、手套流程和真实世界成功率结果
- [Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models](../Inbox/2026-06-22--assistron-bayesian-shared-autonomy-with-off-the-shelf-vision-language-action-models.md): Assistron 的共享自主设计和新手用户基准结果
- [CoorDex: Coordinating Body and Hand Priors for Continuous Dexterous Humanoid Loco-Manipulation](../Inbox/2026-06-22--coordex-coordinating-body-and-hand-priors-for-continuous-dexterous-humanoid-loco-manipulation.md): CoorDex 的身体/手部先验和移动操控消融

### 安全与世界模型检查
安全工作正在变得更具体。LIBERO-Safety 增加 75 个任务，覆盖物理和语义安全套件，并包含 19,664 条经人工筛查的无碰撞演示。该基准显示，强任务策略在困难安全设置下仍会失效：OpenVLA-OFT 在 AAG-L2 上成功率降至 1.3%，π0.5 在同一困难的可供性知觉抓取等级上也只有 35.3%。

IOI 通过把精确机器人运动学注入动作条件视频模型来处理仿真 rollout。在 RoboTwin 上，它在列出的基线中报告了最佳的总体 SSIM、LPIPS 和 FVD；其 FVD 为 41.23，IRASim 为 126.20，Ctrl-World 为 64.90。另一篇水印论文为已部署的 VLA 和世界-动作模型服务加入所有权审计角度：在 16 次审计 rollout 下，它报告四种策略-机器人组合在 1% 假阳性率下的真阳性率为 1.00。

#### 资料来源
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety 基准规模和安全评估结果
- [IOI: Decoupling Kinematics and Physics for Interactive World Models](../Inbox/2026-06-22--ioi-decoupling-kinematics-and-physics-for-interactive-world-models.md): IOI 的运动学引导世界模型和 RoboTwin 指标
- [A Watermark for Vision-Language-Action and World Action Models](../Inbox/2026-06-22--a-watermark-for-vision-language-action-and-world-action-models.md): 潜在噪声水印方法和审计结果

### 医疗和空中控制有选择地使用 VLA 式训练
这一时期还包括一些特定领域自主系统论文，它们选用了 VLA 做法中的部分组件。BiliVLA 训练内镜导航策略，为 ERCP 模型任务输出目标类别、边界框和电机命令。它的两阶段训练先做监督调优，再做 group relative policy optimization（GRPO）；报告的总体结果中，成功率提升到 84.85%，EndoVLA 为 58.86%。

SkyJEPA 聚焦四旋翼，避开语言条件操控。它训练潜在世界模型做长时域预测，再把预测潜变量映射回公制状态变量，用于基于采样的控制。可用摘录给出方法细节，并声称做了户外闭环测试，但没有提供指标值，因此可据此得出的结论更窄：潜在预测正在与具有物理形状约束的读出结合，用于实时控制。

#### 资料来源
- [BiliVLA: Scene-Aware Vision-Language-Action Model with Reinforcement Learning for Autonomous Biliary Endoscopic Navigation](../Inbox/2026-06-22--bilivla-scene-aware-vision-language-action-model-with-reinforcement-learning-for-autonomous-biliary-endoscopic-navigation.md): BiliVLA 训练设置和 ERCP 模型结果
- [SkyJEPA: Learning Long-Horizon World Models for Zero-Shot Sim-to-Real Control of Quadrotors](../Inbox/2026-06-22--skyjepa-learning-long-horizon-world-models-for-zero-shot-sim-to-real-control-of-quadrotors.md): SkyJEPA 潜在世界模型设计和可用报告指标的限制
