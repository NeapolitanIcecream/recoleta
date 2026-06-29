---
source: arxiv
url: https://arxiv.org/abs/2606.23641v1
published_at: '2026-06-22T17:30:29'
authors:
- Haochen Zhang
- Yonatan Bisk
topics:
- vision-language-action
- robot-foundation-model
- instruction-following
- sharpness-aware-minimization
- robot-finetuning
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Flatness Preserves Instruction Following in Vision-Language-Action Models

## Summary
## 摘要
在 VLA 微调中使用锐度感知最小化，可以在使用相同微调数据的反事实机器人任务上提升指令遵循能力。论文认为，收益来自更平坦的参数区域，这会减少模型对视觉捷径的过拟合。

## 问题
- VLA 模型在小规模、有偏的机器人数据集上微调时，常会失去预训练得到的视觉-语言对齐能力。
- 这会导致指令盲视：机器人沿用训练时的视觉模式，忽略已改变的语言指令，例如拿起见过的物体，而不是指令要求的物体。
- 这个问题很重要，因为基于语言条件的机器人策略需要处理新的指令-场景组合，而不能为每一种组合都重新收集示范数据。

## 方法
- 该方法在标准 VLA 微调中加入锐度感知最小化（SAM），不需要新数据、架构改动或完整重训。
- 在每一步中，SAM 先沿着会增大损失的方向寻找一个小的权重扰动，然后用该扰动点上的梯度更新原始权重。
- 简单说，模型会被训练成在当前权重附近的一个小邻域内表现良好，这会偏向更平坦的解，并降低模型对小幅参数变化的敏感性。
- 实验主要将 SAM 应用于 π0.5 VLA，使用 AdamW 进行 30k 步 LIBERO 微调，然后在新的观察-指令配对上做零样本测试。
- 论文还测试了只作用于组件的 SAM、锐度指标、Hessian 最大特征值，以及与 SAM 结合的推理时引导。

## 结果
- 论文报告称，相对于默认微调的 π0.5 模型，指令遵循能力在 LIBERO-PRO Task 上相对提升 60.2%，在 LangGap 上提升 70.2%，在 LIBERO-CF 上提升 217%。
- 在 LIBERO-PRO Task 上，π0.5_SAM 的平均成功率达到 42.6%，相比之下 π0.5 为 26.6%，π0.5_cfg 为 30.2%，π0.5_LORA 为 6.75%，OpenVLA-OFT 为 1.4%。
- 在 LangGap 上，π0.5_SAM 的平均成功率达到 41.7%，相比之下 π0.5 为 24.5%，π0.5_cfg 为 29.4%，π0.5_LangGap 为 24.8%，π0.5_LORA 为 0.2%。
- 在 LIBERO-CF 上，π0.5_SAM 的平均成功率达到 47.8%，相比之下 π0.5 为 13.2%，π0.5_cfg 为 36.3%，π0.5 CAG 为 21.7%，OpenVLA-OFT CAG 为 11.3%，π0.5_LORA 为 5.7%。
- 锐度指标从 π0.5 的 0.012 降至 π0.5_SAM 的 0.005，Hessian 最大特征值从 0.93 降至 0.52。
- 在真实世界的 DROID 风格抓取放置测试中，SAM 将平均任务成功率从 13.8% 提高到 36.3%，相对提升 163%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23641v1](https://arxiv.org/abs/2606.23641v1)
