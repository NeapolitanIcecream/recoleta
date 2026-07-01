---
kind: trend
trend_doc_id: 763
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
topics:
- robot learning
- vision-language-action models
- reinforcement learning
- humanoid manipulation
- tactile sensing
- world models
- robot safety
run_id: materialize-outputs
aliases:
- recoleta-trend-763
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/world-models
- topic/robot-safety
language_code: zh-CN
---

# 机器人 VLA 论文优先关注可执行控制和实测反馈

## Overview
当天的机器人论文集中在让 vision-language-action (VLA) 策略可执行：在线适配、3D/接触反馈和成本更低的规划模型。SARL、3D HAMSTER 和 DVG-WM 显示，当前重点是能经受控制循环、几何和物理交互检验的证据。

## Clusters

### 在线 VLA 适配
多篇论文把部署当作学习循环。SARL 将语言提示作为语义动作来训练，然后用奖励学习哪些提示能产生有用的机器人行为。在 Libero-10 和四个真实 WidowX 任务上，论文报告单一任务提示下的初始成功率接近 0%，经过 60 到 100 个在线 episode 后成功率约为 80%。

Z-1 在监督微调后，对基于 flow 的 VLA 策略应用强化学习。在 24 个 RoboCasa 任务上，其平均成功率从监督微调后的 67.4% 提高到 group relative policy optimization 后的 80.6%。最强的受控结论是相对作者自身初始化提高 13.2 个百分点，因为部分外部比较使用了既有工作的报告数值。

一项剪枝研究补充了部署成本视角。它使用 VLM 到 VLA 适配过程中的权重变化，判断 OpenVLA 和 pi_0.5 的哪些组件可以移除。报告目标是在不进行剪枝后恢复的情况下，减少 12% 到 30% 参数，同时保持约 90% 的原始 LIBERO 性能。

#### Evidence
- [Adapting Generalist Robot Policies with Semantic Reinforcement Learning](../Inbox/2026-06-30--adapting-generalist-robot-policies-with-semantic-reinforcement-learning.md): SARL 提示级强化学习和在线适配结果。
- [Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models](../Inbox/2026-06-30--z-1-efficient-reinforcement-learning-for-vision-language-action-models.md): Z-1 的 RL 后训练设计和 RoboCasa 成功率提升。
- [Revisiting Parameter Redundancy in Vision-Language-Action Models: Insights from VLM-to-VLA Adaptation](../Inbox/2026-06-30--revisiting-parameter-redundancy-in-vision-language-action-models-insights-from-vlm-to-vla-adaptation.md): 基于 VLM 到 VLA 权重差异的 VLA 剪枝结果。

### 3D 和触觉执行信号
几何和接触被作为控制输入处理，而非可有可无的感知。3D HAMSTER 将末端执行器路点预测为 3D 坐标，并把它们输入点云控制策略。在 DroidSpatial-Bench 上，它在 10 cm 阈值下达到 65.5% Both 准确率，高于 RoboBrain-2.5-8B 的 60.1%，也远高于所给结果中的通用 VLM 基线。

UniTacVLA 为接触密集任务加入触觉 token、未来触觉预测和高频校正控制器。在八个真实机器人子任务上，每个设置 50 次试验，论文报告 clean 成功率为 64.0%，perturbed 成功率为 53.5%。扰动结果给出的信号更明确：复现的触觉基线 pi0.5-TacVLA 在扰动下达到 16.25%。

数据侧也符合这一重点。RoboTacDex 在 Unitree G1 上提供 6,000 条人形机器人轨迹，包含多视角 RGB-D、触觉信号、关节状态、动作和任务标签。Human-as-Humanoid 采用另一条路线，将同步的 ego-exo 人类视频转换为可执行的 60-DoF 人形机器人标签，并声称相对人形机器人遥操作，示范吞吐量提升 4.8× 到 7.2×。

#### Evidence
- [3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance](../Inbox/2026-06-30--3d-hamster-bridging-planning-and-control-in-hierarchical-vision-language-action-models-through-3d-trajectory-guidance.md): 3D HAMSTER 路点规划、深度编码和 DroidSpatial-Bench 结果。
- [UniTacVLA: Unified Tactile Understanding and Prediction in Vision Language Action Models](../Inbox/2026-06-30--unitacvla-unified-tactile-understanding-and-prediction-in-vision-language-action-models.md): UniTacVLA 触觉预测、校正控制器和真实机器人成功率。
- [RoboTacDex: A Dexterous Visual-Tactile-Action Dataset for Humanoid Manipulation](../Inbox/2026-06-30--robotacdex-a-dexterous-visual-tactile-action-dataset-for-humanoid-manipulation.md): RoboTacDex 数据集规模、模态和人形机器人操作覆盖范围。
- [Human-as-Humanoid: Enabling Zero-Shot Humanoid Learning from Ego-Exo Human Videos with Human-Aligned Embodiments](../Inbox/2026-06-30--human-as-humanoid-enabling-zero-shot-humanoid-learning-from-ego-exo-human-videos-with-human-aligned-embodiments.md): Human-as-Humanoid 转换流程和人形机器人示范吞吐量主张。

### 世界模型和安全指标
世界模型工作关注可用于控制内部的规划信号，要求速度足够快，并且对动作足够敏感。DVG-WM 将视频预测拆分为低分辨率动力学和高分辨率细化。在 LIBERO 视频预测上，它报告 89% 的物体级准确率和 88.7 秒推理时间；相比之下，CogVideoX-5B 为 236.8 秒，LVP-14B 为 354.2 秒。

AdaJEPA 在模型预测控制期间，使用执行后刚观察到的转移来适配潜在世界模型。所给结果中最强的是未见过的 PointMaze 布局：GD 成功率从 53.3 ± 8.2 提高到 78.7 ± 5.0，CEM 成功率从 49.3 ± 6.2 提高到 70.7 ± 3.8。

Delta-JEPA 在不做像素重建的情况下针对动作敏感性。它的潜在位移动作解码器根据潜在状态之间的变化重建已执行动作。在四个规划任务上，它报告了所给表格中的最佳成功率，包括 Push-T 上的 89.07 ± 1.90 和 OGB-Cube 上的 79.27 ± 1.81。

OopsieVerse 增加了单独的安全信号：面向家庭操作的显式损伤跟踪。其基准包含 OmniGibson 和 RoboCasa 中的 32 个任务实例，覆盖机械、热和流体损伤类别。所给文本提供的是基准范围，而非定量策略收益，因此其贡献主要在评测设计。

#### Evidence
- [DVG-WM: Disentangled Video Generation Enables Efficient Embodied World Model for Robotic Manipulation](../Inbox/2026-06-30--dvg-wm-disentangled-video-generation-enables-efficient-embodied-world-model-for-robotic-manipulation.md): DVG-WM 视频世界模型设计以及 LIBERO 速度和质量结果。
- [AdaJEPA: An Adaptive Latent World Model](../Inbox/2026-06-30--adajepa-an-adaptive-latent-world-model.md): AdaJEPA 闭环测试时适配和 PointMaze 结果。
- [Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding](../Inbox/2026-06-30--delta-jepa-learning-action-sensitive-world-models-via-latent-difference-decoding.md): Delta-JEPA 潜在位移解码器和规划成功率。
- [OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation](../Inbox/2026-06-30--oopsieverse-a-safety-benchmark-with-damage-aware-simulation-for-robot-manipulation.md): OopsieVerse 损伤感知基准范围和损伤类别。
