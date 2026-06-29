---
source: arxiv
url: https://arxiv.org/abs/2605.20473v1
published_at: '2026-05-19T20:39:14'
authors:
- Yifeng He
- Ethan Wang
- Jicheng Wang
- Xuanxin Ouyang
- Hao Chen
topics:
- code-generation
- test-time-scaling
- differential-testing
- coverage-guided-fuzzing
- code-intelligence
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Code Generation by Differential Test Time Scaling

## Summary
## 概述
DIFFCODEGEN 先生成多个 LLM 候选代码，再通过模糊测试生成输入，比较候选程序的运行时行为，最后选出最大行为簇的中心样本。它面向没有公开测试用例、且额外 LLM 选择调用成本过高的实际代码生成场景。

## 问题
- 代码模型可以采样出很多可能的解，但编码助手通常只需要返回一个最终程序，所以候选选择在真实使用中很重要。
- 以往的 test-time scaling 方法常常依赖公开测试，或者再调用一次 LLM 来合成输入或判断候选，这会增加延迟和 token 成本。
- 这篇论文处理的是缺少 oracle 的情况：新代码可能没有期望输出，因此系统需要一种不依赖真实测试用例来比较候选的方法。

## 方法
- DIFFCODEGEN 先用随机采样、beam search，或 18 种保持语义不变的提示扰动，从同一个提示生成多个代码候选。
- 它先选一个参考候选，再用 coverage-guided fuzzing 生成能覆盖其代码路径的输入。脚本程序使用 AFL++ 或 py-afl，库函数使用 libFuzzer 或 Atheris。
- 它把每个候选都在这些 fuzz 输入上执行，并记录输出、错误、返回值、异常和退出码，作为程序的动态行为。
- 它把两个候选在共享的有效输入上产生不同归一化执行结果的比例，定义为两者的行为距离。
- 它用 average-linkage 的凝聚层次聚类把候选分成 2 个行为组，然后返回较大簇的 medoid。

## 结果
- 评估覆盖 4 个 LLM，包括开源权重模型和闭源模型，结果显示相比基线生成方法有稳定提升。
- 与不依赖公开测试的 SOTA test-time scaling 方法相比，论文声称 PASS@1 表现具有竞争力或更好，但摘要没有给出具体 PASS@1 数值。
- 在 LiveCodeBench 上，DIFFCODEGEN 对本地部署的 LLM 运行时，使用的执行时间大约是以往 TTS 方法的 20%。
- 在 API 型 LLM 上，它报告的时间用量大约是以往 TTS 方法的 5%。
- 由于候选选择阶段不再额外调用 LLM，它消耗的输入 token 大约是前人工作的 4%。
- differential prompting 变体使用 18 种提示扰动方法，在不改变任务语义的前提下增加候选多样性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20473v1](https://arxiv.org/abs/2605.20473v1)
