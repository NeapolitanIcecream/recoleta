---
source: arxiv
url: https://arxiv.org/abs/2605.06175v2
published_at: '2026-05-07T12:56:58'
authors:
- Yuhua Jiang
- Junjie Lu
- Xinyao Qin
- Xiaoyu Chen
- Kaixin Wang
- Feifei Gao
- Li Zhao
topics:
- vision-language-action
- parameter-efficient-finetuning
- robot-manipulation
- mixture-of-experts
- svd-initialization
- libero-plus
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts

## Summary
## 摘要
VLA-GSE 通过向冻结的 VLM 骨干加入用 SVD 初始化的共享低秩专家和路由低秩专家，改进视觉-语言-动作模型的参数高效微调。论文报告称，在只训练 2.51% 模型参数的情况下，它在 LIBERO-Plus 零样本成功率上高于全量微调和 PEFT 基线。

## 问题
- VLA 模型需要把预训练的视觉-语言骨干适配到低层机器人动作，但机器人数据集有限，控制任务又要求精确行为。
- 全量微调可能过拟合机器人数据，并损害预训练的视觉-语言能力。
- LoRA 等标准 PEFT 方法能保留更多 VLM 知识，但论文称它们在精细操作任务上的适配不足。

## 方法
- VLA-GSE 冻结大部分 VLM 骨干，并训练一个结构化低秩更新和一个动作头。
- 对每个冻结权重矩阵，它执行 SVD。靠前的奇异分量初始化一个始终激活的泛化专家，后续互不重叠的奇异片段初始化专用专家。
- top-k 路由器按输入选择专用专家，泛化专家始终参与计算。
- 按专家进行的梯度尺度平衡会把每个专用专家的尺度设为其分配到的奇异值迹的倒数，使谱幅度不同的专家获得相近的更新大小。
- 骨干权重调整会从冻结权重中减去初始化专家贡献的期望值，使该模块在初始化时的期望输出匹配原始骨干。

## 结果
- VLA-GSE 在 4,551.85M 参数中训练 114.04M 个参数，占 2.51%；其中 48.41M 是 GSE 参数，65.62M 是动作头参数。
- 在 LIBERO-Plus 零样本评估中，VLA-GSE 的平均成功率达到 81.2%，高于 ABot-M0 的 80.5%、VLANeXt 的 80.1% 和 OpenVLA-OFT 的 69.6%。
- 在相同骨干的微调对比中，VLA-GSE 达到 81.2%，FFT 为 74.9%，LoRA 为 69.2%，MoLoRA 为 76.2%，GOAT 为 76.8%；相较 FFT 提升 +6.3 个百分点，相较 GOAT 提升 +4.4 个百分点。
- VLA-GSE 的 LIBERO-Plus 扰动分数为：Camera 64.4%、Robot 68.5%、Language 88.8%、Light 97.3%、Background 97.3%、Noise 79.4%、Layout 82.6%。
- 论文报告称，在四个任务和四种分布偏移下，VLA-GSE 的真实世界操作成功率为 82.5%，比 FFT 高 +16.7 个百分点。
- 论文称，VLA-GSE 在 VLA 微调后能把预训练多模态理解能力保持在接近 LoRA 的水平，而 FFT 和共同训练的 VLA 基线损失更多 VLM 能力；摘录未包含具体基准表数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06175v2](https://arxiv.org/abs/2605.06175v2)
