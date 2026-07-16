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

# 机器人 VLA 工作正按控制时延、动作结构和数据复用来评估

## 概览
当天最强的信号是：机器人在严格的时延和数据限制下执行任务。Vision-Language-Action（VLA）工作集中在动作拆分、高效采样、人类视频先验和边缘安全上。Libra-VLA、CF-VLA 和 AsyncShield 给出了最清楚的证据。

## 研究发现

### 粗到细的动作生成
两篇操作论文把动作结构当作控制问题来处理。Libra-VLA 把预测拆成离散的宏方向意图和连续的精细控制，然后通过意图缓冲区让更重的规划器降低运行频率。它在 LIBERO 上的平均成功率是 97.2%，在 LIBERO-Plus 上的零样本成功率是 79.5%。

CF-VLA 把类似的粗到细思路用于基于流的动作采样。它只做两次函数评估：一次粗粒度、感知动作的起点，一次局部修正。报告的权衡很明确：在 NFE=2 时，LIBERO 平均成功率是 96.5%，动作采样延迟降低 75.4%，真实机器人实验中的平均成功率是 83.0%。

#### 资料来源
- [Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System](../Inbox/2026-04-27--libra-vla-achieving-learning-equilibrium-via-asynchronous-coarse-to-fine-dual-system.md): Libra-VLA summary, method split, LIBERO and LIBERO-Plus results.
- [CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies](../Inbox/2026-04-27--cf-vla-efficient-coarse-to-fine-action-generation-for-vision-language-action-policies.md): CF-VLA summary, two-stage sampling, latency and real-robot results.

### 用于可泛化操作的数据复用
数据结果最强的是 MoT-HRA。它构建了 HA-2.2M，一个 220 万 episode 的人类操作数据集，然后把意图拆成 3D 轨迹专家、MANO 风格的手部动作专家和机器人动作专家。在 SimplerEnv-WidowX 上，它报告的平均成功率是 66.1%，高于论文里列出的 ThinkACT、SpatialVLA、OpenVLA-OFT、RoboVLMs 和 pi0 变体。

M²-VLA 处理的是模型内部的泛化问题。它保持视觉语言骨干冻结，选取有用的层特征，并检索存储的元技能来引导动作预测。它在指令改写和对象变化下的提升最明显：在改写后的 LIBERO Spatial 指令上成功率是 66.2%，在新物体抓放测试上是 34.4%，比 OpenVLA 和 VLA-Adapter 的下降更小。

#### 资料来源
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): MoT-HRA dataset, factorized experts, and SimplerEnv-WidowX results.
- [$M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills](../Inbox/2026-04-27--m-2-vla-boosting-vision-language-models-for-generalizable-manipulation-via-layer-mixture-and-meta-skills.md): M²-VLA frozen-backbone method and generalization results.

### 机器人上的延迟与异步安全
部署工作正在测量完整的 observe-infer-act 循环。跨 XPU 的 VLA 研究在 RTX 4090、Jetson Thor、AGX Orin、Intel B60 Pro 和 Ascend NPU 上分析推理，然后按成本、能耗和时间对硬件排序。它对 pi0 的测量说明，峰值速度并不够：编译前 RTX 4090 的延迟是 102.3 ms，Jetson Thor 是 246.0 ms，AGX Orin 是 920.6 ms，而且能耗不同。

AsyncShield 处理另一种时序故障模式：云端 VLA 里过时的航点。它用 SE(2) 位姿变换对延迟航点重新对齐，并结合带安全约束的本地策略和 LiDAR 输入。在混合网络退化条件下，它的成功率是 76.7%，而去掉时间对齐的消融降到 36.7%。

#### 资料来源
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): Cross-accelerator VLA profiling, CET ranking, latency and speedup results.
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): AsyncShield method and mixed-degradation results with ablations.
