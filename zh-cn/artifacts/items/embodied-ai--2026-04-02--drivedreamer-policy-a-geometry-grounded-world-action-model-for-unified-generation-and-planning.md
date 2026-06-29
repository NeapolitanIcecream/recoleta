---
source: arxiv
url: http://arxiv.org/abs/2604.01765v1
published_at: '2026-04-02T08:33:18'
authors:
- Yang Zhou
- Xiaofeng Wang
- Hao Shao
- Letian Wang
- Guosheng Zhao
- Jiangnan Shao
- Jiagang Zhu
- Tingdong Yu
- Zheng Zhu
- Guan Huang
- Steven L. Waslander
topics:
- world-action-model
- autonomous-driving
- geometry-grounding
- video-prediction
- motion-planning
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning

## Summary
## 摘要
DriveDreamer-Policy 是一个驾驶世界-动作模型，把深度、未来视频和驾驶动作放在同一个系统里预测。它的核心主张是，显式几何信息能同时帮助想象和规划；在 Navsim 上，它报告了更高的规划分数，以及更好的视频和深度生成结果。

## 问题
- 现有的驾驶 VLA 和世界-动作模型往往只预测动作或未来图像，没有显式的 3D 几何，这会削弱遮挡推理、距离估计和安全相关规划。
- 如果表示里没有空旷空间、布局和物理结构，视觉上合理的未来并不一定对控制有用。
- 这对自动驾驶很重要，因为规划依赖 3D 场景如何随时间变化，尤其是在罕见或安全关键的情况下。

## 方法
- 模型使用多模态 LLM 主干 Qwen3-VL-2B 读取语言指令、多视角 RGB 图像和当前动作上下文，然后输出紧凑的查询嵌入。
- 它把三个轻量生成器接到这些嵌入上：像素空间深度生成器、潜空间视频生成器，以及用于轨迹的基于扩散的动作生成器。
- 查询组遵循固定的因果顺序：深度查询先于视频查询，二者再先于动作查询。简单说，模型先预测几何，再预测未来外观，最后预测驾驶动作。
- 深度以单目深度图的形式显式生成，并作为未来视频预测和规划的几何支架。
- 这个系统是模块化的：它可以只做规划、做带想象的规划，或者做完整的世界生成，用于仿真和数据合成。

## 结果
- 在 Navsim v1 上，DriveDreamer-Policy 达到 **89.2 PDMS**，高于 PWM 的 **88.1**、WoTE 的 **88.3**、DriveVLA-W0 的 **88.4** 和 AutoVLA 的 **89.1**。
- 在 Navsim v2 上，它达到 **88.7 EPDMS**；论文写明这比前一个方法高 **+2.6**，表格里 DriveVLA-W0 是 **86.1**。
- 在视频生成上，FVD 从 PWM 的 **85.95** 降到 **53.59**，下降 **32.36**。LPIPS 也从 **0.23** 降到 **0.20**，而 PSNR 为 **21.05**，PWM 为 **21.57**。
- 在深度生成上，它报告 **AbsRel 8.1**、**δ1 92.8**、**δ2 98.6**、**δ3 99.5**。一个微调后的 PPD 基线是 **AbsRel 9.3**、**δ1 91.4**、**δ2 98.3**、**δ3 99.5**。
- 论文声称消融实验显示，显式深度给视频想象带来互补收益，并提高规划鲁棒性，但节选里没有给出消融表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01765v1](http://arxiv.org/abs/2604.01765v1)
