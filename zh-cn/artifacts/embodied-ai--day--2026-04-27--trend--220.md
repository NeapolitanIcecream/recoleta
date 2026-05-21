---
kind: trend
trend_doc_id: 220
granularity: day
period_start: '2026-04-27T00:00:00'
period_end: '2026-04-28T00:00:00'
topics:
- vision-language-action
- robot manipulation
- coarse-to-fine control
- robot deployment
- human demonstrations
- edge safety
run_id: materialize-outputs
aliases:
- recoleta-trend-220
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/coarse-to-fine-control
- topic/robot-deployment
- topic/human-demonstrations
- topic/edge-safety
language_code: zh-CN
---

# 机器人 VLA 工作正在按控制延迟、动作结构和数据复用来评估

## Overview
当天最强的信号是机器人在严格时间和数据限制下的实际执行。视觉-语言-动作（VLA）研究集中在动作分解、高效采样、人类视频先验和边缘安全上。Libra-VLA、CF-VLA 和 AsyncShield 给出了最清楚的证据。

## Clusters

### 粗到细动作生成
两篇操作论文把动作结构当作控制问题处理。Libra-VLA 将预测拆成离散的宏观方向意图和连续的精细控制，再通过意图缓冲区降低较重规划器的运行频率。它报告的 LIBERO 平均成功率为 97.2%，LIBERO-Plus 零样本成功率为 79.5%。

CF-VLA 将类似的粗到细思路用于基于流的动作采样。它使用两次函数评估：一个感知动作的粗起点和一次局部修正。论文给出的取舍很具体：NFE=2 时 LIBERO 平均成功率为 96.5，动作采样延迟降低 75.4%，真实机器人实验平均成功率为 83.0。

#### Evidence
- [Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System](../Inbox/2026-04-27--libra-vla-achieving-learning-equilibrium-via-asynchronous-coarse-to-fine-dual-system.md): Libra-VLA 摘要、方法拆分、LIBERO 和 LIBERO-Plus 结果。
- [CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies](../Inbox/2026-04-27--cf-vla-efficient-coarse-to-fine-action-generation-for-vision-language-action-policies.md): CF-VLA 摘要、两阶段采样、延迟和真实机器人结果。

### 面向可泛化操作的数据复用
最强的数据结果来自 MoT-HRA。它构建了 HA-2.2M，一个包含 220 万个片段的人类操作数据集，然后把意图拆分为 3D 轨迹专家、MANO 风格手部运动专家和机器人动作专家。在 SimplerEnv-WidowX 上，它报告的平均成功率为 66.1%，高于论文中列出的 ThinkACT、SpatialVLA、OpenVLA-OFT、RoboVLMs 和 pi0 变体。

M²-VLA 处理模型内部的泛化问题。它冻结视觉语言主干，选择有用的层特征，并检索已存储的元技能来引导动作预测。报告中的收益在指令和物体变化下最清楚：改写后的 LIBERO Spatial 指令成功率为 66.2%，新物体拾放测试成功率为 34.4%，性能下降幅度小于 OpenVLA 和 VLA-Adapter。

#### Evidence
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): MoT-HRA 数据集、因子化专家和 SimplerEnv-WidowX 结果。
- [$M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills](../Inbox/2026-04-27--m-2-vla-boosting-vision-language-models-for-generalizable-manipulation-via-layer-mixture-and-meta-skills.md): M²-VLA 冻结主干方法和泛化结果。

### 机器人端延迟和异步安全
部署研究正在测量完整的观察、推理、动作循环。跨 XPU VLA 研究在 RTX 4090、Jetson Thor、AGX Orin、Intel B60 Pro 和 Ascend NPU 上分析推理表现，然后按成本、能耗和时间对硬件排序。它的 pi0 测量显示，只看峰值速度不够：编译前 RTX 4090 达到 102.3 ms，Jetson Thor 为 246.0 ms，AGX Orin 为 920.6 ms，并且能耗成本不同。

AsyncShield 处理另一类时序故障：过期的云端 VLA 路点。它用 SE(2) 位姿变换重新对齐延迟路点，并使用带 LiDAR 输入的安全约束本地策略。在混合网络退化下，它报告的成功率为 76.7%；无时间对齐消融版本降至 36.7%。

#### Evidence
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): 跨加速器 VLA 性能分析、CET 排序、延迟和加速结果。
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): AsyncShield 方法以及带消融的混合退化结果。
