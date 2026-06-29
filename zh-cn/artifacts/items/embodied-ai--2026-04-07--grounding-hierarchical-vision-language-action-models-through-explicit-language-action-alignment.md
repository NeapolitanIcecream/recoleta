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
## 总结
GPLA 训练一个分层视觉-语言-行动模型，让它生成的子任务语言更贴近机器人的视觉场景和动作轨迹。它通过一个学习到的 grounding 评分器和偏好微调来实现这一点，目标是减少对人工子任务标注的需求。

## 问题
- 分层 VLA 模型可以同时输出语言步骤和机器人动作，但它们的训练通常不会强制这两种输出彼此一致。
- 这对机器人透明性和人机协作很重要：只有当描述的子任务与机器人看到和执行的内容一致时，机器人的解释才有用。
- 现有评估通常关注任务成功率或动作准确率，却没有检查中间语言是否真的扎根于观察和行为。

## 方法
- 论文构建了一个分层 VLA：高层使用 Gemma-3-4B-IT VLM 生成低层指令，低层使用 SmolVLA 预测 LanguageTable 上的 8 步动作轨迹。
- 它训练了一个单独的 grounding 模型，把视觉-动作对和文本映射到共享嵌入空间。这个模型使用冻结的 SigLIP 2 视觉/文本编码器、一个用于动作的小型 Transformer，以及用 FiLM 层让动作条件化视觉特征。
- grounding 模型用对称的 InfoNCE 对比损失和一个多样性正则项训练，让匹配的语言与视觉-动作对得分高于不匹配的对。
- 在 GPLA 训练时，分层 VLA 会对同一个输入采样多个语言-动作候选，grounding 模型对它们排序，得分最高和最低的输出组成选择/拒绝偏好对。
- 之后用 SimPO 偏好优化更新高层 VLM，让它生成的子任务描述更符合对应的动作和场景，而不需要新的人工偏好标注。

## 结果
- 在 LanguageTable 上，监督训练在低层指令生成的文本重叠指标上最好：BLEU **0.111 ± 0.05**，ROUGE **0.405 ± 0.12**，METEOR **0.313 ± 0.12**，BERTScore **0.984 ± 0.00**。
- GPLA 变体的 token 重叠文本指标更低，例如带动作条件 grounding 模型的 GPLA 达到 BLEU **0.063 ± 0.05**，ROUGE **0.300 ± 0.12**，METEOR **0.218 ± 0.12**，BERTScore **0.980 ± 0.00**。
- 动作质量与监督基线很接近。监督训练的 MSE 为 **0.046 ± 0.02**，MAE 为 **0.164 ± 0.04**；GPLA（动作条件版）的 MSE 为 **0.045 ± 0.02**，MAE 为 **0.163 ± 0.04**。
- 因此，GPLA 声称在使用由学习到的 grounding 评分生成的偏好对、而不是昂贵的额外标注的情况下，动作表现可以接近完全监督微调。
- 在 GPLA 的各个变体中，CLIP、SigLIP 2 和动作条件 grounding 模型的轨迹指标非常接近；论文的核心主张是显式的语言-动作 grounding 机制，而不是大幅的原始性能提升。
- 论文还声称，和现成的视觉-语言编码器相比，动作条件 grounding 模型为语言与视觉-动作对齐提供了更好的共享嵌入空间，这一结论来自嵌入空间分析和定性示例。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05614v1](http://arxiv.org/abs/2604.05614v1)
