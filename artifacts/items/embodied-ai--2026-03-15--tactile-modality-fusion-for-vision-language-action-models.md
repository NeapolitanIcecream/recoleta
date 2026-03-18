---
source: arxiv
url: http://arxiv.org/abs/2603.14604v1
published_at: '2026-03-15T20:57:51'
authors:
- Charlotte Morissette
- Amin Abyaneh
- Wei-Di Chang
- Anas Houssaini
- David Meger
- Hsiu-Chin Lin
- Jonathan Tremblay
- Gregory Dudek
topics:
- vision-language-action
- tactile-fusion
- contact-rich-manipulation
- robot-policy-finetuning
- film-conditioning
relevance_score: 0.95
run_id: materialize-outputs
---

# Tactile Modality Fusion for Vision-Language-Action Models

## Summary
本文提出 TacFiLM，一种将触觉信息轻量注入视觉-语言-动作模型的后训练融合方法，用于提升接触密集型机器人操作。核心思想是不用增加输入 token，而是让预训练触觉表征去调制中间视觉特征，从而在保留原有 VLA 先验的同时增强接触感知。

## Problem
- 现有 VLA 模型大多依赖视觉，但在插入、插线等接触密集任务中，视觉难以可靠感知接触力、摩擦、顺应性、剪切和遮挡下的细微位姿误差。
- 现有将触觉接入 VLA 的方法常靠 token 拼接或额外大规模多模态预训练，带来更长上下文、更高算力成本和更复杂训练流程。
- 机器人行为模型本身训练/微调已经昂贵，因此需要一种**后训练、参数高效、计算轻量**的触觉融合机制。

## Approach
- 基于 OpenVLA-OFT，作者提出 **TacFiLM**：先用预训练触觉编码器（如 T3、Sparsh）把 DIGIT 触觉图像编码成嵌入，再用该嵌入生成 FiLM 的缩放与偏移参数。
- 这些 FiLM 参数被插入到视觉 backbone 的中间 ViT block 中，对视觉特征做逐通道仿射调制：让“触觉信息影响视觉表示”，而不是把触觉直接拼成额外 token。
- 这样做的直观含义是：触觉像一个全局条件信号，告诉视觉特征“当前接触状态如何”，从而帮助动作模型在接触瞬间做更细微、更稳的调整。
- 方法不增加语言模型输入序列长度，不需要重新训练大型主干，只进行 LoRA 式参数高效微调，尽量保留原始视觉-语言先验。
- 作者还验证了方法对不同预训练触觉表征的兼容性，说明该融合框架对触觉编码器选择较为灵活。

## Results
- 实验覆盖 **700+ 次真实机器人 rollout**；其中 ID 评测 **270 次**、OOD 评测 **225 次**、消融 **210 次**。
- **ID: Circle-Peg 3mm**：TacFiLM 成功率 **100.00%**，优于 OpenVLA-OFT 的 **86.67%** 和 TactileConcat 的 **96.67%**；直接插入率 **36.67%**，高于 **3.33%/16.67%**；平均最大力 **7.64 N**，低于 **14.94/9.19 N**；平均时间 **52.03 s**，低于 **92.24/75.11 s**。
- **ID: Circle-Peg 2mm**：TacFiLM 成功率 **86.67%**，高于 OpenVLA-OFT **66.67%** 和 TactileConcat **73.33%**；平均最大力 **7.22 N**，低于 **15.09/8.72 N**；平均时间 **87.11 s**，低于 **110.44/114.80 s**。
- **ID: USB-Cable-Plug**：TacFiLM 成功率 **73.33%**，对比 OpenVLA-OFT **33.33%**、TactileConcat **43.33%**；直接插入率 **33.33%**，对比 **0.00%/6.67%**；时间 **99.71 s**，优于 **164.52/135.11 s**。
- **ID 平均**：TacFiLM 成功率 **86.67%**，比次优基线 TactileConcat 的 **71.11%** 高 **15.56 个百分点**；直接插入率 **31.11%**，显著高于 **8.89%** 和 **7.78%**；平均最大力 **8.34 N**，低于 **15.01/10.29 N**；平均时间 **79.62 s**，低于 **122.40/108.34 s**。
- 论文还声称在 **OOD** 设置下，TacFiLM 在 **3mm peg insertion** 上保持 **100% 成功率**，并将 **HDMI cable plugging** 成功率提升 **50%**；在部分任务中只需基线方法约 **1/3 的作用力**。给定摘录中的 OOD 表格不完整，无法逐项核对全部数值，但这些是作者明确宣称的最强结果。

## Link
- [http://arxiv.org/abs/2603.14604v1](http://arxiv.org/abs/2603.14604v1)
