---
source: arxiv
url: https://arxiv.org/abs/2606.25215v1
published_at: '2026-06-23T22:23:35'
authors:
- Qing Lian
- Kent Yu
- Lei Zhang
topics:
- vision-language-action
- robot-foundation-model
- in-context-learning
- action-consequences
- robot-generalization
- manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Reflective VLA: In-Context Action Consequences Make VLAs Generalize

## Summary
## 摘要
Reflective VLA 将过去的观察-动作-结果三元组加入视觉-语言-动作策略，使机器人能在部署期间推断相机、校准和执行器作用效果。论文报告称，在没有测试时微调的情况下，该方法在 LIBERO 分布偏移下取得更高成功率，同时保持了较强的标准基准性能。

## 问题
- 反应式 VLA 根据当前指令和观察预测下一步动作，因此单帧可能无法识别相机到机器人的几何关系、机器人校准误差或执行器偏差。
- 这些隐藏的具身因素很重要，因为同一命令在新设置中可能产生不同的可见运动，从而损害部署泛化能力。
- 普通时间历史可以跟踪任务进度，但它可能无法把已执行动作和随后发生的场景变化绑定起来。

## 方法
- 模型维护一个滚动上下文，包含三元组 `(O_i, A_i, O'_i)`，其中 `O_i` 是动作前观察，`A_i` 是已执行的动作块，`O'_i` 是完整块时域 `C` 之后的观察。
- 先前的动作块在 VLM token 空间中嵌入为 8 个 token，并与第三人称图像、腕部图像、本体感知、语言和时间 token 一起输入。
- 连续 flow-matching 动作专家在预测下一个动作块前，会关注完整的共享 VLM prompt 和当前观察。
- 块因果掩码在一次前向传播中训练所有 `K` 个采样帧，同时阻止每个目标访问自身未来的动作和结果。
- 推理时，系统存储策略自己执行的动作块及观察到的结果，然后复用过去三元组的已缓存 VLM key 和 value。

## 结果
- 在标准 LIBERO 上，Reflective VLA 的平均成功率达到 97.6%，匹配的反应式 `pi_0.5` 基线为 96.9%，提升 +0.7 个百分点。
- 在 SimplerEnv-Bridge 上，它的平均成功率达到 78.2%，匹配的反应式基线为 72.9%，提升 +5.3 个百分点。
- 在 LIBERO-Plus 上，它的平均成功率达到 87.7%，匹配的反应式基线为 82.3%，提升 +5.4 个百分点。列出的最大增益出现在 Robot 偏移上：72.9% 对 50.0%，即 +22.9 个百分点。
- 在 LIBERO-Plus-Hard 上，它的平均成功率达到 68.8%，匹配的反应式基线为 64.6%，提升 +4.2 个百分点。Camera† 为 76.3% 对 74.0%，Robot Calibration† 为 61.3% 对 55.2%。
- 在 Camera、Camera† 和 Robot Calibration† 上的上下文消融显示，完整 `(O,A,O')` 上下文的平均成功率为 77.8%，反应式为 73.1%，仅 `O` 为 72.3%，`(O,A)` 为 73.8%。
- 使用完整三元组的上下文长度消融显示，平均成功率从 `K=1` 时的 73.1% 提升到 `K=2` 时的 75.3%、`K=4` 时的 76.7% 和 `K=8` 时的 77.8%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25215v1](https://arxiv.org/abs/2606.25215v1)
