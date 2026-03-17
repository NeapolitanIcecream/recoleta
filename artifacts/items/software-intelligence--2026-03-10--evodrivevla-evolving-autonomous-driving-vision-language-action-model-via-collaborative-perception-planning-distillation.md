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
- multimodal-learning
relevance_score: 0.38
run_id: materialize-outputs
---

# EvoDriveVLA: Evolving Autonomous Driving Vision-Language-Action Model via Collaborative Perception-Planning Distillation

## Summary
EvoDriveVLA 是一个面向自动驾驶的视觉-语言-动作蒸馏框架，目标是同时修复视觉编码器微调后感知退化和长时规划不稳定的问题。它把“保住原有视觉能力”和“用更强教师教轨迹规划”结合起来，在开放环与闭环评测中都取得了领先结果。

## Problem
- 现有自动驾驶 VLA 在解冻视觉编码器后，容易丢失预训练得到的稳健视觉表征，导致感知能力下降。
- 长时轨迹规划容易出现不稳定和误差累积；若教师与学生训练条件相同，教师本身并不比学生更会规划，蒸馏价值有限。
- 现有多轨迹蒸馏常依赖预定义规划词表，轨迹多样性和场景适应性仍受限，这会影响真实动态驾驶场景中的泛化与安全性。

## Approach
- 提出协同式感知-规划蒸馏框架 EvoDriveVLA，包含两部分：self-anchored visual distillation 与 oracle-guided trajectory distillation。
- 在感知侧，先复制学生的视觉编码器作为“自锚教师”，在微调时用它约束学生不要偏离原始视觉表征；同时用基于真实未来轨迹的 AnchorFormer 给关键视觉 token 更高约束权重。
- 在规划侧，构造一个“oracle 教师”：训练时额外看未来图像和未来自车状态，因此比学生拥有更强的未来感知和轨迹预测能力。
- oracle 教师先生成粗轨迹，再把粗轨迹喂回模型做 coarse-to-fine refinement，得到更准确、更平滑的候选轨迹。
- 再用 MC-Dropout 对隐藏状态做 10 次采样（dropout rate 0.1）扩充候选集，从中选与真值交叉熵最小的最佳轨迹，并在隐藏状态与输出分布两层共同蒸馏给学生。

## Results
- **nuScenes 开放环**：EvoDriveVLA 在 **ST-P3** 设置下达到 **Avg L2 = 0.26 m**、**Avg Collision = 0.06%**；对比 **DiMA** 的 **0.27 m / 0.08%**，分别改善 **0.01 m** 和 **0.02 个百分点**。
- **nuScenes 开放环**：在 **ST-P3** 的 3 秒 L2 / Collision 上，EvoDriveVLA 为 **0.43 m / 0.12%**，优于 **OpenDriveVLA** 的 **0.55 m / 0.22%**，分别降低 **0.12 m** 和 **0.10 个百分点**。
- **nuScenes 开放环**：在 **UniAD** 设置下，EvoDriveVLA 达到 **Avg L2 = 0.52 m**，优于 **DiMA** 的 **0.57 m** 与 **OpenDriveVLA** 的 **0.67 m**。
- **nuScenes 开放环**：在 **UniAD** 设置下，EvoDriveVLA 的 **Avg Collision = 0.12%**；该项低于 **OpenDriveVLA** 的 **0.30%**，但高于 **DiMA** 的 **0.07%**，说明其并非所有开放环子指标都绝对最优。
- **NAVSIM 闭环**：EvoDriveVLA 的 **PDMS = 85.3**，高于 **PARA-Drive** 的 **84.0**、**UniAD** 的 **83.4**、**QwenVL2.5-8B** 的 **83.3**，为表中最佳。
- **NAVSIM 闭环**：EvoDriveVLA 还取得 **NC 98.0**、**DAC 93.3**、**TTC 93.1**、**EP 81.1**、**Comfort 100**；其中 **EP 81.1** 高于 **PARA-Drive 79.3** 与 **UniAD 78.8**，显示其在闭环驾驶质量上有显著提升。

## Link
- [http://arxiv.org/abs/2603.09465v1](http://arxiv.org/abs/2603.09465v1)
