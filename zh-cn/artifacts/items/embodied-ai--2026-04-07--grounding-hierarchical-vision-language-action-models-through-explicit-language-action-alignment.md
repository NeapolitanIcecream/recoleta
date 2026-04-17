---
source: arxiv
url: http://arxiv.org/abs/2604.05614v1
published_at: '2026-04-07T09:03:12'
authors:
- Theodor Wulff
- Federico Tavella
- Rahul Singh Maharjan
- Manith Adikari
- Angelo Cangelosi
topics:
- vision-language-action
- hierarchical-policy
- language-action-alignment
- preference-learning
- robot-transparency
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Grounding Hierarchical Vision-Language-Action Models Through Explicit Language-Action Alignment

## Summary
## 摘要
GPLA 训练一种分层视觉-语言-动作模型，使其生成的子任务语言与机器人的视觉场景和动作轨迹更一致。它通过学习得到的 grounding 评分器和偏好微调来实现这一点，目标是减少对人工子任务标注的依赖。

## 问题
- 分层 VLA 模型可以同时输出语言子步骤和机器人动作，但训练通常不会强制这两种输出彼此一致。
- 这关系到机器人的透明性和人机协作：只有当描述的子任务与机器人看到的内容和执行的动作一致时，机器人的解释才有用。
- 现有评估通常关注任务成功率或动作精度，却没有检验中间语言是否真正扎根于观测和行为。

## 方法
- 论文构建了一个分层 VLA：高层使用 Gemma-3-4B-IT VLM 生成低层指令，低层使用 SmolVLA 在 LanguageTable 上预测 8 步动作轨迹。
- 它训练了一个独立的 grounding 模型，把视觉-动作对和文本映射到同一个嵌入空间。该模型使用冻结的 SigLIP 2 视觉/文本编码器、一个小型 transformer 处理动作，并用 FiLM 层根据动作对视觉特征进行条件化。
- grounding 模型使用对称 InfoNCE 对比损失和多样性正则项进行训练，因此匹配的语言与视觉-动作对会得到更高分，错配对得分更低。
- 在 GPLA 训练过程中，分层 VLA 会针对同一输入采样多个语言-动作候选，grounding 模型对它们排序，最高分和最低分的输出组成 chosen/rejected 偏好对。
- 然后用 SimPO 偏好优化更新高层 VLM，使其生成与最终动作和场景更一致的子任务描述，而不需要新的人工偏好标注。

## 结果
- 在 LanguageTable 上，监督训练在低层指令生成的文本重叠指标上最好：BLEU **0.111 ± 0.05**、ROUGE **0.405 ± 0.12**、METEOR **0.313 ± 0.12**、BERTScore **0.984 ± 0.00**。
- GPLA 各变体在基于 token 重叠的文本指标上更低，例如带动作条件 grounding 模型的 GPLA 达到 BLEU **0.063 ± 0.05**、ROUGE **0.300 ± 0.12**、METEOR **0.218 ± 0.12**、BERTScore **0.980 ± 0.00**。
- 动作质量与监督基线接近。监督训练的 MSE 为 **0.046 ± 0.02**、MAE 为 **0.164 ± 0.04**，而 GPLA（动作条件） 的 MSE 为 **0.045 ± 0.02**、MAE 为 **0.163 ± 0.04**。
- 因此，GPLA 声称，在使用由学习得到的 grounding 分数生成的偏好对、而不是额外昂贵标注的情况下，其动作表现可与全监督微调相比。
- 在 GPLA 各变体中，CLIP、SigLIP 2 和动作条件 grounding 模型得到的轨迹指标非常接近；论文的主要主张是显式的语言-动作 grounding 机制，而不是原始性能的大幅提升。
- 论文还称，基于嵌入空间分析和定性示例，动作条件 grounding 模型比现成的视觉-语言编码器更适合构建用于语言与视觉-动作对齐的共享嵌入空间。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05614v1](http://arxiv.org/abs/2604.05614v1)
