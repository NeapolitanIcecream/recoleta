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

## Summary
近期研究支持三项具体的流程调整：把动作容忍度和控制器增益放进同一个机器人微调闭环；用规划路径中的显式几何信息来评估自动驾驶 world-action 模型；并把物体表面对抗测试加入 VLA 操作系统的发布门禁。在有论文给出与部署决策直接相关的操作指标时，证据最强，包括基于 FAN 的微调在 ManiSkill 上带来的成功率提升、深度优先驾驶模型在 Navsim 上的规划分数提升，以及 Tex3D 攻击下的大幅失败率上升。

## 面向机器人适配的动作分布正则化与增益感知微调
微调 OpenVLA 类策略的机器人团队，可以先加入动作分布正则项，再决定是否投入更多数据采集。这个改动很具体：在微调时让概率质量保持在一小片优质动作邻域内，然后测量它是否能提升目标环境中的留出任务成功率和 OOD 变体表现。FAN 论文为这项检查给出了明确参照。在 ManiSkill 上对 OpenVLA 做监督式微调时，分布内成功率从 78.1 提高到 89.8，平均 OOD 成功率从 58.1 提高到 63.3。这个幅度已经足以让任何仍按单一精确动作标签训练的操作系统做一次轻量消融实验。

这也为部署团队指出了一个实用的配套层：在微调过程中检查动作分布的尖锐程度。如果策略收缩成很窄的峰值，这可能是小规模示范集和轻微执行偏移下的失效模式。一个低成本的首轮测试是回放当前微调数据集，比较仅用对数似然训练，与在同样设置下围绕首选动作加入局部高斯先验的训练效果，再跟踪在小幅视觉、语义和执行偏移下的成功率。控制器增益论文进一步支持这种流程，因为它表明，可学习性不仅取决于策略目标，也取决于控制接口。在行为克隆中，最佳闭环成功率出现在顺应性较强、过阻尼的增益设置下；而 torque-to-position retargeting 在最高 25x 降采样的不同增益设置中，仍能保持至少 90% 的成功率，关节位置 MSE 低于 1e-3。把预训练 VLA 适配到新机械臂或新控制器的团队，可以把动作容忍度调节和增益选择当成同一个微调问题，而不是两个分开的收尾步骤。

### Evidence
- [Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior](../Inbox/2026-04-02--boosting-vision-language-action-finetuning-with-feasible-action-neighborhood-prior.md): 报告了核心 FAN 正则项，以及在 OpenVLA 微调中经验证的 ManiSkill 分布内和 OOD 成功率提升。
- [Tune to Learn: How Controller Gains Shape Robot Policy Learning](../Inbox/2026-04-02--tune-to-learn-how-controller-gains-shape-robot-policy-learning.md): 表明控制器增益会实质影响行为克隆的可学习性，且重定向后的轨迹在不同增益设置下仍保持较高保真度。

## 用于自动驾驶评估的深度优先 world-action 规划
构建 world-action 模型的自动驾驶团队，现在可以为“几何优先”的规划栈提供更充分的依据，因为已经有具体的闭环结果支撑这一路线。实现方式也很明确：先预测深度，再预测未来视频和动作；把深度图作为想象与规划的显式支架；同时让各生成器保持模块化，这样仅规划模式和世界生成模式就能共享同一个骨干网络。DriveDreamer-Policy 为这种设计提供了清晰的基准锚点。在 Navsim v1 上，它达到 89.2 PDMS，高于 PWM 的 88.1、WoTE 的 88.3、DriveVLA-W0 的 88.4，以及 AutoVLA 的 89.1。在 Navsim v2 上，它达到 88.7 EPDMS，论文称这比表中的上一方法高 2.6 分。

实际流程上的变化，既在模型设计，也在评估方法。若表征遗漏了自由空间、布局或遮挡结构，光有看起来可信的 rollout 还不够。一个简单的采用路径，是对现有未来视频规划器做一次深度优先消融，然后比较闭环规划分数和一小组遮挡较重案例的表现。机器人 world model 的 WAV 也用了相同思路：把未来状态合理性和动作可达性分开检查后，验证效果会更好；论文报告称，在九个任务上，样本效率提升 2x，下游策略表现提升 18%。这些结果共同支持这样一种规划流程：把几何和可达性设为显式的中间检查项，而不只看最终动作损失。

### Evidence
- [DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning](../Inbox/2026-04-02--drivedreamer-policy-a-geometry-grounded-world-action-model-for-unified-generation-and-planning.md): 提供了几何优先架构，以及在 Navsim v1 和 v2 上经过基准验证的规划性能提升。
- [World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry](../Inbox/2026-04-02--world-action-verifier-self-improving-world-models-via-forward-inverse-asymmetry.md): 支持更广泛的显式中间验证流程，并给出了样本效率和下游策略质量的测量增益。

## 面向 VLA 操作发布检查的物体表面对抗测试
任何在真实物理任务上评估 VLA 操作系统的团队，都需要把物体表面攻击测试加入发布检查清单。Tex3D 已经足够具体，可以把这件事从研究层面的提醒变成标准红队步骤。攻击附着在被操作物体的 3D 纹理上，通过可微渲染路径优化，并用轨迹感知加权让它在长时序任务中保持有效。在仿真中，多个常见模型的失败率都大幅上升：OpenVLA 在无目标攻击下从 24.1% 升到 88.1%，OpenVLA-OFT 从 4.7% 升到 76.0%，pi0 从 4.6% 升到 71.8%。在 OpenVLA 的空间任务上，定向攻击下的失败率达到 96.7%。

流程上的变化也很直接。在发布新 checkpoint 之前，先选一小组基准物体，在仿真中针对冻结策略优化其表面纹理，再按任务类别和物体类别记录失败率。这样，团队就能找出那些依赖脆弱视觉捷径的策略，即使标准扰动测试看起来没有问题。论文还没有给出带有恢复指标验证的防御方案，所以短期内更现实的产出是评测 harness 和验收阈值，而不是鲁棒性结论。对于把 VLA 系统卖给仓库、实验室或家庭场景的团队，这类 harness 比等待完整的训练时防御栈更容易落地。

### Evidence
- [Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models](../Inbox/2026-04-02--tex3d-objects-as-attack-surfaces-via-adversarial-3d-textures-for-vision-language-action-models.md): 记录了具备物理基础的 3D 纹理攻击方法，以及在 OpenVLA、OpenVLA-OFT 和 pi0 上测得的大幅失败率上升。
