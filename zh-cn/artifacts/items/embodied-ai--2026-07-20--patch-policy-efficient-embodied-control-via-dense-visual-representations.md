---
source: arxiv
url: https://arxiv.org/abs/2607.18236v1
published_at: '2026-07-20T17:59:41'
authors:
- Gaoyue Zhou
- Zichen Jeff Cui
- Ada Langford
- Bowen Tan
- Yann LeCun
- Lerrel Pinto
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Patch Policy: Efficient Embodied Control via Dense Visual Representations

## Summary
## 摘要
Patch Policy 是一种轻量级 Transformer 策略，使用稠密的预训练 Vision Transformer patch 特征进行机器人控制，而不是将每张图像压缩为一个全局 token，或使用拥有数十亿参数的视觉语言动作模型。在四个仿真基准和三个真实世界操作任务中，该方法报告了更高的控制性能，同时显著减少了参数量并保持较低延迟。

## 问题
- 全局池化和 CLS token 会丢失精确操作所需的细粒度空间信息。
- 大型视觉语言动作模型能够保留稠密视觉输入，但训练和推理成本高，限制了其在高频控制中的应用。
- 论文探讨了冻结的、在互联网数据上预训练的稠密视觉特征，能否在不承担完整 VLM 成本的情况下改进标准视觉运动策略。

## 方法
- Patch Policy 将每次观测中的全部 Vision Transformer patch 嵌入直接输入基于 Transformer 的策略，而不是将其池化为一个向量。
- 分块因果注意力掩码允许同一帧内的 patch 之间进行完全双向注意力，同时保持跨时间的因果注意力。
- 该架构兼容标准动作头，包括 VQ-BeT 和 Diffusion Policy，并支持图像目标或向量目标。
- 视觉编码器保持冻结，因此只训练策略；实验使用了包括 DINOv2、DINOv3、WebSSL、V-JEPA 2 和 SigLIP 2 在内的表征。

## 结果
- 在 Push-T、LIBERO Goal、BlockPush 和 Cube 上，使用 WebSSL patch 特征的 Diffusion Policy 得分分别为 0.80、0.98、1.65 和 1.73；对应的全局特征基线得分分别为 0.79、0.99、1.34 和 0.21。
- 在每项任务进行 20 次试验的真实机器人任务中，DINOv2 Patch Policy 在 Cable Insertion、Pen Collection 和 Tool Hanging 上的最终阶段成功率分别达到 0.70、0.85 和 0.90，高于报告中的 OpenVLA-OFT 成功率 0.30、0.60 和 0.65。
- 论文报告称，在其评估套件中，相比使用最先进全局池化表征的策略，该方法相对提升 40%；相比经过微调的 OpenVLA-OFT，提升 18%。
- DINOv2 VQ-BeT 共拥有 51.55M 个参数，在 NVIDIA H200 上的延迟为 10.99 ms；相比之下，OpenVLA-OFT 拥有 7.61B 个参数，延迟为 61.71 ms。DINOv2 Patch Policy 的训练耗时为 6.5 个 GPU 小时，而 OpenVLA-OFT 为 16 个 GPU 小时。
- 在 Push-T 上，保留 256 个 patch 时得分为 0.69；压缩为 64、16、4 和 1 个 patch 时，得分分别为 0.52、0.53、0.51 和 0.48，这支持了空间压缩会损害精确控制的说法。
- 证据涵盖四个仿真环境，以及在同一套 7 自由度 Franka 设备上进行的三个任务；该摘录无法证明其在更广泛的机器人本体、数据集或长期部署条件下的性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18236v1](https://arxiv.org/abs/2607.18236v1)
