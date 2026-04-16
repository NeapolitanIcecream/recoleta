---
source: arxiv
url: http://arxiv.org/abs/2604.05080v1
published_at: '2026-04-06T18:32:09'
authors:
- Danil Gorinevski
topics:
- ai-software-engineering
- code-governance
- formal-verification
- llm-agents
- traceability
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Nidus: Externalized Reasoning for AI-Assisted Engineering

## Summary
## 摘要
Nidus 是一个用于 AI 辅助软件工程的治理运行时，它把需求、架构、可追溯性和验证放进一个由求解器检查的统一工件中。论文的核心主张是，工程纪律应由外部机制在每次变更时强制执行，而不是交给 LLM 的行为自行维持。

## 问题
- LLM 编码代理可以生成代码，但它们无法稳定保留工程不变量，例如需求可追溯性、经过论证的设计决策和交付证据。
- 在安全关键或高保障场景中，由提出变更的同一个模型自行检查，只能提供较弱的保障；论文认为，验证必须来自一个外部的、可判定的检查器。
- 常见的项目状态分散在 issue 跟踪器、文档、电子表格和 CI 日志等工具中，这使代理很难看到并维护完整的工程上下文。

## 方法
- Nidus 用 S 表达式把整个项目存储为一个统一的“活规范”：包括需求、架构、设计、工作流、功能、追踪关系、证明义务、协同状态，以及导入的组织规则。
- 每个提议的变更在保存前都会被检查。内核会运行有限的结构检查和使用 Z3 的 SMT 检查；失败的变更会因违规和 UNSAT 反馈被拒绝。
- 组织标准会编译成可复用的“guidebooks”。项目导入后，继承的约束会与本地证明义务一起被自动执行。
- 人类、LLM 代理和求解器读取的是同一个工件。论文将其称为表征闭合：一个对象同时是数据库、模型上下文、规范和验证器输入。
- 系统还会用租约和只追加的 friction ledger 跟踪代理声明，然后根据拒绝历史调整代理的信任层级。

## 结果
- 论文报告了一个自托管部署：三个 LLM 家族 Claude、Gemini 和 Codex 在**每次提交**都要检查证明义务的条件下，交付了一个 **100,000 行**的系统。
- 论文声称实现了递归式自治理：系统在构建过程中治理了对其自身治理工件的变更。
- 论文给出一个具体验证例子：某个功能交付因 guidebook 约束 **GC-SCOPE-COMPLETENESS** 发现缺失的测试路径而被拒绝；Z3 返回 **UNSAT**，代理补上 `tests/test_brain.py` 后，交付通过。
- 论文将每次变更的形式化验证成本写为 **O(|Π| · |S|)**，其中图检查为 **O(|C| + |E| + |T|)**，模式检查为 **O(|F|)**，固定大小守卫下的工作流算术在多项式时间内求解。
- 这段摘录**没有**提供缺陷率、通过率、延迟、消融实验或与基线工具链的对比等基准指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05080v1](http://arxiv.org/abs/2604.05080v1)
