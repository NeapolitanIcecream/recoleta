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
ClawVM 在有状态工具使用型 LLM 智能体的 harness 中加入了类似操作系统的虚拟内存层。它的目标是阻止由压缩、重置和不安全持久化引起的内存故障，同时只增加很少的运行时开销。

## 问题
- 有状态智能体把上下文窗口当作工作内存，但当前的 harness 对内存驻留和持久化基本按尽力而为的方式处理。这会在压缩或重置后导致指令丢失、计划丢失、工具重复调用，以及状态被覆盖。
- 论文针对的是可由策略控制的故障：提示组装时缺少必需状态、破坏性生命周期事件前漏掉 flush、破坏性回写，以及没有原因代码的静默内存查找失败。
- 这很重要，因为用于编程、邮件、日历和其他工具的长时间运行智能体，可能会跨越许多上下文窗口连续运行数小时或数天。内存处理出错时，智能体会重复工作、违反用户约束，或丢失进度。

## 方法
- ClawVM 把内存控制移到智能体 harness 中。harness 本来就负责组装提示、协调工具调用，并能看到生命周期事件。harness 将智能体状态跟踪为带类型的页，例如引导指令、约束、计划、偏好、证据和对话片段。
- 每个页都有一个最低保真度不变量，以及几种预先计算好的表示：完整、压缩、结构化或指针。在 token 紧张时，系统只会把页降级到其不变量允许的程度。
- 提示组装使用一个确定性的两阶段策略：先放入所有必需的最低表示，再把剩余 token 分配给每个 token 效用最高的升级项。
- ClawVM 增加了一个显式故障模型，包括 refetch faults、duplicate-tool faults、pinned invariant misses、post-compaction bootstrap faults、silent-recall faults 和 flush-miss faults。它还用 thrash index 衡量分页不稳定性。
- 持久化在每个生命周期边界使用分阶段、经过验证的回写。更新带有类型，经过 schema 检查，有明确作用域，不会破坏原有内容，并记录到日志中，因此故障可以审计和重放。

## 结果
- 在 4 个源自 OpenClaw 的工作负载家族和 6 种 token 预算下，只要最低保真度集合能放入预算中，ClawVM 就把可由策略控制的故障平均数从 retrieval 基线的 67.8 和 practitioner-configured compaction+retrieval 基线的 1.5 降到 0。
- 与 retrieval 相比，它将分页不稳定性降低了 77.4%；与 practitioner-configured 基线相比，降低了 11.4%。
- 带有未来信息的离线 oracle 没有发现剩余的故障改进空间：论文称，在线 ClawVM 策略已经达到了最优故障数。
- 在 12 条真实会话轨迹和 30 次任务级重放上，论文报告在最紧的预算下同样实现了 0 个可由策略控制的故障和 100% 成功率，而 practitioner-configured 基线为 76.7%。
- 报告的 policy-engine 开销中位数是每轮低于 50 微秒。
- 摘要称，在合成工作负载、真实轨迹和对抗性压力测试中，只要最低保真度集合能放入 token 预算，零故障结论就成立。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10352v1](http://arxiv.org/abs/2604.10352v1)
