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
## 概要
DuST 先让代码模型用执行标签判断自己生成的解，再用同一个训练后的模型做代码生成。论文声称，这种只优化排序的 GRPO 训练能同时提升 LiveCodeBench 上的判断能力和 pass@1 生成效果。

## 问题
- 代码模型通常只拿到单个生成程序的稀疏通过/失败信号，这些信号对接近正确的解提供的信息很少。
- 先生成再判断的 test-time scaling 会采样多个程序并排序，但标准流程会在推理后丢掉排序信号。
- 复用这部分信号有价值，因为它能减少重复采样成本，也能直接改进生成器本身。

## 方法
- 对每道编程题，基础模型会采样很多候选程序；作者在主要数据构建中每题使用 64 个候选。
- 沙箱会执行每个候选，并给出二元正确性标签：通过全部测试或失败。
- 候选按 4 个一组分组，只保留同时包含正确和错误解的混合组。
- 模型接收题目和候选集，输出排序，并因把正确程序排在错误程序前面而获得奖励。每组会产生 n+ × n- 个成对比较。
- GRPO 更新的是后续也用于生成的同一套模型参数；奖励只针对排序质量，生成代码不会直接获得正确性奖励。

## 结果
- 训练数据：约 10K 个去重后的 rSTARcoder 题目；每题 64 个采样候选；主模型约有 6.9K 个有效查询和 37K 个训练组。
- Qwen3-30B-Thinking 在 LiveCodeBench v6 上：pass@1 从 65.4% 升到 68.5%（+3.1），判断 NDCG 从 70.1 升到 76.3（+6.2），Best-of-4 准确率从 68.7% 升到 72.6%（+3.9）。
- Qwen3-30B-Thinking 在 LiveCodeBench v5 上：pass@1 从 69.2% 升到 71.0%（+1.8），NDCG 从 76.0 升到 78.2（+2.2），Best-of-4 准确率从 72.3% 升到 75.2%（+2.9）。
- GPT-OSS-20B 在 LiveCodeBench v6 上的 Best-of-4 准确率从 65.2% 升到 69.4%（+4.2），在 v5 上从 67.5% 升到 72.8%（+5.3）。
- Qwen3-4B-Thinking 在 LiveCodeBench v6 上的 Best-of-4 准确率从 55.0% 升到 59.4%（+4.4）；Qwen3-30B-Instruct 从 43.1% 升到 47.1%（+4.0）。
- 在 Qwen3-30B-Thinking 的消融实验里，LiveCodeBench v6 上的 off-policy 排序达到 72.6% 的 TTS 准确率、68.3% 的生成 pass@1 和 76.3 的 NDCG，优于 on-policy 生成的 71.4%、67.1% 和 74.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.11299v2](https://arxiv.org/abs/2605.11299v2)
