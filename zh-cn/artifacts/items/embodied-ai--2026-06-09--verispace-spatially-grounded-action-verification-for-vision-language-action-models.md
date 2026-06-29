---
source: arxiv
url: https://arxiv.org/abs/2606.10568v1
published_at: '2026-06-09T08:31:59'
authors:
- Guiyu Zhao
- Longteng Guo
- Junyou Zhu
- Jun Fu
- Yanghong Mei
- Bin Cao
- Jie Jiang
- Xingjian He
- Jing Liu
topics:
- vision-language-action
- action-verification
- robot-manipulation
- spatial-reasoning
- rgb-d-perception
- test-time-scaling
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models

## Summary
## 摘要
VeriSpace 是一个用于视觉-语言-动作机器人策略的测试时动作验证器。它采样多个动作，用 RGB-D 空间推理打分，然后执行得分最高的动作。

## 问题
- VLA 策略通常只预测一个动作并立刻执行，所以很小的位姿或夹爪误差就可能导致抓取失败、碰撞，或任务推进错误。
- 现有从 2D 图像给候选动作打分的验证器，可能看不出接触、间隙和物体对齐上的细小 3D 差异。
- 这个问题很重要，因为机器人动作会改变物理场景，坏动作会让后续恢复更难，或者更不安全。

## 方法
- 一个冻结的 VLA 策略采样候选 7D 动作，包括 6-DoF 末端执行器运动和夹爪指令。VeriSpace 对每个候选动作打分，并选出排名最高的动作。
- 验证器使用 RGB-D 输入。它用相机参数把深度反投影到 3D 场景坐标，再用正弦特征和 MLP 编码这些坐标。
- 双路径场景编码同时生成显式 3D 几何 token 和视觉 token，并把 3D 位置信息注入 CLIP 图像特征。
- 几何引导的局部聚合使用最远点采样和 3D 半径邻域，捕捉物体表面、边缘、缝隙和可能接触区域附近的局部形状线索。
- 训练使用 Bradley-Terry 成对偏好损失来做动作排序，同时用 chain-of-thought 空间推理的交叉熵监督。文中报告的验证器使用带 LoRA 的 LLaVA-7B。

## 结果
- 在 SimplerEnv-WidowX 上，使用 OpenVLA 时，4 个任务、每个任务 50 次试验的平均成功率从 37.0% 升到 55.0%，提高了 18.0 个百分点。
- 在同一 OpenVLA 设置下，VeriSpace 比列出的最强验证器基线 Robomonkey 平均高 14.5 个百分点：55.0% 对 40.5%。
- OpenVLA 各任务的提升分别是：Eggplant in Basket 从 54.0% 到 76.0%（+22.0），Carrot on Plate 从 22.0% 到 34.0%（+12.0），Stack Cubes 从 28.0% 到 62.0%（+34.0），Spoon on Towel 从 44.0% 到 48.0%（+4.0）。
- 使用 π0-FAST 时，平均成功率从 57.0% 升到 60.5%，提高了 3.5 个百分点。该块中列出的最强验证器基线是 Robomonkey，得分 58.5%。
- 论文说 VeriSpace 在 SIMPLER 上比之前最好的方法高 13.0 个百分点，但给出的表格摘录显示，在列出的 OpenVLA 验证器基线中，它的优势更大，为 14.5 个百分点。
- 摘录说真实世界的分布内和分布外实验都有提升，但可见文本没有给出真实世界的成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10568v1](https://arxiv.org/abs/2606.10568v1)
