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

# Robot VLA deployment controls

## 摘要
机器人 VLA 的采用正在变成控制回路工程问题。下一步该做的工作是：在目标硬件上测动作延迟，为延迟的云端航点加边缘修正，并在机器人动作训练前通过意图级监督复用人类操作视频。

## Action-generation latency benchmark for VLA manipulation policies
测试 VLA 操作策略的机器人团队应增加一个发布门槛，测量动作采样延迟、NFE、端到端 observe-infer-act 时间，以及同一操作套件上的任务成功率。这个门槛应先在目标机器人计算机上运行，再在编译、缓存、采样器更改或动作头更改后重复测试。

CF-VLA 给出了一个具体基线。它在 NFE=2 时报告 LIBERO 平均成功率 96.5%，动作采样延迟减少 75.4%，真实机器人实验平均成功率 83.0%。Libra-VLA 指向了类似的实现方式：让更重的语义规划器少运行一些，把粗粒度意图存进 FIFO 缓冲区，并让动作细化器保持控制频率。硬件分析论文说明了这为什么要放进部署流程。对 pi0 来说，编译前测得的延迟在 RTX 4090 上为 102.3 ms，在 Jetson Thor 上为 246.0 ms，在 AGX Orin 上为 920.6 ms，而能耗和成本在不同设备上变化不同。

一个低成本的验证跑法是做两列对比：当前采样器对比粗到细或带缓冲的变体，同时记录成功率和延迟。一个能省毫秒但降低接触任务成功率的采样器应该被门槛拦下。

### 资料来源
- [CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies](../Inbox/2026-04-27--cf-vla-efficient-coarse-to-fine-action-generation-for-vision-language-action-policies.md): CF-VLA reports the two-step NFE=2 sampler, LIBERO success, action sampling latency reduction, and real-robot success.
- [Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System](../Inbox/2026-04-27--libra-vla-achieving-learning-equilibrium-via-asynchronous-coarse-to-fine-dual-system.md): Libra-VLA describes coarse intent prediction, continuous refinement, and an inference-time FIFO intent buffer.
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): The deployment study reports model-hardware latency, energy, and compilation effects for VLA inference.

## Edge waypoint realignment and LiDAR safety policy for cloud VLA navigation
运行云端 VLA 导航的团队应在延迟到达的航点和机器人控制器之间放一个小型边缘适配器。这个适配器需要带时间戳的位姿缓冲区、把过期航点映射到当前 ego frame 的 SE(2) 变换，以及一个本地策略，用修正后的前视点和 LiDAR 近距离信息来选择子目标。

AsyncShield 是一个直接模板。它使用 5 个重新对齐的前视航点，间隔 0.2 m，再加上 144 个 LiDAR 近距离值，然后用带 LiDAR 安全代价的 PPO-Lagrangian 策略。在混合网络退化下，它报告 76.7% 的成功率、0.725 m 的 cross-track error 和 1.3% 的风险暴露率。去掉时间对齐后，成功率降到 36.7%；去掉安全约束后，跟踪误差较低，但安全性较差。

第一次现场测试可以回放已记录的云端 VLA 数据包，同时注入延迟、抖动和丢包，让机器人在一个已建模的障碍课程中行驶。通过条件应同时看到达、cross-track error 和最小距离违规，因为航点过期时，贴线跟踪仍然可能不安全。

### 资料来源
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): AsyncShield provides the pose-buffer, SE(2) realignment, LiDAR policy, network-degradation results, and ablations.
- [AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation](../Inbox/2026-04-27--asyncshield-a-plug-and-play-edge-adapter-for-asynchronous-cloud-based-vla-navigation.md): The paper abstract states the cloud-to-edge latency problem and the edge correction mechanism.
- [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](../Inbox/2026-04-27--characterizing-vision-language-action-models-across-xpus-constraints-and-acceleration-for-on-robot-deployment.md): The VLA deployment profiling paper frames latency as a closed-loop robot failure source.

## Human-video intent pretraining before robot-action fine-tuning
机器人示教数据有限的操作团队应先测试一个人类视频预训练阶段，让模型先预测交互轨迹和手部动作意图，再训练机器人动作头。这里有用的单元是可迁移的意图：手往哪里移动、哪里发生接触、物体交互如何展开。微调时，机器人动作损失不应覆盖掉这个先验。

MoT-HRA 给出了最具体的方案。它的 HA-2.2M 数据集来自 HowTo100M、Ego4D、EPIC-KITCHENS 和 Something-Something-V2，再经过以手为中心的筛选、MANO 风格姿态、深度对齐、时间分割和语言标注进行过滤与重建。模型分成三个部分：与具身无关的 3D trajectory expert、MANO 风格的 hand-motion expert，以及 robot action expert。在 SimplerEnv-WidowX 上，它报告平均成功率 66.1%，高于列出的 ThinkACT、SpatialVLA、OpenVLA-OFT、RoboVLMs、π0-FAST 和 π0 等基线。

一个可行的试点是整理一个小型任务相关的人类视频子集，先预训练轨迹头和手部动作头，然后用与只用机器人数据的基线相同的 50 到 100 条机器人示教进行微调。对比应包含新物体摆放和指令变化，因为 $M^2$-VLA 也报告说，当训练后指令和物体发生变化时，收益更大。

### 资料来源
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): MoT-HRA describes HA-2.2M, the three-expert split, read-only transfer, and SimplerEnv-WidowX results.
- [Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation](../Inbox/2026-04-27--learning-human-intention-priors-from-large-scale-human-demonstrations-for-robotic-manipulation.md): The paper abstract describes learning human-intention priors from reconstructed large-scale human demonstrations.
- [$M^2$-VLA: Boosting Vision-Language Models for Generalizable Manipulation via Layer Mixture and Meta-Skills](../Inbox/2026-04-27--m-2-vla-boosting-vision-language-models-for-generalizable-manipulation-via-layer-mixture-and-meta-skills.md): $M^2$-VLA reports gains under rephrased instructions and novel-object tests using frozen VLM features and retrieved meta-skills.
