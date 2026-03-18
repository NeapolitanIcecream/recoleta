---
source: hn
url: https://eon.systems/updates/embodied-brain-emulation
published_at: '2026-03-15T23:44:34'
authors:
- LopRabbit
topics:
- embodied-simulation
- connectome-model
- computational-neuroscience
- brain-body-interface
- virtual-agent
relevance_score: 0.34
run_id: materialize-outputs
---

# How the Eon Team Produced a Virtual Embodied Fly

## Summary
这篇文章介绍了 Eon 团队如何把果蝇连接组脑模型、视觉模型和物理身体模拟整合成一个“具身虚拟果蝇”，用于展示大脑如何闭环控制身体。其意义主要在于提供一个可实验的脑-体接口研究平台，而不是宣称已经完整复现真实果蝇。

## Problem
- 要解决的问题是：如何把**连接组约束的大脑模型**与**物理身体模型**耦合起来，使虚拟动物能根据感觉输入产生闭环行为。
- 这很重要，因为仅有脑网络或仅有身体仿真都不足以研究真实的感觉-运动控制；需要一个端到端系统来测试“结构是否足以产生行为”。
- 难点在于如何把感觉事件映射到特定神经元，以及如何把下降神经元活动映射成关节力矩、步态和动作序列。

## Approach
- 以 Shiu 等人的果蝇中央脑 LIF 模型为核心：约 **14 万个神经元**、约 **5000 万个突触连接**，并利用推断的神经递质身份决定突触正负。
- 集成 Lappalainen 等人的视觉运动通路模型，与 **NeuroMechFly** 身体模型结合；身体具有 **87 个独立关节**，运行在 **MuJoCo** 物理引擎上。
- 采用四步闭环：环境感觉事件 → 映射到感觉神经元/通路 → 更新连接组约束脑活动 → 读取少量下降输出驱动身体 → 身体运动再改变感觉输入。
- 当前脑体同步周期为 **15 ms**；控制接口是低维的，只读取少量已知与行为相关的下降神经元/运动神经元，如 **DNa01/DNa02**（转向）、**oDN1**（前进）、**MN9**（摄食）、天线相关下降神经元（梳理）。
- 已接入的感觉模态包括味觉、嗅觉、机械感觉和部分视觉；其中视觉输入目前更多是“装饰性”的，对行为输出影响还有限。

## Results
- 系统演示了一个闭环具身虚拟果蝇，能够在环境中利用味觉线索接近食物，并在“虚拟灰尘”触发下停下进行天线梳理，然后继续前进并开始进食。
- 文章未报告新的正式定量基准结果、统计显著性或与其他具身系统的数值对比；更像是**集成演示/研究平台**而非完成版论文结果。
- 关键规模指标包括：脑模型约 **140,000 neurons**、约 **50 million synapses**；身体模型含 **87 joints**；脑-体耦合更新步长为 **15 ms**。
- 作者明确声称当前成果主要是**集成既有已发表组件**，并非证明“仅靠结构就足以严格恢复完整行为谱”。
- 已展示/讨论的行为包括：**grooming、feeding、foraging**；**escape** 在无具身脑模型中可激活相关下降通路，但尚未在身体中完整实现。
- 最强的具体主张是：该系统把连接组脑模型与物理身体放入同一闭环中，产生了可识别的感觉驱动行为，因此可作为测试脑-体接口、连接组约束控制和具身脑模拟的研究试验台。

## Link
- [https://eon.systems/updates/embodied-brain-emulation](https://eon.systems/updates/embodied-brain-emulation)
