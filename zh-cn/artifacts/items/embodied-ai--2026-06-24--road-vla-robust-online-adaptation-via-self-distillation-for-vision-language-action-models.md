---
source: arxiv
url: https://arxiv.org/abs/2606.25800v1
published_at: '2026-06-24T13:17:59'
authors:
- Kejing Wang
- Toan Nguyen
- Minh Hoang Nguyen
- Simon Khan
- Flora D. Salim
topics:
- vision-language-action
- online-adaptation
- robot-foundation-model
- self-distillation
- reinforcement-learning
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ROAD-VLA: Robust Online Adaptation via Self-Distillation for Vision-Language-Action Models

## Summary
## 摘要
ROAD-VLA 通过把稀疏奖励转成 token 级动作监督，在线适配 OpenVLA 风格的机器人策略。它用校准后的优势估计移动动作 token 的 logits，从当前策略构建教师模型，然后把策略蒸馏到这个教师模型。

## 问题
- VLA 策略需要在线适配，因为机器人在预训练后会遇到新的背景、物体布局、传感器噪声和执行错误。
- PPO 把每个优势估计作为采样动作的标量权重。对于高维自回归动作 token，这种监督较弱。
- 作者测试中，使用演示、检索经验或计划的基于文本的特权教师，未能提供可靠的低层动作指导。

## 方法
- ROAD-VLA 使用 OpenVLA 进行 on-policy rollout，并从稀疏任务奖励中估计逐步优势。
- 它在匹配批次统计量后，将内在优势估计与冻结的 PPO critic 估计混合；只有当两个估计符号相同时，才使用该参考。
- 它对混合后的优势进行标准化和裁剪，然后按这个带符号的权重上移或下移采样动作 token 的 logit。
- 移动后的 logits 在动作 token 空间中定义一个邻近的教师分布。学生模型在每个时间步、每个动作 token 上用 teacher-to-student KL 训练。
- 论文证明：当优势估计经过校准且学生模型与教师模型足够接近时，存在一个策略改进下界。

## 结果
- 评估覆盖 7 个操控环境和 3 类分布变化：3 个视觉鲁棒性任务、2 个组合推理任务、2 个执行鲁棒性任务。
- 基础模型是 OpenVLA-7B。ROAD-VLA 和 PPO 都从同一个 warm-up checkpoint 开始，该 checkpoint 在 140 条专家轨迹上微调得到。
- OpenVLA 动作使用 7 个离散动作 token，每个动作维度被离散化为 256 个 bin；ROAD-VLA 在这个 token 层级应用蒸馏。
- 作者称 ROAD-VLA 在几乎所有分布内和分布外设置中都优于 PPO，但所给摘录没有包含成功率、置信区间或逐任务表格。
- 摘录中报告的固定方法设置包括优势混合系数 alpha = 0.5、裁剪 c = 2.0、logit 扰动强度 eta = 1.0。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25800v1](https://arxiv.org/abs/2606.25800v1)
