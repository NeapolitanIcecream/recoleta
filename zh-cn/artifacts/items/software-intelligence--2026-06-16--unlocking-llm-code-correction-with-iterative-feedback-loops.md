---
source: arxiv
url: https://arxiv.org/abs/2606.17514v1
published_at: '2026-06-16T04:47:42'
authors:
- Le Zhang
- Suresh Kothari
topics:
- code-correction
- iterative-feedback
- llm-code-generation
- execution-feedback
- code-intelligence
- reasoning-models
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Unlocking LLM Code Correction with Iterative Feedback Loops

## Summary
## 摘要
论文测试 LLM 是否能在多次尝试中利用编译器错误、运行时错误、失败测试用例和资源限制反馈来修复失败代码。结果显示，推理模型在迭代中的提升更大，而语法和运行时失败比逻辑和算法错误更容易修复。

## 问题
- 单次尝试的 pass@1 分数漏掉了一种常见的软件工作流：代码失败，测试返回反馈，开发者再修改代码。
- 这一点很重要，因为生成的代码失败后仍需要修复；如果 LLM 能自动修复，就能减少编码工具中的人工纠错工作。
- 论文研究哪些模型能从反馈中受益、哪些错误类型会被修复，以及多少轮迭代有用。

## 方法
- 研究使用 Python 和 Java 的 LeetCode 任务：450 个 Core 问题、200 个侧重效率的 Strain 问题，以及 32 个从高频失败中选出的 Challenge 问题。
- 研究评估四个模型：DeepSeek-R1、DeepSeek-V3、GPT-o4-mini 和 GPT-4.1-mini，并比较推理模型与非推理模型。
- 修正循环很简单：生成代码，运行代码，返回错误或失败测试细节，然后要求模型修改代码。
- 反馈包括编译错误、运行时错误、带有期望输出和实际输出的错误答案测试用例、超时失败和内存超限失败。
- 论文定义了首次尝试的 pass@1、k 轮内成功的 ISR@k，以及解决一个任务所需迭代次数的中位数 MIS。

## 结果
- 在包含 450 个问题的 Core Dataset 上，GPT-o4-mini 的总体 pass@1 最好：Python 为 89.11%，Java 为 87.33%。DeepSeek-R1 得分为 84.00% 和 82.44%，GPT-4.1-mini 得分为 76.22% 和 75.11%，DeepSeek-V3 得分为 72.44% 和 71.56%。
- 困难问题显示出最大的模型差距。GPT-o4-mini 在 Python 中的 pass@1 为 80.00%，在 Java 中为 74.00%；DeepSeek-R1 为 65.33% 和 62.67%；GPT-4.1-mini 为 54.67% 和 54.00%；DeepSeek-V3 为 46.67% 和 45.33%。
- 简单问题接近饱和：不同模型和语言的分数范围为 97.33% 到 100.00%。
- 在使用 DeepSeek-R1 进行迭代修复的 top-p 校准中，top-p 为 0.1 时 ISR@10 为 65.6%，0.3 时为 68.8%，0.5 时为 68.8%，0.7 时为 65.6%，0.9 时为 62.5%；研究选择 top-p 0.3。
- 摘录没有给出 32 个问题的 Challenge Dataset 图中确切的 ISR@10 数值。文中称，所有模型相较单次尝试结果都有提升，其中 DeepSeek-R1 和 GPT-o4-mini 的提升比 DeepSeek-V3 和 GPT-4.1-mini 更稳定。
- 论文报告称，加入指令“Optimize the time complexity of your algorithm”减少了 200 个问题的 Strain Dataset 上 Java 的超时失败，但摘录没有提供图中的确切数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17514v1](https://arxiv.org/abs/2606.17514v1)
