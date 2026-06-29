---
kind: trend
trend_doc_id: 171
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
topics:
- robotics
- vision-language-action
- world-models
- cross-embodiment
- tactile-sensing
- medical-robotics
run_id: materialize-outputs
aliases:
- recoleta-trend-171
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/cross-embodiment
- topic/tactile-sensing
- topic/medical-robotics
language_code: zh-CN
---

# 机器人基础模型正在在迁移、规划和接触上变得更落地

## Overview
这一天最强的主线是：机器人论文正在把广泛预训练、显式规划和接触反馈，和具体的执行指标连接起来。JoyAI-RA、Cortex 2.0 和 Open-H-Embodiment 构成了核心。它们在跨本体迁移、长时程规划和医疗机器人上都给出了提升，而且结果已经落到真实机器人、工业部署，或两者兼有。

## Clusters

### Cross-embodiment training gets real benchmark wins
视觉-语言-动作工作在数据上覆盖更广，也更明确说明动作如何在不同本体之间迁移。JoyAI-RA 用网页数据、第一人称人类视频、仿真和机器人轨迹训练一个策略，然后把动作映射到共享表示中。报告的提升在仿真和真实人形基准上都很大：RoboTwin Easy 和 Hard 分别是 90.48% 和 89.28%，RoboCasa GR1 Tabletop 是 63.2%，AgiBot 真实世界基准的平均成功率是 0.74，π0.5 是 0.62。Open-H-Embodiment 在医疗机器人里用同样的规模论证，数据量是 770 小时、20 个平台，GR00T-H 策略在端到端缝合上达到 25% 成功率，而 ACT、GR00T-N1.6 和 LingBot-VA 都是 20 次试验里 0 次成功。当天最强的证据表明，跨本体学习正在变成明确的训练目标，而不只是对泛化能力的主张。

#### Evidence
- [JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy](../Inbox/2026-04-22--joyai-ra-0-1-a-foundation-model-for-robotic-autonomy.md): JoyAI-RA data mix, unified action space, and benchmark gains across simulation and real robot settings
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): Open-H dataset scale and cross-platform medical VLA results with GR00T-H

### Planning over futures moves into deployed robot systems
世界模型越来越多地出现在长时程里错误会不断累积的场景中。Cortex 2.0 给工业 VLA 栈加入潜在轨迹展开规划，在动作执行前对进展、风险和完成情况打分。摘要称它在四个已部署仓储任务上拿到最好的成功率，评估时没有人工介入，不过摘录里没有给出逐任务的具体数字。在更严格的安全场景里，面向血管取栓的 TD-MPC2 世界模型智能体在留出的仿真解剖上平均成功率达到 58%，SAC 是 36%，路径比率从 22% 提高到 49%，最大导丝尖端力保持在 0.55 N，远低于论文给出的 1.5 N 破裂阈值。医疗机器人也通过 Open-H 的动作条件手术模拟器加入了这条路线，这个模拟器是在九个平台上训练的。

#### Evidence
- [Cortex 2.0: Grounding World Models in Real-World Industrial Deployment](../Inbox/2026-04-22--cortex-2-0-grounding-world-models-in-real-world-industrial-deployment.md): Industrial world-model planning with deployment-scale data and claimed real-world gains
- [Toward Safe Autonomous Robotic Endovascular Interventions using World Models](../Inbox/2026-04-22--toward-safe-autonomous-robotic-endovascular-interventions-using-world-models.md): World-model RL improves held-out navigation and reports force-based safety numbers
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): Multi-embodiment surgical world model trained across nine platforms

### Compact VLA systems add task structure and confidence signals
更小的模型在动作学习前获得了更多结构。PokeVLA 围绕具身预训练、来自基座和腕部视角的目标分割，以及训练中的几何对齐构建了一个紧凑 VLA。报告中的提升之所以重要，是因为它们在迁移和扰动下都能保持：在 LIBERO-Plus 变体上比 OpenVLA-OFT 高 9.7%，比 VLA-Adapter 高 20.2%，在真实世界扰动下还有 20.0% 的提升。另一篇论文处理的是另一个薄弱点：置信度。Temporal Difference Calibration 把整个回合的成功预测定义出来，用时序差分目标训练，并在 OpenVLA、π0、π0-FAST 和 UniVLA 上报告了更好的校准和更早的失败检测。它还在 LIBERO 上为 OpenVLA 带来 15% 的成功率提升，条件是用学到的价值预测器给采样动作排序。共同点是，轻量或黑盒 VLA 系统现在拿到的是围绕感知和可靠性的任务特定监督，而不只是更大的主干网络。

#### Evidence
- [PokeVLA: Empowering Pocket-Sized Vision-Language-Action Model with Comprehensive World Knowledge Guidance](../Inbox/2026-04-22--pokevla-empowering-pocket-sized-vision-language-action-model-with-comprehensive-world-knowledge-guidance.md): Compact VLA with embodied pretraining, segmentation token, and perturbation robustness gains
- [Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models](../Inbox/2026-04-22--temporal-difference-calibration-in-sequential-tasks-application-to-vision-language-action-models.md): Sequential calibration for VLA policies and reported early-failure detection improvements

### Tactile work gets cheaper to build and faster to train
接触丰富的机器人工作正在从两个方向同时提升感知质量：更好的硬件和更快的仿真。FingerEye 用一个很小的指尖模块，把接触前、接触开始和接触后都保持在一个视觉流里，材料成本大约 60 美元。论文报告了六轴力矩传感灵敏度，并把这个信号用于精细抓取，包括在脆弱物体上做接触感知停止。ETac 从训练侧处理同一个问题。它用快速传播模型加一个小的学习残差来近似 FEM 质量的触觉形变，达到 4,096 个并行环境和单张 RTX 4090 上 869 FPS，并训练出在四类物体上平均成功率为 84.45% 的盲抓取策略。当天的触觉论文给出的结论很直接：更丰富的接触反馈正在变得更容易搭建，也更容易在大规模上训练。

#### Evidence
- [FingerEye: Continuous and Unified Vision-Tactile Sensing for Dexterous Manipulation](../Inbox/2026-04-22--fingereye-continuous-and-unified-vision-tactile-sensing-for-dexterous-manipulation.md): Continuous vision-tactile sensing hardware with low cost and contact-onset use in dexterous tasks
- [ETac: A Lightweight and Efficient Tactile Simulation Framework for Learning Dexterous Manipulation](../Inbox/2026-04-22--etac-a-lightweight-and-efficient-tactile-simulation-framework-for-learning-dexterous-manipulation.md): Efficient tactile simulation and large-scale RL throughput for blind grasping
