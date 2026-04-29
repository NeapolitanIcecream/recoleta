---
source: arxiv
url: http://arxiv.org/abs/2604.19825v1
published_at: '2026-04-20T13:00:46'
authors:
- Woojin Lee
- Jin-Xia Huang
topics:
- llm-code-generation
- multi-agent-systems
- execution-grounding
- program-synthesis
- property-based-testing
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution

## Summary
## 摘要
SolidCoder 通过用真实的沙箱执行和基于性质的测试替代想象中的执行检查，提升了 LLM 的代码生成效果。论文认为，当前的智能体流水线会失败，原因是模型在规划阶段漏掉边界情况，随后又在验证阶段误判有缺陷的代码。

## 问题
- 现有代码生成智能体常依赖心理模拟来规划和调试，因此它们会编造执行轨迹，并批准错误代码。
- 论文将这种失败分成两部分：前期漏掉边界情况的 **Specification Gap**，以及后期把有缺陷的代码当成正确代码的 **Verification Gap**。
- 这很重要，因为竞赛编程和类似任务需要代码通过隐藏测试，而错误的自信会导致最终提交出错。

## 方法
- SolidCoder 是一个多智能体流水线，核心规则只有一条：执行代码，而不是相信模型内部的执行轨迹。
- **Shift-left Planning** 要求模型在编写算法前先找出边界情况，让规划从一开始就覆盖边界条件。
- **Oracle-based Assertions** 通过测试输出性质而不是精确答案，避开缺少判定器的问题，例如检查顺序、长度或排列约束。
- **Live Execution** 在沙箱中运行生成的代码，并用真实的失败、断言错误和运行时错误来推动调试。
- **Intermediate Simulation** 在代码生成后提供一次低成本的初步检查，**Defensive Accumulation** 则保留每一个已发现的失败测试，避免后续修复重新引入旧 bug。

## 结果
- 在 **GPT-4o** 上，SolidCoder 报告了当前最好的 **pass@1**：**HumanEval 上 95.7%**，而 **CodeSIM 为 95.1%**（**+0.6%p**）；**CodeContests 上 77.0%**，而 **72.7%**（**+4.3%p**）；**APPS 上 26.7%**，而 **23.3%**（**+3.4%p**）。
- 在全部三个测试模型上，SolidCoder 在全部九个模型-基准组合中都追平或超过 CodeSIM。平均 pass@1 从 **97.0% 提高到 97.2%**（HumanEval），从 **85.3% 提高到 89.1%**（CodeContests），从 **34.6% 提高到 36.5%**（APPS）。
- 在 **CodeContests** 上，各模型的提升都较稳定：**GPT-4o 72.7% -> 77.0% (+4.3%p)**、**GPT-OSS-120B 87.9% -> 92.1% (+4.2%p)**、**Grok-4.1-Fast 95.2% -> 98.2% (+3.0%p)**。
- 在 **CodeContests with GPT-4o** 的消融实验中，移除 **Shift-left Planning** 的下降幅度最大：**77.0% -> 53.3% (-23.7%p)**。移除其他模块也会带来损失：**Intermediate Simulation 64.0% (-13.0%p)**、**Oracle-based Assertions 65.4% (-11.6%p)**、**Live Execution 69.1% (-7.9%p)**、**Defensive Accumulation 70.3% (-6.7%p)**。
- 效率表显示，这些提升需要更多推理开销。对于 **GPT-4o on APPS**，SolidCoder 使用 **35 次 API 调用 / 60.4K tokens**，而 CodeSIM 为 **26 / 49.3K**。对于 **Grok-4.1-Fast on APPS**，它使用 **47 次调用 / 520.9K tokens**，而 CodeSIM 为 **20 / 266.5K**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19825v1](http://arxiv.org/abs/2604.19825v1)
