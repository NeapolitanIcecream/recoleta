---
source: arxiv
url: https://arxiv.org/abs/2605.25829v1
published_at: '2026-05-25T13:28:33'
authors:
- Xinzhe Chen
- Sihua Ren
- Liqi Huang
- Haowen Sun
- Mingyang Li
- Xingyu Chen
- Zeyang Liu
- Xuguang Lan
topics:
- vision-language-action
- robot-manipulation
- se3-trajectory-prediction
- action-space-alignment
- world-action-models
- sim2real
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation

## Summary
## 摘要
OASIS 是一个用于机器人操作的视觉-运动策略，它先预测 SE(3) 中的未来末端执行器位姿，再解码动作。论文称，这种带位姿监督的中间表示让 6-DoF 动作生成更容易，并提升了仿真、真机和分布外场景下的成功率。

## 问题
- VLA 模型和世界动作模型通常从图像、语言或未来视觉特征中解码 6-DoF 动作，但这些特征没有显式暴露刚体位姿结构。
- 这会让动作解码器自己推断目标末端执行器位姿，再把它转换成相对动作，从而可能影响空间泛化和长时程操作。
- 这个问题很重要，因为操作任务依赖精确的 3D 位置、旋转和夹爪时序，尤其是在相机视角、背景或任务布局变化时。

## 方法
- OASIS 使用一个 3D 感知编码器，把来自 Qwen2.5-0.5B VLM 的视觉-语言特征与来自冻结的 Depth Anything 3 DA3METRIC-LARGE 模型的度量深度特征结合起来。
- 一个 Transformer 轨迹预测器接收这一表示，并预测一个 8 步的、以相机坐标系表示的 SE(3) 末端执行器轨迹。
- 每个预测位姿都包含 3D 位置和轴角旋转，因此这条轨迹给动作解码器提供了明确的刚体位姿信息。
- 动作解码器关注带位姿监督的轨迹隐藏状态和当前机器人状态，然后输出一个 8 步动作块，其中包含 6-DoF 相对动作和夹爪指令。
- 训练使用标准专家演示和两个损失：L1 轨迹损失和 L1 动作损失，轨迹损失权重为 0.1；方法没有使用大规模机器人预训练或额外的空间标注。

## 结果
- 在 LIBERO 上，OASIS 报告的 Spatial、Object、Goal 和 Long 四项平均成功率为 97.6%，高于 Unified-VLA 的 95.5%、UniVLA 的 95.2%、QDepth-VLA 的 94.9% 和 pi0 的 94.1%。
- LIBERO 套件分数分别为 99.0% Spatial、98.8% Object、97.4% Goal 和 95.2% Long；OASIS 在没有大规模机器人预训练的情况下报告了这些结果。
- 在 CALVIN ABC 到 D 上，OASIS 报告平均序列长度为 4.57，五个连续任务的成功率为 83.3%，高于 DreamVLA 的 4.44 和 78.1%、Unified-VLA 的 4.41 和 75.1%，以及 VPP 的 4.33 和 76.9%。
- 消融结果显示，新增收益最大的是 SE(3) 轨迹预测器：LIBERO-Long 从 89.5% 提升到 95.2%，LIBERO-Spatial 从 91.6% 提升到 99.0%。
- 在 Franka Research 3 和 Kinova Gen3 机器人的真实世界测试中，OASIS 在多任务、空间关系和长时程套件上的平均成功率为 89.2%，在给出的对比中优于 pi0.5、RDT、Seer-Large 和 ACT。
- 在 Goal 任务的分布外扰动下，包括未见过的背景、改变后的相机视角和人工干扰，OASIS 报告平均成功率为 90.8%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.25829v1](https://arxiv.org/abs/2605.25829v1)
