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
## 摘要
BACE 通过把生成的测试视为带噪声的证据而不是真值，来改进 LLM 代码生成。它让代码群体和测试群体共同演化，并用贝叶斯方式更新置信度，同时把搜索约束在公开示例用例上。

## 问题
- LLM 生成的代码经常包含单次提示难以发现的逻辑错误，因此一些系统会使用带有生成测试的反馈循环。
- 生成测试并不可靠：错误代码可能通过薄弱测试，正确代码也可能因为错误断言被推向错误修改。
- 近期系统如 MapCoder 和 CodeSIM 因为这种失败模式而避开测试生成，这也放弃了本可利用的执行信号。

## 方法
- BACE 维护一个候选程序的**群体**和一个生成测试的**群体**，而不是依赖单个代码样本和单个测试套件。
- 每个代码候选和每个测试都有一个贝叶斯置信分数，即其正确或有效的概率。通过/失败结果被当作带噪声的观测来更新这些置信度，而不是当作硬性真值。
- 噪声模型为误导性情况设定了三个通过概率：有效代码在损坏测试上的错误通过（$\alpha$）、错误代码在有效测试上的偶然通过（$\beta$），以及错误代码在损坏测试上的巧合通过（$\gamma$）。
- 提示中的公开输入/输出示例被固定为高置信锚点。未通过锚点的代码，其置信度会被压到零；通过锚点的代码会得到强烈的正向更新。
- BACE 交替演化测试和代码，并通过基于行为的精英保留和差分测试保留高置信且多样化的个体。

## 结果
- 在 **LiveCodeBench v6 (post-March 2025)** 上，BACE 在 **GPT-5-Mini** 下比 **CodeSIM** 高 **3.8%**。
- 在同一基准上，BACE 在 **Qwen2.5-Coder-7B** 下比 **CodeSIM** 高 **5.0%**。
- 论文称，在专有模型和开放权重小型语言模型上，BACE 的表现都好于领先的多智能体框架。
- 该摘录没有给出完整的绝对分数、pass@k 数值、方差或完整的基线表。
- 作者还表示，**AgentCoder 在使用 GPT-5-Mini 处理中等难度问题时的表现低于直接提示**，但摘录没有给出这一差距的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28653v1](http://arxiv.org/abs/2603.28653v1)
