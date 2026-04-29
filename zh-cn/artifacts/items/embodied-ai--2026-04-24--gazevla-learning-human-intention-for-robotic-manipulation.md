---
source: arxiv
url: http://arxiv.org/abs/2604.22615v1
published_at: '2026-04-24T14:46:03'
authors:
- Chengyang Li
- Kaiyi Xiong
- Yuan Xu
- Lei Qian
- Yizhou Wang
- Wentao Zhu
topics:
- vision-language-action
- human-to-robot-transfer
- gaze-modeling
- robot-manipulation
- few-shot-robot-learning
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# GazeVLA: Learning Human Intention for Robotic Manipulation

## Summary
## 摘要
GazeVLA 从第一人称人类视频中学习人类意图，并将这一信号迁移到机器人操作中。它把注视点作为意图信号，在动作之前先预测意图，并报告称，相比以往基于机器人数据或人类预训练的基线方法，它在少样本场景下表现更好，且分布外泛化更强。

## 问题
- 视觉-语言-动作模型仍然需要大量机器人演示数据，这类数据采集成本高，也很难扩展。
- 人类第一人称视频更容易采集，但直接迁移很难，因为人与机器人的身体结构和动作空间不同。
- 以往工作大多学习要执行**什么**动作。本文关注执行该动作的**原因**，并把意图作为桥梁。

## 方法
- 论文提出 **VLIA**（Vision-Language-Intention-Action），用**人类注视点**来建模意图，并将其作为感知与动作之间的中间步骤。
- 它在一个整理后的第一人称人类数据集上进行预训练。该数据集由 **13 个数据集**构成，包含**超过 1.5 亿帧**，使用了注视点、手部标注和语言信息。
- 模型使用 **PaliGemma** 作为视觉语言骨干，并使用 **conditional flow matching** 动作专家来生成连续动作。
- 在推理时，它遵循意图-动作链：先根据图像和指令预测离散化的注视点 token，再在该预测意图的条件下生成未来动作。
- 在后训练阶段，它按 **1:1 采样比例**混合少量机器人数据与人类数据；机器人数据没有意图标签，因此意图知识只来自人类监督。

## 结果
- 在人类预训练评估中，意图预测误差为**图像对角线的 4.8%**，在 **224×224** 图像上约为**11 像素**。手部运动重建达到 **4.71 cm** 的平均关键点误差和 **12.31°** 的手腕旋转误差。
- 在 **AV-ALOHA** 仿真基准上，分布内平均成功率为 **49**，优于 **pi0.5: 41**、**LFA: 43**、**H-RDT: 39** 和 **DP: 28**。
- 在带干扰物的 AV-ALOHA 分布外测试中，平均成功率为 **28**，高于 **pi0.5: 22**、**LFA: 14**、**H-RDT: 14** 和 **DP: 7**。
- 在光照变化的 AV-ALOHA 分布外测试中，平均成功率为 **27**，高于 **pi0.5: 23**、**H-RDT: 6** 和 **LFA/DP: 0**。论文称这相比 **pi0.5** 在 OOD 设置下有 **22% 的相对提升**。
- 在单项仿真任务上，它在 cube transfer ID 上达到 **100**，在 slot insertion OOD-distractors 上达到 **56**；作为对比，**pi0.5** 分别为 **94** 和 **47**。
- 在真实机器人实验中，摘录称它在夹爪任务和灵巧操作任务上都更强，每个任务只使用 **10 条机器人轨迹**和 **50 条人类轨迹**。文中给出一个明确数字：简单 pick-and-place 的成功率为 **85%**；同时称 screw tightening 的成功率达到 **pi0.5** 的 **2×**。摘录未包含 Figure 6 的完整数值表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22615v1](http://arxiv.org/abs/2604.22615v1)
