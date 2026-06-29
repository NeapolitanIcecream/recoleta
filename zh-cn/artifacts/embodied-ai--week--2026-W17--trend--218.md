---
kind: trend
trend_doc_id: 218
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- robotics
- vision-language-action
- contact-rich manipulation
- world models
- evaluation
- safety
- adaptation
run_id: materialize-outputs
aliases:
- recoleta-trend-218
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/contact-rich-manipulation
- topic/world-models
- topic/evaluation
- topic/safety
- topic/adaptation
language_code: zh-CN
---

# 本周机器人研究聚焦于能够恢复、适应并保持贴近真实执行的控制

## Overview
本周的机器人研究集中在真实任务压力下的执行质量。最强的一批论文把控制状态显式化，在接触时刻加入物理反馈，并用以动作为基础的评估来判断进展。与最近几周相比，这份简报对部署条件写得更具体：恢复、干预、安全和小数据适应都被当作核心方法选择，而不是附带分析。

## Clusters

### 结构化执行与纠错
本周的论文继续在动作循环内部加入显式结构。记忆、子任务规划、理由监督、干预信号和恢复逻辑都被当作一等控制要素。重点很实际：更长程的任务需要策略能够暴露状态、接受纠正，并在出错后恢复执行。

#### Evidence
- [AnchorRefine: Synergy-Manipulation Based on Trajectory Anchor and Residual Refinement for Vision-Language-Action Models](../Inbox/2026-04-20--anchorrefine-synergy-manipulation-based-on-trajectory-anchor-and-residual-refinement-for-vision-language-action-models.md)

### 接触时刻控制与物理反馈
高接触操作是一个明确的重心。多篇论文将更好的结果与触觉、力矩或视觉-触觉反馈联系起来，还有一篇报告称，加入物理反馈后，接触密集任务的平均成功率接近翻倍。另一篇把接近阶段和接触阶段拆成两个独立的行为阶段，这说明精细控制正在围绕接触发生的时刻来组织。

#### Evidence
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md)

### 以执行为基础的评估与安全
评估现在更贴近可执行行为。世界模型的判断标准不再只是预测质量，还看它们是否保留与任务相关的结构、是否能帮助真实动作执行。同一周里，安全范围也写得更明确：物理安全测试、基准局限性以及一篇广泛的 VLA 安全综述，与新的控制方法一起出现。

#### Evidence
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md)
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md)
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md)
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md)
- [dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model](../Inbox/2026-04-24--dworldeval-scalable-robotic-policy-evaluation-via-discrete-diffusion-world-model.md)
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md)

### 面向部署的训练与适应
训练与适应类论文面向部署条件。反复出现的判断是：当训练数据更像真实机器人的经验、并且后训练能在小数据预算下保住指令跟随能力时，机器人性能会更好。跨 embodiment 迁移和在线适应仍然活跃，但更强的信号是，作者正把这些提升与真实机器人或部署式测试直接挂钩。

#### Evidence
- [JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy](../Inbox/2026-04-22--joyai-ra-0-1-a-foundation-model-for-robotic-autonomy.md)
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md)
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md)
- [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](../Inbox/2026-04-24--vision-language-action-in-robotics-a-survey-of-datasets-benchmarks-and-data-engines.md)
- [Can Explicit Physical Feasibility Benefit VLA Learning? An Empirical Study](../Inbox/2026-04-20--can-explicit-physical-feasibility-benefit-vla-learning-an-empirical-study.md)
- [Cortex 2.0: Grounding World Models in Real-World Industrial Deployment](../Inbox/2026-04-22--cortex-2-0-grounding-world-models-in-real-world-industrial-deployment.md)
