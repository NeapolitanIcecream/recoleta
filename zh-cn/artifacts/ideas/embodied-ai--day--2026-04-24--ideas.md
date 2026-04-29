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
机器人学习正在走向支持真实部署的工具和工作流：在冻结 VLA 之上做快速在线修正、在 rollout 前进行场景级物理安全测试，以及用与真实执行足够接近的离线策略排序来减少昂贵的机器人运行。这组工作里最有力的案例都对应明确的操作瓶颈：接触密集型末端阶段、有效场景中的风险发现，以及多种策略变体带来的评估成本。

## 面向精密末端阶段的冻结 VLA 在线适配
对 VLA 团队来说，一个务实的部署步骤是加入只学习最后一段修正的在线适配头。RL Token 保持预训练模型冻结，暴露一个紧凑状态，并训练一个小型 actor-critic，在真实机器人练习时调整参考动作块。论文报告的收益正好落在阻碍生产落地的操作环节：拧螺丝、插入充电器、插入以太网线和扎紧束线带这些任务，都能在数分钟到数小时的在线训练后改进，在最难阶段执行速度最高提升 3×，螺丝插入成功率从 20% 提高到 65%。

这指向了一套可实施的工作流，适合那些已经有一个总体能力不错、但在接触密集型末端动作上速度慢或可靠性不足的 VLA 策略集成团队。这里的产品不是新的基础模型，而是一层很薄的适配层，包含任务局部奖励、对基础策略的动作正则化，以及在目标工位上的快速练习循环。一个低成本的验证方法是，选一个当前需要操作员反复重试或远程操控的精密瓶颈环节，冻结基础 VLA，测量一个小型在线头是否能在一个班次内降低节拍时间或失败率。

### Evidence
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): 报告了基于冻结 VLA 的真实机器人在线适配，执行速度最高提升 3×，且螺丝插入成功率在数分钟到数小时后从 20% 提高到 65%。
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): 摘要确认，该方法是在预训练 VLA 上进行轻量级在线强化学习微调的路径，只需要数小时真实世界练习。

## 机器人部署前的场景级物理红队测试
机器人团队需要一种部署前安全测试，扰动的是场景，而不只是提示词。RedVLA 固定任务指令，加入一个风险物体，并围绕机器人最可能的交互路径细化其放置位置，直到出现不安全行为。在六个 VLA 模型上，平均攻击成功率介于 64.9% 到 95.5% 之间，而“危险物品误用”的累积型场景在六个模型上都达到 100% 攻击成功率。同一篇论文还报告，一个用这些生成案例训练出的轻量级防护器，能在任务代价较小的情况下把在线攻击成功率降低 59.5%。

这支持为实验室和向家庭、仓库或工业单元交付操作策略的产品团队提供一项具体的评估服务。工作流很直接：先记录某个任务的正常轨迹，在移动、抓取和振动区域附近生成场景级危险物放置方案，再用得到的失败案例同时评估策略并训练运行时检测器。一个低成本的初步检查是，拿一个现有基准任务或内部演示，加入一个放置位置可控的危险物体，看看策略能否在避开新危险的同时保持任务成功。

### Evidence
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): 提供了六个 VLA 模型上的场景级物理红队测试结果，包括最高 95.5% 的攻击成功率，以及危险物品误用场景中 100% 的攻击成功率。
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): 摘要说明，RedVLA 用于在部署前发现物理安全风险，并提出了一个基于生成数据构建的轻量级防护器。

## 基于动作条件世界模型评估的离线策略排序
策略评估已经接近成为团队可用的工具，可以在昂贵 rollout 之前对机器人策略进行排序。dWorldEval 把语言、图像和机器人动作放进同一个 token 空间，预测未来观测和任务进度，再用这个模型估计成功率。它的代理分数与真实执行高度相关，论文报告在 LIBERO 上 Pearson r 为 0.910，在 RoboTwin 上为 0.927，在真实世界任务上为 0.918。论文还显示，它的长时程漂移低于以往评估器。关于 VLA 数据集和基准的综述则补充了这件事在运营层面的原因：当前基准设计仍然不一致，导致策略比较很难完全可信，尤其是在组合泛化和长时程任务上。

这为一个用于模型选择和回归测试的离线评估工具链留下了空间。近期用户会是已经训练了多个策略变体、但承担不起在每个环境或硬件配置上都实际运行一遍的机器人团队。一个有用的第一版产品，可以接收候选策略的任务描述、观测轨迹和动作块，然后输出排序后的候选短名单，以及仍然需要真实执行来裁决的分歧案例。第一个检查很简单：把这个工具链的排序结果与少量任务上的小规模真实世界对比测试进行比较，看排序是否足够稳定，从而减少 rollout 数量。

### Evidence
- [dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model](../Inbox/2026-04-24--dworldeval-scalable-robotic-policy-evaluation-via-discrete-diffusion-world-model.md): 报告了以动作为条件的世界模型评估，其结果在 LIBERO、RoboTwin 和真实世界任务上都与真实执行高度相关，并且长时程漂移更低。
- [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](../Inbox/2026-04-24--vision-language-action-in-robotics-a-survey-of-datasets-benchmarks-and-data-engines.md): 综述指出了组合泛化和长时程推理方面的基准缺口，这支持了对更可靠评估工作流的需求。
