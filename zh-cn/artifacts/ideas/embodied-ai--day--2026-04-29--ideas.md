---
kind: ideas
granularity: day
period_start: '2026-04-29T00:00:00'
period_end: '2026-04-30T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- world models
- Vision-Language-Action
- 3D generation
- simulation
- social navigation
tags:
- recoleta/ideas
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/3d-generation
- topic/simulation
- topic/social-navigation
language_code: zh-CN
---

# Geometry Checks for Robot Training

## Summary
机器人操作工作现在给了团队一个具体办法来测试预测几何是否改善执行：在策略评估中加入 RGB-D 未来预测、末端执行器几何和接触区域检查。相关的 3D 生成工作则给仿真团队指明了一个实用的资产门槛：生成对象在可用于机器人训练前，需要有关节、物理参数、碰撞几何和兼容模拟器的文件。面向户外、语言引导的导航很有前景，但现有证据主要支持一套带完整安全与完成日志的实地测试流程。

## Contact-region evaluation for RGB-D manipulation policies
操作团队应在 VLA 策略测试中增加一个接触区域评估切片。适合的测试用例是那些 3D 误差很小也会改变结果的任务：用把手挂杯子、递交、按压工具、把物体穿过开口放入，以及在障碍物附近移动。评估应记录成功率、碰撞、抓取失败、接触点误差、末端执行器间隙，以及模型是否关注了控制动作的物体区域。

STARRY 提供了一个可以直接参考和测试的设计。它预测未来深度和末端执行器位置，将预测深度反投影到 3D，计算 token 到预测末端执行器的距离，并用这些距离给 action-to-video 注意力加权。论文报告，在 50 个 RoboTwin 2.0 双臂任务上，clean 平均成功率为 93.82%，randomized 平均成功率为 93.30%；在真实 ARX R5 双臂实验中，使用每个任务 50 个示范和每种方法 20 次评估 rollout，平均成功率为 70.8%。它带来的最大价值是失败分析：当策略漏掉把手或在开口附近发生碰撞时，团队可以先检查预测深度、末端执行器轨迹和注意力权重，再继续采集更多示范。

### Evidence
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): Describes STARRY’s future depth and end-effector geometry, GASAM attention weighting, benchmark results, and real ARX R5 evaluation.
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): Names contact-sensitive manipulation examples and the failure modes caused by local geometry errors.

## Action-first denoising latency test for world-action policies
把视频扩散模型改造成机器人控制模型的团队，应做一个让动作解码早于视频的延迟测试。测试很简单：训练或微调一个同时预测未来 RGB-D 帧、机器人状态和一段未来动作的模型，然后在不同的动作和视频去噪预算下比较控制延迟和任务成功率。通过标准很实用，不是看图效果：机器人必须足够快地输出动作，才能做闭环控制，同时深度和视频预测还要足够好，能用于调试和规划。

X-WAM 是一个可参考的实现。它在多视角机器人数据上微调 Wan2.2-TI2V-5B，预测 8 帧未来 RGB 图像、8 个未来状态和 32 个未来动作，并且在不把 token 序列翻倍的情况下增加了一个深度分支。它的 Asynchronous Noise Sampling 让视频和动作的噪声水平从耦合分布中采样，这样推理时动作可以用更少的去噪步数。论文报告的结果包括：RoboCasa 的 24 个任务上平均成功率 79.2%，RoboTwin 2.0 Randomized 上 90.7%。实验室即使不做同等规模，也可以复现最相关的部分：在降低动作去噪预算时，测量每个动作的毫秒数、成功率和几何预测质量。

### Evidence
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): Describes X-WAM’s multi-view RGB-D, state, and action prediction setup, asynchronous denoising, training scale, and benchmark results.
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): States that X-WAM predicts multi-view RGB-D futures and uses Asynchronous Noise Sampling for efficient action execution.

## Simulator import checks for generated robot-training assets
使用生成 3D 资产的仿真团队，应在资产进入机器人训练流程前加一道导入检查。这个检查应拒绝只有形状和纹理的对象。可用的生成资产需要有效的网格几何、碰撞几何、关节定义、关节限位、质量、摩擦、相关的材料行为，以及导出为 URDF、MJCF 或 USD 等格式。检查流程应在目标模拟器中加载资产，执行其关节，在物理环境下让它下落或被推，并确认这个文件能在团队的训练任务中复用。

这篇 3D 生成综述把采用障碍说得很清楚：视觉质量并不保证物理有效性。它把 simulation readiness 定义为几何、物理参数化、运动学可执行性和模拟器兼容性，并把生成内容接到 MuJoCo、Isaac Sim、Habitat、AI2-THOR、OmniGibson、PyBullet、ManiSkill3、Genesis，以及 URDF、MJCF 和 USD 这些引擎与格式上。这样一来，资产生成就成了机器人团队里一个可以测试的流程问题。一个小型校验脚本加一个模拟器冒烟测试，就能在策略训练消耗坏场景之前拦下很多失败。

### Evidence
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): Defines simulation-ready 3D generation requirements, including geometry, physical parameters, kinematics, and simulator compatibility.
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): Names URDF, MJCF, joint configurations, mass distributions, and friction coefficients as necessary for useful generated assets.
