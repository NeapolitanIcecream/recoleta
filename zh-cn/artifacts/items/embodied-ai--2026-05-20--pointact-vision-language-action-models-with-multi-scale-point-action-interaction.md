---
source: arxiv
url: https://arxiv.org/abs/2605.21414v1
published_at: '2026-05-20T17:10:31'
authors:
- Shizhe Chen
- Paul Pacaud
- Cordelia Schmid
topics:
- vision-language-action
- robot-manipulation
- point-clouds
- 3d-vla
- action-decoding
- spatial-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction

## Summary
## 摘要
PointACT 是一种面向机器人操控的 3D 感知视觉-语言-动作策略，把点云几何信息送入动作解码器。它的核心主张是，动作 token 需要与多尺度点特征直接、反复交互，才能预测精确的 3D 动作。

## 问题
- 现有 VLA 大多使用 2D 图像 token，这削弱了操控任务中的 3D 位姿、接触和空间推理能力。
- 以前的 3D 感知 VLA 往往只在高层加入深度或点特征，因此细粒度几何对最终动作输出的影响有限。
- 这个问题很重要，因为 RGB-D 传感很常见，而且许多机器人任务依赖精确几何，而不只是物体标签。

## 方法
- PointACT 使用冻结的 Qwen2.5-VL 骨干网络提取图像和语言特征，再配一个单独可训练的动作专家负责控制。
- Point Transformer v3 编码器处理彩色点云，并输出多尺度的层级点特征。
- 在解码时，动作 token 被广播到空间点窗口中，并通过瓶颈窗口自注意力与局部点 token 交互。
- 随后，动作 token 在不同窗口之间汇总信息，再与 VLM 特征做交叉注意力，让几何和语言共同约束动作预测。
- 该模型支持用于增量末端执行器动作的回归，也支持用于关键点位姿预测的点锚定分类。

## 结果
- 在 LIBERO 上，PointACT 在 4 个子集上的平均成功率为 96.0%：Spatial 97.4%、Object 99.6%、Goal 96.2%、Long 90.6%。
- 在同一 LIBERO 表中，PointACT 的平均表现比 SpatialVLA 高 17.9 个百分点：96.0% 对 78.1%。
- 相比 LIBERO 上复现的 EO1 基线，PointACT 的平均成功率提高 2.9 个百分点：96.0% 对 93.1%。
- 论文报告，在有挑战性的 RLBench-10Tasks 套件上，相比预训练 VLA 基线，成功率提升 10%；但摘录里没有给出完整的 RLBench 表格。
- 可训练的 PointACT 模块大约有 3 亿参数，在 1 cm 体素化后最多使用 4096 个点云点，并在 2 块 NVIDIA H100 GPU 上以批大小 128 训练 2 万到 5 万步。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21414v1](https://arxiv.org/abs/2605.21414v1)
