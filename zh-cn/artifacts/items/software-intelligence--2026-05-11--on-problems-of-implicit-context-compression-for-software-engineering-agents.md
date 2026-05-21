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
本文测试了用于软件工程代理的 ICAE 式连续上下文压缩，发现它在多步编码任务上明显失败。它扩展了上下文并加快了生成速度，但解决的 SWE-bench Verified 问题少于未压缩的 Qwen3-8B 基线。

## 问题
- 随着工具输出、文件、日志和先前动作填满提示词，LLM 编码代理会触及上下文限制。
- 类 SWE-bench 的长任务平均可能需要消耗超过 100 万个 token；当关键事实埋在很长的历史记录中时，模型质量会下降。
- 稠密记忆 token 可以降低上下文成本，但本文测试它们是否能保留足够细节来支持多步代码编辑。

## 方法
- 作者改造了 In-Context Autoencoder（ICAE）：一个可训练的 Qwen3-8B 编码器将文本压缩为连续记忆 token，一个冻结的 Qwen3-8B 解码器读取这些 token 和当前提示词。
- 预训练使用 SlimPajama-6B，文本重建目标和续写目标按 50/50 混合，训练 100,000 步。
- 微调覆盖 SQuAD、RepoQA 和 SWE-Smith 代理轨迹；在代理训练中，只有超过 256 个 token 的观察会被压缩。
- 对于代理任务，动作、短观察和系统提示词保留为普通 token，模型学习根据包含压缩观察的历史预测下一次工具调用。
- 评估比较了 Base Qwen3-8B、任务微调的 Qwen3-8B，以及名义压缩率为 4x 的 ICAE。

## 结果
- 在 SQuAD 上，ICAE 达到 BLEU 0.73 和 EM 0.67，高于 Base 的 BLEU 0.67 和 EM 0.54，低于 SFT 的 BLEU 0.75 和 EM 0.70；相对 Base 的 EM 提升为 p < 0.0001。
- 在 RepoQA 上，ICAE 达到 BLEU 0.87 和 Pass@0.8 0.69，接近 Base 的 BLEU 0.81 和 Pass@0.8 0.65；SFT 更高，为 BLEU 0.90 和 Pass@0.8 0.85；ICAE 对比 Base 的 Pass@0.8 为 p = 0.6075。
- 在 SWE-bench Verified 上，ICAE 在 500 个问题中解决了 7 个，低于 Base 的 19 个，远低于 SFT 的 86 个；多次运行分析中，相对 Base 的解决率下降为 p = 0.0062。
- ICAE 改善了中间 SWE-bench 轨迹匹配指标：BLEU_ref 为 0.51，Base 为 0.48，SFT 达到 0.55。
- 有效压缩率在 SQuAD 上为 1.46x，在 RepoQA 上为 3.74x，在 SWE-bench Verified 上为 2.0x；在 SWE-bench Verified 上，它允许平均轨迹达到 113 步，而 Base 为 81 步，并将生成时间减少 10%。
- 作者将 SWE-bench 失败归因于会随步骤累积的重建错误，例如错误的 URL 或文件路径，以及训练信号只优化最新压缩观察而不优化其未来有用性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.11051v1](https://arxiv.org/abs/2605.11051v1)
