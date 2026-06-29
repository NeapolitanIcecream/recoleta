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

# 动作学习正在变得更精确，而 VLA 鲁棒性仍然落后

## Overview
这一天最强的模式是实用的动作学习。论文通过缩短预测、动作和控制细节之间的距离，改进了机器人和驾驶系统。最明显的提升来自经过验证的世界模型、更平滑的动作分布，以及几何感知规划。与此同时，Tex3D 表明当前 VLA 模型仍然很容易被物体级视觉攻击打偏。

## Clusters

### 验证过的世界模型和几何约束规划
这一时期的世界模型工作更具体地说明了预测在哪些地方会出错，以及如何把这个信号用于训练。WAV 把验证拆成两个更简单的检查：未来状态看起来是否合理，以及动作是否真的能到达它。这个设计面向数据稀缺场景，而这正是动作条件动力学模型最容易受影响的地方。单日结果也很强：9 个任务上的样本效率提升 2 倍，下游策略提升 18%。同一时期，world-action 建模也扩展到了驾驶。DriveDreamer-Policy 在一个系统里预测深度、未来视频和动作，并先生成深度作为几何骨架。在 Navsim 上，它报告 v1 的 89.2 PDMS 和 v2 的 88.7 EPDMS，同时未来视频质量更好。

#### Evidence
- [World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry](../Inbox/2026-04-02--world-action-verifier-self-improving-world-models-via-forward-inverse-asymmetry.md): WAV summary with method and headline results
- [DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning](../Inbox/2026-04-02--drivedreamer-policy-a-geometry-grounded-world-action-model-for-unified-generation-and-planning.md): DriveDreamer-Policy summary with geometry-first design and Navsim metrics

### 训练目标正在更接近动作容忍度
VLA 微调论文现在更关注动作分布，而不只是更大的骨干网络。FAN prior 论文认为，很多机器人状态都有一小组几乎等价的好动作，所以训练时应该把概率质量保留在这个邻域里。在 ManiSkill 上用 OpenVLA 做监督微调时，它把分布内成功率从 78.1 提高到 89.8，并把平均 OOD 成功率从 58.1 提高到 63.3。另一篇控制论文在更底层给出类似结论：控制器增益会影响策略有多容易学习和迁移。它的行为克隆结果更支持柔顺、过阻尼的增益设置，而它的重定向方案在增益设置最高到 25x 降采样时，仍保持至少 90% 的成功率，关节位置 MSE 低于 1e-3。放在一起看，实践重点很清楚：动作容忍度和控制接口选择正在变成一线训练变量。

#### Evidence
- [Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior](../Inbox/2026-04-02--boosting-vision-language-action-finetuning-with-feasible-action-neighborhood-prior.md): FAN prior summary with concrete ManiSkill/OpenVLA gains
- [Tune to Learn: How Controller Gains Shape Robot Policy Learning](../Inbox/2026-04-02--tune-to-learn-how-controller-gains-shape-robot-policy-learning.md): Controller-gain study summary with learnability framing and reported metrics

### VLA 设计正在向无人机和驾驶场景分化
具身 VLA 工作正在进入新的运行场景，而且模型里已经加入速度和结构约束。UAV-Track VLA 为跟随指令的无人机跟踪加入了时间压缩、空间对齐，以及一个 25 步 flow-matching 动作头。它依托一个规模很大的 CARLA 基准，包含 892,756 帧、176 个任务和 85 个物体，并报告了长距离行人跟踪 61.76% 的成功率，以及每步延迟降低 33.4%。驾驶论文也在按功能拆分 VLA 系统。UniDriveVLA 把理解、感知和规划拆成不同的 transformer expert，以减少语言推理和空间感知之间的干扰。摘录里没有给出最终结果行，但它声称在 nuScenes 和 Bench2Drive 上达到最先进结果，并且比更早的驾驶 VLA 报告提供了更强的基线背景。

#### Evidence
- [UAV-Track VLA: Embodied Aerial Tracking via Vision-Language-Action Models](../Inbox/2026-04-02--uav-track-vla-embodied-aerial-tracking-via-vision-language-action-models.md): UAV-Track VLA summary with benchmark scale, success rate, and latency
- [UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving](../Inbox/2026-04-02--unidrivevla-unifying-understanding-perception-and-action-planning-for-autonomous-driving.md): UniDriveVLA summary with expert separation design and benchmark claims

### 物理攻击面仍然完全暴露
当前 VLA 系统的鲁棒性仍然是硬限制。Tex3D 表明，施加在被操纵物体上的对抗性 3D 纹理可以把策略打坏，而且这种失败率很难被当作边缘案例忽略。这个攻击直接作用在物体表面，通过可微渲染路径优化，并用轨迹感知加权在长回合中稳定下来。报告的失败率在无目标攻击下从 OpenVLA 的 24.1% 升到 88.1%，OpenVLA-OFT 从 4.7% 升到 76.0%，pi0 从 4.6% 升到 71.8%。在 OpenVLA 的空间任务上，有目标攻击下的失败率达到 96.7%。这为这一时期的能力提升提供了必要的反向参照：更好的训练和更好的规划，并不能消除大面积的视觉攻击面。

#### Evidence
- [Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models](../Inbox/2026-04-02--tex3d-objects-as-attack-surfaces-via-adversarial-3d-textures-for-vision-language-action-models.md): Tex3D summary with method and failure-rate increases across VLA models
