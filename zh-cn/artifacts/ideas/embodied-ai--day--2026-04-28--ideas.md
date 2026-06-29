---
kind: ideas
granularity: day
period_start: '2026-04-28T00:00:00'
period_end: '2026-04-29T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- photorealistic simulation
- 3D Gaussian Splatting
- dexterous manipulation
- contact-rich robotics
tags:
- recoleta/ideas
- topic/robot-learning
- topic/photorealistic-simulation
- topic/3d-gaussian-splatting
- topic/dexterous-manipulation
- topic/contact-rich-robotics
language_code: zh-CN
---

# Contact-ready manipulation training

## Summary
有两项实用改动很明确：在长时间视觉 RL 运行前先验证真实采集的仿真场景；按灵巧抓取为下一步动作留下了哪些手指来打分。这两项都在解决同一种训练时间浪费来源：策略在接触前看起来稳定，一到需要物理执行就失败。

## Capture-to-simulation checks for contact-rich visual RL scenes
训练相机条件操作策略的机器人团队，可以在长时间 RL 运行前加一个短验证步骤：采集 RGB 视图，用网格、位姿、尺度和碰撞元素生成 3DGS 资产，然后运行固定的接触测试和渲染图像吞吐量测试。

GS-Playground 把这套流程做成了具体实现。它的 Real2Sim 管线把 RGB 采集转成可用于仿真的场景部件，渲染器把高斯资产绑定到刚体上，让渲染对象在接触过程中跟着物理状态移动。报告的规模已经足够做实用的冒烟测试：在 RTX 4090 级配置上，640×480 分辨率下 3DGS 渲染约 10,000 FPS；在这个分辨率下最多可渲染 2048 个场景；高斯裁剪超过 90%，PSNR 损失低于 0.05。

一个实用的首个版本，是给操作实验室做一个场景接入脚本：接收采集到的物体集合，生成视觉和碰撞资产，裁剪高斯，然后运行少量推、堆叠或抓取操作，同时检查图像质量、刚体绑定、接触稳定性和 GPU 内存。没通过这些检查的场景，可以在占用 RL 训练时间前先修好。

### Evidence
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): Summarizes GS-Playground's batched 3DGS renderer, Real2Sim pipeline, rigid-body Gaussian binding, rendering throughput, pruning result, and contact-oriented physics details.
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): Describes the bottleneck in high-resolution rendering, out-of-memory failures, and the manual work of creating simulation-ready assets.
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): States that the workflow converts real-world scenes into functional digital twins with visual realism and physical consistency.

## Finger reservation tests for two-step LEAP Hand tasks
做多指手部策略的团队，可以加一个抓取评估，测量第一个物体被握住后还有哪些手指能继续使用。测试很直接：训练或采样第一阶段抓取，标记分配给被握物体的手指，对为下一步动作保留的手指施加力惩罚，然后把每个抓取当作第二个任务的起始状态来评估。

HANDFUL 说明了这件事为什么重要，适用于清理桌面和整理工作区这类任务：手先握住一个物体，再去按按钮、拉抽屉、拧旋钮，或拿起另一个物体。在仿真中，这个方法在 Push Object 上达到 69.90% 成功率，在 Press Button 上达到 77.75%，在 Twist Knob 上达到 61.52%，在 Pull Drawer 上达到 78.94%，在 Pick Second 上达到 76.54%。去掉手指约束后，Pick Second 掉到 0.00%，其他几个任务也明显下降。

一个实用的改动，是把第一阶段抓取当作任务序列候选项，只保留能支持下一步动作的那些。HANDFUL 的课程训练在把第二阶段训练从 9000 万步降到 5400 万步的同时，保持了接近的最终成功率，这给团队提供了一个明确的训练预算检查点。

### Evidence
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Summarizes the two-step task setup, finger-level contact rewards and penalties, curriculum, simulation success rates, and ablation results.
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Explains the failure mode where stable grasps occupy fingers or contact regions needed for later actions.
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Describes preserving unused fingers and contact regions, selecting grasps for downstream subtasks, and the LEAP Hand benchmark tasks.
