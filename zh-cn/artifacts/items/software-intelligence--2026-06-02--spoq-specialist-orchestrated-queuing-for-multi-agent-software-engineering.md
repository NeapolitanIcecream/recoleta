---
source: arxiv
url: https://arxiv.org/abs/2606.03115v1
published_at: '2026-06-02T03:59:56'
authors:
- Royce Carbowitz
- Dheeraj Kumar
topics:
- multi-agent-software-engineering
- llm-orchestration
- code-intelligence
- human-ai-interaction
- task-scheduling
- software-quality-assurance
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering

## Summary
## 摘要
SPOQ 是一种多智能体软件工程方法。它把依赖任务按并行波次调度，用评分门检查计划和代码，并让一名人类专家作为主动参与者加入流程。它的目标是比顺序式智能体交接更快完成项目，并减少缺陷。

## 问题
- 多智能体编码系统常常通过角色对话或交接把工作串行化，即使有可用智能体，独立任务也要等待。
- 计划和代码检查不够严格，会导致后期返工、测试失败和模型调用浪费。
- 完全自治的运行可能忽略需求歧义和设计取舍，而这些地方需要人工判断来避免错误的任务拆分。

## 方法
- SPOQ 把一个 epic 拆成 1 到 4 小时的原子任务，并用 DAG 明确任务依赖。
- 拓扑排序会把任务分配到不同波次：同一波次的任务并行执行，后续波次等待前置任务完成。
- 两个验证门分别对计划和代码进行评分，每个门都基于 10 项指标，在继续前要求总通过率达到 95%。
- 三层智能体配置中，Opus 工作者负责实现，Sonnet 审查者负责 QA，Haiku 调查者负责构建失败分流处理。
- Human-as-an-Agent 让人类专家参与任务拆分、计划验证，并在执行过程中回答智能体问题。

## 结果
- 在无上限的合成 DAG 上，波次调度达到 1.03 到 1.11 的关键路径比，报告的加速比最高为 14.3 倍。
- 在一个带真实 LLM 调用的 2 槽本地后端上，SPOQ 报告了稳定的 1.4 倍加速，与文中给出的硬件并发上限一致。
- 在四个全栈规划任务上，结构化规划把覆盖率从 93.0 提高到 99.75，消除了循环计划，并把并行潜力从 31.0 提高到 75.25。
- 双重验证把缺陷数从每个任务 0.34 降到 0.20，并把测试通过率从 91.25% 提高到 99.75%。
- Human-as-Agent 规划把残留缺陷从每个任务 0.47 降到 0.03，并把通过率从 96.5% 提高到 99.75%。
- 一项部署研究报告了 17 个仓库、8,589 次提交、1,822 个已完成任务、13,866 次已执行测试，以及 99.87% 的总通过率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03115v1](https://arxiv.org/abs/2606.03115v1)
