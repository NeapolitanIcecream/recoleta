---
kind: ideas
granularity: day
period_start: '2026-04-11T00:00:00'
period_end: '2026-04-12T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- verification
- agent-memory
- benchmarks
- systems-optimization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/verification
- topic/agent-memory
- topic/benchmarks
- topic/systems-optimization
language_code: zh-CN
---

# Agent Runtime Infrastructure

## Summary
这些证据里最清楚的可落地变化，是用于代码导航的结构化文件、代理 harness 里的记忆控制，以及在 Apache DataFusion 中经过执行验证的计划重写。每一项都给出了一种具体的构建或流程改动，并带有可测量的效果；更宽泛的结对编程和基准论文，更适合作为支持性背景，而不是立刻要做的产品方向。

## Versioned architecture descriptor files for agent code navigation
仓库维护者可以把架构描述符作为编码代理的一级文件加入仓库，然后先测它是否减少导航，再决定是否让代理做更自主的编辑。这里的证据更指向减少无效搜索，而不是原始编码质量。在那项受控研究里，架构上下文把一个 22K 行 Rust 项目的平均导航步数从 5.2 降到 3.4（S-expression 或 JSON），Markdown 则降到 2.9。在第二项针对 43K 行 Rust 项目的研究里，一个自动生成的 170 行描述符在 15 个任务上的准确率达到 100%，而盲搜只有 80%。这些结果足以支持一个具体方案：生成一个仓库描述符，写清组件、符号边界、约束和数据流，把它放进版本控制，在任务开始时交给代理。

短期内的用户是已经在中等规模代码库里使用 Claude Code、Cursor 或类似工具的团队，代理在 grep、文件搜索和模块阅读上花了太多轮次。低成本验证很直接：在一组固定的代码定位和补丁任务上，对比加入描述符前后的 explore/edit 比例和工具调用次数。格式问题对模型表现来说次要。论文报告了 S-expression、JSON、YAML 和 Markdown 的理解结果相近；在错误注入测试里，JSON 的静默损坏最低，而 S-expression 对结构完整性错误的检测更可靠。这指向一条落地路径：团队选一个最适合自己工具链和校验需求的格式，然后在 CI 里用 schema 检查强制执行。

### Evidence
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): Architecture descriptors reduced navigation steps and an auto-generated descriptor improved task accuracy.
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): The paper frames codebase exploration overhead as the operational pain for coding agents.

## Harness-managed typed memory pages for long-running coding sessions
代理构建者现在已经有足够证据，把长会话的记忆控制从提示词里移到 harness 里。编码会话跨过很多上下文窗口时，常见问题很明确：压缩后计划消失，重置后约束丢失，代理反复调用工具，因为它分不清哪些状态仍然有效。ClawVM 给出了一种具体实现：把状态存成带类型的页面，为每类页面定义最低保真表示，用两阶段方式组装提示词，保证必需状态先进入上下文，并在生命周期边界要求经过验证的回写。

论文报告的收益已经足够支持一个实现决策。在四类工作负载和六个 token 预算下，当最低保真集合能装进预算时，ClawVM 把平均可由策略控制的故障数从检索基线的 67.8、压缩加检索基线的 1.5 降到 0。在 12 条真实轨迹和 30 次任务回放上，它也报告了 0 个可由策略控制的故障，并且在最紧预算下成功率为 100%，中位策略开销低于每轮 50 微秒。一个实用的首个部署目标，是那些需要在长会话里保留计划、约束、证据和用户偏好的编码代理。第一步验证很简单：看带类型的内存页是否能在你的真实轨迹上减少重复工具调用、计划丢失和重置失败，而且不会把延迟推到用户能感知的程度。

### Evidence
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): ClawVM reports zero policy-controllable faults under fit-to-budget conditions and describes the typed-page memory policy.
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): The abstract states that harness-managed residency and durability are the enforcement point for long-running tool-using agents.

## Offline JSON Patch plan rewriting for expensive DataFusion queries
在 Apache DataFusion 上做数据库工作的团队，可以试用一个 LLM 辅助的物理计划重写器，用 JSON Patch 编辑计划，并只保留执行更快的改写。这是一个范围很窄的流程，但机制具体，用户能直接看到效果。系统把物理算子图序列化成紧凑的 JSON 形式，让模型给出像 join 重排这样的局部编辑，通过执行验证候选计划，然后从改进后的计划继续迭代。

主案例研究把一个 `d_year=2001` 过滤条件提前到计划前面，在后续 join 之前把销售事实表从 1510 万行削到 290 万行。那次运行报告了 4.78x 的提速，哈希表构建时间从 10.16 秒降到 0.41 秒，构建内存从 3.3 GB 降到 411 MB。在生成的 TPC-H 和 TPC-DS 工作负载上，中位收益更小，大约是 1.1x 到 1.2x，所以它最适合复杂 OLAP 查询里的定向调优，前提是基数估计不准。一个低成本的验证路径是：在离线状态下，把补丁循环跑在一组已保存的坏计划上，通过执行要求语义等价，并记录哪些算子编辑反复出现，足够多时再把它们固化成原生优化器规则。

### Evidence
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): The summary gives the JSON Patch mechanism and the measured speed and memory improvements in Apache DataFusion.
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): The content describes DBPlanBench exposing compact physical plans to the LLM because native plans are too large to reason over directly.
