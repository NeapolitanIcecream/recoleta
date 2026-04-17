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

# 代理运行时基础设施

## Summary
这组证据里最明确的可落地变化是：用于代码导航的结构化文件、放在代理 harness 中的内存控制，以及 Apache DataFusion 中经执行验证的计划重写。每一项都对应具体的构建或工作流改动，并且有可量化的效果；相比之下，那些更宽泛的结对编程和基准测试论文更适合作为补充背景，而不是直接的产品方向。

## 用于代理代码导航的版本化架构描述符文件
仓库维护者可以把架构描述符作为面向编码代理的一等文件加入仓库，然后先衡量它是否减少了导航开销，再决定是否让代理承担更多自主修改。这里的证据主要指向搜索浪费，而不是代码生成质量本身。在受控研究中，在一个 22K 行的 Rust 项目里，加入架构上下文后，平均导航步数从 5.2 降到 3.4（S-expressions 或 JSON），用 Markdown 时降到 2.9。在第二项针对 43K 行 Rust 项目的研究中，一个自动生成的 170 行描述符在 15 个任务上达到 100% 准确率，而盲目搜索是 80%。这些结果已经足以支持一个明确的构建方案：生成一个仓库描述符，写清组件、符号边界、约束和数据流，把它放进版本控制，并在任务开始时提供给代理。

近期最适合的用户，是已经在中等规模代码库上使用 Claude Code、Cursor 或类似工具的团队，这些代理在 grep、文件搜索和模块阅读上花了太多轮次。低成本验证方式很直接：在加入描述符前后，对一组固定的代码定位和补丁任务比较 explore/edit 比率和工具调用次数。格式问题看起来对模型表现不是首要因素。论文报告说，S-expression、JSON、YAML 和 Markdown 的理解效果接近；同时，JSON 在错误注入测试中的静默损坏最低，而 S-expressions 在捕获结构完整性错误上更稳定。这说明一个可行的采用路径是：团队按自己的工具链和校验需求选择格式，然后在 CI 中用 schema checks 强制执行。

### Evidence
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): 架构描述符减少了导航步数，自动生成的描述符也提升了任务准确率。
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): 论文把代码库探索开销界定为编码代理的主要操作痛点。

## 用于长时间编码会话的 harness 管理类型化内存页面
代理构建者现在已经有足够证据把长会话内存控制从提示词文本移到 harness 中。在跨越多个上下文窗口的编码会话里，这类问题很常见：压缩后计划消失，重置后约束丢失，代理因为无法判断哪些状态仍然有效而重复调用工具。ClawVM 给出了一种明确实现：把状态存成类型化页面，为每种页面类型定义最低保真表示，用两阶段方式组装提示，先保证必需状态进入上下文，再要求在生命周期边界做经过验证的回写。

论文报告的收益已经足以支持一次构建决策。在四类工作负载和六种 token 预算下，只要最低保真集合能放进预算，ClawVM 就把可由策略控制的平均故障数从检索基线的 67.8 和压缩加检索基线的 1.5 降到 0。在 12 条真实轨迹和 30 次任务回放中，它同样报告了 0 个可由策略控制的故障，并在最紧预算下达到 100% 成功率，中位策略开销低于每轮 50 微秒。一个实际的首个部署目标，是那些需要在长会话中持续保存计划、约束、证据和用户偏好的编码代理。第一项测试应当看类型化内存页面是否能在你自己的轨迹上减少重复工具调用、计划丢失事件和重置失败，同时不会把延迟推高到用户能明显察觉的程度。

### Evidence
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): ClawVM 在满足预算条件下报告了 0 个可由策略控制的故障，并描述了类型化页面内存策略。
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): 摘要指出，对于长期运行的工具使用型代理，驻留控制和持久化保证的执行点在 harness。

## 针对高成本 DataFusion 查询的离线 JSON Patch 计划重写
在 Apache DataFusion 上工作的数据库团队可以试用一种由 LLM 辅助的物理计划重写器：它用 JSON Patch 编辑执行计划，只保留执行后更快的改写。这是一个范围较窄的工作流，但机制明确，用户可感知的效果也清楚。系统先把物理算子图序列化为紧凑的 JSON 形式，再让模型提出局部修改，例如连接重排；然后通过执行验证候选计划，并从改进后的计划继续迭代。

主要案例研究把一个 `d_year=2001` 过滤条件提前到执行计划前面，使销售表在后续连接前的行数从 1510 万降到 290 万。那次运行报告了 4.78x 的加速，哈希表构建时间从 10.16 秒降到 0.41 秒，构建内存从 3.3 GB 降到 411 MB。在生成的 TPC-H 和 TPC-DS 工作负载上，中位数提升较小，大约在 1.1x 到 1.2x 之间，所以它更适合作为复杂 OLAP 查询的定向调优步骤，尤其是在基数估计较弱的场景。一个低成本验证路径是：对一组保存下来的糟糕计划离线运行这套 patch 循环，通过执行要求语义等价，并记录哪些算子修改反复出现到足以固化为原生优化器规则。

### Evidence
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): 摘要给出了 JSON Patch 机制，以及 Apache DataFusion 中测得的速度和内存改进。
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): 内容说明 DBPlanBench 向 LLM 提供紧凑的物理计划，因为原生计划过大，无法直接推理。
