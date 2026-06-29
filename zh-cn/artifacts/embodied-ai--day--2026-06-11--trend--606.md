---
kind: trend
trend_doc_id: 606
granularity: day
period_start: '2026-06-11T00:00:00'
period_end: '2026-06-12T00:00:00'
topics:
- robot manipulation
- VLA
- tactile sensing
- world models
- data annotation
- dexterous robotics
- real-time control
run_id: materialize-outputs
aliases:
- recoleta-trend-606
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vla
- topic/tactile-sensing
- topic/world-models
- topic/data-annotation
- topic/dexterous-robotics
- topic/real-time-control
language_code: zh-CN
---

# 机器人学习正在按标注、接触、时序和任务上下文来评判

## Overview
这一时期的机器人学习论文把模型提升和可部署约束联系起来：可靠标注、接触控制、延迟和任务相关对齐。SPARC、Mana 和 LabVLA 显示了主要重点：在扩大模型之前，先让数据和策略贴合物理任务。

## Clusters

### 可靠的对齐数据
一些论文把对齐错误当作数据问题来处理。SPARC 会给机器人示范自动标注被交互对象的框、轨迹和阶段标签，再根据运动、夹爪接近程度和机器人身体重叠情况计算可靠性分数进行筛选。在 IA-Bench 上，它的被交互对象定位准确率为 80.2%，高于 58.1% 的检测置信度基线，并且在 90% 精度的工作点上保留了 77.6% 的覆盖率。

LabVLA 在仿真中构建实验室监督，因为标准视觉-语言-动作（VLA）策略很少见到实验器材、液体和流程式操作。它的 RoboGenesis 引擎生成了 2,947 个带标注的资产、1,000 多种纹理、10,000 个实验室场景，以及覆盖 16 种机器人平台的示范数据。GIVE 把人类手势加入 VLA 输入用于交接：骨架叠加、指尖射线和简短的语义手势描述把真实世界交接成功率提高到 80.0%，而报告中的基础策略是 0.0%。

#### Evidence
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): SPARC summary gives the interaction-aware auto-labeling method and IA-Bench precision/coverage results.
- [LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories](../Inbox/2026-06-11--labvla-grounding-vision-language-action-models-in-scientific-laboratories.md): LabVLA summary gives the laboratory data engine scale and cross-embodiment setup.
- [GIVE: Grounding Human Gestures in Vision-Language-Action Models](../Inbox/2026-06-11--give-grounding-human-gestures-in-vision-language-action-models.md): GIVE summary gives the gesture augmentation method and real-world handover metrics.

### 接触密集的灵巧操作
灵巧操作论文关注失败的物理来源：细长工具容易打滑，触觉传感器会因硬件不同而变化，手部机械结构在软件看到稳定状态之前就已经决定了接触方式。Mana 先为可动工具生成抓取关键帧，再用短视野强化学习补齐接触密集阶段。它在钳子、老虎钳、晾衣夹和注射器上报告了零样本仿真到真实迁移，很多单任务成功率在 10 次试验中约为 0.6 到 0.8。

FTP-1 通过把异构触觉输入映射到一个共享、感知形态的 token 空间来处理触觉迁移。它先在约 3,000 小时、来自 26 个来源和 21 种触觉传感器的数据上预训练，然后在 UniVTAC 上报告 66.66% 的平均成功率，在未见过的传感器设置上报告 46.6%，而它的 FTP-pi0.5 基线只有 15.0%。MCR-Bionic Hand 从硬件侧补充了这一点：一个肌肉骨骼手如果有 23 块骨头、61 条腕部韧带、103 个以上软组织约束和 46 个肌肉单元，就能在结构中编码有用的抓握预成形和指尖力量路径。

#### Evidence
- [Mana: Dexterous Manipulation of Articulated Tools](../Inbox/2026-06-11--mana-dexterous-manipulation-of-articulated-tools.md): Mana summary gives the articulated-tool pipeline and sim-to-real success ranges.
- [FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation](../Inbox/2026-06-11--ftp-1-a-generalist-foundation-tactile-policy-across-tactile-sensors-for-contact-rich-manipulation.md): FTP-1 summary gives tactile pretraining scale and seen/unseen sensor results.
- [MCR-Bionic Hand: Anatomical Structural Priors for Dexterous Manipulation](../Inbox/2026-06-11--mcr-bionic-hand-anatomical-structural-priors-for-dexterous-manipulation.md): MCR-Bionic Hand summary gives the anatomical design details and hardware claims.

### 真实执行的策略结构
执行类论文围绕机器人何时看、双臂如何动作，以及在延迟限制下如何解码动作 token 增加结构。实时自回归策略论文改变了动作 token 的分块方式，并使用受约束解码，让推理保持在固定的延迟预算内。在 LIBERO 上，pi0-REALFAST 的平均任务成功率达到 95.7%，高于带实时控制的 pi0 的 89.4% 和带实时控制的 pi0.5 的 94.7%。

双臂操作论文把视觉路由和动作路由分开。View-Selective Visual Router 会重新加权左右腕部摄像头 token，Interaction-Aware Action Mixture-of-Experts 会选择协调式或单臂式动作路径。在 RoboTwin 2.0 的六个任务上，完整模型的平均成功率达到 69.6%，高于单体基线的 41.9%。在三个长时程真实世界任务中，报告中相对同一基线的提升为 43.3 个百分点。

#### Evidence
- [Real-Time Execution with Autoregressive Policies](../Inbox/2026-06-11--real-time-execution-with-autoregressive-policies.md): Real-time autoregressive policy summary gives the constrained decoding method and LIBERO results.
- [See Selectively, Act Adaptively: Dual-Level Structural Decomposition for Bimanual Robot Manipulation](../Inbox/2026-06-11--see-selectively-act-adaptively-dual-level-structural-decomposition-for-bimanual-robot-manipulation.md): Bimanual manipulation summary gives the visual/action routing design and simulation plus real-world gains.

### 带动作评分的世界模型
世界模型论文通过加入动作价值、事件或直接控制输出，让预测变得有用。WEAVER 从多视角输入和动作分块预测未来潜在状态、奖励和解码后的观测。在 DROID 外部视角验证集上、16 NFE 条件下，它报告 FID 10.20、FVD 27.83，策略评估中与真实世界成功率的相关系数为 0.870，并且在不增加真实世界交互的情况下，让 pi0.5 的真实世界成功率提升了 38%。

EA-WM 把事件预测和验证加入特征滚动预测。它的验证器按任务进度、语义一致性、物理可行性和不确定性为想象中的未来打分；在 LIBERO 的酒架任务上，一个在线混合设置在 horizon 20 时达到 97/100 的成功率。NavWAM 把同样的以动作为中心的思路用到目标条件视觉导航中，把未来视图、动作分块和目标进度值一起学习。在真实机器人测试中，它在 24 个回合里有 19 个到达目标，而 OmniVLA 是 14 个，NWM 是 4 个。

#### Evidence
- [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](../Inbox/2026-06-11--texttt-weaver-better-faster-longer-an-effective-world-model-for-robotic-manipulation.md): WEAVER summary gives multiview world-model design, prediction metrics, and policy improvement results.
- [EA-WM: Event-Aware World Models with Task-Specification Grounding for Long-Horizon Manipulation](../Inbox/2026-06-11--ea-wm-event-aware-world-models-with-task-specification-grounding-for-long-horizon-manipulation.md): EA-WM summary gives task-event verification and LIBERO wine-rack success.
- [NavWAM: A Navigation World Action Model for Goal-Conditioned Visual Navigation](../Inbox/2026-06-11--navwam-a-navigation-world-action-model-for-goal-conditioned-visual-navigation.md): NavWAM summary gives joint prediction/action/value training and real-robot navigation results.
