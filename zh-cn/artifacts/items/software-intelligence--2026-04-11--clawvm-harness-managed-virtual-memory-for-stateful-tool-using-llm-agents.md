---
source: arxiv
url: http://arxiv.org/abs/2604.10352v1
published_at: '2026-04-11T21:38:15'
authors:
- Mofasshara Rafique
- Laurent Bindschaedler
topics:
- llm-agents
- agent-memory
- virtual-memory
- tool-using-agents
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents

## Summary
## 摘要
ClawVM 在代理 harness 中加入了类操作系统的虚拟内存层，面向有状态的、使用工具的 LLM 代理。它的目标是在几乎不增加运行时开销的情况下，阻止由压缩、重置和不安全持久化引起的内存故障。

## 问题
- 有状态代理把上下文窗口当作工作内存，但现有 harness 通常把内存驻留和持久化当作尽力而为的事。这会在压缩或重置后导致指令丢失、计划丢失、重复调用工具，以及状态被覆盖。
- 论文针对的是可由策略控制的故障：在 prompt 组装中缺少必需状态、在破坏性的生命周期事件前漏掉 flush、破坏性写回，以及没有原因码的静默内存检索失败。
- 这很重要，因为运行时间很长的代理会在编码、邮件、日历和其他工具上连续运行数小时或数天，跨过很多个上下文窗口。内存处理一旦失败，代理就会重复工作、违反用户约束，或丢失进度。

## 方法
- ClawVM 把内存控制放进代理 harness。这个 harness 本来就负责组装 prompt、协调工具，并观察生命周期事件。harness 把代理状态按类型页来管理，例如启动指令、约束、计划、偏好、证据和对话片段。
- 每个页都有最小保真不变量，以及几种预先计算好的表示：完整、压缩、结构化或指针式。在 token 受限时，系统只会把页降级到其不变量允许的程度。
- Prompt 组装使用确定性的两阶段策略：先放入所有必需的最小表示，再把剩余 token 用在单位 token 价值最高的升级上。
- ClawVM 为 refetch 故障、duplicate-tool 故障、pinned invariant miss、post-compaction bootstrap 故障、silent-recall 故障和 flush-miss 故障加入了明确的故障模型。它还用 thrash index 衡量分页不稳定性。
- 持久化使用分阶段、经过验证的 writeback，发生在每个生命周期边界。更新是类型化的、经过 schema 检查的、限定作用域的、非破坏性的，并记录在 journal 中，因此故障可以审计和重放。

## 结果
- 在 4 组基于 OpenClaw 的工作负载家族和 6 个 token 预算下，只要最小保真集合能放进预算，ClawVM 就把 policy-controllable 故障的均值从 retrieval baseline 的 67.8 和 practitioner-configured compaction+retrieval baseline 的 1.5 降到 0。
- 相比 retrieval，它把分页不稳定性降低了 77.4%；相比 practitioner-configured baseline，降低了 11.4%。
- 一个具有未来信息的 offline oracle 没有发现剩余的故障空间：论文声称，在线的 ClawVM 策略已经达到最优故障数。
- 在 12 条真实会话轨迹和 30 次任务级重放中，论文报告了同样的 0 个 policy-controllable 故障，以及在最紧预算下 100% 的成功率；相比之下，practitioner-configured baseline 的成功率是 76.7%。
- 报告中的 policy-engine 中位开销为每轮低于 50 微秒。
- 摘要说明，只要最小保真集合能放进 token 预算，这个零故障结果就适用于合成工作负载、真实轨迹和对抗性压力测试。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10352v1](http://arxiv.org/abs/2604.10352v1)
