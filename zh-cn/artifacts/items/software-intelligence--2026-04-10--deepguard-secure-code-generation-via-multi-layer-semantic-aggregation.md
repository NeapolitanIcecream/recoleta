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
## 总结
DeepGuard 通过使用来自多个 transformer 层的安全信号，而不是只依赖最后一层，来增强代码 LLM 的安全性。它把多层特征聚合、安全感知微调和低成本的推理期 logit 偏置结合起来，提高安全且正确的代码生成率。

## 问题
- 代码 LLM 常会复现训练数据里的不安全编码模式，已有工作报告了较高的失败率，例如 Copilot 生成样本中大约 40% 含有漏洞。
- 许多安全调优方法只监督最后一层 transformer，但论文显示，漏洞相关线索在中上层最明显，接近输出层时会变弱。
- 这很重要，因为安全代码生成需要在提升安全性的同时保持功能正确性，而功能正确性正是代码模型在开发流程中的核心价值。

## 方法
- DeepGuard 对模型各层做探测，发现漏洞判别信息在上层的一段区间最强，而不只在最后一层。
- 它在顶部 N 层上构建一个基于注意力的聚合器，把这些层的隐藏状态融合成每个 token 的单一安全敏感表示。
- 一个小型安全分析器利用聚合后的表示和学习到的 token 级安全嵌入来给 token 和序列打分；训练时用间隔损失推动安全代码的得分高于配对的含漏洞代码。
- 模型在 LoRA 下用多目标损失进行适配：安全代码上的下一个 token 损失、漏洞与安全样本对之间的安全对比损失，以及让模型保持接近基模型的 KL 正则项。
- 在推理阶段，DeepGuard 先计算一个受提示词条件影响的安全分数，再把它与从安全/漏洞训练数据中学到的 token 先验结合，并在解码时对 logits 加上固定偏置，不需要在每一步都调用分析器。

## 结果
- 在五个代码 LLM 上，DeepGuard 相比强基线 **SVEN**，平均把安全且正确的生成率提高了 **11.9%**。
- 在 **Qwen2.5-Coder-3B** 上，**sec-pass@1** 从 **SVEN** 的 **70.47%** 提升到 **DeepGuard** 的 **80.76%**；**pass@1** 为 **86.65%**，论文称这接近原始模型。
- 在 **Qwen2.5-Coder-7B** 上，DeepGuard 报告的 **pass@1** 为 **83.18%**，**sec@1_pass** 为 **88.19%**，**sec-pass@1** 为 **73.35%**，**SVEN-SR** 为 **89.21%**。
- 在 **DeepSeek-Coder-1.3B** 上，DeepGuard 报告的 **pass@1** 为 **81.06%**，**sec@1_pass** 为 **84.91%**，**sec-pass@1** 为 **68.82%**，**SVEN-SR** 为 **87.71%**。
- 在 **DeepSeek-Coder-6.7B** 上，DeepGuard 报告的 **pass@1** 为 **88.47%**，**sec@1_pass** 为 **79.52%**，**sec-pass@1** 为 **70.35%**，**SVEN-SR** 为 **81.82%**。
- 在 **Seed-Coder-8B** 上，DeepGuard 报告的 **pass@1** 为 **86.59%**，**sec@1_pass** 为 **93.21%**，**sec-pass@1** 为 **80.71%**，**SVEN-SR** 为 **93.21%**；论文还声称它能泛化到留出的漏洞类型，但节选没有给出留出划分的具体数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09089v1](http://arxiv.org/abs/2604.09089v1)
