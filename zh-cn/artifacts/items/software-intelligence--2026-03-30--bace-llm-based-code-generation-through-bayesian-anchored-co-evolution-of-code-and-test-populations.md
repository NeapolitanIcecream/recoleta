---
source: arxiv
url: http://arxiv.org/abs/2603.28653v1
published_at: '2026-03-30T16:40:11'
authors:
- Kaushitha Silva
- Srinath Perera
topics:
- llm-code-generation
- program-synthesis
- bayesian-inference
- test-generation
- co-evolution
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# BACE: LLM-based Code Generation through Bayesian Anchored Co-Evolution of Code and Test Populations

## Summary
## 总结
BACE 将生成的测试视为噪声证据，而不是把它们当作真实标签，从而提升了 LLM 的代码生成效果。它用贝叶斯信念更新让代码和测试两个种群共同演化，同时把搜索过程绑定到公共示例用例上。

## 问题
- LLM 生成的代码常有逻辑错误，单次提示很容易漏掉，所以系统会用带生成测试的反馈循环。
- 生成的测试不可靠：错误代码可能通过薄弱测试，正确代码也可能被错误断言逼着改错。
- 最近的系统，如 MapCoder 和 CodeSIM，因这种失效模式而避开测试生成，这也让有用的执行信号没有被用上。

## 方法
- BACE 保留一个候选程序的**种群**和一个生成测试的**种群**，而不是只依赖一个代码样本和一个测试集。
- 每个代码候选和每个测试都会得到一个贝叶斯信念分数，表示它是否正确或有效。通过或失败的结果会把这些信念当作带噪观察来更新，而不是当作硬事实。
- 噪声模型为误导性情况设置了三个通过概率：错误测试上正确代码的误通过率（$\alpha$）、正确测试上错误代码的偶然通过率（$\beta$）、以及错误测试上错误代码的碰巧通过率（$\gamma$）。
- 提示中的公开输入/输出示例被固定为高置信锚点。代码如果无法通过锚点，信念会被压到零；通过锚点则会得到强正向更新。
- BACE 在测试和代码之间交替演化，并通过基于行为的精英保留和差分测试保留高信念且多样的个体。

## 结果
- 在 **LiveCodeBench v6（2025 年 3 月后）** 上，BACE 使用 **GPT-5-Mini** 比 **CodeSIM** 高 **3.8%**。
- 在同一基准上，BACE 使用 **Qwen2.5-Coder-7B** 比 **CodeSIM** 高 **5.0%**。
- 论文称，在专有模型和开源权重小模型上，BACE 都优于领先的多智能体框架。
- 摘要没有给出完整的绝对分数、pass@k 数值、方差或完整基线表。
- 作者还说，**AgentCoder 在中等难度问题上用 GPT-5-Mini 的表现低于直接提示**，但摘要没有给出这个差距的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28653v1](http://arxiv.org/abs/2603.28653v1)
