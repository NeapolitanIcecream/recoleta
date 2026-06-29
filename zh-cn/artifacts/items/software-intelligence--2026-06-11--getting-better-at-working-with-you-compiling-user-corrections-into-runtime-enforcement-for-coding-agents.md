---
source: arxiv
url: https://arxiv.org/abs/2606.13174v1
published_at: '2026-06-11T10:43:40'
authors:
- Yujun Zhou
- Kehan Guo
- Haomin Zhuang
- Xiangqi Wang
- Yue Huang
- Zhenwen Liang
- Pin-Yu Chen
- Tian Gao
- Nuno Moniz
- Nitesh V. Chawla
- Xiangliang Zhang
topics:
- coding-agents
- runtime-enforcement
- user-corrections
- agent-memory
- preference-compliance
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents

## Summary
## 摘要
Trace 把用户纠正转成编码代理的运行时检查，代理必须先满足这些纠正，才能完成任务。它针对的是一种常见失效：记忆可以回忆起偏好，但代理还是会违反它。

## 问题
- 编码代理常常在不同会话里重复同样的、针对用户的错误，即使这些纠正已经被存储或检索出来。
- 论文测量了这种“可访问性和遵守性之间的差距”，并显示仅靠记忆并不能让纠正变成强制约束。
- 这会让用户在后续会话里反复重述同一条约束，打断交互式工作。

## 方法
- Trace 扫描用户消息中的纠正信号，例如长期偏好或重复出现的摩擦点。
- 它把每条纠正改写成带适用条件的原子规则。
- 它用 noop、update、supersede、split、new 等操作，把新规则和每个用户的规则库对齐。
- 它把规则编译成一个运行时工件，包含适用性检查、行为指令和验证器。
- 挂钩会阻止任务完成，直到当前验证器通过。

## 结果
- 在一个诊断集上，数据来自 32 段长上下文编码代理对话和 19 个保留任务，共 29 条偏好检查，Mem0 仍让 57.5% 的适用偏好检查没有被满足。
- 在 ClawArena 的分布内任务上，Trace 把违规率从 100.0% 降到 37.6%；在分布外任务上，把违规率从 100.0% 降到 2.0%。
- 在基于 MemoryArena 的分布内任务上，Trace 把违规率从 100.0% 降到 60.5%，并且在任务通过率上达到或超过最强的记忆基线。
- 在 ClawArena 中，Trace 把平均用户轮次从没有记忆时的 2.00 降到分布内 1.37 和分布外 1.02。
- 论文报告的模拟验证指标为 Precision 0.864、Recall 0.953、F1 0.906 和 Specificity 0.940。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13174v1](https://arxiv.org/abs/2606.13174v1)
