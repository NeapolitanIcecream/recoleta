---
source: arxiv
url: http://arxiv.org/abs/2603.09465v1
published_at: '2026-03-10T10:19:07'
authors:
- Jiajun Cao
- Xiaoan Zhang
- Xiaobao Wei
- Liyuqiu Huang
- Wang Zijian
- Hanzhen Zhang
- Zhengyu Jia
- Wei Mao
- Hao Wang
- Xianming Liu
- Shuchang Zhou Liu
- Yang Wang
- Shanghang Zhang
topics:
- autonomous-driving
- vision-language-action
- knowledge-distillation
- trajectory-planning
- perception-planning
- closed-loop-evaluation
relevance_score: 0.67
run_id: materialize-outputs
---

# EvoDriveVLA: Evolving Autonomous Driving Vision-Language-Action Model via Collaborative Perception-Planning Distillation

## Summary
EvoDriveVLA提出一种面向自动驾驶VLA模型的协同蒸馏框架，同时改进感知与规划。核心思想是用“自锚定”保护视觉表征、用“oracle教师”提供更强轨迹监督，从而提升开环和闭环驾驶性能。

## Problem
- 现有自动驾驶VLA在微调时，解冻视觉编码器容易破坏预训练得到的通用感知能力，导致感知退化。
- 长时域轨迹规划容易不稳定；而常规蒸馏中的教师若与学生训练条件相同，规划能力并没有明显优势，难以提供高质量指导。
- 现有多轨迹蒸馏通常依赖预定义规划词表，轨迹多样性和场景适应性仍受限，这会影响真实驾驶中的泛化与安全性。

## Approach
- 提出**collaborative perception-planning distillation**：把感知蒸馏和规划蒸馏联合起来，而不是只蒸馏最终轨迹。
- 在感知侧，使用**self-anchored visual distillation**：先复制学生当前视觉编码器作为“自锚定教师”，训练时让学生视觉token不要偏离太多，从而在适应驾驶任务时保留原有视觉能力。
- 设计**AnchorFormer**，利用指令、车辆状态和真实未来轨迹，为不同视觉区域分配不同锚定强度；与未来轨迹更相关的关键区域被更强约束。
- 在规划侧，构建使用未来图像与未来自车状态的**future-aware oracle teacher**，先生成粗轨迹，再做**coarse-to-fine refinement**得到更优轨迹候选。
- 再通过**MC-dropout sampling**以较低额外开销生成更多高质量、多样化候选，并选择与真值交叉熵最小的候选作为软目标，对学生的隐藏状态和logits做双层蒸馏。

## Results
- 在**nuScenes开环评测**上取得SOTA。以**ST-P3 protocol**为例，EvoDriveVLA的平均L2误差为**0.26 m**，优于**DiMA 0.27 m**、**OpenDriveVLA 0.33 m**、**OmniDrive 0.33 m**；3s L2为**0.43 m**，优于**DiMA 0.44 m**。
- 在**nuScenes / ST-P3 collision**上，平均碰撞率为**0.06%**，与**DistillDrive 0.06%**持平，优于**DiMA 0.08%**、**OpenDriveVLA 0.10%**；3s collision为**0.12%**，优于**DiMA 0.15%**。
- 在**nuScenes开环评测（UniAD protocol）**上，平均L2为**0.52 m**，优于**DiMA 0.57 m**、**OpenDriveVLA 0.67 m**、**GPT-Driver 0.84 m**；其中1s/2s/3s L2分别为**0.16/0.44/0.96 m**。
- 但在**UniAD protocol collision**上并非所有指标都最优：EvoDriveVLA平均碰撞率为**0.12%**，高于**DiMA 0.07%**与**OpenDriveVLA 0.30%**中的最优项分量表现不一致；例如2s collision为**0.02%**优于**DiMA 0.05%**，但3s为**0.33%**高于**DiMA 0.16%**。
- 在**NAVSIM闭环 navtest**上，EvoDriveVLA的**PDMS为85.3**，优于**PARA-Drive 84.0**、**TransFuser 84.0**、**UniAD 83.4**、**QwenVL2.5-8B 83.3**；同时**EP=81.1**，高于**UniAD 78.8**与**InternVL3-8B 78.9**。
- 闭环其他指标也达到最佳或并列最佳：**NC 98.0**、**DAC 93.3**、**TTC 93.1**、**Comfort 100**，整体显示其不仅开环预测更准，也能提升真实决策闭环表现。

## Link
- [http://arxiv.org/abs/2603.09465v1](http://arxiv.org/abs/2603.09465v1)
