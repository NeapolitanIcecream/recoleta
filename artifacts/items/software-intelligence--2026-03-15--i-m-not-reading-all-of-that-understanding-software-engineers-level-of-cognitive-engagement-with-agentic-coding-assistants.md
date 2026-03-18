---
source: arxiv
url: http://arxiv.org/abs/2603.14225v1
published_at: '2026-03-15T05:03:20'
authors:
- Carlos Rafael Catalan
- Lheane Marie Dizon
- Patricia Nicole Monderin
- Emily Kuang
topics:
- agentic-coding-assistant
- human-ai-interaction
- code-intelligence
- cognitive-engagement
- software-engineering
relevance_score: 0.91
run_id: materialize-outputs
---

# I'm Not Reading All of That: Understanding Software Engineers' Level of Cognitive Engagement with Agentic Coding Assistants

## Summary
这篇论文研究软件工程师与具代理性的编码助手协作时的认知投入，指出开发者在任务推进过程中会越来越少地思考过程本身。作者据此主张将 ACA 设计成真正支持思考的“思维工具”，而不只是自动产出代码的执行器。

## Problem
- 论文要解决的问题是：软件工程师在使用 agentic coding assistants（ACA）时，是否会随着代理自主性增强而降低批判性思考与过程理解。
- 这很重要，因为软件工程师需要判断正确性、权衡取舍并识别失败模式，而 LLM/ACA 仍可能出现幻觉、偏差或隐藏缺陷。
- 如果开发者只验证“结果对不对”而不理解“它是怎么做的”，高风险软件场景中可能更容易漏掉错误、边界条件和安全问题。

## Approach
- 作者做了一个形成性用户研究，招募 **4 名**软件工程师，经验跨度从 **少于 1 年到 10 年以上**，让他们使用 **Cline** 完成一个 Excel 处理代码生成任务。
- 任务流程分为 **Plan** 和 **Act** 两阶段，研究者现场观察参与者如何阅读计划、回应澄清问题、查看执行输出，以及是否审查生成代码。
- 研究以 **Bloom 分类法**作为认知参与框架，把认知投入拆成 **recall / understand / analyze / evaluate** 四类，并在任务后立即发放自报告问卷以降低记忆偏差。
- 作者再将问卷回答与实际工作目录、生成文件和观察记录交叉核对，并做主题分析，识别认知投入随阶段变化的模式。
- 核心机制可以用最简单的话概括：先让工程师真实使用 ACA 做任务，再检查他们到底记住了多少、理解了多少、分析了多少、评估了多少，从而判断 ACA 是否在削弱思考。

## Results
- 样本规模很小，仅 **4 名参与者**，论文没有报告统计显著性或大规模基准结果；其结论属于 **形成性/探索性发现**。
- 作者声称认知投入在任务推进中持续下降：规划阶段投入最高，执行阶段因文本信息过载而下降，评估阶段则主要只看输出是否正确，而较少检查代码生成过程。
- 在回忆题中，关于“生成脚本有多少个函数/方法”，**4/4 都答错（0% 正确）**，说明对代码结构的记忆非常薄弱。
- 关于工作目录名称的回忆，只有 **2/4 答对（50%）**；关于第一个创建的文件名，**3/4 答对（75%）**。
- 论文还报告：只有 **一半（2/4）** 参与者能理解第一个函数的作用并给出可靠概述；也只有 **一半（2/4）** 能较好分析代码并对其处理边界情况有信心。
- 在是否继续手动修改代码上，参与者给出的理由集中于“**It generated my desired output**”“**I trust Cline**”“**It worked**”，支持作者的核心结论：开发者更关注 happy path 和最终输出，而非过程级验证。

## Link
- [http://arxiv.org/abs/2603.14225v1](http://arxiv.org/abs/2603.14225v1)
