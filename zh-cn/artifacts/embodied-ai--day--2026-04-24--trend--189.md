---
kind: trend
trend_doc_id: 189
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
topics:
- robotics
- vision-language-action
- evaluation
- safety
- online-rl
- long-horizon-planning
run_id: materialize-outputs
aliases:
- recoleta-trend-189
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/evaluation
- topic/safety
- topic/online-rl
- topic/long-horizon-planning
language_code: zh-CN
---

# 机器人学习工作围绕部署级适应、评估和安全展开

## Overview
这一天的机器人论文最强的部分，是更接近真实部署的执行系统。重点很具体：快速在线适应、动作约束的评估、物理安全测试，以及长任务记忆。RL Token、dWorldEval 和 RedVLA 以真实机器人或部署式代理结果作为支撑，而综述论文说明，数据和基准设计仍然限制了这些进展的可比性。

## Clusters

### Sample-efficient adaptation with compact control signals
真实机器人适应正在变得更有针对性。RL Token 把一个预训练的视觉-语言-动作模型冻结起来，暴露一个紧凑状态供强化学习使用，只在线更新一个小型 actor-critic。它在精密操作上的效果很具体：最难阶段的执行速度最高快 3 倍，螺丝插入任务在几分钟到几小时练习后，成功率从 20% 提升到 65%。GazeVLA 从另一个角度解决同一个数据瓶颈。它把人类视线当作意图信号，在超过 1.5 亿帧的第一视角数据上预训练，并报告只用每个任务 10 条机器人轨迹和 50 条人类轨迹时仍有更强的 few-shot 迁移能力，包括简单抓放任务 85% 的成功率，以及在螺丝拧紧上相对 pi0.5 的 2 倍提升。

#### Evidence
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): RL Token method and real-robot gains
- [GazeVLA: Learning Human Intention for Robotic Manipulation](../Inbox/2026-04-24--gazevla-learning-human-intention-for-robotic-manipulation.md): GazeVLA intention transfer and few-shot results

### Evaluation infrastructure gets treated as core research
评估正在更接近部署约束。dWorldEval 把策略评估当作受动作条件约束的未来预测，把语言、图像和机器人动作放在同一个 token 空间里。它的代理分数和真实执行很接近，在 LIBERO、RoboTwin 和真实世界任务上的相关系数约为 0.91 到 0.93。同一篇论文还报告了比以往评估器更好的动作可控性和更低的长时程漂移。配套的 VLA 数据与基准综述把这件事说得更清楚：现有基准仍难以把任务复杂度和环境结构区分开来，对组合泛化和长时程推理的测试也还不够。

#### Evidence
- [dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model](../Inbox/2026-04-24--dworldeval-scalable-robotic-policy-evaluation-via-discrete-diffusion-world-model.md): dWorldEval proxy evaluation metrics and correlation with real execution
- [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](../Inbox/2026-04-24--vision-language-action-in-robotics-a-survey-of-datasets-benchmarks-and-data-engines.md): Survey evidence on benchmark and data gaps

### Safety work targets scene-level physical failure modes
安全测试正在变得更物理，也更模型特定。RedVLA 保持任务指令不变，在场景里加入一个风险物体，再调整它的位置来触发不安全行为。跨六个 VLA 模型，平均攻击成功率从 64.9% 到 95.5%，而累计危险物品误用在六个模型上都达到了 100% 的攻击成功率。论文还报告，在这个设置里更强的基础策略反而更容易被利用，而用 RedVLA 数据训练的轻量防护器把在线攻击成功率降低了 59.5%，对任务性能的影响很小。这让安全评估看起来更像围绕真实机器人运动进行的对抗式场景设计，而不是提示词过滤。

#### Evidence
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): Physical red teaming setup, vulnerability rates, and guard results

### Long-horizon VLAs add persistent state and planner logic
长时程机器人控制正在加入更明确的记忆和任务结构。CodeGraphVLP 构建一个持久的语义图，调用一次 LLM 写出任务专用规划器，然后把执行器 VLA 只与相关物体的掩码视图配对。在三个真实世界桌面任务上，它报告平均成功率 81.7%，高于 Gr00T N1.5 + Multi-frame 的 56.7% 和 π0 的 30.0%。机制很清楚：早期观测以图状态保留下来，进度检查写在代码里，动作策略在每一步看到的干扰更少。

#### Evidence
- [CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models](../Inbox/2026-04-24--codegraphvlp-code-as-planner-meets-semantic-graph-state-for-non-markovian-vision-language-action-models.md): Semantic graph planner design and real-world task results
