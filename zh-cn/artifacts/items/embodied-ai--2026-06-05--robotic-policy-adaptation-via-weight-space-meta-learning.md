---
source: arxiv
url: https://arxiv.org/abs/2606.07217v1
published_at: '2026-06-05T12:29:28'
authors:
- Christian Bianchi
- Siamak Yousefi
- Alessio Sampieri
- Andrea Roberti
- Luca Rigazio
- Fabio Galasso
- Luca Franco
topics:
- vision-language-action
- robot-policy-adaptation
- weight-space-meta-learning
- lora-adaptation
- zero-shot-robot-learning
- libero-benchmark
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Robotic Policy Adaptation via Weight-Space Meta-Learning

## Summary
## 摘要
WIZARD 通过从语言指令和一段短演示视频预测任务专属的 LoRA 权重，来适配一个冻结的视觉-语言-动作机器人策略。它去掉了目标任务的动作标签和测试时微调，并在保留出的 LIBERO 任务上报告了大幅提升。

## 问题
- 大型 VLA 机器人策略在未见过的操作任务上仍然会失败，而且通常需要带动作标签的演示和针对每个新任务的微调。
- 这会增加数据采集、计算和适配器存储成本，机器人才能处理新任务。
- 论文给出的适配差距很大：预训练的 $\pi_{0.5}$ 在 LIBERO-Spatial 上成功率为 0%，在相关的 LIBERO 数据集上微调后达到 19%，而直接在目标任务上微调可达 94%。

## 方法
- WIZARD 先在元训练集中的任务上训练 LoRA 专家适配器，同时保持 VLA 主干冻结。
- 它用冻结的 VLA 编码器分别编码任务语言提示和视觉演示，然后把多个回合的嵌入平均成一个任务嵌入。
- 一个元网络学习从任务嵌入到专家 LoRA 权重的映射，并使用权重重建、逐层尺度预测和余弦对齐损失。
- LoRA 张量按 VLA 组件来组织，视觉、语言和动作部分分开，这样生成器会遵守策略架构。
- 在推理时，新提示和短视频会在一次前向传播中生成一个 LoRA 适配器；机器人策略随后使用这个生成的适配器运行，不做梯度更新。

## 结果
- 在保留出的 LIBERO-Spatial 上，WIZARD 的平均成功率为 0.40；MT-VLA 配合 $\pi_{0.5}$ 为 0.19，MT-VLA 配合 OpenVLA-OFT 为 0.09，最近邻适配器检索为 0.02，任务专属专家为 0.97。
- 在单个 LIBERO-Spatial 任务上，WIZARD 在任务 1 达到 0.90，任务 3 达到 0.82，任务 4 达到 0.84；在任务 6 上达到 0.28，而表中最强的 MT-VLA 基线只有 0.02，提升了 14 倍。
- 在保留出的 LIBERO-Goal 上，WIZARD 的平均成功率为 0.22；MT-VLA 配合 $\pi_{0.5}$ 为 0.14，OpenVLA-OFT 为 0.05，最近邻检索为 0.02，专家为 0.93；任务 5 和任务 9 都达到 0.86。
- 在保留出的 LIBERO-Object 上，性能较低，但仍高于基线：WIZARD 的平均成功率为 0.03，MT-VLA 配合 $\pi_{0.5}$ 为 0.01，最近邻检索和 OpenVLA-OFT 都是 0.00；专家平均为 0.97。
- 在 LIBERO-10 的子任务指标上，WIZARD 的 A/B 子任务平均成功率分别为 0.09/0.07；MT-VLA 配合 $\pi_{0.5}$ 为 0.03/0.03，OpenVLA-OFT 为 0.01/0.01；文中说完整任务的零样本完成率仍然是 0.00。
- 摘要声称，在未见过的数据集集合上最高可提升约 2 倍，在未见过的任务上最高可提升约 14 倍。文中还描述了一个真实的 Franka Emika Panda 测试，包含 7 自由度机械臂、三台 RealSense 相机、15 Hz 的 VLA 输出和 1 kHz 的底层控制，但节选中没有给出真实世界的成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07217v1](https://arxiv.org/abs/2606.07217v1)
