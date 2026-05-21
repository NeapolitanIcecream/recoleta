---
kind: trend
trend_doc_id: 237
granularity: day
period_start: '2026-04-29T00:00:00'
period_end: '2026-04-30T00:00:00'
topics:
- robotics
- world models
- Vision-Language-Action
- 3D generation
- simulation
- social navigation
run_id: materialize-outputs
aliases:
- recoleta-trend-237
tags:
- recoleta/trend
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/3d-generation
- topic/simulation
- topic/social-navigation
language_code: zh-CN
---

# 几何进入机器人策略的控制回路

## Overview
当天的机器人研究把几何纳入执行过程。STARRY 和 X-WAM 将未来 RGB-D 预测与动作扩散相连，并报告了操作基准上的提升。一篇关于具身 3D 生成的综述说明了这类工作的资产要求，户外导航研究则在真实街道中测试基于语言落地的辅助能力。

## Clusters

### 用于操作的世界-动作模型
Vision-Language-Action (VLA) 策略正在围绕预测的 3D 结构和未来接触来构建。STARRY 联合去噪未来时空潜变量和动作，然后使用预测深度和末端执行器几何，让注意力偏向把手、开口、接触表面和附近障碍物。它在 50 个 RoboTwin 2.0 双臂任务上报告了 93.82% 的 Clean 成功率和 93.30% 的 Randomized 成功率；在真实 ARX R5 实验中，三个任务的平均成功率为 70.8%。

X-WAM 采用更宽的世界-动作建模路线。它在一个扩散模型中预测多视角 RGB-D 视频、机器人状态和 32 个未来动作。它的异步去噪调度让动作能用比视频更少的步数解码，这对闭环控制有实际意义。论文报告 RoboCasa 平均成功率为 79.2%，RoboTwin 2.0 Randomized 成功率为 90.7%，同时评估视觉和几何预测指标。

#### Evidence
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): STARRY 关于联合世界预测和动作生成的摘要、方法和基准结果。
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): X-WAM 摘要、异步去噪方法，以及 RoboCasa/RoboTwin 结果。

### 面向仿真的 3D 生成
这篇 3D 生成综述为具身 AI 资产设定了实用门槛。生成的物体和场景需要有效几何、物理参数、可执行运动学，以及与仿真器兼容的文件。这意味着关节、质量、摩擦、材料行为、碰撞几何，以及 URDF、MJCF、USD 等格式，和外观同样重要。

该综述把 3D 生成划分为物体资产生成、交互式仿真环境和 sim-to-real 支持。它还比较了 MuJoCo、Isaac Sim、Habitat、AI2-THOR、OmniGibson、PyBullet、ManiSkill3 和 Genesis 等主要仿真平台。开放问题很具体：物理标注有限、视觉质量和物理有效性之间的一致性弱、评估分散，以及 sim-to-real 差距。

#### Evidence
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): 综述摘要，涵盖仿真就绪标准、分类、平台比较和瓶颈。

### 基于语言落地的户外社交导航
Walk With Me 将语言条件机器人扩展到长距离户外路线。系统使用 GPS 上下文和公共地图兴趣点，把抽象请求映射到具体目的地，然后查询步行路线 API，并把路线转换为航点。Vision-Language Model (VLM) 负责目的地落地和安全推理，低层 VLA 策略预测局部运动。

证据主要来自真实世界系统演示。评估在 Athena 2.0 Pro 机器人上进行，覆盖最后一公里配送和盲人引导场景，共 20 次户外试验。论文声称支持公里级运行，但现有摘要没有给出成功率、碰撞率、路径长度分布、完成时间或全系统基线比较。

#### Evidence
- [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](../Inbox/2026-04-29--walk-with-me-long-horizon-social-navigation-for-human-centric-outdoor-assistance.md): Walk With Me 摘要、系统设计、试验设置和缺失的定量指标。
