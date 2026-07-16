---
kind: trend
trend_doc_id: 645
granularity: day
period_start: '2026-06-17T00:00:00'
period_end: '2026-06-18T00:00:00'
topics:
- robotics
- vision-language-action models
- world models
- robot safety
- sim-to-real
- data poisoning
run_id: materialize-outputs
aliases:
- recoleta-trend-645
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/robot-safety
- topic/sim-to-real
- topic/data-poisoning
language_code: zh-CN
---

# 机器人 VLA 研究聚焦执行检查、记忆和伤害安全

## 概览
这一时间窗口主要是机器人论文。最强的模式是实际控制：视觉-语言-动作（VLA）模型获得运动预训练、运行时校正、持久世界模型和明确的伤害测试。RoboShackles、Mem-World 和 DREAM-Chunk 显示，当前重点放在策略离线训练完成后会发生什么。

## 研究发现

### 跨具身运动预训练
一篇论文针对通用 VLA 训练中的数据瓶颈：机器人动作标签稀缺，而人类第一视角操作视频数量充足。该方法用解耦 VQ-VAE 学习带掩码的潜在动作 token，并用物理掩码把前景运动与场景背景分开。随后，一个 Prismatic-7B 视觉语言模型在机器人适配前预测这些 token。

报告的提升很具体。在 LIBERO 上，完整方法达到 91.8% 的平均成功率，高于 OpenVLA 的 76.5% 和 Diffusion Policy 的 72.4%。在 RoboTwin 2.0 双臂仿真中，它在 10 个任务上的平均成功率达到 67.7%。下游设置中每个任务约使用 50 条轨迹，因此该主张指向用无标签视频预训练后降低适配成本。

#### 资料来源
- [Motion-Focused Latent Action Enables Cross-Embodiment VLA Training from Human EgoVideos](../Inbox/2026-06-17--motion-focused-latent-action-enables-cross-embodiment-vla-training-from-human-egovideos.md): 潜在动作 VLA 训练的摘要、方法，以及报告的 LIBERO/RoboTwin 结果。

### 动作分块策略的运行时校正
两篇论文把 VLA 执行视为实时控制问题。DREAM-Chunk 在测试时采样多个候选动作块，用一个小型世界模型预测它们的潜在未来，并执行预测状态最符合观测轨迹的动作块。在受扰动的精密插入任务上，它报告 π0.5 成功率为 65%，而开环执行为 10%。

以对象为中心的残差强化学习提供了另一条校正路径。冻结的 VLA 提供基础动作，在仿真中训练的基于位姿的残差策略则在真实 FR3 机器人上调整这些动作。在五个桌面任务中，加入残差策略后的平均真实成功率为 76%，基础 VLA 为 42%。残差 actor 很小：每次 GPU 前向传播约 0.06 ms，而 VLA 约需 140 ms。

#### 资料来源
- [DREAM-Chunk: Reactive Action Chunking with Latent World Model](../Inbox/2026-06-17--dream-chunk-reactive-action-chunking-with-latent-world-model.md): DREAM-Chunk 摘要、测试时选择机制、硬件设置和插入任务结果。
- [Object-Centric Residual RL for Zero-Shot Sim-to-Real VLA Enhancement](../Inbox/2026-06-17--object-centric-residual-rl-for-zero-shot-sim-to-real-vla-enhancement.md): 以对象为中心的残差 RL 摘要、仿真到现实设置、真实机器人成功率和计算成本。

### 世界模型记忆与世界模型篡改
世界模型同时用于能力提升和安全研究。Mem-World 增加了以腕部视角为中心的 surfel 记忆，使机器人视频模型能在腕部相机被遮挡或快速移动时检索有用的历史视角。在 34 条 DROID 记忆压力回放轨迹上，它把第三视角 PSNR 提高到 25.30，而 Ctrl-World 为 23.17。它的仿真成功率估计也与真实世界成功率更接近，在五个任务上的相关系数为 r=0.97。

SWAAP 把同一类学习到的动力学作为攻击面来研究。它污染微调缓冲区中选定的下一状态目标，同时保持状态、动作和奖励不变。论文报告了在 DMControl、MyoSuite 和 MetaWorld 上对 TD-MPC2 与 DINO-WM 的评估，并测试其对残差、CUSUM 和 TRIM 风格防御的隐蔽性。现有摘要没有给出数值化的回报下降，因此可靠结论是攻击构造和已评估的威胁设置。

#### 资料来源
- [Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation](../Inbox/2026-06-17--mem-world-memory-augmented-action-conditioned-world-models-for-persistent-robot-manipulation.md): Mem-World 摘要、surfel 记忆机制、DROID 结果和策略评估相关性。
- [Stealthy World Model Manipulation via Data Poisoning](../Inbox/2026-06-17--stealthy-world-model-manipulation-via-data-poisoning.md): SWAAP 摘要、投毒机制、评估的智能体、基准套件和防御类型。

### 具身模型的伤害预防基准
RoboShackles 关注机器人行动前的拒绝行为。它基于真实 DROID 观测构建了 10,000 个合成危险机器人视频片段，覆盖手部和人类直接伤害，以及火灾、电气、水和跌落风险。测试集有 1,200 个样本，每类 200 个。

评估规则很严格：具身基础模型（EFM）只有在拒绝指令或不产生可执行动作时才算安全。六个接受测试的 EFM，包括 Cosmos-Policy、DreamZero、LingBot-VA、FastWAM、VLA-JEPA 和 World Guidance，在每个测试类别中都产生了不安全动作。这个结果是一个基准失败信号，不能说明训练修复方案已经存在。

#### 资料来源
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): RoboShackles 数据集构建、危险类别、严格拒绝规则和 100% 不安全动作结果。
