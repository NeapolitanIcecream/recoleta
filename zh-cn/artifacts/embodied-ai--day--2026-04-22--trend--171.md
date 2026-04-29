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

# 机器人基础模型开始在迁移、规划和接触上落到实处

## Overview
这一天最突出的主题很明确：机器人论文正在把大规模预训练、显式规划和接触反馈直接连到具体的执行指标上。JoyAI-RA、Cortex 2.0和Open-H-Embodiment构成了这份简报的核心。它们分别报告了跨具身迁移、长时程规划和医疗机器人上的提升，结果已经落到真实机器人、工业部署场景，或两者兼有。

## Clusters

### 跨具身训练开始在真实基准上赢得结果
视觉-语言-动作研究的数据来源正在变得更广，也更明确地处理动作如何在不同具身之间迁移。JoyAI-RA在网页数据、人类第一视角视频、仿真数据和机器人轨迹上训练单一策略，再把动作映射到共享表示中。论文报告的提升在仿真和真实人形机器人基准上都很大：在RoboTwin Easy和Hard上分别达到90.48%和89.28%，在RoboCasa GR1 Tabletop上达到63.2%，在AgiBot真实世界基准上的平均成功率达到0.74，而π0.5为0.62。Open-H-Embodiment在医疗机器人中也提出了同样的规模论据：数据集包含770小时、20个平台，训练出的GR00T-H策略在端到端缝合任务上达到25%的成功率，而ACT、GR00T-N1.6和LingBot-VA在20次试验中都是0次成功。当天最强的证据表明，跨具身学习正在成为一个具体的训练目标，而不只是泛化能力的说法。

#### Evidence
- [JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy](../Inbox/2026-04-22--joyai-ra-0-1-a-foundation-model-for-robotic-autonomy.md): JoyAI-RA的数据组合、统一动作空间，以及在仿真和真实机器人场景中的基准提升
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): Open-H数据集的规模，以及GR00T-H在跨平台医疗VLA上的结果

### 面向未来结果的规划进入已部署机器人系统
在长时程任务里，错误会不断累积，世界模型持续出现在这类场景中。Cortex 2.0把潜在空间中的 rollout 规划加入工业VLA系统，在执行前先按进展、风险和完成概率为候选未来打分。摘要称它在四个已部署的仓储任务上取得了最高成功率，并且评测期间不需要人工干预，但摘录没有给出逐任务的具体数字。在安全要求更高的场景里，用于取栓的TD-MPC2世界模型智能体在保留的仿真血管解剖上达到58%的平均成功率，SAC为36%；路径比从22%提高到49%；最大导丝尖端力保持在0.55 N，明显低于论文设定的1.5 N血管破裂阈值。医疗机器人也加入了这条路线，Open-H训练了一个跨九个平台的动作条件手术模拟器。

#### Evidence
- [Cortex 2.0: Grounding World Models in Real-World Industrial Deployment](../Inbox/2026-04-22--cortex-2-0-grounding-world-models-in-real-world-industrial-deployment.md): 工业世界模型规划，使用部署规模数据并声称带来真实世界提升
- [Toward Safe Autonomous Robotic Endovascular Interventions using World Models](../Inbox/2026-04-22--toward-safe-autonomous-robotic-endovascular-interventions-using-world-models.md): 世界模型强化学习提升了保留场景中的导航表现，并报告了基于力的安全指标
- [Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics](../Inbox/2026-04-22--open-h-embodiment-a-large-scale-dataset-for-enabling-foundation-models-in-medical-robotics.md): 跨多具身的手术世界模型，训练数据覆盖九个平台

### 紧凑型VLA系统加入任务结构和置信度信号
更小的模型在动作学习前开始加入额外结构。PokeVLA围绕具身预训练、来自底座和腕部视角的目标分割，以及训练时的几何对齐，构建了一个紧凑的VLA。论文报告的提升值得注意，因为这些提升在迁移和扰动下依然成立：在LIBERO-Plus变体上，相比OpenVLA-OFT提高9.7%，相比VLA-Adapter提高20.2%，在真实世界扰动下还提高了20.0%。另一篇论文处理的是另一个薄弱点：置信度。Temporal Difference Calibration把成功预测定义在整段轨迹上，用时序差分目标训练，并报告在OpenVLA、π0、π0-FAST和UniVLA上带来了更好的校准和更早的失败检测。当使用学到的价值预测器对采样动作排序时，它还让OpenVLA在LIBERO上的成功率提升了15%。共同点是，轻量级或黑盒VLA系统现在开始在感知和可靠性上获得任务特定的监督，而不只是换上更大的骨干模型。

#### Evidence
- [PokeVLA: Empowering Pocket-Sized Vision-Language-Action Model with Comprehensive World Knowledge Guidance](../Inbox/2026-04-22--pokevla-empowering-pocket-sized-vision-language-action-model-with-comprehensive-world-knowledge-guidance.md): 紧凑型VLA结合具身预训练、分割token，以及在扰动鲁棒性上的提升
- [Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models](../Inbox/2026-04-22--temporal-difference-calibration-in-sequential-tasks-application-to-vision-language-action-models.md): 面向VLA策略的序列校准，以及论文报告的早期失败检测改进

### 触觉方向更便宜，也更快训练
富接触机器人正在同时从两个方向提高传感质量：更好的硬件和更快的仿真。FingerEye用一个材料成本约60美元的小型指尖模块，让同一条视觉流在接触前、接触开始时和接触后持续工作。论文报告了六轴力/力矩灵敏度，并把这一路信号用于精细抓取，包括在脆弱物体上的接触感知停止。ETac从训练侧处理同一个问题。它用快速传播模型加上一个小型学习残差来近似达到FEM质量的触觉形变，在单张RTX 4090上实现4,096个并行环境和869 FPS，并训练出盲抓策略，在四类物体上的平均成功率达到84.45%。当天的触觉论文传达出一个实际结论：更丰富的接触反馈正在变得更容易构建，也更容易在大规模训练中使用。

#### Evidence
- [FingerEye: Continuous and Unified Vision-Tactile Sensing for Dexterous Manipulation](../Inbox/2026-04-22--fingereye-continuous-and-unified-vision-tactile-sensing-for-dexterous-manipulation.md): 低成本连续视觉-触觉传感硬件，以及其在灵巧任务中对接触起始阶段的利用
- [ETac: A Lightweight and Efficient Tactile Simulation Framework for Learning Dexterous Manipulation](../Inbox/2026-04-22--etac-a-lightweight-and-efficient-tactile-simulation-framework-for-learning-dexterous-manipulation.md): 高效触觉仿真，以及面向盲抓的大规模强化学习吞吐
