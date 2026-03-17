---
source: arxiv
url: http://arxiv.org/abs/2603.10712v1
published_at: '2026-03-11T12:39:55'
authors:
- Xiaoxu Xu
- Hao Li
- Jinhui Ye
- Yilun Chen
- Jia Zeng
- Xinyi Chen
- Linning Xu
- Dahua Lin
- Weixin Li
- Jiangmiao Pang
topics:
- vision-language-action
- world-model
- generalist-robot-policy
- sim2real
- robot-manipulation
relevance_score: 0.98
run_id: materialize-outputs
---

# FutureVLA: Joint Visuomotor Prediction for Vision-Language-Action Model

## Summary
FutureVLA面向机器人Vision-Language-Action模型中的“未来感知”问题，学习一种同时结合视觉约束与动作动力学的联合视动表征。核心思想是把视觉和电机控制信息先分开学，再通过门控交互重新结合，并把这种未来先验蒸馏到下游VLA中。

## Problem
- 现有VLA虽尝试加入未来监督，但常见做法要么重建未来画面，容易把容量浪费在任务无关的视觉细节上；要么只看稀疏帧对，破坏机器人动作本应具有的连续时间结构。
- 这会导致表示被静态场景外观主导，难以真正抓住“环境几何如何约束动作执行”的联合视动关系。
- 该问题重要，因为机器人控制不仅要看当前，还要预测动作后果；若未来建模不准，长时程和接触丰富任务会更容易失败。

## Approach
- 提出两阶段框架 **FutureVLA**：先做联合视动预训练，再做下游VLA后训练对齐。
- 预训练时输入连续多帧视频片段，而非稀疏帧对；先用冻结的3D-VAE把视频压成时序token，保留动态信息同时减少冗余。
- 设计 **Joint Visuomotor Gating (JVG)**：把表征拆成视觉流和动作流。视觉流只负责保留初始场景信息；动作流只负责预测连续动作块，从而减少“视觉主导”。
- 动作流通过门控交叉注意力按需查询视觉流中的空间/几何约束，相当于“动作负责怎么动，视觉负责在哪些约束下动”，最终形成联合视动嵌入。
- 后训练时不改下游VLA推理结构，只用一个轻量adapter把VLA中间表征对齐到这些联合视动嵌入，让单帧输入的VLA也能内化未来动态先验；并展示可兼容OFT-style与GR00T-style动作头。

## Results
- 论文声称在 **SimplerEnv** 上平均提升 **11.4%**，在**真实机器人**上提升 **21.7%**（相对“无联合视动嵌入指导”的基线）。
- 在 **Google robot / SimplerEnv / Visual Matching** 设置下，**FutureVLA-GT** 平均 **80.1**，高于 **GR00T-N1.5 35.2**，绝对提升 **44.9**；**FutureVLA-OT** 平均 **77.6**，高于 **OpenVLA-OFT 47.5**，提升 **30.1**。其中 **Put in Drawer** 从 **7.4** 提升到 **85.2**（GT）。
- 在 **WidowX / SimplerEnv** 上，**FutureVLA-GT** 平均 **71.9**，高于 **GR00T-N1.5 61.9**、**UniVLA 47.9**、**Villa-X 40.8**；**FutureVLA-OT** 为 **63.6**。论文还在消融中报告，引入JVPM指导后，两种架构都比各自 **wo/ JVPM** 平均提升 **9.4** 个点（GT: **62.5→71.9**，OT: **54.2→63.6**）。
- 在 **LIBERO** 上，**FutureVLA-GT/OT** 平均分别为 **98.3/98.2**，优于 **UniVLA 95.2**、**pi_0 94.2**、**GR00T-N1.5 93.9**。在长时程 **Long** 子集上，**FutureVLA-GT 96.0**，高于 **UniVLA 92.0**、**pi_0 85.2**、**WorldVLA 60.0**。
- 在 **真实Franka机器人** 四项任务上，**FutureVLA-GT** 平均成功率 **70.0%**，比 **pi_0** 高 **26.7%**。摘要还强调其在真实操作中相对基线有 **21.7%** 的显著增益，尤其在持续控制/接触丰富任务（如白板擦除）更明显。

## Link
- [http://arxiv.org/abs/2603.10712v1](http://arxiv.org/abs/2603.10712v1)
