---
kind: trend
trend_doc_id: 481
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- reinforcement learning
- robot deployment
- adversarial reliability
run_id: materialize-outputs
aliases:
- recoleta-trend-481
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/reinforcement-learning
- topic/robot-deployment
- topic/adversarial-reliability
language_code: zh-CN
---

# 机器人学习工作集中在可部署控制和可测失败模式上

## Overview
当天最强的信号是实用机器人控制。视觉-语言-动作（VLA）工作把快速的真实机器人微调和动作空间几何结合起来，世界模型论文则收紧潜在规划和策略搜索。EXPO-FT、OASIS 和 MBDPO 提供了主要的实证结果；部署和对抗研究补充了可靠性检查。

## Clusters

### VLA 操作微调
VLA 操作论文更看重真实执行指标。EXPO-FT 保留一个预训练的 π0.5 策略，并用离策略强化学习训练一个轻量编辑策略。它报告在 8 个真实世界操作任务上，每个任务都达到 30/30 的最终成功率，平均只用了 19.1 分钟的在线机器人数据。

OASIS 直接处理动作解码问题。它先预测一个 8 步的 SE(3) 末端执行器轨迹，也就是三维位置和旋转，再生成 6-DoF 动作和夹爪指令。论文报告在 LIBERO 上平均成功率为 97.6%，在 Franka Research 3 和 Kinova Gen3 机器人上的真实世界测试平均成功率为 89.2%。

#### Evidence
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): EXPO-FT summary gives the pretrained VLA fine-tuning setup, 8 real-world tasks, 30/30 success, and 19.1 minutes of online data.
- [OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation](../Inbox/2026-05-25--oasis-observation-action-space-alignment-via-se-3-trajectory-prediction-for-robotic-manipulation.md): OASIS summary gives the SE(3) trajectory predictor, action-chunk decoder, LIBERO score, and real-robot success rate.

### 工厂部署和攻击检查
部署证据更偏向操作流程，而不是结构设计。西门子工厂车间案例研究把 Pi0.5 微调到透明配件袋包装任务上，使用了 2,535 个 episode 和大约 10 小时的数据。它的失败分解很具体：在无约束试验中，袋内物品留在产品上方占失败 episode 的 65%，多袋抓取占 23%，抓取不佳或抓取失败占 15%。

另一篇 VLA 可靠性论文给出了能力和对抗可靠性的一个信息论上界。它引用 OpenVLA-7B 在 16/255 的 PGD 图像攻击下，LIBERO 成功率从 95% 以上降到 5% 以下，然后在覆盖高斯代理、OpenVLA、LIBERO 套件、攻击类型、最长到 10 步的时域，以及两种动作头设计的 320 个单元上验证了这个上界，没有出现违反。

#### Evidence
- [A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons](../Inbox/2026-05-25--a-factory-floor-deployment-case-study-of-vla-pipelines-for-industrial-packaging-task-workflow-failures-and-lessons.md): Factory case summary provides the Pi0.5 packaging task, dataset size, training workflow, and failure-rate breakdown.
- [Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models](../Inbox/2026-05-25--capability-and-robustness-cannot-both-be-free-an-information-theoretic-bound-for-vision-language-action-models.md): Reliability-bound summary provides the OpenVLA attack example, formal bound scope, and 320-cell validation result.

### 世界模型控制
世界模型论文关注能支持规划和策略改进的状态表示。TC-WM 把冻结的视觉基础特征和本体感觉压缩成任务中心潜变量，然后训练带动作条件的动力学模型，用于规划或强化学习。报告覆盖 9 个基准，跨 Robomimic、D4RL、导航、运动控制、操作，以及模拟和真实世界设置，不过摘要没有给出具体分数表。

MBDPO 在潜在世界模型中训练扩散动作策略，因此想象 rollout 和执行时使用的是同一个策略分布。它最强的数值结论来自规模和覆盖面：模型参数从 1.7M 增长到 340M，在线实验覆盖 4 个基准套件和 121 个任务，8 个任务的漂移研究显示它的动作漂移低于 TD-MPC2。

LeJEPA 补充了一个学习到的表示在什么条件下能充当可用世界模型的理论。在线性高斯潜变量和平稳加性噪声正样本对下，最优解会把潜在状态恢复到一个正交变换下的等价形式。论文还说明，当代价对这类变换不变时，这种恢复如何和有限时域规划联系起来。

#### Evidence
- [Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations](../Inbox/2026-05-25--back-to-parsimonious-latents-learning-task-centric-world-models-from-visual-foundations.md): TC-WM summary gives the compact latent design, planning uses, benchmark coverage, and missing exact metric caveat.
- [Scaling World-Model Reinforcement Learning Through Diffusion Policy Optimization](../Inbox/2026-05-25--scaling-world-model-reinforcement-learning-through-diffusion-policy-optimization.md): MBDPO summary gives the diffusion policy inside a world model, scaling range, benchmark breadth, and action-drift comparison.
- [When Does LeJEPA Learn a World Model?](../Inbox/2026-05-25--when-does-lejepa-learn-a-world-model.md): LeJEPA summary gives the Gaussian identifiability conditions, theorem statements, and planning link.
