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

# 长时程机器人控制正越来越明确地处理规划、记忆和引导

## Overview
这一天的机器人论文更偏向明确结构，而不是单体式控制。HiVLA 和 Goal2Skill 都报告说，把规划、场景落地、记忆和恢复与底层动作生成分开后，效果更好。VLAJS 在训练阶段也用了同样思路，把 VLA 模型作为强化学习前期的稀疏引导。最具体的提升出现在长时程操作上；无人机导航那篇论文则补充了一份尚未解决的部署约束清单。

## Clusters

### 分层规划正在支撑长时程操作
长时程操作论文越来越明确地区分执行器策略之上的控制回路。HiVLA让视觉语言模型（VLM）负责规划和场景落地，再把执行交给一个同时使用全局场景 token 和高分辨率局部裁剪的扩散策略。这个设置在 RoboTwin 2.0 上取得了 83.3% 的平均成功率，高于 H-RDT 的 70.6%。Goal2Skill 为多阶段任务加入了结构化记忆、后置条件检查和恢复逻辑。在五个 RMBench 任务上，它报告的平均成功率是 32.4%，而最强基线是 9.8%。共同的信息很直接：长时程任务表现的提升，现在更多来自明确的子任务结构、场景落地和步骤验证，而不只是更大的端到端策略。

#### Evidence
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): HiVLA 架构和 RoboTwin 2.0 结果
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Goal2Skill 的记忆、验证和 RMBench 结果

### VLA 先验正被用作临时训练信号
另一个明显主题是，如何使用预训练视觉语言动作先验，同时不把机器人锁定在教师模型上。VLAJS 把来自 OpenVLA 这类模型的稀疏引导加入 PPO，在 rollout 步骤中最多只查询教师模型 20% 的步数，并让动作方向与教师对齐，同时把动作幅度交给强化学习决定。引导权重会随着奖励进展衰减，并在学习稳定后移除。在论文报告的 ManiSkill 结果中，这让若干任务所需的环境交互次数减少了 50% 以上，同时最终控制器仍是一个高频 RL 策略。这是一种实用做法：前期借用语义先验，后期保留闭环控制。

#### Evidence
- [Jump-Start Reinforcement Learning with Vision-Language-Action Regularization](../Inbox/2026-04-15--jump-start-reinforcement-learning-with-vision-language-action-regularization.md): VLAJS 方法细节和样本效率结论

### UAV 语言导航仍然受部署限制定义
这里的空中语言条件机器人更像是一张开放部署问题清单，而不是新的模型结果。UAV-VLN 综述把无人机导航表述为一个带自然语言输入的部分可观测控制问题，再按模块化系统、时空模型和基础模型智能体来组织现有方法。它在这个时期最有用的贡献是那份约束清单：sim-to-real transfer、户外感知漂移、指令歧义和机载算力仍是主要障碍。这使这篇论文更像一份研究议程，而不是基准进展的证据。

#### Evidence
- [Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap](../Inbox/2026-04-15--vision-and-language-navigation-for-uavs-progress-challenges-and-a-research-roadmap.md): UAV-VLN 的综述分类和部署瓶颈
