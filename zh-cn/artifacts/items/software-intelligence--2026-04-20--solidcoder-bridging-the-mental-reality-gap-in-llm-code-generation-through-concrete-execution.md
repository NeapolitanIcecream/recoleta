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
SolidCoder 通过把想象中的执行检查替换为沙箱中的真实执行和基于性质的测试，提升了大模型代码生成效果。论文认为，现有代理流水线之所以失效，是因为模型在规划阶段漏掉边界情况，又在验证阶段误判有缺陷的代码。

## 问题
- 现有代码生成代理常依赖 mental simulation 来做规划和调试，所以它们会编造执行轨迹，并批准错误代码。
- 论文把这种失败拆成两部分：**Specification Gap** 指早期规划时漏掉边界情况，**Verification Gap** 指后期把有缺陷的代码当成正确代码。
- 这在竞赛编程和类似任务中很重要，因为这类任务要求代码通过隐藏测试；一旦过度自信，最终提交就会出错。

## 方法
- SolidCoder 是一个多智能体流水线，核心规则只有一条：执行代码，不要相信模型内部的轨迹。
- **Shift-left Planning** 要求模型在写算法前先暴露边界情况，让方案一开始就考虑边界条件。
- **Oracle-based Assertions** 通过测试输出性质而不是精确答案来避免缺少 oracle 的问题，例如顺序、长度或排列约束。
- **Live Execution** 在沙箱中运行生成的代码，并用真实失败、断言错误和运行时错误来推进调试。
- **Intermediate Simulation** 在代码生成后提供一次低成本的初步检查，**Defensive Accumulation** 会保留所有发现的失败测试，避免后续修复把旧 bug 重新引入。

## 结果
- 在 **GPT-4o** 上，SolidCoder 报告的 **pass@1** 达到最新水平：**HumanEval 95.7%**，对比 **CodeSIM 的 95.1%**，提升 **+0.6%p**；**CodeContests 77.0%**，对比 **72.7%**，提升 **+4.3%p**；**APPS 26.7%**，对比 **23.3%**，提升 **+3.4%p**。
- 在测试的三种模型上，SolidCoder 在全部九组模型-基准组合中都追平或超过了 CodeSIM。HumanEval 的平均 pass@1 从 **97.0% 升到 97.2%**，CodeContests 从 **85.3% 升到 89.1%**，APPS 从 **34.6% 升到 36.5%**。
- 在 **CodeContests** 上，不同模型的提升都很一致：**GPT-4o 72.7% -> 77.0%（+4.3%p）**，**GPT-OSS-120B 87.9% -> 92.1%（+4.2%p）**，**Grok-4.1-Fast 95.2% -> 98.2%（+3.0%p）**。
- **GPT-4o 在 CodeContests 上的消融实验** 显示，去掉 **Shift-left Planning** 时下降最大：**77.0% -> 53.3%（-23.7%p）**。去掉其他模块也会变差：**Intermediate Simulation 64.0%（-13.0%p）**，**Oracle-based Assertions 65.4%（-11.6%p）**，**Live Execution 69.1%（-7.9%p）**，**Defensive Accumulation 70.3%（-6.7%p）**。
- 效率表显示，这些提升带来了更多推理开销。对于 **GPT-4o 在 APPS 上**，SolidCoder 需要 **35 次 API 调用 / 60.4K tokens**，而 CodeSIM 需要 **26 次 / 49.3K**。对于 **Grok-4.1-Fast 在 APPS 上**，SolidCoder 需要 **47 次调用 / 520.9K tokens**，而 CodeSIM 需要 **20 次 / 266.5K**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19825v1](http://arxiv.org/abs/2604.19825v1)
