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
relevance_score: 0.95
run_id: materialize-outputs
---

# AgentAssay: Token-Efficient Regression Testing for Non-Deterministic AI Agent Workflows

## Summary
AgentAssay提出了一个面向**非确定性AI代理工作流**的回归测试框架，把传统二元测试改为带统计保证的概率式测试，并重点解决测试成本过高的问题。其核心价值是在保持显著性/功效保证的同时，大幅降低代理回归测试所需的token与运行成本。

## Problem
- 论文要解决的是：**同一代理在相同输入下会因采样、模型更新、工具波动、上下文变化而产生不同结果**，导致传统“单次运行 + 二元通过/失败”的测试方法无法可靠发现回归。
- 这很重要，因为生产环境中的代理可能在提示词、工具、模型或编排逻辑微调后悄然退化；文中举例称客户支持路由准确率可从 **93% 降到 71%**，但传统测试与告警都可能漏检。
- 另一个关键问题是成本：若按固定样本做统计检验，文中估算 **50个场景 × 每场景100次试验 = 5,000次代理调用**，对前沿模型一次回归检查可能花费 **25,000–75,000美元**。

## Approach
- 核心机制是把测试语义从“是否输出等于期望答案”改为“**代理满足某性质的概率是否高于阈值**”，并用三值结论 **Pass / Fail / Inconclusive** 取代硬性的二值结论。
- 它对同一场景执行多次试验，计算通过率与置信区间；若区间下界高于阈值则Pass，区间上界低于阈值则Fail，否则说明证据不足、判为Inconclusive。
- 为降低成本，论文提出三种主要的token-efficient手段：**behavioral fingerprinting**（把执行轨迹压缩成低维行为向量做多变量回归检测）、**adaptive budget optimization**（根据真实行为方差自适应决定试验次数）、**trace-first offline analysis**（利用预录制轨迹离线完成覆盖率/契约/变形/变异等测试）。
- 除统计判定外，框架还补齐了代理测试基础设施：**5维覆盖率指标**（tool/path/state/boundary/model）、面向prompt/tool/model/context的**变异测试算子**、适用于多步代理的**metamorphic relations**、以及用于CI/CD的**统计部署闸门**。
- 论文还声称与AgentAssert契约框架集成，使行为契约可作为形式化测试oracle，用于部署前验证代理是否仍满足要求。

## Results
- 综合评测覆盖 **5个模型、3个代理场景、7,605次试验**，总实验成本为 **227美元**；模型包括 **GPT-5.2、Claude Sonnet 4.6、Mistral-Large-3、Llama-4-Maverick、Phi-4**。
- 论文宣称 **SPRT顺序概率比检验** 在所有场景中都把试验次数降低了 **78%**，同时保持相同统计保证。
- **Behavioral fingerprinting** 的回归检测功效达到 **86% detection power**，而基于二元pass/fail的测试在对应设置下为 **0%**。
- **Adaptive budget optimization** 对稳定代理可把所需试验数再减少 **4–7×**。
- 论文总体声称其token-efficient技术可实现 **5–20× cost reduction**，并在 **trace-first offline analysis** 下对四类测试达到 **100% cost savings / zero additional token cost**。
- 摘要中还给出整体范围：在保持严格统计保证的前提下，AgentAssay实现 **78–100% 成本下降**；这是其最核心的突破性结果声明。

## Link
- [http://arxiv.org/abs/2603.02601v1](http://arxiv.org/abs/2603.02601v1)
