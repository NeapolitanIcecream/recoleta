---
kind: trend
trend_doc_id: 29
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
topics:
- world-models
- vla-finetuning
- autonomous-driving
- uav-tracking
- robot-control
- adversarial-robustness
run_id: materialize-outputs
aliases:
- recoleta-trend-29
tags:
- recoleta/trend
- topic/world-models
- topic/vla-finetuning
- topic/autonomous-driving
- topic/uav-tracking
- topic/robot-control
- topic/adversarial-robustness
language_code: zh-CN
---

# 动作学习更精准了，但 VLA 鲁棒性仍然落后

## Overview
当天最明显的模式是面向实践的动作学习。多篇论文通过收紧预测、动作和控制细节之间的联系，提升了机器人和驾驶系统。最清晰的提升来自经过验证的世界模型、更平滑的动作分布，以及考虑几何结构的规划。同时，Tex3D 表明，当前 VLA 模型仍然很容易被物体级视觉攻击带偏。

## Clusters

### 经过验证的世界模型与基于几何的规划
这一时期的世界模型工作更具体地说明了预测会在什么地方失败，以及如何把这个信号用于训练。WAV把验证拆成两个更简单的检查：未来状态是否看起来合理，以及动作是否真的能够到达该状态。这个设计针对的是数据稀疏场景，而这类场景对动作条件动力学模型的伤害最大。按单日论文产出来看，核心数字很强：在九个任务上，样本效率提升到 2 倍，下游策略性能提升 18%。同一时期，世界-动作建模也扩展到了驾驶领域。DriveDreamer-Policy在一个模型栈中同时预测深度、未来视频和动作，并先生成深度，作为几何骨架。在 Navsim 上，它在 v1 上报告了 89.2 PDMS，在 v2 上报告了 88.7 EPDMS，同时未来视频质量也更好。

#### Evidence
- [World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry](../Inbox/2026-04-02--world-action-verifier-self-improving-world-models-via-forward-inverse-asymmetry.md): WAV 摘要，包含方法和主要结果
- [DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning](../Inbox/2026-04-02--drivedreamer-policy-a-geometry-grounded-world-action-model-for-unified-generation-and-planning.md): DriveDreamer-Policy 摘要，包含几何优先设计和 Navsim 指标

### 训练目标正更接近动作容忍度
VLA 微调论文开始把重点放在动作分布上，而不只是更大的骨干模型。FAN prior 论文认为，很多机器人状态都对应一小组近似等价的优质动作，因此训练应当在这片邻域上保留概率质量。在 ManiSkill 上结合 OpenVLA 做监督微调时，它把分布内成功率从 78.1 提高到 89.8，并把平均 OOD 成功率从 58.1 提高到 63.3。另一篇控制论文在更底层提出了相关观点：控制器增益会改变策略学习和迁移的难易程度。它的行为克隆结果更偏向顺从、过阻尼的增益设置；在重定向设置里，在增益设置扩展到 25x decimation 时，仍能保持至少 90% 的成功率，且关节位置 MSE 低于 1e-3。合起来看，实践重点已经很明确：动作容忍度和控制接口选择正成为一阶训练变量。

#### Evidence
- [Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior](../Inbox/2026-04-02--boosting-vision-language-action-finetuning-with-feasible-action-neighborhood-prior.md): FAN prior 摘要，包含具体的 ManiSkill/OpenVLA 提升
- [Tune to Learn: How Controller Gains Shape Robot Policy Learning](../Inbox/2026-04-02--tune-to-learn-how-controller-gains-shape-robot-policy-learning.md): 控制器增益研究摘要，包含可学习性视角和报告指标

### VLA 设计正针对无人机和驾驶进一步专门化
具身 VLA 工作正在进入新的运行领域，模型内部也直接加入了速度和结构设计。UAV-Track VLA 为按指令执行的无人机跟踪加入了时间压缩、空间定位，以及一个 25 步的 flow-matching 动作头。它基于一个大规模 CARLA 基准，包含 892,756 帧、176 个任务和 85 个对象，并报告在长距离行人跟踪上取得 61.76% 的成功率，同时单步延迟降低 33.4%。驾驶论文也在按角色组织 VLA 系统。UniDriveVLA 将理解、感知和规划拆分为独立的 transformer 专家，以减少语言推理与空间感知之间的干扰。提供的摘录没有给出最后的主结果行，但它声称在 nuScenes 和 Bench2Drive 上达到最优结果，并且比更早的驾驶 VLA 报告提供了更强的基线背景。

#### Evidence
- [UAV-Track VLA: Embodied Aerial Tracking via Vision-Language-Action Models](../Inbox/2026-04-02--uav-track-vla-embodied-aerial-tracking-via-vision-language-action-models.md): UAV-Track VLA 摘要，包含基准规模、成功率和延迟
- [UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving](../Inbox/2026-04-02--unidrivevla-unifying-understanding-perception-and-action-planning-for-autonomous-driving.md): UniDriveVLA 摘要，包含专家分离设计和基准声明

### 物理攻击面仍然大幅敞开
鲁棒性仍然是当前 VLA 系统的硬限制。Tex3D 表明，施加在被操作物体上的对抗性 3D 纹理，能够以很难被当作边缘情况忽略的比例破坏策略。该攻击直接作用于物体表面，通过可微渲染路径优化，并用轨迹感知加权在长时序回合中保持稳定。报告的失败率在无目标攻击下，从 OpenVLA 的 24.1% 升到 88.1%，从 OpenVLA-OFT 的 4.7% 升到 76.0%，从 pi0 的 4.6% 升到 71.8%。在 OpenVLA 的空间任务上，定向攻击下的失败率达到 96.7%。这对同期能力提升形成了一个实际的制衡：更好的训练和更好的规划，并不会消除大面积的视觉攻击面。

#### Evidence
- [Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models](../Inbox/2026-04-02--tex3d-objects-as-attack-surfaces-via-adversarial-3d-textures-for-vision-language-action-models.md): Tex3D 摘要，包含方法和各个 VLA 模型上的失败率上升
