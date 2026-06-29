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
Nidus 是一个面向 AI 辅助软件工程的治理运行时，把需求、架构、可追溯性和验证放进一个由求解器检查的工件中。论文的核心主张是：工程纪律应由外部机制在每次变更时强制执行，而不是交给 LLM 的行为来维持。

## 问题
- LLM 编码代理可以生成代码，但不能可靠地保住工程不变量，例如需求可追溯性、经过论证的设计决策，以及交付证据。
- 在安全关键或高保证工作中，让提出变更的同一个模型自检，只能提供很弱的保证；论文认为，验证必须来自外部的、可判定的检查器。
- 常见的项目状态分散在 issue 跟踪器、文档、电子表格和 CI 日志等工具里，这让代理很难看到并维护完整的工程上下文。

## 方法
- Nidus 用 S 表达式把整个项目存成一个单一的“活的规范”：需求、架构、设计、工作流、功能、追踪关系、证明义务、协调状态，以及导入的组织规则。
- 每个候选变更都会在保存前检查。内核运行有限的结构检查和 Z3 的 SMT 检查；失败的变更会被拒绝，并返回违规和 UNSAT 反馈。
- 组织标准会编译成可复用的“指南”。项目导入这些指南，继承的约束会和本地证明义务一起自动执行。
- 人类、LLM 代理和求解器都读取同一个工件。论文把这称为表征闭包：一个对象同时充当数据库、模型上下文、规范和验证器输入。
- 系统还用租约和只追加的摩擦账本跟踪代理声明，然后根据拒绝历史调整代理信任层级。

## 结果
- 论文报告了一个自托管部署：Claude、Gemini 和 Codex 这三类 LLM 在**每次提交**都检查证明义务的条件下，交付了一个**10 万行**的系统。
- 论文声称实现了递归自我治理：系统在构建过程中管理了自身治理工件的变更。
- 论文给出一个具体的验证例子：某个功能交付因为指南约束 **GC-SCOPE-COMPLETENESS** 发现测试路径缺失而被拒绝；Z3 返回 **UNSAT**，代理补上 `tests/test_brain.py`，然后该交付通过。
- 论文把每次变更的形式化验证成本写成 **O(|Π| · |S|)**，图检查是 **O(|C| + |E| + |T|)**，模式检查是 **O(|F|)**，在守卫规模固定时，工作流算术可在多项式时间内求解。
- 该节选**没有**提供缺陷率、通过率、延迟、消融实验，或与基线工具链比较等基准指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05080v1](http://arxiv.org/abs/2604.05080v1)
