---
kind: trend
trend_doc_id: 131
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
topics:
- robotics
- long-horizon manipulation
- hierarchical control
- reinforcement learning
- uav navigation
run_id: materialize-outputs
aliases:
- recoleta-trend-131
tags:
- recoleta/trend
- topic/robotics
- topic/long-horizon-manipulation
- topic/hierarchical-control
- topic/reinforcement-learning
- topic/uav-navigation
language_code: zh-CN
---

# 长时程机器人控制正在更明确地区分规划、记忆和引导

## Overview
这一天的机器人论文更偏向显式结构，而不是单体控制。HiVLA 和 Goal2Skill 都从把规划、落地、记忆和恢复从底层动作生成中分离出来中得到提升。VLAJS 在训练阶段用同样的思路，把 VLA 模型作为强化学习的稀疏早期指导。最具体的收益出现在长时程操作上；无人机导航论文则补充了一份清晰的未解决部署约束清单。

## Clusters

### 分层规划正在推动长时程操作
长时程操作论文越来越明确地把控制环放在执行器策略之上。HiVLA 把视觉-语言模型（VLM）用于规划和落地，再把执行交给一个扩散策略，同时使用全局场景 token 和高分辨率局部裁剪。这个设置在 RoboTwin 2.0 上的平均成功率为 83.3%，高于 H-RDT 的 70.6%。Goal2Skill 为多阶段任务加入了结构化记忆、后置条件检查和恢复逻辑。在五个 RMBench 任务上，它报告的平均成功率是 32.4%，而最强基线为 9.8%。共同的信息很明确：更好的长时程结果现在来自显式的子任务结构、场景落地和步骤验证，而不只是更大的端到端策略。

#### Evidence
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): HiVLA architecture and RoboTwin 2.0 results
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Goal2Skill memory, verification, and RMBench results

### VLA 先验正在作为临时训练信号使用
另一个明显主题是，如何使用预训练的视觉-语言-动作先验，同时不把机器人绑死在教师模型上。VLAJS 把 OpenVLA 之类模型的稀疏指导加到 PPO 上，最多只在 rollout 步骤的 20% 里查询教师，并把动作方向对齐，而把动作幅度留给强化学习。随着奖励进展，指导权重会衰减，在学习稳定后被移除。在报告的 ManiSkill 结果中，这让多个任务所需的环境交互次数减少了 50% 以上，同时最终控制器仍然是高频 RL 策略。这是一种可直接使用的方法，先借助语义先验，再保留后期的闭环控制。

#### Evidence
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): VLAJS method details and sample-efficiency claim

### 无人机语言导航仍受部署限制定义
空中语言条件机器人在这里出现时，更像是一张待解决部署问题的地图，而不是新的模型结果。UAV-VLN 综述把无人机导航框定为一个带自然语言输入的部分可观测控制问题，然后按模块化系统、时空模型和基础模型智能体来组织方法。它在这个阶段最有用的贡献是约束清单：仿真到现实迁移、户外感知漂移、指令歧义和机载算力仍然是主要阻碍。这让这篇论文更像研究议程，而不是基准进展证据。

#### Evidence
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md): Survey taxonomy and deployment bottlenecks for UAV-VLN
