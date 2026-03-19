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
- robotics
- vision-language-action
- tactile-sensing
- multimodal-fusion
- film-conditioning
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# Tactile Modality Fusion for Vision-Language-Action Models

## Summary
本文提出 **TacFiLM**，一种把触觉信息轻量注入视觉-语言-动作（VLA）机器人大模型的方法，用于提升接触密集型操作。它通过后训练微调而非大规模重训，在插入类真实机器人任务上显著提升成功率、直接插入率、速度与受力稳定性。

## Problem
- 现有 VLA 机器人策略主要依赖视觉，但视觉难以可靠感知接触力、摩擦、顺应性、剪切等接触动态，尤其在插入、插线等精细操作中容易失败。
- 现有触觉融合方案常用 token 拼接或额外多模态预训练，会增加序列长度、计算成本和训练复杂度，不利于大模型的高效适配。
- 这个问题重要，因为接触密集型 manipulation 是机器人落地的核心难点；若不能低成本引入触觉，通用机器人基础模型很难在真实物理交互中稳定工作。

## Approach
- 作者提出 **TacFiLM**：不把触觉当成额外 token 拼到输入里，而是用预训练触觉编码器先提取触觉 embedding，再用 **FiLM** 对视觉 backbone 的中间特征做按通道缩放与平移调制。
- 核心机制可理解为：**让触觉去“轻量地改写”视觉特征，而不是扩展上下文长度**，从而保留原有视觉-语言先验并减少计算负担。
- 具体上，方法建立在 OpenVLA-OFT 上；触觉图像经预训练模型（如 **T3**、**Sparsh**）编码后，生成每层视觉特征的 amma/eta 参数，并在 ViT block 中进行 FiLM 调制。
- 训练时主要采用 **LoRA 后训练微调**，冻结大部分原模型，只更新少量参数与融合模块，因此参数高效且不需要额外大规模多模态预训练。
- 方法声称对触觉编码器选择较为无关（encoder-agnostic），并可在不增加 token 序列长度的前提下完成视觉-触觉融合。

## Results
- 实验基于真实机器人 **700+ rollouts**；其中含 **270** 个分布内评测、**225** 个分布外评测、以及 **210** 个消融实验。
- 分布内 **Circle-Peg (3mm)**：TacFiLM 达到 **100.00%** 成功率，优于 OpenVLA-OFT 的 **86.67%** 和 TactileConcat 的 **96.67%**；直接插入率 **36.67%**，高于 **3.33% / 16.67%**；平均最大力 **7.64N**，低于 **14.94N / 9.19N**；平均完成时间 **52.03s**，低于 **92.24s / 75.11s**。
- 分布内 **Circle-Peg (2mm)**：TacFiLM 成功率 **86.67%**，对比 OpenVLA-OFT **66.67%**、TactileConcat **73.33%**；平均最大力 **7.22N**，低于 **15.09N / 8.72N**；平均时间 **87.11s**，优于 **110.44s / 114.80s**。
- 分布内 **USB-Cable-Plug**：TacFiLM 成功率 **73.33%**，明显高于 OpenVLA-OFT **33.33%** 和 TactileConcat **43.33%**；直接插入率 **33.33%**，高于 **0.00% / 6.67%**；平均时间 **99.71s**，优于 **164.52s / 135.11s**。
- 分布内平均表现：TacFiLM 成功率 **86.67%**，相比 OpenVLA-OFT **62.22%** 与 TactileConcat **71.11%**；直接插入率 **31.11%**，远高于 **8.89% / 7.78%**；平均最大力 **8.34N**，低于 **15.01N / 10.29N**；平均时间 **79.62s**，优于 **122.40s / 108.34s**。
- 分布外 **Square-Peg (3mm)**：TacFiLM 成功率 **100.00%**，高于 OpenVLA-OFT 和 TactileConcat 的 **93.33%**；直接插入率 **46.67%**，高于 **0.00% / 13.33%**；平均最大力 **5.37N**，显著低于 **18.31N / 9.34N**。
- 论文还明确声称：在选定任务上，TacFiLM 相比次优基线可带来 **最高 30%** 的成功率提升；在分布外 **HDMI** 插线任务上成功率提升 **50%**；在部分任务中所需作用力约为基线的 **1/3**。

## Link
- [http://arxiv.org/abs/2603.14604v1](http://arxiv.org/abs/2603.14604v1)
