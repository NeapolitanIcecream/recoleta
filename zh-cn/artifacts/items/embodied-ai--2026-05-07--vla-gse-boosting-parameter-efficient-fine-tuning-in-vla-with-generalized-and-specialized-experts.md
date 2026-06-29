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
VLA-GSE 通过在冻结的 VLM 骨干上加入由 SVD 初始化的共享和路由低秩专家，改进了视觉-语言-动作模型的参数高效微调。它报告在训练 2.51% 模型参数的情况下，LIBERO-Plus 的 zero-shot 成功率高于全量微调和 PEFT 基线。

## 问题
- VLA 模型需要把预训练的视觉-语言骨干适配到低层机器人动作，但机器人数据有限，控制又要求精确行为。
- 全量微调会在机器人数据上过拟合，并损害预训练的视觉-语言能力。
- 诸如 LoRA 之类的标准 PEFT 方法能保留更多 VLM 知识，但论文称它们在精细操作任务上的适配不足。

## 方法
- VLA-GSE 保留大部分 VLM 骨干冻结，只训练一个结构化的低秩更新和一个动作头。
- 对每个冻结权重矩阵，它先做 SVD。前几个奇异分量初始化一个始终激活的 generalized expert，后续不重叠的奇异分段初始化 specialized experts。
- 一个 top-k 路由器会按输入选择 specialized experts，而 generalized expert 始终使用。
- 按专家的梯度尺度平衡会让每个 specialized expert 的尺度与其分配到的奇异值迹成反比，这样奇异值规模不同的专家得到可比的更新幅度。
- 骨干权重调整会从冻结权重中减去预期的已初始化专家贡献，使该模块在初始化时在期望上与原始骨干一致。

## 结果
- VLA-GSE 训练了 4,551.85M 参数中的 114.04M，即 2.51%；其中 48.41M 是 GSE 参数，65.62M 是动作头参数。
- 在 LIBERO-Plus 的 zero-shot 评估中，VLA-GSE 的平均成功率达到 81.2%，高于 ABot-M0 的 80.5%、VLANeXt 的 80.1% 和 OpenVLA-OFT 的 69.6%。
- 在相同骨干的微调对比中，VLA-GSE 达到 81.2%，而 FFT 为 74.9%、LoRA 为 69.2%、MoLoRA 为 76.2%、GOAT 为 76.8%；相对 FFT 提升 6.3 个百分点，相对 GOAT 提升 4.4 个百分点。
- VLA-GSE 在 LIBERO-Plus 扰动评分中的结果为：Camera 64.4%、Robot 68.5%、Language 88.8%、Light 97.3%、Background 97.3%、Noise 79.4%、Layout 82.6%。
- 论文报告在四个任务和四种分布偏移下，真实世界操作成功率为 82.5%，比 FFT 高 16.7 个百分点。
- 论文称，VLA-GSE 在 VLA 微调后保留的预训练多模态理解能力接近 LoRA，而 FFT 和联合训练的 VLA 基线丢失了更多 VLM 能力；摘录中没有给出精确的基准表数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06175v2](https://arxiv.org/abs/2605.06175v2)
