---
source: arxiv
url: https://arxiv.org/abs/2605.11299v2
published_at: '2026-05-11T22:34:45'
authors:
- Yizhu Jiao
- Ruixiang Zhang
- Richard Bai
- Jiawei Han
- Ronan Collobert
- Yizhe Zhang
topics:
- code-generation
- self-training
- test-time-scaling
- reinforcement-learning
- program-ranking
- livecodebench
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Primal Generation, Dual Judgment: Self-Training from Test-Time Scaling

## Summary
## 摘要
DuST 训练代码模型用执行标签判断自己生成的解法，然后用同一个训练后的模型生成代码。论文声称，这种仅基于排序的 GRPO 训练同时提升了 LiveCodeBench 上的判断能力和 pass@1 生成能力。

## 问题
- 代码模型通常只针对一个生成程序获得稀疏的通过/失败信号，这对接近正确但未通过的解法提供的信息很少。
- 生成后再判断的测试时扩展会采样多个程序并对它们排序，但标准流程在推理后会丢弃排序信号。
- 更好地复用这个信号很重要，因为它可以减少重复采样成本，并改进生成器本身。

## 方法
- 对每个编程问题，基础模型采样许多候选程序；作者在主要数据构建中对每个问题使用 64 个候选程序。
- 沙盒执行每个候选程序，并分配二元正确性标签：通过所有测试或失败。
- 候选程序按 4 个一组分组，只保留至少包含一个正确解法和一个错误解法的混合组。
- 模型接收问题和候选集合，输出排序，并因把正确程序排在错误程序之前而获得奖励。每组产生 n+ × n- 个成对比较。
- GRPO 更新之后用于生成的同一组模型参数；奖励只针对排序质量，生成的代码没有直接的正确性奖励。

## 结果
- 训练数据：约 10K 个去重后的 rSTARcoder 问题；每个问题采样 64 个候选程序；主要模型约有 6.9K 个有效查询和 37K 个训练组。
- Qwen3-30B-Thinking 在 LiveCodeBench v6 上：pass@1 从 65.4% 升至 68.5%（+3.1），判断 NDCG 从 70.1 升至 76.3（+6.2），Best-of-4 准确率从 68.7% 升至 72.6%（+3.9）。
- Qwen3-30B-Thinking 在 LiveCodeBench v5 上：pass@1 从 69.2% 升至 71.0%（+1.8），NDCG 从 76.0 升至 78.2（+2.2），Best-of-4 准确率从 72.3% 升至 75.2%（+2.9）。
- GPT-OSS-20B 在 LiveCodeBench v6 上的 Best-of-4 准确率从 65.2% 升至 69.4%（+4.2），在 v5 上从 67.5% 升至 72.8%（+5.3）。
- Qwen3-4B-Thinking 在 LiveCodeBench v6 上的 Best-of-4 准确率从 55.0% 升至 59.4%（+4.4）；Qwen3-30B-Instruct 从 43.1% 升至 47.1%（+4.0）。
- 在 Qwen3-30B-Thinking 针对 LiveCodeBench v6 的消融实验中，离策略排序达到 72.6% TTS 准确率、68.3% 生成 pass@1 和 76.3 NDCG，分别高于在线策略生成的 71.4%、67.1% 和 74.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.11299v2](https://arxiv.org/abs/2605.11299v2)
