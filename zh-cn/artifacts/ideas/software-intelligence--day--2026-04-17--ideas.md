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
短期内最清晰的可构建方向，是在智能体行动前加入检查其是否真正理解任务的控制层。这里最具体的三个例子是：面向纯意图查询的结构化仓库定位器、围绕代码生成的需求对齐门禁，以及面向长时编码会话的规则执行封装。它们都在中间环节加入了明确检查，并且各自都有直接证据表明能改进定位效果、任务匹配度或规则遵循率。

## 用于无名称工程请求的 Datalog 仓库定位
仓库智能体需要一种结构化代码定位器，用来处理不包含有效名称的请求。LogicLoc 给出了这一层的具体做法：提取仓库事实，让模型基于这些事实编写 Datalog，然后在 Soufflé 执行前，用解析器检查和 synthesize-check-refine 循环为查询设卡。它适合用于 issue 分诊和仓库导航，尤其是在请求描述的是代码库的某种属性，而不是一个搜索字符串时。论文中的示例查询要求找出参数超过 15 个且非 `__init__` 的函数，结果在 Astropy 中返回两个精确匹配；这类答案通常是词法检索器容易漏掉的。一个低成本的产品测试很直接：收集内部工程问题，这些问题提到行为、结构或约束，但省略文件名和符号名，然后把精确命中率与你当前的仓库搜索或智能体检索栈做对比。

### Evidence
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md): 概述了与关键词无关的定位问题、LogicLoc 的架构，以及 Astropy 示例中的精确匹配结果。
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md): 确认该系统会把自然语言查询转成 Datalog，并在经过验证的闭环中执行。

## 代码生成前后基于需求清单的门禁
编码助手可以在代码生成前加入一步需求检查，并在首个草稿生成后再做一次。REA-Coder 提供了一个直接可用的模板：把提示词转成需求问题清单，将模型答案与参考答案对比，在发现缺口时重写需求，再生成代码；如果输出失败，就遮蔽需求中的关键语义片段，并让模型根据生成的代码恢复这些内容。这个方法适合已经有测试，但仍经常拿到“代码能运行却做错任务”的团队。论文报告的提升幅度足以支持先在高难度提示词类别中小范围上线：相对最强基线，CodeContests-raw 的平均提升达到 30.25%，CodeContests 达到 26.75%；即使只做生成前的需求对齐，也能让首次生成代码相对 zero-shot 在 APPS 上提升 210.44%，在 xCodeEval 上提升 344.67%。一个实际的首个部署点，是给处理长篇自然语言验收标准工单的编码智能体加上 pre-submit 门禁。

### Evidence
- [Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation](../Inbox/2026-04-17--bridging-the-gap-between-user-intent-and-llm-a-requirement-alignment-approach-for-code-generation.md): 给出了完整的 REA-Coder 循环，以及它在不同模型和数据集上的基准提升，包括生成前需求对齐的收益。
- [Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation](../Inbox/2026-04-17--bridging-the-gap-between-user-intent-and-llm-a-requirement-alignment-approach-for-code-generation.md): 确认了论文的说法：现有方法很少验证模型是否真的理解了需求。

## AI 编码会话中的步骤级规则执行
使用 `AGENTS.md` 或类似规则文件的团队，可以把规则遵循从提示词记忆里移出来，改成与计划步骤绑定的执行门禁。Zoro 展示了这层支持机制的样子：规划完成后，把规则挂到具体步骤上；执行过程中，对每条已应用规则都要求提交证明；对于可测试规则，在进入下一步前还要提供单元测试。这能处理长时间编码会话中的常见问题：智能体逐渐偏离架构、工作流或 UI 约束，开发者不得不一再重复这些要求。论文报告的结果是，在 36 次会话中，规则遵循率提高了 57%；该系统也被设计成可通过共享指令文件和证据目录接入现有智能体。可以立刻动手做的版本，是在你当前编码智能体外包一层轻量封装，记录是哪条规则阻塞了进度、提交了什么证明，以及哪些规则总是在失败后被用户反复修改。

### Evidence
- [ZORO: Active Rules for Reliable Vibe Coding](../Inbox/2026-04-17--zoro-active-rules-for-reliable-vibe-coding.md): 描述了 Enrich-Enforce-Evolve 工作流，以及在 36 次会话中规则遵循率提升 57% 的结果。
- [ZORO: Active Rules for Reliable Vibe Coding](../Inbox/2026-04-17--zoro-active-rules-for-reliable-vibe-coding.md): 说明了实际操作中的痛点：智能体会随着时间推移忽视指令，开发者需要反复重申项目规则。
