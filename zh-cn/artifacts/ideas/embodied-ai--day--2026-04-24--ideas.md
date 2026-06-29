---
kind: ideas
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- evaluation
- safety
- online-rl
- long-horizon-planning
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/evaluation
- topic/safety
- topic/online-rl
- topic/long-horizon-planning
language_code: zh-CN
---

# 面向部署的机器人学习

## Summary
机器人学习工作正在转向支持真实部署的工具和工作流：冻结 VLA 上的快速在线纠正、上线前的场景级物理安全测试，以及能足够贴近真实执行的离线策略排序，从而减少昂贵的机器人运行。这个集合里最强的案例都对准了具体的操作瓶颈：接触密集的末端阶段、有效场景中的风险发现，以及多个策略变体下的评测成本。

## 冻结 VLA 的在线适配，用于精度末端阶段
VLA 团队一个实用的部署步骤是加一个只学习最后一段修正的在线适配头。RL Token 把预训练模型冻结，暴露一个紧凑状态，并训练一个小型 actor-critic，在真实机器人练习中调整参考动作块。报告中的收益对应的是阻碍量产的那一段操作：螺丝安装、充电器插入、以太网插入和扎带固定都在几分钟到几小时的在线训练后得到提升，最难阶段的执行速度最高快 3 倍，螺丝插入成功率从 20% 提升到 65%。

这说明，已经有一个大体能用、但在接触密集的末端环节速度慢或不稳定的 VLA 策略时，可以做出一套可落地的工作流。产品不是新的基础模型，而是一层很薄的适配层，带任务局部奖励、相对于基础策略的动作正则化，以及在目标工位上的快速练习循环。一个成本低的验证方法是，挑一个当前需要操作员反复重试或远程操控的精度瓶颈，冻结基础 VLA，测一个小型在线头能否在一个班次内压低节拍时间或失败率。

### Evidence
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): Reports real-robot online adaptation with a frozen VLA, up to 3× faster execution, and screw insertion improvement from 20% to 65% after minutes to a few hours.
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): Abstract confirms the method is a lightweight online RL fine-tuning path for pretrained VLAs using only a few hours of real-world practice.

## 机器人部署前的场景级物理红队测试
机器人团队需要的是部署前的安全测试，改的是场景，不只是提示词。RedVLA 固定任务指令，加入一个风险物体，然后围绕机器人最可能接触的路径调整它的位置，直到出现不安全行为。六个 VLA 模型上，平均攻击成功率在 64.9% 到 95.5% 之间，累积型危险物品误用在全部六个模型上都达到 100% 攻击成功。论文还报告，用这些生成样本训练出的轻量防护器把在线攻击成功率降低了 59.5%，对任务性能的影响很小。

这支持给实验室和产品团队提供一项具体的评测服务，面向把操作策略发往家庭、仓库或工业工位的场景。流程很直接：先记录一个任务的无害轨迹，再在通行区、抓取区和振动区附近生成场景级危险物摆放，然后用得到的失败案例同时给策略打分并训练运行时检测器。一个低成本的初步检查是，拿一个已有基准任务或内部演示，加一个位置可控的危险物体，看看策略能否在保持任务成功的同时避开新风险。

### Evidence
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): Provides scene-level physical red teaming results across six VLA models, including attack success rates up to 95.5% and 100% attack success for dangerous item misuse scenarios.
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): Abstract states RedVLA is designed to detect physical safety risks before deployment and introduces a lightweight guard built from generated data.

## 用动作驱动的世界模型做离线策略排序
策略评测已经接近一个能在昂贵全量 rollout 前给机器人策略排序的工具。dWorldEval 把语言、图像和机器人动作映射到同一个 token 空间，同时预测未来观测和任务进度，然后用这个模型估计成功率。它的代理分数和真实执行很接近，报告中的 Pearson r 在 LIBERO 上是 0.910，在 RoboTwin 上是 0.927，在真实世界任务上是 0.918。论文还显示，它比先前评测器在长时程上的漂移更小。VLA 数据集和基准的综述补充了这件事为什么重要：基准设计仍然不一致，尤其是在组合泛化和长时程任务上，策略比较很难让人放心。

这给离线评测框架留下了空间，可以用于模型选择和回归测试。短期用户是已经训练多个策略变体、又负担不起把每个变体都跑遍每个环境或硬件配置的机器人团队。一个有用的第一版产品会接收任务描述、观测轨迹和候选策略的动作块，然后输出一个排序后的候选列表，以及仍然需要真实执行来裁决的分歧样本。最直接的检查是，把这个框架的排序结果和少量真实世界对比测试做对照，看排序是否稳定到足以减少 rollout 数量。

### Evidence
- [dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model](../Inbox/2026-04-24--dworldeval-scalable-robotic-policy-evaluation-via-discrete-diffusion-world-model.md): Reports action-grounded world-model evaluation with strong correlation to real execution across LIBERO, RoboTwin, and real-world tasks, plus lower long-horizon drift.
- [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](../Inbox/2026-04-24--vision-language-action-in-robotics-a-survey-of-datasets-benchmarks-and-data-engines.md): Survey documents benchmark gaps in compositional generalization and long-horizon reasoning, which supports demand for a more reliable evaluation workflow.
