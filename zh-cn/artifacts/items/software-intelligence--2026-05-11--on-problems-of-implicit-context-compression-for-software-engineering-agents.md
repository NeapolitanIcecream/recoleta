---
source: arxiv
url: https://arxiv.org/abs/2605.11051v1
published_at: '2026-05-11T14:47:07'
authors:
- Kirill Gelvan
- Igor Slinko
- Felix Steinbauer
- Egor Bogomolov
- Florian Kofler
- Yaroslav Zharov
topics:
- software-engineering-agents
- context-compression
- code-intelligence
- swe-bench
- llm-agents
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# On Problems of Implicit Context Compression for Software Engineering Agents

## Summary
## 摘要
这篇论文测试了面向软件工程代理的 ICAE 式连续上下文压缩，发现它在多步编码任务上明显失效。它能扩展上下文并加快生成，但在 SWE-bench Verified 上解决的问题数少于未压缩的 Qwen3-8B 基线。

## 问题
- LLM 编码代理会在工具输出、文件、日志和先前操作填满提示词时碰到上下文限制。
- 长篇 SWE-bench 类任务平均可能消耗超过 100 万个 token，而当关键信息被埋在很长的历史里时，模型质量会下降。
- 稠密记忆 token 可以降低上下文成本，但论文检验它们是否能保留足够细节，支撑多步代码编辑。

## 方法
- 作者改造了 In-Context Autoencoder（ICAE）：一个可训练的 Qwen3-8B 编码器把文本压缩成连续记忆 token，一个冻结的 Qwen3-8B 解码器读取这些 token 和当前提示词。
- 预训练使用 SlimPajama-6B，训练 100,000 步，文本重建和续写目标各占 50%。
- 微调覆盖 SQuAD、RepoQA 和 SWE-Smith 的代理轨迹；在代理训练中，只有长度超过 256 个 token 的观测会被压缩。
- 对代理任务，动作、较短观测和系统提示词仍然保留为普通 token，模型学习从包含压缩观测的历史中预测下一次工具调用。
- 评估比较了基础版 Qwen3-8B、任务微调后的 Qwen3-8B 和按名义 4 倍压缩率运行的 ICAE。

## 结果
- 在 SQuAD 上，ICAE 的 BLEU 为 0.73、EM 为 0.67，高于基础版的 BLEU 0.67 和 EM 0.54，低于 SFT 的 BLEU 0.75 和 EM 0.70；相对基础版的 EM 提升在统计上显著，p < 0.0001。
- 在 RepoQA 上，ICAE 的 BLEU 为 0.87、Pass@0.8 为 0.69，接近基础版的 BLEU 0.81 和 Pass@0.8 0.65；SFT 更高，BLEU 0.90、Pass@0.8 0.85；ICAE 与基础版在 Pass@0.8 上的 p = 0.6075。
- 在 SWE-bench Verified 上，ICAE 解决了 500 个问题中的 7 个，低于基础版的 19 个，也远低于 SFT 的 86 个；多轮分析中，相对基础版的解决率下降 p = 0.0062。
- ICAE 提高了中间的 SWE-bench 轨迹匹配指标：BLEU_ref 为 0.51，基础版为 0.48，SFT 为 0.55。
- 有效压缩率在 SQuAD 上为 1.46 倍，在 RepoQA 上为 3.74 倍，在 SWE-bench Verified 上为 2.0 倍；在 SWE-bench Verified 上，它让平均轨迹长度达到 113 步，基础版为 81 步，并把生成时间减少了 10%。
- 作者把 SWE-bench 失败归因于跨步骤累积的重建错误，比如错误的 URL 或文件路径，以及一种只优化最新压缩观测、而不是未来可用性的训练信号。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.11051v1](https://arxiv.org/abs/2605.11051v1)
