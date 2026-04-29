---
kind: ideas
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- token-cost
- repo-level-generation
- verification
- traceability
- agent-safety
tags:
- recoleta/ideas
- topic/coding-agents
- topic/token-cost
- topic/repo-level-generation
- topic/verification
- topic/traceability
- topic/agent-safety
language_code: zh-CN
---

# 代码变更控制

## Summary
最明确的近期变化在执行层面。编码代理产品需要在运行过程中加入明确的 token 控制，仓库级生成在项目变大后需要按依赖顺序组织工作流，而维护团队也有充分理由采用一层可追踪性能力，用更小的上下文和可见证据把需求与代码关联起来。

## 用于编码代理运行的仓库感知 token 预算控制器
使用编码代理的工程团队需要在长时程运行前设置成本闸门，并对重复查看和编辑文件设定硬性停止条件。现在的证据已经不只是对代理昂贵的模糊抱怨。在 OpenHands 的 SWE-bench Verified 上，agentic coding 的 token 使用量约为单轮 code reasoning 的 3500×，约为多轮 code chat 的 1200×，而同一任务的不同运行之间最多可相差 30×。论文将最糟糕的失败与冗余搜索行为联系起来，尤其是重复访问文件和重复编辑，并指出模型在开始前很难准确预测自己的 token 开销。

一个可行的产品形态是仓库感知的预算控制器，实时监控动作轨迹，在代理开始空转时把运行切分成更小的范围。控制点很直接：统计文件打开次数、重复访问次数、编辑回退次数和上下文增长，然后在这些计数超过阈值时，要求缩小子任务范围，或由人工批准继续。已经为自主修 bug 或功能开发付费的团队会最先在意这一点，因为他们要承担失败轨迹的成本，而且通常无法事先得到可靠的费用估算。

一个低成本测试是回放过去的代理轨迹，衡量在文件反复变动后提前停止，能有多大概率在不降低通过率的前提下减少 token 消耗。如果这个控制器主要拦住的是失败运行和后期游走，它就适合作为编码代理产品的默认保护措施发布。

### Evidence
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Token 成本研究报告了 3500× 和 1200× 的成本差距、最高 30× 的运行波动，以及较差的自我预测能力。
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): 论文摘录将更高成本与重复动作联系起来，并显示成本增长主要由输入 token 驱动。

## 面向 1000 LOC 以上仓库的按依赖顺序文件生成
当项目规模超过约 1000 行代码时，仓库级代码生成流程应当把规划与实现拆开。RealBench 表明，即使模型拿到自然语言需求以及 UML 包图和类图，它们在完整仓库上的表现仍然很差。最佳平均 Pass@1 只有 19.39%，500 LOC 以下的表现高于 40%，2000 LOC 以上低于 15%，而且平均只有 44.73% 的方法是独立的。在最大的仓库中，独立方法比例降到 26.23%，这说明依赖处理是主要失败来源。

具体的流程变化是，不要再让模型在中大型代码库上直接输出整个仓库。应先让模型根据设计产物梳理模块、接口和依赖边，再按文件逐步生成，并在每一步后运行测试。RealBench 自身的对比也支持这一点：完整仓库生成在较小仓库上效果更好，而仓库规模变大后，增量生成效果更好。

一个低成本检查方法是，选一个内部待办项，它已经有架构说明或图表，然后用两种方式各跑一次：一次性完整仓库生成，以及按依赖顺序生成文件。衡量测试通过率、导入损坏数量和人工修复时间。构建内部脚手架、SDK 或 CRUD 密集型服务的团队，可以在不改动整套工具链的前提下试用这种做法。

### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): RealBench 摘要提供了按仓库规模划分的 Pass@1 和依赖统计。
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): 论文摘录指出，小型仓库更适合完整仓库生成，而复杂仓库更适合增量生成。

## 用于按需求关联影响分析的 pull-request 可追踪性侧边工具
需求可追踪性现在已经足以支持一种更聚焦的维护工具：把变更后的需求关联到最可能受影响的文件、类或方法，同时把上下文控制在日常开发可接受的范围内。R2Code 在五个数据集上相对强基线平均提升了 7.4% 的 F1，并通过自适应上下文控制将 token 使用量最多降低 41.7%。它的机制对产品设计有直接意义：它把需求和代码拆成相互对齐的语义部分，检查每条候选链接的解释，并根据需求复杂度调整检索深度。

这支持一种具体的产品形态，适合处理陈旧工单、文档薄弱或受监管变更审查的团队：一个 pull request 侧边工具，输入 requirement ID，给出代码链接建议，展示每条链接的解释，并将一致性较低的匹配标出来供人工审核。当任务是影响分析或审计准备时，这比宽泛的代码聊天更有用，因为用户需要的是与命名工件绑定的紧凑证据链。

一个低成本检查方法是，从某个服务中抽样已解决工单，先隐藏实际修改过的文件，再将工具给出的 top-k 链接建议与真实实现 diff 对比。如果这些链接足够准确，能减少维护者的查找时间，那么这层可追踪性能力就值得在更广泛的代理工作流之前先落地。

### Evidence
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): R2Code 摘要报告了 F1 提升、自适应检索和更低的 token 使用。
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): 论文摘录指出，平均 F1 提升 7.4%，token 消耗最多降低 41.7%。
