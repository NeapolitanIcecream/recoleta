---
source: hn
url: https://eon.systems/updates/embodied-brain-emulation
published_at: '2026-03-15T23:44:34'
authors:
- LopRabbit
topics:
- embodied-neuroscience
- connectome-constrained-model
- brain-body-integration
- neuromechanical-simulation
- drosophila
relevance_score: 0.42
run_id: materialize-outputs
---

# How the Eon Team Produced a Virtual Embodied Fly

## Summary
这篇文章介绍了一个“虚拟具身果蝇”原型：把果蝇连接组约束的脑模型、视觉模型和物理身体仿真整合成闭环系统，用于演示感知驱动的导航、梳理和进食。它更像一个研究平台和概念验证，而非完成的、经过严格量化验证的通用行为模型。

## Problem
- 目标是把**脑模型**真正接到**身体与环境**上，验证连接组约束的神经动力学能否在闭环中控制具身行为。
- 这很重要，因为仅有离体神经仿真无法回答“神经活动如何通过身体与环境反馈形成行为”这一核心问题。
- 难点在于脑-身接口：如何把特定感觉输入映射到神经元活动，以及把下降神经元活动映射成关节力矩、步态、转向、梳理和进食等动作控制。

## Approach
- 将多个已发表组件集成：**FlyWire/Shiu 等的中央脑 LIF 模型**、**Lappalainen 等的视觉运动通路模型**、以及 **NeuroMechFly** 物理身体模型。
- 脑模型规模约 **140,000 个神经元**、约 **5,000 万个突触连接**；身体模型含 **87 个独立关节**，运行在 **MuJoCo** 中。
- 系统采用四步闭环：环境感觉事件映射到感觉神经元/通路 → 连接组约束脑模型更新活动 → 选定下降输出转成低维动作命令 → 身体运动改变感觉，再反馈回脑。
- 当前脑-身同步周期为 **15 ms**：先计算脑对感觉输入的反应，再模拟身体接下来的 15 ms 响应。
- 动作控制不是完整生物运动层级，而是用少量已知功能的下降神经元作为“控制手柄”，驱动模仿学习得到的身体控制器，例如转向（DNa01/DNa02）、前进（oDN1）、梳理、以及进食相关运动元件。

## Results
- 文中**没有提供系统级定量评测结果**，没有给出成功率、回报、轨迹误差、神经预测分数或与其他 embodied agent 的数值对比。
- 文章声称该原型已能在演示中完成一个闭环行为序列：利用**不可见味觉线索**朝食物导航、在“虚拟灰尘”积累后停止并进行**触角梳理**、随后继续前进并**开始进食**。
- 已接入的核心规模包括：中央脑 **~140k neurons**、**~50M synapses**；视觉模型覆盖 **64 visual cell types**、跨视觉场的**数万神经元**；身体模型有 **87 joints**；脑身耦合时间步长为 **15 ms**。
- 作者明确说明视觉目前对行为输出的影响仍较弱、部分是“**decorative**”；例如 looming 相关神经元可在脑模型中激活逃逸相关下降神经元，但**逃逸行为尚未在身体中实现**。
- 主要贡献被定位为**集成性突破**而非新的单模块 SOTA：把现有连接组脑模型、视觉模型和神经力学身体首次拼成一个可运行的虚拟具身果蝇闭环平台。
- 作者同时强调这**不能证明仅靠结构就足以恢复完整行为 repertoire**；缺少学习、可塑性、内稳态/动机状态、更完整感觉与下降控制接口，以及严格科学验证。

## Link
- [https://eon.systems/updates/embodied-brain-emulation](https://eon.systems/updates/embodied-brain-emulation)
