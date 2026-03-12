---
source: arxiv
url: http://arxiv.org/abs/2603.03233v1
published_at: '2026-03-03T18:25:00'
authors:
- Zihang Zeng
- Jiaquan Zhang
- Pengze Li
- Yuan Qi
- Xi Chen
topics:
- multi-agent-systems
- scientific-code-generation
- bayesian-optimization
- low-code-platform
- llm-reliability
relevance_score: 0.85
run_id: materialize-outputs
---

# AI-for-Science Low-code Platform with Bayesian Adversarial Multi-Agent Framework

## Summary
本文提出一个面向 AI4S 的低代码平台，把任务规划、代码生成和测试评估拆给三个代理，并用贝叶斯更新来持续改进提示词、测试用例和候选代码。核心目标是降低 LLM 幻觉与多代理误差传播，使较小模型也能更稳定地产生科学代码。

## Problem
- 科学代码生成不仅会出现普通代码错误，还会违反领域约束、物理规律或复杂执行流程要求，因此单次生成和静态单元测试都不够可靠。
- 多代理系统虽然能分工，但一个代理生成的错误代码或错误测试会传递给下游代理，导致错误被放大而不是被纠正。
- 领域科学家常用自然语言提出模糊需求，不擅长提示工程，这会让模型更容易误解任务并输出不可信结果。

## Approach
- 提出三代理框架：Task Manager 负责把用户需求拆成可执行计划并生成/更新测试；Solution Generator 生成多份候选代码；Evaluator 对代码、测试和提示整体打分。
- 用对抗式循环让 TM 像“出题人”一样不断构造更能暴露弱点的测试，SG 像“解题人”一样根据反馈迭代改进代码，从而共同提升质量。
- 用非 LLM 的贝叶斯更新规则，根据提示对应的历史表现分数 \(S_3\) 递归选择更好的测试用例与样例代码组合，减少系统对任何单一 LLM 可靠性的依赖。
- 为了避免每轮都执行所有候选代码的高成本，使用基于 AST 结构与代码嵌入的贝叶斯优化来预测未充分测试代码的潜力，优先评估更有希望的候选。
- 平台支持用户先审阅任务计划并反馈，系统再把高层自然语言需求转成更明确的科学子任务、约束和初始测试，降低非程序员使用门槛。

## Results
- 在 SciCode 上，框架对所有底座模型都带来稳定提升；作者声称开源模型最高相对提升达 **87.1%**，对应 **Qwen3-8B** 在 **Without Knowledge / Sub** 指标上从 **13.2** 提升到 **24.7**。
- 在 SciCode 上，**Qwen3-14B + 本框架** 在 **Without Knowledge / Sub** 达到 **30.6**，与 **Qwen3-235B-A22B-Instruct** 基线的 **30.6** 持平，作者据此强调小模型可追平大模型。
- 论文摘要特别声称：在 ScienceCode/SciCode 基准上，借助该框架，**32B 开源模型可击败 235B 模型**；表中对应地 **Qwen3-32B + Ours** 在 **Without Knowledge / Sub** 为 **33.0**，高于 **Qwen3-235B baseline** 的 **30.6**。
- 其他 SciCode 例子：**GPT-4o** 从 **24.1/1.5** 提升到 **37.2/7.7**（Without Knowledge 的 Sub/Main），带知识设置下从 **33.7/7.7** 提升到 **40.6/10.8**；**Claude-sonnet-4** 从 **31.3/7.7** 提升到 **42.7/13.8**。
- 在 **ScienceAgentBench** 上，以 **GPT-4o** 为底座时，作者声称达到新的 SOTA，尤其是 **VER**：**90.2%（without knowledge）** 和 **87.3%（with knowledge）**，显著超过其他方法；文中还称其在 **SR** 和 **CBS** 上也处于领先，但截取内容未给出完整对比表数字。
- 实验设置中，系统默认每轮生成 **20** 段代码、初始 **15** 个测试、最少保留 **20** 个测试，并用采集函数再挑选 **5** 个代码做进一步评估，表明方法在实践上是面向迭代筛选而非单次生成。

## Link
- [http://arxiv.org/abs/2603.03233v1](http://arxiv.org/abs/2603.03233v1)
