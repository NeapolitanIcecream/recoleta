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
HarmoWAM 是一个机器人操作策略，把视频世界模型、两个动作专家和一个学习到的门控机制结合在一起。它要解决这样一个问题：有些策略能在新场景里找到物体，但控制不够细；另一些策略能精细操作，但换到新场景时容易失效。

## 问题
- 现有的 World Action Models 分成两类：先视频后动作的推断方式在接近目标物体时表现更好，而联合视频-动作建模在目标附近的精细操作上更强。
- 论文的双任务研究显示，Imagine-then-Execute 在所有 OOD 迁移场景中的到达目标成功率都是 10/10，但交互成功率最低只有 2/10。Joint Modeling 在靠近物体初始化时，OOD 交互成功率平均为 95%，但 OOD 迁移成功率降到 32%。
- 这很重要，因为真实机器人任务既需要长距离移动到正确物体前，也需要准确接触、抓取、堆叠、倾倒、书写或双臂协作。

## 方法
- HarmoWAM 使用 Wan2.2-TI2V-5B 作为世界模型，并在约 190 万条机器人轨迹上继续训练。它以 256x320 分辨率预测 13 帧未来视频，去噪步骤为 5 步。
- 预测专家是一个 10 亿参数的扩散 Transformer，包含 28 个 Transformer block。它使用当前视觉特征、文本特征和世界模型的潜变量特征，生成时间上一致的动作片段，用于精细交互。
- 反应专家使用预测的未来帧和世界模型潜变量特征。DINOv2 提取视觉特征，然后由一个朝向解码器把这些特征映射成机器人动作，用于迁移和靠近目标。
- Process-Adaptive Gating Mechanism 根据视觉 token 判断当前阶段是迁移还是交互。推理时，分数高于 0.5 时控制权交给预测专家；分数不高于 0.5 时控制权交给反应专家。
- 训练分两阶段进行：先用 flow matching 微调世界模型，再用扩散损失、Smooth L1 动作损失和二元交叉熵门控损失微调动作专家和门控机制。

## 结果
- 评测覆盖 6 个真实世界任务：4 个单臂任务和 2 个双臂任务，每个任务有 100 条示范轨迹和 20 次独立评测回合。
- 在域内设置下，HarmoWAM 相比之前的 VLA 模型平均提升 15 个百分点，相比之前的 WAM 平均提升 11 个百分点。
- 在背景、位置和物体变化的 OOD 设置下，HarmoWAM 相比之前的 VLA 模型平均提升 33 个百分点，相比之前的 WAM 平均提升 29 个百分点。
- 动机研究报告说，Imagine-then-Execute 的交互成功率在域内平均低于 75%，在 OOD 场景中平均低于 55%；Joint Modeling 的 OOD 迁移成功率降到 32%。
- 推理速度为 48 Hz，动作片段长度为 12。
- 论文还声称它在更长时程的真实部署中表现更强，但摘要没有给出具体的长时程成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10942v1](https://arxiv.org/abs/2605.10942v1)
