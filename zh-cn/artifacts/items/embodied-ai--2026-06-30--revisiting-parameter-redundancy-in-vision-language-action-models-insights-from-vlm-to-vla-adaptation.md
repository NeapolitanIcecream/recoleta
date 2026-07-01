---
source: arxiv
url: https://arxiv.org/abs/2606.31382v1
published_at: '2026-06-30T09:10:31'
authors:
- Fengnian Zhang
- Tao Huang
- Siyu Xu
- Zhong Jin
- Chang Xu
topics:
- vision-language-action
- robot-policy-compression
- vlm-to-vla-adaptation
- parameter-pruning
- libero-benchmark
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Revisiting Parameter Redundancy in Vision-Language-Action Models: Insights from VLM-to-VLA Adaptation

## Summary
## 摘要
这篇论文研究 VLM 适配成 VLA 机器人策略后，哪些 VLM 参数仍然重要。论文称，基于 VLM 到 VLA 的权重变化进行剪枝，可以将 OpenVLA 和 pi_0.5 缩小 12%–30%，同时在不微调的情况下保留原始 LIBERO 成功率的约 90%。

## 问题
- VLA 模型继承了大型 VLM 骨干网络，这会增加机器人部署的内存和计算成本。
- 常见剪枝方法会损害机器人策略，然后使用 LoRA、RL 或 SVD 校正；这种做法会掩盖被移除的权重是否冗余。
- 论文询问，VLM 到 VLA 适配期间的权重变化，是否能识别出对动作生成重要的注意力头和 FFN 通道。

## 方法
- 作者比较成对模型：Prismatic 到 OpenVLA，以及 PaLI-Gemma 到 pi_0.5。
- 他们计算共享模块中 VLM 权重与 VLA 权重之间的相对 L2 权重差异。
- 他们按差异对注意力头和 FFN 通道排序，然后在不微调的情况下剪除最高差异或最低差异的子集，以测量其对 LIBERO 成功率的直接影响。
- 他们分别处理视觉、语言和投影器模块，因为同一种差异信号在不同模块中的含义不同。
- 他们使用观察到的模块模式构建联合剪枝方案，在移除参数的同时避免剪枝后恢复。

## 结果
- 在使用 OpenVLA 的 LIBERO-Spatial 上，基线成功率为 84.7%。按最低差异剪除 20% 的 LLM FFN 通道，会使微调前成功率降至 1.5%；剪除 20% 最高差异通道则保留 76.3%。
- 在同一 OpenVLA 设置中，进行 10k 步 LoRA 恢复会把受损模型重新提升到高成功率：20% 最低差异剪枝从 1.5% 升至 86.5%，50% 最低差异剪枝从 0.0% 升至 81.0%。
- OpenVLA DINOv2 在不同子模块上表现相反：剪除 12.5% 最高差异注意力头得到 1.6% SR，而剪除 20% 最低差异 FFN 通道得到 0.0% SR。
- OpenVLA 语言模块也表现出强敏感性：剪除 12.5% 最低差异 Llama2 注意力头得到 0.0% SR，而最高差异注意力头剪枝保留 84.3% SR。
- 对于 pi_0.5，摘录报告称，在视觉和语言中剪除最高差异 FFN 通道可保留约 95.0% SR，而移除最低差异通道会导致大幅下降。
- 最终主张是，在 OpenVLA 和 pi_0.5 上减少 12%–30% 参数，同时在没有剪枝后恢复的情况下维持原始 LIBERO 性能的约 90%；据报告，现有剪枝标准在相同的无恢复设置下会崩溃。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31382v1](https://arxiv.org/abs/2606.31382v1)
