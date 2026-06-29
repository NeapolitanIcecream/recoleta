---
source: arxiv
url: http://arxiv.org/abs/2604.05000v1
published_at: '2026-04-05T21:54:03'
authors:
- Elias Calboreanu
topics:
- autonomous-software-development
- jira-orchestration
- bounded-autonomy
- software-lifecycle-automation
- safety-controls
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation

## Summary
## 摘要
本文描述了一个生产案例研究，主题是由确定性的、基于 Jira 的控制环路驱动的自主软件生命周期管理，而不是开放式代码生成器。核心主张是，受限的 AI 动作、明确的状态转换和恢复规则，可以以较高的实际可靠性自动处理待办事项和工单工作。

## 问题
- 软件团队把需求、工单、合规项和扫描结果分散在很多地方，导致待办维护缓慢、不一致，也难以审计。
- 论文报告了一个碎片化基线：Jira 中有 820 项处于 To Do，223 项处于 In Progress，689 项处于 Done，外加 13 份结构化源文档和与合规相关的工单家族。
- 缺少的是一个闭环：它能接收入参、去重并排序工作、执行修复、验证结果，并把结果发布回 Jira，同时不丢失可追溯性，也不让并发代理发生冲突。

## 方法
- 系统使用一个确定性的七阶段流水线，由 7 条定时自动化通道实现：接入、代码库审计、待办整理、AI 代码修复、运维监控、质量门控和规范完整性审计。
- 它维护两份同步的工作视图：本地规范化待办作为记录权威，Jira 作为共享状态界面。带有 To Do、In Progress、On Hold 和 Done 状态的 Jira 状态契约充当工单锁定和重新进入策略。
- AI 被限制在固定边界内执行监督角色：结构化上下文包、置信度阈值、时间预算、差异大小审查规则、输出复验和人工审查门控。置信度分数 `s >= 0.83` 的项目可以自主运行，`0.50 <= s < 0.83` 的项目进入人工审查，更低分数的项目会重新接入。
- 匹配和工单映射使用四步规范化流程，包括精确标签、键匹配、加权摘要相似度和模糊文本匹配。执行在隔离的工作树中进行，然后由产品和安全验证器检查结果，再更新 Jira。
- 安全控制包括 19 个 FMEA 故障模式、12 个集中式锁机制、Jira 中断期间的降级模式运行、基于检查点的超时，以及包含重试、重放日志、退避、熔断和卡住状态处理的恢复级联。

## 结果
- 在初始评估窗口内，系统完成了 152 次运行，**终端状态成功率为 100%**，**95% Clopper-Pearson 区间为 [97.6%, 100%]**。
- 随后的持续运行中，部署累计产生了**超过 795 个运行工件**。
- 三轮对抗性代码审查产生了**51 项发现**；其中**48 项已完全修复**，**3 项因延后硬化而关闭**，论文还报告**注入集合中没有漏报**。
- 在包含 **10 项** 的自主安全工单家族中，**6 项通过派发和验证自主完成**，**2 项需要人工修复**，**2 项由策略决定关闭**。
- 该架构从 **11 条通道整合为 7 条**，脚本数量减少了 **55%（51 个降到 23 个）**，自动化代码减少了 **45%（22,946 行降到 12,661 行）**，同时保留了安全控制。
- 论文还报告，在评估期间**没有重复的 Jira 发布**。用于规范完整性检查的第 7 条通道已经实现，但摘要说明其经验验证仍是后续工作。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05000v1](http://arxiv.org/abs/2604.05000v1)
