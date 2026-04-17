---
source: arxiv
url: http://arxiv.org/abs/2604.09089v1
published_at: '2026-04-10T08:19:48'
authors:
- Li Huang
- Zhongxin Liu
- Yifan Wu
- Tao Yin
- Dong Li
- Jichao Bi
- Nankun Mu
- Hongyu Zhang
- Meng Yan
topics:
- secure-code-generation
- code-llm
- multi-layer-representations
- vulnerability-detection
- lora-fine-tuning
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation

## Summary
## 摘要
DeepGuard 通过利用多个 Transformer 层中的安全信号，而不是只依赖最后一层，来提升代码 LLM 对不安全代码生成的防护能力。它结合了多层特征聚合、安全感知微调，以及低成本的推理时 logit 偏置，以提高安全且正确的代码生成率。

## 问题
- 代码 LLM 往往会复现训练数据中的不安全编码模式，已有工作报告了较高的失败率，例如 Copilot 生成样本中约有 40% 的代码存在漏洞。
- 许多安全调优方法只对最后一个 Transformer 层施加监督，但论文表明，漏洞线索在中上层最明显，接近输出层时反而减弱。
- 这一点很重要，因为安全代码生成必须在提升安全性的同时不破坏功能正确性，而功能正确性正是代码模型在开发工作流中的主要价值。

## 方法
- DeepGuard 对模型各层进行探测，发现用于区分漏洞的信息在一段高层区间内最强，而不是只集中在最后一层。
- 它在顶部 N 层之上构建了一个基于注意力的聚合器，将这些层的隐藏状态融合为每个 token 的单一安全敏感表示。
- 一个小型安全分析器使用聚合表示以及学习得到的 token 级安全嵌入，对 token 和序列打分；训练时使用间隔损失，使安全代码的得分高于对应的不安全代码。
- 模型通过 LoRA 在多目标损失下进行适配：安全代码上的 next-token 损失、漏洞代码与安全代码配对之间的安全对比损失，以及用于保持接近基础模型的 KL 正则项。
- 在推理阶段，DeepGuard 计算一个由提示词条件决定的安全分数，将其与基于安全和漏洞训练数据学到的 token 先验结合，并在解码时向 logits 加入固定偏置，无需在每一步调用分析器。

## 结果
- 在五个代码 LLM 上，DeepGuard 相比强基线 **SVEN**，将安全且正确的代码生成率平均提高了 **11.9%**。
- 在 **Qwen2.5-Coder-3B** 上，**sec-pass@1** 从 **SVEN** 的 **70.47%** 提升到 **DeepGuard** 的 **80.76%**；**pass@1** 为 **86.65%**，论文称这一结果接近原始模型。
- 在 **Qwen2.5-Coder-7B** 上，DeepGuard 报告 **pass@1 83.18%**、**sec@1_pass 88.19%**、**sec-pass@1 73.35%** 和 **SVEN-SR 89.21%**。
- 在 **DeepSeek-Coder-1.3B** 上，DeepGuard 报告 **pass@1 81.06%**、**sec@1_pass 84.91%**、**sec-pass@1 68.82%** 和 **SVEN-SR 87.71%**。
- 在 **DeepSeek-Coder-6.7B** 上，DeepGuard 报告 **pass@1 88.47%**、**sec@1_pass 79.52%**、**sec-pass@1 70.35%** 和 **SVEN-SR 81.82%**。
- 在 **Seed-Coder-8B** 上，DeepGuard 报告 **pass@1 86.59%**、**sec@1_pass 93.21%**、**sec-pass@1 80.71%** 和 **SVEN-SR 93.21%**；论文还声称它能泛化到留出的漏洞类型，但摘录中没有给出留出划分的具体数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09089v1](http://arxiv.org/abs/2604.09089v1)
