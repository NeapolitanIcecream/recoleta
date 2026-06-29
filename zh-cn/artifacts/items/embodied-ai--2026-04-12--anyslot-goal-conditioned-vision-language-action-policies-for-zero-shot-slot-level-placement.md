---
source: arxiv
url: http://arxiv.org/abs/2604.10432v2
published_at: '2026-04-12T03:09:44'
authors:
- Zhaofeng Hu
- Sifan Zhou
- Qinbo Zhang
- Rongtao Xu
- Qi Su
- Ci-Jyun Liang
topics:
- vision-language-action
- goal-conditioned-policy
- zero-shot-manipulation
- slot-level-placement
- spatial-reasoning
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement

## Summary
## 摘要
AnySlot 面向自然语言条件下的槽位级机器人放置任务，要求机器人在未见过的布局中选中精确槽位，并以亚厘米级精度完成放置。它先把指令转换成一个明确的视觉目标标记，再用一个目标条件化的 VLA 策略执行放置。

## 问题
- 这篇论文研究零样本槽位级放置：给定一条复合语言指令，机器人必须在密集候选槽位中找出正确槽位，并把物体放到足够准确的位置，才能完成物理任务。
- 这类任务对精密装配和工厂自动化很重要，因为选错隔间，或者对齐偏差只有一点点，任务就会失败。
- 现有的平面式 VLA 策略把语言推理和运动控制放在一个模型里，之前的模块化系统又常把目标简化成单个坐标，这会丢掉精确执行所需的槽位形状和边界信息。

## 方法
- AnySlot 使用两阶段流程。高层对齐模块先读取初始场景图像和语言指令，然后在目标槽位上编辑图像，放置一个彩色球体标记。
- 系统提取这个标记的中心，结合深度图和相机标定把它提升到三维空间，再把它重新投影到所有相机视角中，形成一致的叠加层。这个叠加层就是视觉目标。
- 一个目标条件化的 VLA 策略以 π0.5 为基础，使用 PaliGemma-3B 主干和 flow-matching 动作专家，接收多视角观测和叠加后的标记，并输出连续机器人动作。
- 低层指令固定为简单模板，例如在蓝色球体引导下把物体移动到槽位中。基于语言的槽位推理保留在高层模块里，低层策略只负责执行。
- 论文还提出了 SlotBench，这是一个基于 SAPIEN 仿真的基准，包含 9 类槽位级推理任务：序数、大小、高度、距离、组合关系、否定、模糊语言、可供性和常识。

## 结果
- 论文声称 AnySlot 在 SlotBench 的 9 类零样本槽位放置任务上，平均成功率接近 **90%**。
- SlotBench 使用很紧的几何约束：槽位大小约为 **0.03 m**，物体长度约为 **0.15 m**，而且只有预测与真实槽位中心的距离在 **0.02 m** 以内时，才算指令正确。
- 低层策略先在合成模拟数据集上训练，物体位姿加入最多 **0.05 m** 的平移随机扰动，然后在未见过的布局和指令上做零样本评测。
- 从可见表格摘录来看，平面 Diffusion Policy 基线在序数推理上只有 **16%** 成功率，在其他展示类别上为 **0%**，这与论文关于平面基线在大多数 SlotBench 任务上失效的判断一致。
- 这段摘录没有给出所有基线和 AnySlot 的完整定量表，因此各类别的精确提升、基线平均值和比较差距无法从所提供文本中完整还原。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10432v2](http://arxiv.org/abs/2604.10432v2)
