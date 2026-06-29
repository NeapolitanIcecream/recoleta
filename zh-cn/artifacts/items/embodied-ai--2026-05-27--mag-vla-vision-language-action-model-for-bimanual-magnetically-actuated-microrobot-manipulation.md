---
source: arxiv
url: https://arxiv.org/abs/2605.28486v1
published_at: '2026-05-27T13:44:00'
authors:
- Yongchen Wang
- Kangyi Lu
- Lan Wei
- Dandan Zhang
topics:
- vision-language-action
- magnetic-microrobots
- bimanual-manipulation
- action-chunking
- microscale-robotics
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Mag-VLA: Vision-Language-Action Model for Bimanual Magnetically Actuated Microrobot Manipulation

## Summary
## 摘要
Mag-VLA 将一个 7B 视觉-语言模型改造成可控制两个装有磁体的微操纵器，用于微尺度双手操作。它根据显微镜图像、语言指令和机械臂位置，预测带有阶段感知的多步双臂运动。

## 问题
- 磁驱微型机器人难以控制，因为运动来自间接磁场，显微镜感知有限，而且执行器运动与微型机器人运动之间存在非线性耦合。
- 双臂磁控制可以完成单臂无法实现的重新定向和搬运，但两条机械臂必须在共享工作空间内协同运动。
- 在微创和微尺度操作任务中，更强的自主能力很重要，因为遥操作速度慢，而且需要很高的精度。

## 方法
- 该系统用 LoRA 微调 Qwen2.5-VL-7B，输入包括四帧 RGB 显微镜图像、语言提示，以及左右磁臂当前的二维位置。
- 一个基于运动感知的阶段分类器判断任务处于接近阶段还是运输阶段。
- 预测出的阶段会作为 Action Chunking Transformer 解码器的条件，后者一次输出未来五步双臂动作增量：ΔxL、ΔyL、ΔxR 和 ΔyR。
- 在部署时，重叠的动作块会通过时间集成进行融合，以平滑滚动预测控制。
- 训练使用了 75 个遥操作回合、20,724 帧 RGB 图像、三种任务配置和 70 种提示变体。

## 结果
- 在真实机器人测试中，Mag-VLA 在任务 A、B 和 C 上的接近成功率都达到 90%。
- 随着路径曲率增加，运输成功率下降：任务 A 为 80%，任务 B 为 70%，任务 C 为 50%。
- 在固定 Qwen2.5-VL-7B 的情况下，ACT 动作头的整体 RMSE 为 79.56 ticks，而 Diffusion Policy 为 153.52，Flow Matching 为 140.50。
- ACT 也改善了终点误差：平均值 133.74 ticks，中位数 107.82 ticks；Diffusion Policy 分别为 275.96/260.79，Flow Matching 分别为 265.75/251.25。
- ACT 的方向准确率为 98.26%，平均余弦相似度为 0.791，高于论文中报告的扩散和流动作头。
- 使用 ACT 时，阶段头的整体阶段准确率达到 97.21%，其中接近阶段为 97.36%，运输阶段为 97.04%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28486v1](https://arxiv.org/abs/2605.28486v1)
