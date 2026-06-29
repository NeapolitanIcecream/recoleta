---
source: arxiv
url: https://arxiv.org/abs/2606.03852v1
published_at: '2026-06-02T16:29:17'
authors:
- Yinsheng Yao
- Hongxiang Zhang
- Weixi Tong
- Tianyi Zhang
topics:
- code-intelligence
- llm-code-repair
- fault-localization
- iterative-refinement
- automated-software-production
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement

## Summary
## 摘要
FLARE 通过把行级 bug 定位加入执行反馈，改进了迭代式 LLM 代码修复。它使用一个小型诊断模型和 top-k 候选搜索，把修复引导到更可能出错的代码行。

## 问题
- LLM 常会生成测试失败的代码，而用户能信任的代码生成系统需要迭代修复。
- 测试失败通常只描述失败现象，不会指出出错的代码行。
- 自我批评和自然语言调试能给出较宽泛的建议，但不会告诉模型该改哪里。

## 方法
- FLARE 在 10,504 个 Collu-Bench 有 bug 代码解答及其真实 bug 位置上，训练了一个 6 层、8 头的双向 Transformer 诊断模型。
- 它把生成器 LLM 的子词概率对齐到代码词法单元，例如标识符、运算符和关键字。
- 诊断模型结合词法单元文本嵌入、语法 token 类型和对齐后的 token 概率，然后为每个词法单元打出可疑度分数。
- 它用最大池化把词法分数转换成行分数，再把排名靠前的可疑行、当前程序和执行反馈送入修复提示词。
- 每轮迭代都会在 top-k 个可疑行上搜索，每行生成一个候选修订，运行公开测试，并保留通过测试的候选，或保留通过测试最多的候选。

## 结果
- 在 LiveCodeBench 上，FLARE 在 k=10 时，五个基础 LLM 的 Pass@1 分数分别为 46.86、44.57、33.71、76.57 和 65.14；对应的 LLM 单独分数为 30.86、26.86、20.57、46.86 和 44.00。
- 在 BigCodeBench 上，FLARE 在 k=10 时的 Pass@1 分数分别为 64.47、55.79、45.61、72.81 和 69.65；NL-Debugging 的分数为 55.00、47.02、40.35、58.33 和 56.67。
- 在 k=1 时，FLARE 在 10 个设置中的 9 个上超过了 NL-Debugging。表中可见的增益范围是 0.18 到 7.42 个百分点。
- 候选搜索相对 k=1 平均带来 8.50 个百分点的提升。报告的增益在 LiveCodeBench 上为 4.57 到 12.00 个百分点，在 BigCodeBench 上为 5.08 到 13.42 个百分点。
- 仅诊断模型在 100 个 LiveCodeBench 任务上达到 67% 的 Top-1、75% 的 Top-3 和 89% 的 Top-10 定位准确率；LLMAO 对应为 63%、74% 和 87%。
- 在 GPT-4o-mini 上，完整 FLARE 在 k=10 时在 LiveCodeBench 上达到 65.14% 的 Pass@1，在 BigCodeBench 上达到 69.65%；仅执行反馈分别为 58.29% 和 59.47%，仅诊断反馈分别为 55.43% 和 58.42%。在 LiveCodeBench 上，k=1 的运行时间为 73.76 秒/任务，k=10 为 610.19 秒/任务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03852v1](https://arxiv.org/abs/2606.03852v1)
