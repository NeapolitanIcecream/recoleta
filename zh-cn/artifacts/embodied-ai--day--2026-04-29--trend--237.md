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

# Geometry enters the control loop for robot policies

## 概览
这一天的机器人工作把几何放进了执行回路。STARRY 和 X-WAM 把未来 RGB-D 预测和动作扩散联系起来，并在操作基准上报告了提升。一篇关于具身 3D 生成的综述说明了这类工作的资产要求，而户外导航研究则在真实街道上测试了语言落地的辅助能力。

## 研究发现

### World-action models for manipulation
Vision-Language-Action（VLA）策略正在围绕预测的 3D 结构和未来接触来构建。STARRY 将未来的时空潜变量和动作联合去噪，然后用预测深度和末端执行器几何来把注意力偏向把手、开口、接触面和附近障碍物。它在 50 个 RoboTwin 2.0 双臂任务上报告了 93.82% 的 clean 成功率和 93.30% 的 randomized 成功率，在真实 ARX R5 实验中，3 个任务的平均成功率为 70.8%。

X-WAM 走的是更宽的 world-action 路线。它在一个扩散模型里同时预测多视角 RGB-D 视频、机器人状态和 32 个未来动作。它的异步去噪调度让动作比视频用更少步数解码，这对闭环控制很重要。论文报告了 RoboCasa 上 79.2% 的平均成功率，以及 RoboTwin 2.0 Randomized 上 90.7% 的成功率，同时也评估了视觉和几何预测指标。

#### 资料来源
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): STARRY summary, method, and benchmark results for joint world prediction and action generation.
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): X-WAM summary, asynchronous denoising method, and RoboCasa/RoboTwin results.

### Simulation-ready 3D generation
这篇 3D 生成综述给具身 AI 资产设定了一个实用门槛。生成的物体和场景需要有效几何、物理参数、可执行的运动学，以及与模拟器兼容的文件。这意味着关节、质量、摩擦、材料行为、碰撞几何，以及 URDF、MJCF 和 USD 这类格式和外观一样重要。

综述把 3D 生成分成物体资产生成、交互式仿真环境和 sim-to-real 支持。它还比较了 MuJoCo、Isaac Sim、Habitat、AI2-THOR、OmniGibson、PyBullet、ManiSkill3 和 Genesis 等主要仿真平台。开放问题很具体：物理标注不足、视觉质量和物理有效性之间一致性弱、评估分散，以及 sim-to-real 差距。

#### 资料来源
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): Survey summary with simulation-readiness criteria, taxonomy, platform comparison, and bottlenecks.

### Outdoor language-grounded social navigation
Walk With Me 把语言条件机器人扩展到长距离户外路线。系统用 GPS 上下文和公共地图兴趣点把抽象请求映射到具体目的地，然后查询步行路线 API，把路线转成航点。一个 Vision-Language Model（VLM）负责目的地落地和安全推理，底层 VLA 策略预测局部运动。

证据主要来自真实系统演示。评估覆盖 Athena 2.0 Pro 机器人上的 20 次户外试验，场景包括末端配送和盲人引导。论文声称可以在公里级范围运行，但现有摘要没有给出成功率、碰撞率、路径长度分布、完成时间或完整系统的基线对比。

#### 资料来源
- [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](../Inbox/2026-04-29--walk-with-me-long-horizon-social-navigation-for-human-centric-outdoor-assistance.md): Walk With Me summary, system design, trial setup, and missing quantitative metrics.
