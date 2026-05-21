---
source: arxiv
url: https://arxiv.org/abs/2605.10942v1
published_at: '2026-05-11T17:59:56'
authors:
- Qiuxuan Feng
- Jiale Yu
- Jiaming Liu
- Yueru Jia
- Zhuangzhe Wu
- Hao Chen
- Zezhong Qian
- Shuo Gu
- Peng Jia
- Siwei Ma
- Shanghang Zhang
topics:
- world-action-models
- vision-language-action
- robot-manipulation
- world-model
- adaptive-gating
- zero-shot-generalization
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models

## Summary
## 摘要
HarmoWAM 是一种机器人操作策略，结合了视频世界模型、两个动作专家和一个学习得到的门控。它面向两类策略之间的差距：一类能在新场景中到达物体，另一类能以精细控制操作物体。

## 问题
- 现有 World Action Models 分为两种模式：先处理视频再推断动作的方法在到达物体方面表现较强，联合视频-动作建模在目标附近的精细操作方面表现更好。
- 在论文的双任务研究中，Imagine-then-Execute 在所有 OOD 移动案例中到达目标的结果均为 10/10，但交互成功率最低降至 2/10。Joint Modeling 在物体附近初始化时保持了 95% 的平均 OOD 交互成功率，但 OOD 移动成功率降至 32%。
- 这一点很重要，因为真实机器人任务同时需要长距离移动到正确物体，以及准确接触、抓取、堆叠、倾倒、书写或双臂协作。

## 方法
- HarmoWAM 使用 Wan2.2-TI2V-5B 作为世界模型，并在约 1.9M 条机器人轨迹上继续训练。它以 256x320 分辨率预测 13 个未来视频帧，并使用 5 个去噪步骤。
- 预测专家是一个 1B 参数的扩散 Transformer，包含 28 个 Transformer 块。它使用当前视觉、文本和世界模型潜在特征，生成时间上连续的动作块，用于精细交互。
- 反应专家使用预测的未来帧和世界模型潜在特征。DINOv2 提取视觉特征，然后由方向解码器将这些特征映射为机器人动作，用于移动和接近目标。
- Process-Adaptive Gating Mechanism 根据视觉 token 将当前阶段分类为移动或交互。推理时，分数高于 0.5 时将控制路由到预测专家；分数小于或等于 0.5 时将控制路由到反应专家。
- 训练分为两个阶段：先用 flow matching 微调世界模型，再用扩散损失、Smooth L1 动作损失和二元交叉熵门控损失微调动作专家和门控。

## 结果
- 评估覆盖 6 个真实世界任务：4 个单臂任务和 2 个双臂任务，每个任务有 100 条演示轨迹，并且每个任务有 20 个独立评估 episode。
- 在域内设置中，HarmoWAM 报告其平均表现比先前 VLA 模型高 15 个百分点，比先前 WAM 高 11 个百分点。
- 在包含背景、位置和物体变化的 OOD 设置中，HarmoWAM 报告其平均表现比先前 VLA 模型高 33 个百分点，比先前 WAM 高 29 个百分点。
- 动机研究报告称，Imagine-then-Execute 的交互成功率平均在域内低于 75%，在 OOD 中低于 55%，而 Joint Modeling 的 OOD 移动成功率降至 32%。
- 推理以 48 Hz 运行，动作块大小为 12。
- 论文还声称其在长时程真实世界部署中表现更强，但摘录未提供确切的长时程成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10942v1](https://arxiv.org/abs/2605.10942v1)
