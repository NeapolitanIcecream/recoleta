---
source: arxiv
url: https://arxiv.org/abs/2606.09956v1
published_at: '2026-06-08T11:15:49'
authors:
- Nikolai Rozanov
topics:
- bug-localization
- code-intelligence
- software-verification
- llm-fine-tuning
- line-level-classification
- developer-tools
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-task LLMs for Bug Classification: Efficient Inference with Auxiliary Decoding Heads

## Summary
## 摘要
本文提出 MLC，这是一种行级 bug 定位方法，在冻结的代码 LLM 上加入一个小型 bug/no-bug 解码头。它通过每个文件只生成一个 token 来更快地做整文件 bug 分类。

## 问题
- LLM 编码工具可以快速生成代码，但验证和 bug 定位仍然缓慢、成本高，而且往往太粗，无法直接用于修复。
- 代理式 bug 定位每个文件可能要花 1 到 2 分钟，还会生成数千个 token；很多方法只能定位到文件或函数，而不是精确到行。
- 以前的行级 LLM 方法常用较短的上下文窗口，或者依赖换行 token，但这不可靠，因为分词器会把换行和周围文本合并。

## 方法
- MLC 在整个文件上运行一个预训练代码 LLM，并在主设置中保持骨干模型冻结。
- 一个 token-行对齐算法把分词器输出映射回源代码行，避免把换行 token 当作行分隔符的假设。
- 模型用 sum、mean 或 last-token pooling 聚合每一行的 token 隐状态。
- 一个小型辅助解码头为每一行预测 BUG 或 NO BUG；可选的 LoRA/PEFT 适配器可以训练额外的 bug 定位特征。
- 训练时对文件内所有行一次性使用加权二元交叉熵，以处理类别不平衡和文件长度变化。

## 结果
- 在整文件 Defects4J 上，MLC Qwen1.7B + PEFT 的 Top-1 为 16.3%，Top-3 为 23.3%，Top-5 为 39.5%；DeepFL 分别为 14.4%、24.1% 和 34.2%，Ochiai 分别为 4.8%、16.5% 和 25.1%。
- Defects4J 上的监督微调基线表现很差：SFT QwenCode7B 的 Top-1 为 0.0%，Top-3 为 7.4%，Top-5 为 14.3%。
- 在 PypiBugs 上，MLC Qwen1.7B + PEFT 的 Top-1 为 8.6%，Top-3 为 27.4%，Top-5 为 37.1%；表中最好的非 PEFT 结果是 MLC Qwen8B，分别为 10.3%、26.3% 和 36.6%。
- 在短上下文的 Defects4J v1.2.0 对比中，MLC CodeGen16B 的 Top-1 为 28.6%，Top-5 为 71.4%；LLMAO CodeGen16B 分别为 22.3% 和 46.3%。
- 与函数级代理系统相比，MLC CodeGen16B 的 Top-5 71.4% 接近使用 GPT-4.1-mini 的 MemFL 的 73.9%，但 MemFL 报告的是函数级结果，而 MLC 在短上下文设置下报告的是行级结果。
- 在从 PypiBugs 训练得到的域外 BugsEval 集上，MLC Qwen8B 的 Top-1 为 13.8%，Top-3 为 23.1%，Top-5 为 29.2%；BugsEval 包含 12 个项目、121 个 bug 和 67 个文件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09956v1](https://arxiv.org/abs/2606.09956v1)
