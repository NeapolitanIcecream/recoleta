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

# 机器人学习工作聚焦于面向部署的适应、评估和安全

## Overview
这一天的机器人论文最强的部分，是更接近真实部署的执行系统。重点很明确：快速在线适应、以动作为基础的评估、物理安全测试，以及面向长任务的记忆。RL Token、dWorldEval 和 RedVLA 用真实机器人结果或接近部署的代理指标支撑了这份简报，而那篇综述则说明，数据和基准设计仍然限制了这些进展能被多好地相互比较。

## Clusters

### 用紧凑控制信号实现高样本效率的适应
真实机器人适应正在变得更有针对性。RL Token 冻结预训练的视觉-语言-动作模型，暴露一个用于强化学习的紧凑状态，并且在线只更新一个小型 actor-critic。它在高精度任务上的收益很直接：最困难阶段的执行速度最高提升 3×，螺丝插入成功率在几分钟到几小时的练习后从 20% 提升到 65%。GazeVLA 从另一个方向处理同样的数据瓶颈。它把人类注视作为意图信号，在超过 1.5 亿帧第一人称视角数据上进行预训练，并且报告了更强的小样本迁移能力，每个任务只用 10 条机器人轨迹和 50 条人类轨迹，其中简单抓取放置任务成功率达到 85%，螺丝拧紧任务相对 pi0.5 有 2× 提升。

#### Evidence
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): RL Token 方法和真实机器人收益
- [GazeVLA: Learning Human Intention for Robotic Manipulation](../Inbox/2026-04-24--gazevla-learning-human-intention-for-robotic-manipulation.md): GazeVLA 的意图迁移和小样本结果

### 评估基础设施被当作核心研究对象
评估正在更接近部署约束。dWorldEval 把策略评估视为动作条件下的未来预测，把语言、图像和机器人动作放进同一个 token 空间。它的代理评分与真实执行结果高度一致，在 LIBERO、RoboTwin 和真实世界任务上的相关性约为 0.91 到 0.93。同一篇论文还报告了比以往评估器更好的动作可控性，以及更低的长时程漂移。配套的 VLA 数据与基准综述进一步说明了这一点为何重要：当前基准仍然难以把任务复杂度和环境结构区分开，也没有充分测试组合泛化和长时程推理。

#### Evidence
- [dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model](../Inbox/2026-04-24--dworldeval-scalable-robotic-policy-evaluation-via-discrete-diffusion-world-model.md): dWorldEval 代理评估指标及其与真实执行的相关性
- [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](../Inbox/2026-04-24--vision-language-action-in-robotics-a-survey-of-datasets-benchmarks-and-data-engines.md): 关于基准和数据缺口的综述证据

### 安全研究开始针对场景级物理失效模式
安全测试正在变得更偏重物理场景，也更针对具体模型。RedVLA 保持任务指令不变，在场景中加入一个风险物体，然后细化它的位置来触发不安全行为。在六个 VLA 模型上，平均攻击成功率为 64.9% 到 95.5%，其中“累积性危险物品误用”这一项在六个模型上的攻击成功率都是 100%。论文还报告，在这种设置下，更强的基础策略反而可能更容易被利用；而一个基于 RedVLA 数据训练的轻量级防护器，在只带来较小任务代价的情况下，把在线攻击成功率降低了 59.5%。这让安全评估更像是围绕真实机器人运动进行对抗式场景设计，而不是做提示词过滤。

#### Evidence
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): 物理红队测试设置、脆弱性比例和防护器结果

### 长时程 VLA 加入持久状态和规划器逻辑
长时程机器人控制正在加入更明确的记忆和任务结构。CodeGraphVLP 构建持久语义图，调用一次 LLM 写出任务专用规划器，然后只把相关物体的掩码视图送给执行器 VLA。在三个真实世界桌面任务上，它报告的平均成功率为 81.7%，高于 Gr00T N1.5 + Multi-frame 的 56.7% 和 π0 的 30.0%。它的机制很直接：更早的观测会作为图状态保留下来，进度检查写在代码里，执行策略在每一步看到的杂乱信息更少。

#### Evidence
- [CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models](../Inbox/2026-04-24--codegraphvlp-code-as-planner-meets-semantic-graph-state-for-non-markovian-vision-language-action-models.md): 语义图规划器设计和真实世界任务结果
