---
source: arxiv
url: http://arxiv.org/abs/2603.02601v1
published_at: '2026-03-03T04:59:25'
authors:
- Varun Pratap Bhardwaj
topics:
- ai-agent-testing
- regression-testing
- non-deterministic-systems
- behavioral-fingerprinting
- sequential-analysis
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# AgentAssay: Token-Efficient Regression Testing for Non-Deterministic AI Agent Workflows

## Summary
AgentAssay提出了一套面向**非确定性AI代理工作流**的回归测试框架，把传统二元测试改成带统计保证的概率性测试，并重点解决测试成本过高的问题。论文核心卖点是：在保持统计严谨性的同时，用行为指纹、顺序检验和离线轨迹分析把token成本大幅降下来。

## Problem
- 现有软件测试假设**同样输入得到同样输出**，但LLM代理在相同提示、工具和模型下也会多次运行出不同行为，因此普通断言和单次评测无法可靠发现“是否退化”。
- 传统**pass/fail**二值结论不适合随机系统；一次失败可能只是噪声，一次成功也可能只是侥幸，因此需要带置信区间和错误率控制的判定方式。
- 对代理做统计回归测试很贵：文中举例，若检测幅度为0.10的回归，约需**100次/场景**；50个场景就是**5000次调用**，在前沿模型上可能花费**2.5万–7.5万美元**，这会阻碍CI/CD落地。

## Approach
- 提出**三值随机测试语义**：把测试结果定义为 **Pass / Fail / Inconclusive**，基于多次运行的通过率、Wilson/Clopper-Pearson置信区间和显著性/功效参数来决定是否真的通过或退化。
- 用**SPRT顺序概率比检验**替代固定样本测试：证据足够时提前停止，从而减少需要执行的代理试验次数。
- 定义代理专属测试工具箱：**5维覆盖率**（tool/path/state/boundary/model）、**4类变异算子**（prompt/tool/model/context）、以及适用于多步代理的**变形关系**，用于更系统地测代理而不仅看最终答案。
- 引入**behavioral fingerprinting**：把一次执行轨迹压缩成低维行为向量，再做多变量统计检验；直观上是“不要把一条复杂轨迹只压成1个pass/fail比特，而是保留更多行为信息”，以提高单位样本的信息量。
- 提出**adaptive budget optimization**与**trace-first offline analysis**：前者根据实际行为方差动态决定需要多少次试验，后者直接在预录制生产轨迹上做覆盖、契约、变形关系和部分变异分析，实现零额外token成本的离线测试。

## Results
- 论文声称这是首个面向非确定性AI代理工作流的**token-efficient regression testing**框架，并给出跨**5个模型、3个场景、7605次试验**的评估，总成本为**227美元**。
- **SPRT**在所有场景中把试验次数降低了**78%**，同时保持统计保证不变。
- **behavioral fingerprinting**的回归检测能力达到**86% detection power**，而二元pass/fail测试在对应设置下是**0%**。
- **adaptive budget optimization**对稳定代理可把所需试验数减少**4–7×**。
- 整体token-efficient pipeline实现了**5–20×成本下降**；摘要中还声称通过**trace-first offline analysis**，对部分测试类型可达到**100% cost savings**。
- 涉及模型包括**GPT-5.2、Claude Sonnet 4.6、Mistral-Large-3、Llama-4-Maverick、Phi-4**；场景包括**电商、客服、代码生成**。

## Link
- [http://arxiv.org/abs/2603.02601v1](http://arxiv.org/abs/2603.02601v1)
