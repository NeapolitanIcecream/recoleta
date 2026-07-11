---
source: arxiv
url: https://arxiv.org/abs/2607.07052v1
published_at: '2026-07-08T06:27:36'
authors:
- Arun Malik
topics:
- llm-agents
- agent-workflows
- it-operations
- workflow-automation
- cost-reduction
- deterministic-playbooks
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Progressive Crystallization: Turning Agent Exploration into Deterministic, Lower-Cost Workflows in Production

## Summary
## 摘要
渐进式固化把 LLM 智能体反复成功处理的事件转成混合式或确定性 playbook。在一个云网络运维部署中，8 个月后确定性执行约占 45%，单事件智能体成本下降超过 70%，同时事件量约翻倍。

## 问题
- 用于 IT 运维的 LLM 智能体会在重复事件上重新运行完整推理，因此成本和延迟会随事件量增长。
- 成功调查通常只作为 trace 被丢弃，这会迫使系统重新发现同类处理路径，并可能在同一事件类型上产生不同结果。
- 传统工作流自动化需要人工工程投入，且无法处理新事件；微调仍会留下概率性的运行时行为。

## 方法
- 论文定义了三种执行类型：类型 3 是智能体编排运行，约 10k-50k tokens；类型 2 是混合式 playbook，约 1k-5k tokens；类型 1 是确定性 playbook，运行时 tokens 为零。
- 在一次经验证成功的类型 3 运行之后，系统从 trace 中提取可复用模板：工具调用顺序、分支条件、schema、依赖、参数化值和人工审批门槛。
- 从类型 3 晋升到类型 2 需要至少 10 次成功运行、零安全违规、至少 90% 的动作序列匹配、通过生成的测试，并且近期没有人工覆盖。
- 从类型 2 晋升到类型 1 需要至少 50 次成功的混合式运行、至少 99% 的 LLM 分类一致性、对已观察输入变化的确定性覆盖、在不使用 LLM 的情况下通过回归测试，并经过人工审查。
- 当执行失败、发生安全违规或验收测试回退时，熔断器会将 playbook 降级。

## 结果
- 在每月处理数万起事件的生产云网络运维中，类型 1 执行在 8 个月内从 0% 上升到约 45%；最终构成为约 45% 类型 1、30% 类型 2、25% 类型 3。
- 同期单事件智能体成本下降超过 70%，事件量约翻倍。
- 该平台自主解决了 90% 以上的常见事件类别。
- 平均解决时间从数小时降至数分钟。
- 误报修复率保持在 5% 以下，且未报告客户可见影响。
- 在论文的分类中，安全指标随类型改善：可复现性在类型 3 中约为 50%，类型 2 中约为 90%，类型 1 中为 100%；运行时 token 成本从 10k-50k 降到 1k-5k，再降到零。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.07052v1](https://arxiv.org/abs/2607.07052v1)
