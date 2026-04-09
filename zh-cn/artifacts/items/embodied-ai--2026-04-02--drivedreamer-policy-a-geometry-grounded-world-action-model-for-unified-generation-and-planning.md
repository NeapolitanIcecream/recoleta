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
DriveDreamer-Policy 是一个用于驾驶的 world-action model，在一个系统中同时预测深度、未来视频和驾驶动作。论文的核心观点是，显式几何信息同时有助于未来场景想象和规划，并且它在 Navsim 上报告了当前最好的规划分数，同时视频和深度生成效果也更好。

## 问题
- 现有的驾驶 VLA 和 world-action model 往往在没有显式 3D 几何的情况下预测动作或未来图像，这会削弱对遮挡、距离估计和安全相关规划的推理能力。
- 如果表征没有编码可行驶空间、场景布局和物理结构，那么视觉上看似合理的未来场景不一定对控制有用。
- 这对自动驾驶很重要，因为规划依赖于对 3D 场景如何随时间演变的判断，尤其是在罕见或安全关键的情形下。

## 方法
- 该模型使用多模态 LLM 主干 Qwen3-VL-2B 读取语言指令、多视角 RGB 图像和当前动作上下文，然后输出紧凑的查询嵌入。
- 它在这些嵌入之上接入三个轻量生成器：一个像素空间深度生成器、一个潜在视频生成器，以及一个基于扩散的轨迹动作生成器。
- 查询组遵循固定的因果顺序：深度查询先提供给视频查询，二者再提供给动作查询。简单说，模型先预测几何，再预测未来外观，最后预测驾驶动作。
- 深度以单目深度图的形式显式生成，并作为几何支架用于未来视频预测和规划。
- 该系统是模块化的：可以只运行规划，也可以运行带想象的规划，或用于仿真和数据合成的完整世界生成。

## 结果
- 在 Navsim v1 上，DriveDreamer-Policy 达到 **89.2 PDMS**，高于 PWM 的 **88.1**、WoTE 的 **88.3**、DriveVLA-W0 的 **88.4** 和 AutoVLA 的 **89.1**。
- 在 Navsim v2 上，它达到 **88.7 EPDMS**。论文称这比前一种方法高 **+2.6**；表格中 DriveVLA-W0 为 **86.1**。
- 在视频生成上，**FVD** 从 PWM 的 **85.95** 降到 **53.59**，下降 **32.36**。**LPIPS** 也从 **0.23** 改善到 **0.20**，而 **PSNR** 为 **21.05**，PWM 为 **21.57**。
- 在深度生成上，论文报告 **AbsRel 8.1**、**δ1 92.8**、**δ2 98.6**、**δ3 99.5**。一个微调后的 PPD 基线得到 **AbsRel 9.3**、**δ1 91.4**、**δ2 98.3**、**δ3 99.5**。
- 论文称消融实验表明，显式深度学习能为视频想象提供互补收益，并提高规划鲁棒性，但这里的摘录没有包含消融表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01765v1](http://arxiv.org/abs/2604.01765v1)
