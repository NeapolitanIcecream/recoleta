---
kind: ideas
granularity: day
period_start: '2026-04-17T00:00:00'
period_end: '2026-04-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code-agents
- repository-reasoning
- requirement-alignment
- multimodal-retrieval
- formal-verification
tags:
- recoleta/ideas
- topic/code-agents
- topic/repository-reasoning
- topic/requirement-alignment
- topic/multimodal-retrieval
- topic/formal-verification
language_code: zh-CN
---

# 中间动作检查

## Summary
短期最清晰的构建方向，是在代理行动前加控制层检查理解情况。这里最具体的三个例子分别是：面向意图型查询的结构化仓库定位器、围绕代码生成的需求对齐门禁，以及面向长编码会话的规则执行封装。每一个都插入了一个明确的中间检查，并且都有更好定位、更好任务匹配或更好守规则的直接证据。

## 基于 Datalog 的仓库定位，用于无名称工程请求
仓库代理需要一种结构化代码定位器，来处理没有任何有用名称的请求。LogicLoc 就是这一层的具体做法：先提取仓库事实，让模型基于这些事实写 Datalog，再在 Soufflé 执行前用解析器检查和 synthesize-check-refine 循环把查询关住。它适合处理问题分流和仓库导航，尤其是请求描述的是代码库的属性，而不是搜索字符串。论文中的示例查询要求找出参数超过 15 个且不是 `__init__` 的函数，并返回了 Astropy 里的两个精确匹配，这类答案通常是词法检索器会漏掉的。一个便宜的产品测试很直接：收集内部工程问题，保留对行为、结构或约束的描述，但去掉文件名和符号名，然后把精确命中率和现有仓库搜索或代理检索栈做对比。

### Evidence
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md): Summarizes the keyword-agnostic localization problem, LogicLoc architecture, and the concrete Astropy example with exact matches.
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md): Confirms the system translates natural-language queries into Datalog and executes them in a validated closed loop.

## 代码生成前后都做需求清单门禁
编码助手可以在生成代码前加一道需求检查，在初稿之后再加一道检查。REA-Coder 给出了一套直接模板：把提示词转成需求问题清单，把模型回答和参考答案对比，发现缺口时重写需求，再生成代码，然后通过遮盖需求中的关键语义片段，要求模型从代码里恢复这些片段来检查失败输出。这适合已经有测试、但仍会产出解决错任务代码的团队。报告中的增益足以支持在难提示类上做小范围上线：相对最佳基线的平均提升在 CodeContests-raw 上达到 30.25%，在 CodeContests 上达到 26.75%，而仅靠生成前对齐一步，就能把零样本的一次生成表现提升 210.44%（APPS）和 344.67%（xCodeEval）。一个实际的首个落地方式，是给处理长自然语言验收标准的编码代理加一个提交前门禁。

### Evidence
- [Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation](../Inbox/2026-04-17--bridging-the-gap-between-user-intent-and-llm-a-requirement-alignment-approach-for-code-generation.md): Provides the full REA-Coder loop and benchmark gains across models and datasets, including pre-generation alignment gains.
- [Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation](../Inbox/2026-04-17--bridging-the-gap-between-user-intent-and-llm-a-requirement-alignment-approach-for-code-generation.md): Confirms the paper's claim that existing methods rarely verify whether the model actually understood the requirement.

## 面向 AI 编码会话的逐步规则执行
使用 `AGENTS.md` 或类似规则文件的团队，可以把守规则从提示词记忆里移到和计划步骤绑定的执行门禁里。Zoro 展示了这种支持层的样子：在规划后把规则挂到具体步骤上，在执行时要求每条已应用规则都提交证明，并且在可测试规则上继续前必须写单元测试。这解决了长编码会话里的常见问题：代理会逐渐偏离架构、工作流或 UI 约束，开发者只能反复重申这些规则。论文报告的结果是在 36 次会话里守规则率提升了 57%，而且系统通过共享指令文件和证据目录，可以和现有代理一起工作。最直接的构建方式，是在当前编码代理外面包一层薄封装，记录是哪条规则卡住了进度、提交了什么证明，以及用户在失败后还在反复修改哪些规则。

### Evidence
- [ZORO: Active Rules for Reliable Vibe Coding](../Inbox/2026-04-17--zoro-active-rules-for-reliable-vibe-coding.md): Describes the Enrich-Enforce-Evolve workflow and the 57% rule-following improvement across 36 sessions.
- [ZORO: Active Rules for Reliable Vibe Coding](../Inbox/2026-04-17--zoro-active-rules-for-reliable-vibe-coding.md): Shows the operational pain: agents ignore instructions over time and developers repeatedly reassert project rules.
