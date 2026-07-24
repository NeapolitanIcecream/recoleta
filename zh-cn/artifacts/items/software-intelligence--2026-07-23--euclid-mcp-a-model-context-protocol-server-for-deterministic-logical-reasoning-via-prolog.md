---
source: arxiv
url: https://arxiv.org/abs/2607.21412v1
published_at: '2026-07-23T15:15:37'
authors:
- Bartolomeo Bogliolo
topics:
- model-context-protocol
- neuro-symbolic-reasoning
- prolog
- rule-enforcement
- security-compliance
- llm-agents
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Euclid-MCP: A Model Context Protocol Server for Deterministic Logical Reasoning via Prolog

## Summary
## 摘要
Euclid-MCP 是一个开源的 Model Context Protocol 服务器，使基于 LLM 的应用能够将基于规则的演绎交给 SWI-Prolog 执行。它将由 LLM 生成的逻辑表示与确定性推理和证明轨迹结合起来，用于处理业务、安全和合规政策。

## 问题
- LLM 在多步推理中可能产生幻觉或不一致的结果，而规则执行任务要求结论能够从明确的事实和政策中推导出来。
- 语义 RAG 可以检索相似文本，但无法保证规则集在逻辑上充分、一致且可审计。
- 这对安全和合规场景十分重要，因为相关决策需要可复现的答案和可追溯的推导过程。

## 方法
- Euclid-IR 以面向 LLM 生成的人类可读格式表示事实、Horn 子句规则、查询、合取、封闭世界否定、算术运算和通配符。
- 服务器将 Euclid-IR 确定性地编译为经过清理的 SWI-Prolog 代码，排除危险构造，将输入限制在 500 KB 以内，并应用默认 30 秒的执行超时。
- 四个 MCP 工具分别支持带证明树的演绎（`reason`）、失败与成功分析（`diagnose`）、反事实变更（`what_if`）以及知识库验证（`check_kb`）。
- translate-run-inspect-repair 循环使 LLM 能够生成规则、验证规则、执行查询、检查推导过程，并修订编码后的知识库，而无需自行执行演绎。
- 该中间表示旨在支持未来的 Datalog 或 SMT 求解器等后端，但当前原型使用 SWI-Prolog。

## 结果
- 所展示的 IT 安全与合规模型包含 30 个用户、50 个资源，以及 CIS AWS 基准、内部政策和访问控制规则；较大的压力测试变体包含 200 个用户、300 个资源和约 3,872 个事实。
- 在所报告的用例中，系统覆盖 10 个典型查询，涉及单跳权限、多跳政策推理以及时间或阈值条件。
- 摘要称，在较大的知识库上，仅使用 LLM 的推理会系统性地产生幻觉，而 Euclid-MCP 能够以更低的延迟和更紧凑的输出给出准确答案。
- 所提供的文本没有给出准确率、延迟、输出大小或基线比较的数值测量，因此无法在此独立量化这些性能主张的强度。
- 具体实现方面，文中声称系统包含四个 MCP 工具、两种传输模式（stdio 和 HTTP）、证明树输出，以及相对于编码后的事实和规则的确定性执行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.21412v1](https://arxiv.org/abs/2607.21412v1)
