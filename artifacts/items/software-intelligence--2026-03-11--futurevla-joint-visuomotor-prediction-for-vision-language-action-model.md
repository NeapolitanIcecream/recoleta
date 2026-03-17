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
- robotics
- world-models
- future-prediction
- multimodal-learning
relevance_score: 0.32
run_id: materialize-outputs
---

# FutureVLA: Joint Visuomotor Prediction for Vision-Language-Action Model

## Summary
FutureVLA针对机器人视觉-语言-动作模型中的“如何预见未来并据此更好行动”问题，提出了联合视觉-运动预测框架。其核心是把场景视觉约束与连续动作动力学解耦后再融合，作为未来先验去指导下游VLA模型。

## Problem
- 现有未来指导方法要么显式重建未来视频，容易把容量浪费在与任务无关的视觉细节上，导致表示被视觉信息主导。
- 要么只用稀疏帧对学习隐式未来表示，破坏时间连续性，与机器人连续多步动作块不匹配。
- 这很重要，因为机器人动作受环境几何和可操作性严格约束；若不能联合建模“看见什么”和“如何动”，长时序、真实世界操作会更不稳定。

## Approach
- 提出两阶段框架：先做**Joint Visuomotor Pretraining**，再做**Embedding-Guided VLA Post-training**。
- 预训练时输入连续多帧视频，用冻结的3D-VAE压缩成时序token，而不是只看稀疏帧对，从而保留动作所需的时间连续性。
- 设计**Joint Visuomotor Gating (JVG)**：把表示分成视觉流和运动流；视觉流只负责保留初始场景状态，运动流只负责连续物理控制，并通过门控交叉注意力按需查询视觉约束。
- 训练监督也解耦：视觉流重建首帧潜表示，运动流预测动作块；最终得到联合视觉-运动嵌入，再通过潜表示对齐把这些未来先验迁移到下游VLA中，且推理架构无需修改。

## Results
- 论文声称整体上，FutureVLA相比**无联合视觉-运动嵌入指导**的基线，在**SimplerEnv**上平均提升**11.4%**，在**真实机器人操作**上提升**21.7%**。
- 在**SimplerEnv / Google robot / Visual Matching**中，FutureVLA-GT平均**80.1**，高于GR00T-N1.5的**35.2**，绝对提升**44.9**；FutureVLA-OT平均**77.6**，高于OpenVLA-OFT的**47.5**，提升**30.1**。其中“Put in Drawer”从**7.4**提升到**85.2**（GT）最显著。
- 在**SimplerEnv / WidowX**中，FutureVLA-GT平均**71.9**，优于GR00T-N1.5的**61.9**、UniVLA的**47.9**和Villa-X的**40.8**；FutureVLA-OT为**63.6**。作者还报告对无JVPM版本，GT和OT都各自提升**9.4**点（如GT从**62.5**到**71.9**）。
- 在**LIBERO**上，FutureVLA-GT平均**98.3**、FutureVLA-OT平均**98.2**，高于UniVLA的**95.2**、\(\pi_0\)的**94.2**、GR00T-N1.5的**93.9**。在**Long**任务上，FutureVLA-GT达到**96.0**，相对UniVLA的**92.0**提升**4.0**点。
- 在**真实机器人四项任务**中，FutureVLA-GT平均成功率**70.0%**，比\(\pi_0\)高**26.7%**。文中强调提升在需要细粒度、连续控制的接触丰富任务（如白板擦写）上尤为明显，但摘录中未给出各单任务详细数值。

## Link
- [http://arxiv.org/abs/2603.10712v1](http://arxiv.org/abs/2603.10712v1)
