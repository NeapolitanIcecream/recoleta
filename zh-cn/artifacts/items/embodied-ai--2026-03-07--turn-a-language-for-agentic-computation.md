---
source: arxiv
url: http://arxiv.org/abs/2603.08755v1
published_at: '2026-03-07T09:10:09'
authors:
- Muyukani Kizito
topics:
- agentic-programming-language
- llm-systems
- actor-model
- type-safety
- capability-security
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Turn: A Language for Agentic Computation

## Summary
Turn提出了一门面向“代理式计算”的编译型语言，把LLM推理、上下文管理、持久状态与凭证安全做成语言原语，而不是依赖框架约定。其目标是提升基于LLM的自治软件在可靠性、安全性和可恢复性上的工程可控性。

## Problem
- 现有Python/TypeScript等上的Agent框架，通常把**上下文边界、结构化输出、持久执行、状态统一表示、凭证隔离**当作应用层约定，容易失效。
- 这会带来五类常见故障：上下文无限增长并静默截断、LLM输出无类型保证、状态碎片化、长任务无法断点恢复、API密钥等凭证可能泄露给模型。
- 这很重要，因为代理式程序把关键决策交给随机性的LLM；如果这些边界不被语言层强制，系统在规模化运行时会变得不可靠且不安全。

## Approach
- 核心机制是把**LLM推理变成带类型的语言原语**：`infer T { prompt }`。编译器从`struct T`自动生成JSON Schema，运行时VM验证模型输出；只有验证通过才绑定为类型`T`。
- 引入**confidence操作符**，把模型的置信度提取为`[0,1]`标量，用于确定性分支，例如低于阈值时走本地回退逻辑。
- 采用**基于Actor的进程模型**：每个agent进程有独立上下文窗口、持久记忆和邮箱，并支持`suspend/resume`式耐久执行与检查点恢复。
- 设计了**三层结构化上下文**（P0系统、P1工作、P2情节），显式把系统指令放在高召回的开头、近期内容放在高召回的结尾，避免共享消息列表导致的上下文污染。
- 使用**能力型身份系统**与**编译期schema吸收**：`grant identity`返回不可伪造且不可字符串化的凭证句柄，`use schema::<protocol>`在编译时从外部API规范生成类型化绑定。

## Results
- 论文给出了一个**形式化正确性声明**：若`infer T { e }`在最多`k=3`次重试后成功完成，则绑定值在结构上符合声明的`struct T`；这是“类型化LLM输出”的核心保证，但不是传统任务精度指标。
- 上下文架构给出明确容量：P1工作区上限`W=100`条，P2情节区上限`2W=200`条，并固定按`P0 -> P2 -> P1`渲染，以利用文中引用研究的注意力位置差异（约首部`90%`召回、尾部`85%`、中部约`50%`）。
- 文中示例“investment committee”程序仅**89行**，包含3个并发专员actor；其中分析员在`confidence < 0.7`时走确定性回退分支，展示了语言原语如何组合使用。
- 论文声称Turn在“代表性代理工作负载”上进行了评估，并实现了Rust字节码VM、开源仓库与`openapi`适配器；但在给定摘录中**没有提供标准基准上的完整定量对比结果**（如成功率、时延、成本或与LangChain等基线的数值比较）。

## Link
- [http://arxiv.org/abs/2603.08755v1](http://arxiv.org/abs/2603.08755v1)
