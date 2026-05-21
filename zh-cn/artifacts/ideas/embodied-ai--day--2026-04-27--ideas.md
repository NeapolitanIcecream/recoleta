---
kind: ideas
granularity: day
period_start: '2026-04-27T00:00:00'
period_end: '2026-04-28T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- vision-language-action
- robot manipulation
- coarse-to-fine control
- robot deployment
- human demonstrations
- edge safety
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/coarse-to-fine-control
- topic/robot-deployment
- topic/human-demonstrations
- topic/edge-safety
language_code: zh-CN
---

# 机器人 VLA 部署控制

## Summary
机器人 VLA 的采用正在变成控制回路工程问题。下一步有用工作是：在目标硬件上测量动作延迟，为延迟的云端航点增加边缘校正，并在机器人动作训练前通过意图级监督复用人类操作视频。

## VLA 操作策略的动作生成延迟基准
测试 VLA 操作策略的机器人团队应增加一个发布准入检查，在同一个操作套件上测量动作采样延迟、NFE、端到端观察-推理-执行时间和任务成功率。这个检查应在目标机器人计算机上运行，并在编译、缓存、采样器变更或动作头变更后重复运行。

CF-VLA 为这项测试提供了具体基线。它报告在 NFE=2 时 LIBERO 平均成功率为 96.5，动作采样延迟降低 75.4%，真实机器人实验平均成功率为 83.0。Libra-VLA 给出了相关实现方式：降低较重的语义规划器运行频率，把粗粒度意图存入 FIFO 缓冲区，并让动作细化器保持控制频率运行。硬件剖析论文说明了为什么这一步应纳入部署流程。对于 pi0，编译前测得的延迟从 RTX 4090 上的 102.3 ms，到 Jetson Thor 上的 246.0 ms，再到 AGX Orin 上的 920.6 ms；不同设备上的能耗和成本变化并不一致。

一个低成本验证可以做成两列对比：当前采样器对比粗到细或带缓冲的变体，同时记录成功率和延迟。若某个采样器节省了毫秒级时间，却降低了接触任务成功率，就不应通过准入检查。

### Evidence
- [CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies](../Inbox/2026-04-27--cf-vla-efficient-coarse-to-fine-action-generation-for-vision-language-action-policies.md): CF-VLA 报告了两步 NFE=2 采样器、LIBERO 成功率、动作采样延迟降低幅度和真实机器人成功率。
- [Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System](../Inbox/2026-04-27--libra-vla-achieving-learning-equilibrium-via-asynchronous-coarse-to-fine-dual-system.md): Libra-VLA 描述了粗粒度意图预测、连续细化，以及推理时的 FIFO 意图缓冲区。
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): 这项部署研究报告了 VLA 推理中的模型-硬件延迟、能耗和编译效果。

## 面向云端 VLA 导航的边缘航点重新对齐与 LiDAR 安全策略
运行云端 VLA 导航的团队应在延迟到达的航点和机器人控制器之间放置一个小型边缘适配器。该适配器需要带时间戳的位姿缓冲区、一个把过期航点映射到当前本体坐标系的 SE(2) 变换，以及一个使用校正后的前瞻点和 LiDAR 近距信息选择子目标的本地策略。

AsyncShield 是一个直接模板。它使用 5 个重新对齐的前瞻航点，间距为 0.2 m，并使用 144 个 LiDAR 近距值，然后应用带 LiDAR 安全成本的 PPO-Lagrangian 策略。在混合网络退化下，它报告成功率为 76.7%，横向跟踪误差为 0.725 m，风险暴露为 1.3%。移除时间对齐后，成功率降至 36.7%；移除安全约束后，跟踪误差较低，但安全性差。

第一次现场测试可以回放记录的云端 VLA 数据包，并注入延迟、抖动和丢包，让机器人在已建图的障碍物场地中行驶。通过条件应同时包含到达、横向跟踪误差和最小距离违规，因为航点过期时，贴近路径跟踪仍可能不安全。

### Evidence
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): AsyncShield 提供了位姿缓冲、SE(2) 重新对齐、LiDAR 策略、网络退化结果和消融实验。
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): 论文摘要说明了云到边缘的延迟问题和边缘校正机制。
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): 这篇 VLA 部署剖析论文把延迟描述为闭环机器人故障来源。

## 机器人动作微调前的人类视频意图预训练
机器人演示有限的操作团队应测试一个人类视频预训练阶段：在训练机器人动作头之前，先预测交互轨迹和手部运动意图。可迁移意图是有用单位：手往哪里移动、接触在哪里发生、物体交互如何展开。微调期间应避免机器人动作损失覆盖这种先验。

MoT-HRA 给出了最具体的做法。其 HA-2.2M 数据集来自 HowTo100M、Ego4D、EPIC-KITCHENS 和 Something-Something-V2，随后经过以手为中心的选择、MANO 风格姿态、深度对齐、时间分段和语言标注来过滤和重建。该模型分离出与具身形态无关的 3D 轨迹专家、MANO 风格手部运动专家和机器人动作专家。在 SimplerEnv-WidowX 上，它报告平均成功率为 66.1%，高于列出的基线，包括 ThinkACT、SpatialVLA、OpenVLA-OFT、RoboVLMs、π0-FAST 和 π0。

一个可操作的试点是整理一个小型任务特定人类视频子集，预训练轨迹头和手部运动头，然后使用与纯机器人基线相同的 50 到 100 条机器人演示进行微调。对比应包括新物体摆放和指令变化，因为 $M^2$-VLA 也报告称，在训练后指令和物体发生变化时增益更大。

### Evidence
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): MoT-HRA 描述了 HA-2.2M、三专家拆分、只读迁移和 SimplerEnv-WidowX 结果。
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): 论文摘要描述了从重建的大规模人类演示中学习人类意图先验。
- [$M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills](../Inbox/2026-04-27--m-2-vla-boosting-vision-language-models-for-generalizable-manipulation-via-layer-mixture-and-meta-skills.md): $M^2$-VLA 报告了在改写指令和新物体测试中的增益，方法使用冻结的 VLM 特征和检索到的元技能。
