---
source: arxiv
url: https://arxiv.org/abs/2606.25193v1
published_at: '2026-06-23T21:36:42'
authors:
- Bowen Jiang
- Nathan Hagel
- Haowei Cheng
- Benedikt Jutz
- Arne Lange
- Weixing Zhang
- Rahul Sharma
- Ralf Reussner
- Anne Koziolek
topics:
- llm-code-generation
- model-transformation
- domain-specific-languages
- prompt-engineering
- software-engineering-benchmark
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# LLM4MTLs: Automated Generation and Empirical Evaluation of Model Transformation Languages

## Summary
## 摘要
LLM4MTLs 自动完成面向 LLM 生成的模型转换语言代码的提示构造和评估。它面向低资源 DSL，在这些语言中，LLM 生成的代码经常解析效果差，或无法通过转换测试。

## 问题
- ATL、ETL、QVTo 和 Reactions 等模型转换语言需要语言语法知识，以及源元模型和目标元模型知识。
- LLM 在这些 DSL 上的训练数据有限，因此直接提示经常返回带有语法错误或转换行为错误的代码。
- 以往工作缺少一个可复现的基准，能够在多种 MTL 上提供可执行的参考转换和测试。

## 方法
- 该工作流从已有参考转换构建任务提示，然后用这些提示要求 LLM 重新生成 MTL 代码。
- 它测试多种提示变体，这些变体组合了少样本示例、语法文本和特定语言的辅助方法。
- 它使用句法相似度、句法正确性和语义正确性，根据参考脚本和测试套件评估生成代码。
- 作者在 n8n 中实现该工作流，将组件容器化，并发布复现实验包。

## 结果
- 评估套件包含 4 种 MTL 的 47 个转换示例：ATL、ETL、QVTo 和 Reactions。
- 实证研究比较了 3 个 LLM 在 4 种 MTL 和多种提示配置下的表现。
- 少样本提示提升了所有 4 种 MTL 的句法质量，但语义正确性的提升因语言而异。
- 对于 ATL，Pass@1 在所有测试的策略和模型中保持不变，这意味着句法提升没有转化为该语言更好的首次尝试语义成功率。
- 语法提示与少样本示例配合使用时有帮助，但单独使用时，对某些模型-语言组合可能有害或无效。
- 摘录没有提供 47 个示例、4 种语言和 3 个模型这一研究规模之外的 Pass@1、句法、语义或 ChrF 分数的具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25193v1](https://arxiv.org/abs/2606.25193v1)
