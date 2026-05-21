---
source: arxiv
url: https://arxiv.org/abs/2605.12610v1
published_at: '2026-05-12T18:02:04'
authors:
- Smitha S Kumar
- Michael A Lones
- Manuel Maarek
- Hind Zantout
topics:
- code-intelligence
- automated-code-review
- peft
- programming-education
- code-llama
- java-feedback
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Fine-Tuning Models for Automated Code Review Feedback

## Summary
## 摘要
这篇论文对 Code Llama 7B 进行微调，用于为学生生成 Java 代码审查反馈，并分别给出关于错误和下一步的反馈。论文称，在教师评分中，PEFT 优于提示方法；在一项小规模研究中，学生评价的有用性接近 ChatGPT。

## 问题
- 编程学生需要反馈指出 bug，并给出有用的下一步，而不直接提供完整解法。
- 当学生代码被发送到外部系统时，专有 LLM 会带来成本、隐私、透明度和定制化问题。
- Code Llama 等开放模型可以在本地运行，但基础模型如果不做任务适配，给出的反馈较弱。

## 方法
- 作者构建了一个包含 425 个 Java 示例的数据集：85 种 bug 类型，每种 bug 类型 5 个样本，每个样本包含代码、KM 反馈和 KH 反馈。
- DeepSeek-R1 生成初始三元组，第一作者验证反馈。
- CodeLlama-7B-Instruct 使用 QLoRA 风格的 PEFT 进行微调：4-bit nf4 量化、冻结基础权重，并在 q_proj 和 v_proj 上使用 LoRA 适配器。
- 可训练参数从 6,743,789,568 降至 5,242,880，rank 为 10，缩放因子为 16，dropout 为 0.08%。
- 研究将 PEFT 与零样本提示和 3 示例上下文提示进行比较，然后用教师标签、BLEU、ROUGE、BERTScore 和一个 7 名学生的焦点小组评估输出。

## 结果
- PEFT 的 KM 准确率达到 61%，基线 Code Llama 提示为 20%，少样本提示为 54%。
- PEFT 的 KH 有用性达到 60%，基线为 26%，少样本提示为 46%。
- PEFT 的误导性建议降至 47%，基线为 83%，少样本提示为 60%；该指标越低越好。
- PEFT 的提示遵循率达到 95%，基线为 54%，少样本提示为 86%。
- PEFT 在不同错误类别上的表现相近：命令式错误为 49%，面向对象错误为 52%。
- 在学生研究中，7 名 CS1 学生从有用性、清晰度和结构方面评价编译器错误、ChatGPT 反馈和 PEFT 反馈；摘录报告称，ChatGPT 和 PEFT 都获得了正面回应，而编译器错误信息被评为效果不佳。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12610v1](https://arxiv.org/abs/2605.12610v1)
