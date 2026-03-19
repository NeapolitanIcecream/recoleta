---
source: arxiv
url: http://arxiv.org/abs/2603.08755v1
published_at: '2026-03-07T09:10:09'
authors:
- Muyukani Kizito
topics:
- agent-programming-language
- llm-type-safety
- actor-model
- capability-security
- schema-driven-apis
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Turn: A Language for Agentic Computation

## Summary
Turn 是一种面向“代理式计算”的编译型语言，把 LLM 推理、上下文管理、持久化状态和凭证安全直接做成语言原语，而不是依赖框架约定。论文核心主张是：许多 agent 系统的可靠性与安全性问题需要语言级保障。

## Problem
- 现有 Python/TypeScript/Rust + agent 框架方案，把**上下文边界、结构化输出、持久执行、状态一致性、凭证隔离**留给应用层手工维护，容易失效。
- 这很重要，因为 agent 程序会把关键决策交给**随机性的 LLM**；若输出不受类型约束、上下文无界、凭证可见，就会导致错误累积、崩溃或秘密泄露。
- 文中明确列出 5 类失败模式：无界 context、非类型化推理输出、碎片化状态、无持久执行、凭证泄露。

## Approach
- 提出一个**编译型 actor 语言 Turn**：值层面动态类型，但在高风险边界做“定向严格化”。
- 用 `infer Struct { prompt }` 把 LLM 推理变成**有类型的语言原语**：编译器从 struct 自动生成 JSON Schema，运行时 VM 验证模型输出；若成功绑定，则结构上符合声明类型；失败可最多重试，默认 **k=3**。
- 用 `confidence v` 暴露模型置信度，让程序按阈值做**确定性分支**；若供应商不提供信号，则返回默认 **0.5**。
- 用基于 Erlang 的**actor 进程模型**隔离每个 agent 的上下文、持久内存和邮箱，并支持 suspend/resume 的耐久执行；上下文采用三层结构：P0 system、P1 working、P2 episodic，其中 P1 上限 **100** 条，P2 上限 **200** 条。
- 用 `grant identity` 提供**不可伪造、不可字符串化、不可序列化**的 capability 句柄来隔离凭证；再用 `use schema::<protocol>(...)` 在编译期吸收外部 API schema，生成类型化绑定。

## Results
- 论文给出的**定量实验结果非常有限**；摘要称“在代表性 agent 工作负载上进行了评估”，但当前提供的摘录**没有给出具体 benchmark 指标、准确率、延迟或消融数字**。
- 最明确的形式化/机制性结果是：论文声称并证明了一个结构符合性性质——若 `infer` 表达式**无错误完成**，则绑定值的每个字段都符合声明的 struct 类型。
- 上下文设计引用外部研究的注意力现象来支撑动机：长上下文中，信息召回在首位约 **90%**、末位约 **85%**、中间约 **50%**；Turn 通过 P0→P2→P1 渲染顺序把关键内容放在高召回位置。
- 运行示例方面，论文声称一个“investment committee”多代理程序仅用 **89 行** 即可覆盖其 5 项核心语言机制，并展示 3 个专职 actor 并发分析、基于 **0.7** 置信阈值回退、以及带作用域凭证的 I/O。
- 论文还引用既有经验性论据说明 agent 可靠性会随循环次数指数下降：若单步成功率为 **0.95**，则 **20** 步后整体成功率约为 **0.36**；Turn 将此作为需要类型边界与确定性修复路由的动机，而非其自身实验提升数字。

## Link
- [http://arxiv.org/abs/2603.08755v1](http://arxiv.org/abs/2603.08755v1)
