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
- cognitive-engagement
- software-engineering
- user-study
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# I'm Not Reading All of That: Understanding Software Engineers' Level of Cognitive Engagement with Agentic Coding Assistants

## Summary
这篇论文通过一个小规模形成性用户研究，考察软件工程师在使用具身代理式编码助手时的认知参与如何变化。作者发现，随着任务推进，工程师越来越少去理解和核查过程，而更关注“结果看起来对不对”。

## Problem
- 论文要解决的问题是：软件工程师在使用 agentic coding assistants（ACA）时，是否会因为助手过于自主而降低批判性思考、验证和理解。
- 这很重要，因为软件工程师开发的软件常用于高风险真实场景，而 ACA/LLM 仍可能出现幻觉、偏差或遗漏边界情况。
- 如果工程师只看“happy path”并过度信任 ACA，错误代码、脆弱实现甚至潜在安全问题可能被带入生产系统。

## Approach
- 作者进行了一个形成性用户研究，招募 **4 名**来自菲律宾一家大型公司的软件工程师，经验覆盖 **<1 年、1-5 年、6-10 年、>10 年** 四档。
- 参与者使用 **Cline** 完成一个固定的代码生成任务：处理 Excel 文件、定位 dashboard sheet、复制列数据并生成新 workbook。
- 研究将交互划分为 **planning / execution / evaluation** 三阶段，并用 **Bloom’s Taxonomy** 设计事后问卷，衡量回忆、理解、分析、评价四类认知参与。
- 作者把问卷回答与实际工作目录/生成代码进行交叉核对，并结合观察笔记做主题分析，寻找认知参与的变化模式。
- 核心机制可用最简单的话概括：先让工程师完成一次真实 ACA 编程任务，再检查他们究竟记住了什么、理解了什么、分析了什么，以及是否真的评估了代码过程而不只是结果。

## Results
- 主要发现是认知参与随任务推进而下降：参与者在 **planning 阶段最投入**，但在 **execution 阶段** 因为大量文本输出而明显 disengage，到了 **evaluation 阶段** 多数只验证输出、不审查过程。
- 在回忆题中，关于工作目录名，只有 **2/4** 回答正确；关于第一个创建的文件名，**3/4** 正确；关于生成脚本有多少个函数，**4/4 全部答错**。
- 在理解层面，作者报告只有 **一半（2/4）** 参与者能理解第一个函数并可靠地给出简要总结。
- 在分析层面，也只有 **一半（2/4）** 能较好分析代码并对其处理边界情况有信心；参与者主要记住和分析的是通向正确输出的 **“happy path”**。
- 在评价层面，**4/4** 参与者在得到看似正确的 Excel 输出后都没有继续手动修改代码；其理由包括“**It generated my desired output**”“**I trust Cline**”“**It worked**”。
- 论文没有给出统计显著性检验、对照基线或大样本定量性能提升结果；最强的具体主张是：当前 ACA 的文本式交互会造成信息过载，促使工程师采用低成本验证策略，从而削弱深度思考。

## Link
- [http://arxiv.org/abs/2603.14225v1](http://arxiv.org/abs/2603.14225v1)
