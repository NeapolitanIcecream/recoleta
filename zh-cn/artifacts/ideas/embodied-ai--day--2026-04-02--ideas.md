---
kind: ideas
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- world-models
- vla-finetuning
- autonomous-driving
- uav-tracking
- robot-control
- adversarial-robustness
tags:
- recoleta/ideas
- topic/world-models
- topic/vla-finetuning
- topic/autonomous-driving
- topic/uav-tracking
- topic/robot-control
- topic/adversarial-robustness
language_code: zh-CN
---

# 具身策略可靠性检查

## 摘要
近期工作支持三项具体流程改动：把动作容差和控制器增益当作同一个机器人微调循环的一部分；在规划路径里用显式几何来评估驾驶 world-action model；在 VLA 操作发布门禁里加入物体表面对抗测试。证据最强的地方，是论文把指标直接连到部署选择上，包括基于 FAN 的微调在 ManiSkill 上的成功率提升、深度优先驾驶模型在 Navsim 上的规划提升，以及 Tex3D 攻击带来的大幅失效率上升。

## 用于机器人适配的动作分布正则化与增益感知微调
针对 OpenVLA 类策略做微调的机器人团队，可以在投入更多数据采集之前先加一个动作分布正则项。可行的改动很具体：在微调时让概率质量保留在一小块好动作邻域里，然后检查这是否能提升目标环境里的留出任务成功率和 OOD 变体表现。FAN 论文给出了一个明确的检验目标。在 ManiSkill 上用 OpenVLA 做监督微调时，分布内成功率从 78.1 提升到 89.8，平均 OOD 成功率从 58.1 提升到 63.3。这个幅度已经足以支持在仍然依赖单个精确动作标签的任何操作栈里做一次轻量消融。

这也指向一个适合部署团队的配套检查：在微调期间看动作分布是不是过尖。如果策略收缩成很窄的峰值，这在小示范集和轻微执行偏移下就是一个可疑失效模式。一个成本不高的起点，是回放当前微调集，把只用对数似然的训练和在偏好动作周围加入局部高斯先验的同一套训练做对比，并跟踪小幅视觉、语义和执行偏移下的成功率。控制器增益论文强化了这个工作流，因为它说明可学习性取决于控制接口，也取决于策略目标。在行为克隆里，最佳闭环成功率出现在较平滑、过阻尼的增益设置中，而 torque-to-position retargeting 在最高 25x decimation 下仍能保持至少 90% 的成功率，joint-position MSE 低于 1e-3。把预训练 VLA 迁移到新机械臂或新控制器时，团队可以把动作容差调节和增益选择看成一个微调问题，而不是两步分开的清理工作。

### 资料来源
- [Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior](../Inbox/2026-04-02--boosting-vision-language-action-finetuning-with-feasible-action-neighborhood-prior.md): Reports the core FAN regularizer and the verified ManiSkill gains for in-distribution and OOD success with OpenVLA finetuning.
- [Tune to Learn: How Controller Gains Shape Robot Policy Learning](../Inbox/2026-04-02--tune-to-learn-how-controller-gains-shape-robot-policy-learning.md): Shows that controller gains materially affect behavior-cloning learnability and that retargeted trajectories remain faithful across gain settings.

## 用于自动驾驶评估的深度优先 world-action 规划
做 world-action model 的驾驶团队，现在可以把几何优先的规划栈说清楚，因为已经有具体的闭环结果支撑。做法很明确：先预测深度，再预测未来视频和动作，把深度图当作想象和规划的显式支架，并保持生成器模块化，这样只做规划和做完整世界生成时可以共用同一个骨干。DriveDreamer-Policy 给这个设计提供了清晰的基准锚点。在 Navsim v1 上，它达到 89.2 PDMS，高于 PWM 的 88.1、WoTE 的 88.3、DriveVLA-W0 的 88.4 和 AutoVLA 的 89.1。在 Navsim v2 上，它达到 88.7 EPDMS，论文说明这比表中的上一种方法高 2.6 分。

真正需要改的不只是模型设计，还有评估流程。一个看起来合理的 rollout，如果表示里缺少自由空间、布局或遮挡结构，就还不够。一个直接的落地方式，是先拿现有的未来视频规划器做一次以深度为主的消融，再对比闭环规划分数和一组遮挡较重的案例。WAV 在机器人 world model 上也给出同样的思路：把未来状态的合理性和动作可达性分开检查，验证效果会更好，论文报告了跨九个任务 2 倍的样本效率提升，以及 18% 的下游策略提升。把这些结果放在一起看，说明规划流程里应该有几何和可达性的显式中间检查，而不只是最后的动作损失。

### 资料来源
- [DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning](../Inbox/2026-04-02--drivedreamer-policy-a-geometry-grounded-world-action-model-for-unified-generation-and-planning.md): Provides the geometry-first architecture and benchmarked planning gains on Navsim v1 and v2.
- [World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry](../Inbox/2026-04-02--world-action-verifier-self-improving-world-models-via-forward-inverse-asymmetry.md): Supports the broader workflow of explicit intermediate verification with measured gains in sample efficiency and downstream policy quality.

## 用于 VLA 操作发布检查的物体表面对抗测试
任何在物理任务上评估 VLA 操作系统的人，都需要把物体表面攻击测试放进发布清单。Tex3D 已经足够具体，可以把这件事从研究警告变成标准红队步骤。攻击直接作用在被操控物体的 3D 纹理上，通过可微渲染路径优化，并用轨迹感知加权在长序列里保持有效。在仿真里，多个常见模型的失效率都大幅上升：OpenVLA 在非定向攻击下从 24.1% 升到 88.1%，OpenVLA-OFT 从 4.7% 升到 76.0%，pi0 从 4.6% 升到 71.8%。在 OpenVLA 的空间任务上，定向攻击下的失效率达到 96.7%。

工作流改动很直接。在发布新 checkpoint 之前，拿一小组基准物体，在仿真里对冻结策略优化表面纹理，并按任务类别和物体类别记录失效率。这样团队就能找出那些依赖脆弱视觉捷径的策略，即使常规扰动测试看起来没问题。论文目前还没有给出带验证恢复数值的防御方案，所以短期内真正可交付的是评估工具和准入阈值，而不是鲁棒性声明。对把 VLA 系统卖到仓库、实验室或家庭的团队来说，这种工具比等待完整的训练期防御栈更容易落地。

### 资料来源
- [Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models](../Inbox/2026-04-02--tex3d-objects-as-attack-surfaces-via-adversarial-3d-textures-for-vision-language-action-models.md): Documents the physically grounded 3D texture attack method and the large measured failure-rate increases across OpenVLA, OpenVLA-OFT, and pi0.
