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
AnySlot 处理基于自然语言的槽位级机器人放置任务。在这类任务中，机器人需要在未见过的布局里选中准确的槽位，并以亚厘米级精度完成放置。它的方法是先把指令转换成一个明确的视觉目标标记，再用一个目标条件 VLA 策略执行放置。

## 问题
- 论文研究零样本槽位级放置：给定一条组合式语言指令，机器人必须在密集候选槽位中识别正确目标，并以足够高的精度放置物体，才能在物理上成功完成任务。
- 这类能力对精密装配和工厂自动化等场景很重要，因为选错隔间或对齐偏差很小都可能导致失败。
- 现有平坦式 VLA 策略把语言推理和运动控制混在一个模型里，而此前的模块化系统往往把目标简化成单个坐标点，这会丢失精确执行所需的槽位形状和边界信息。

## 方法
- AnySlot 使用两阶段流水线。高层 grounding 模块接收初始场景图像和语言指令，然后通过在目标槽位上放置一个彩色球体标记来编辑图像。
- 系统提取标记中心，结合深度图和相机标定将其提升到 3D，再将其重新投影到所有相机视角中，形成一致的叠加标记。这个叠加标记就是视觉目标。
- 一个目标条件 VLA 策略基于 π0.5 构建，使用 PaliGemma-3B 骨干网络和 flow-matching 动作专家。它接收多视角观测以及叠加后的标记，并输出连续机器人动作。
- 底层指令固定为一个简单模板，例如在蓝色球体引导下把物体移动到槽位中。基于语言的槽位推理留在高层模块中，底层策略只负责执行。
- 论文还提出了 SlotBench，这是一个基于 SAPIEN 的仿真基准，包含 9 类用于槽位级推理的任务：序数、尺寸、高度、距离、组合关系、否定、模糊语言、可供性和世界知识。

## 结果
- 论文称，AnySlot 在 SlotBench 的 9 个零样本槽位放置任务类别上，平均成功率接近 **90%**。
- SlotBench 使用很紧的几何约束：槽位尺寸约为 **0.03 m**，物体长度约为 **0.15 m**，并且只有当预测点距离真实槽位中心不超过 **0.02 m** 时，指令定位才算正确。
- 底层策略在一个合成仿真数据集上训练，其中物体位姿随机化包含最高 **0.05 m** 的平移噪声，然后在未见过的布局和指令上做零样本评估。
- 在可见的表格摘录中，一个平坦式 Diffusion Policy 基线在序数推理上只有 **16% success**，在其余展示的类别上都是 **0%**。这与论文的说法一致，即平坦式基线在大多数 SlotBench 任务上都会失败。
- 摘录没有给出 AnySlot 和所有基线的完整量化表，因此无法仅根据提供的文本完整还原各类别的精确提升、基线平均值和比较差距。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10432v2](http://arxiv.org/abs/2604.10432v2)
