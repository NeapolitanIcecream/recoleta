---
kind: trend
trend_doc_id: 704
granularity: day
period_start: '2026-06-23T00:00:00'
period_end: '2026-06-24T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- manipulation
- navigation
- synthetic data
- evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-704
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/manipulation
- topic/navigation
- topic/synthetic-data
- topic/evaluation
language_code: zh-CN
---

# 机器人 VLA 工作正在优先处理部署反馈、几何和世界模型评分

## Overview
这一时期的机器人论文集中讨论如何让视觉-语言-动作（VLA）策略在部署后可用。InSight 通过机器人 rollout 增加新的操作原语。Reflective VLA 记录动作后果。G3VLA 将相机校准注入视觉 token。共同重点是在新技能、新相机和不完美数据下获得可测量的行为。

## Clusters

### VLA 策略的部署反馈
InSight 将缺失的机器人技能视为可在初始示范集之后获取的原语。它把已有示范切分成带标签的动作，让视觉-语言模型提出缺失原语，收集成功的机器人 rollout，并重新训练策略。论文报告的真实 xArm 结果很具体：扭转成功率 92%，倒液成功率 96%，在没有端到端示范的 14 原语“先扭转再倒液”任务上成功率 80%。

Reflective VLA 加入了另一条反馈路径。它存储观察-动作-后果三元组，使策略能在部署期间推断相机几何、校准误差和执行偏差。在 LIBERO-Plus 上，它报告的平均成功率为 87.7%，匹配的反应式基线为 82.3%；列出的最大增益来自 Robot shift，成功率为 72.9%，基线为 50.0%。

#### Evidence
- [InSight: Self-Guided Skill Acquisition via Steerable VLAs](../Inbox/2026-06-23--insight-self-guided-skill-acquisition-via-steerable-vlas.md): InSight 摘要、方法，以及报告的仿真和真实机器人技能获取结果。
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA 摘要、动作-后果上下文设计，以及 LIBERO-Plus 结果。

### 用于操作的几何和接触信号
多篇论文在不替换基础策略的情况下，为机器人感知加入物理结构。GRA 只将生成的机器人视频用于 2D 末端执行器路点监督，然后在真实示范上训练动作。每个任务使用 25 个真实示范和 75 个生成视频时，它在三个 Franka 拾取放置任务上的平均成功率达到 68.9%，而真实数据同等预算基线为 61.1%。

G3VLA 通过射线嵌入、投影位置编码和跨视角融合，将相机校准写入 VLA 视觉 token。在使用 pi0 的 LIBERO 上，真值几何监督把平均成功率从 84.6% 提高到 88.1%。NoContactNoWorries 将同一实用思路扩展到灵巧手，通过腕部 RGB-D 和关节状态预测指尖接触。在真实 LEAP Hand 上，它在测试物体上的 F1 分数为 0.71 到 0.84。

#### Evidence
- [Supervise What Survives: Geometry-Guided VLA Adaptation from Synthetic Robot Videos](../Inbox/2026-06-23--supervise-what-survives-geometry-guided-vla-adaptation-from-synthetic-robot-videos.md): GRA 摘要、合成视频几何监督方法，以及 Franka 任务结果。
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA 摘要、相机校准 token 设计，以及 LIBERO/RoboCasa/RoboTwin 结果。
- [NoContactNoWorries: Estimating Contact through Vision and Proprioception for In-Hand Dexterous Manipulation](../Inbox/2026-06-23--nocontactnoworries-estimating-contact-through-vision-and-proprioception-for-in-hand-dexterous-manipulation.md): NoContactNoWorries 摘要、伪触觉接触预测设置，以及真实 LEAP Hand 分数。

### 作为进度评分器和规划器的世界模型
这一时期的世界模型工作与控制决策相关。World Value Models 使用预训练视频世界模型估计操作视频中的任务进度，包括犹豫和重试片段。新的 Suboptimal-Value-Bench 包含 3 种具身形态、15 个任务中的 800 条人工标注轨迹。WVM 报告的平均 Hesitation-RMSE 为 0.05，Retry-VOC 为 0.78，优于列出的价值模型基线。

NavWM 将未来预测用于视觉导航。它预测多条候选路径及这些路径对应的未来图像，然后把这种预见用于图像目标导航。在 Go Stanford、SCAND、RECON 和 HuRoN 上，它的平均轨迹误差从 UniWM 的 0.302 降至 0.207。未来帧 PSNR 达到 17.340，已见环境导航成功率从 66% 升至 72%。

#### Evidence
- [World Value Models for Robotic Manipulation](../Inbox/2026-06-23--world-value-models-for-robotic-manipulation.md): WVM 摘要、Suboptimal-Value-Bench 细节，以及价值估计结果。
- [NavWM: A Unified Navigation World Model for Foresight-Driven Planning](../Inbox/2026-06-23--navwm-a-unified-navigation-world-model-for-foresight-driven-planning.md): NavWM 摘要、候选轨迹和未来图像方法，以及导航指标。

### 机器人任务的步骤级评估
MANGO 针对 VLA 测试中的一个实际弱点：终态检查常常掩盖长时程任务失败的具体步骤。它从自然语言指令构建原子任务库，将打开、拾取、放置、关闭等步骤映射到仿真器检查，并使用 Generator、Assessor 和 Judge 智能体改进可执行 oracle。

证据更偏诊断性，而非大量基准结果。论文在 LIBERO_10 和 RoboCasa Humanoid Tabletop 上评估，并报告生成的 oracle 能检测出与手写符号 oracle 相近数量的失败，同时定位失败的原子步骤和顺序违规。可用摘录中没有精确率、召回率和运行时间数字。

#### Evidence
- [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](../Inbox/2026-06-23--mango-automated-multi-agent-test-oracle-generation-for-vision-language-action-models.md): MANGO 摘要、多智能体 oracle 生成方法，以及报告的基准覆盖范围。
