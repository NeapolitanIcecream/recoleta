---
source: arxiv
url: https://arxiv.org/abs/2606.23395v1
published_at: '2026-06-22T14:20:11'
authors:
- Haitham Al-Shami
- Rohail Malik
- Riku Ala-Laurinaho
- "Jari Veps\xE4l\xE4inen"
- Raine Viitala
topics:
- sysml-v2
- semantic-fault-localization
- knowledge-graphs
- code-repair
- mbse
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Automated Semantic Fault Localization in SysML v2: A Human-in-the-Loop Framework Using Knowledge-Graph Augmented LLMs

## Summary
## 摘要
论文提出一种由知识图谱引导的小语言模型方法，用于发现并修复 SysML v2 语法故障和语义故障。主要结论是，微调将语义修复准确率从低于 3% 提高到超过 91%，同时生成更短的 diff 补丁，便于工程师审查。

## 问题
- SysML v2 编译器能捕获语法错误，但可能漏掉能够通过编译、却违反工程规则的模型，例如连接不兼容的机械、电气、流体或信号接口。
- 这些语义故障会影响实际流程，因为它们可能沿着 MBSE 工作流传递，并在后期表现为集成失败。
- SysML v2 训练数据稀缺，这限制了通用 LLM 在有效语法和领域正确修复上的表现。

## 方法
- 该方法构建了一个车辆领域知识图谱，其中包含物理接口兼容性规则；还构建了一个物理量图，用于把量的类别映射到有效单位。
- 它从 256 个有效的 SysML v2 文件开始，创建了 8,301 个样本：5,497 个语法故障、1,402 个语义故障和 1,402 个正确样本。
- 语义故障通过修改原本有效的模型生成，使其仍能编译，但违反知识图谱规则，例如端口领域不匹配或无效单位赋值。
- Qwen2.5 Coder 1.5B Instruct 和 DeepSeek Coder 6.7B Instruct 使用 LoRA 进行微调，用于将代码分类为正确或错误，并输出修复后的代码或 unified diff 补丁。
- 推理时，编译器消息和从知识图谱得出的规则会加入提示词，生成的补丁仍由人工审查。

## 结果
- 在报告的 1,184 个样本评估集上，Qwen2.5 Coder 1.5B 的语义修复从 0.62% 的基线准确率提高到 95.7%（微调后的完整代码输出），补丁输出为 91.9%。
- DeepSeek Coder 6.7B 的语义修复从 2.47% 的基线准确率提高到 91.9%（微调后的完整代码输出），补丁输出为 91.4%。
- Qwen 的总体准确率从 21.8% 的基线提高到 92.8%（微调后的完整代码输出）；其补丁输出达到 73.4% 的总体准确率。
- DeepSeek 的总体准确率从 30.0% 的基线提高到 90.7%（微调后的完整代码输出）；其补丁输出达到 70.2% 的总体准确率。
- 补丁输出更短：Qwen 使用补丁时输出 84 个 token，完整代码修复为 173 个；DeepSeek 分别为 111 个和 271 个。
- 正确代码分类方面，Qwen 在微调后的完整代码输出和补丁输出中均达到 98.1%；DeepSeek 根据输出格式不同，达到 94.7% 到 97.6%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23395v1](https://arxiv.org/abs/2606.23395v1)
