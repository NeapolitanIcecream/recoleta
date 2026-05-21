---
source: arxiv
url: https://arxiv.org/abs/2605.07728v1
published_at: '2026-05-08T13:34:36'
authors:
- Gaston Besanson
topics:
- agentic-ai
- runtime-governance
- ai-compliance
- multi-agent-systems
- auditability
- human-ai-interaction
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# SARC: A Governance-by-Architecture Framework for Agentic AI Systems

## Summary
## 摘要
SARC 将工具使用型智能体的监管和运营义务转成放在智能体循环内的运行时检查。论文的主要主张是架构层面的：约束应在系统运行时阻止、监控、审计或升级处理动作。

## 问题
- 工具使用型智能体可以调用 API、子智能体和外部服务；提示词规则、仪表盘或事后审计可能在违规发生后才发现问题。在受监管部署中，这种时序可能让不允许的动作实际执行。
- 人类监督、可追溯性和上市后监测等监管职责需要可执行检查，因为仅靠文档无法阻止有问题的工具调用。
- 有限奖励惩罚不能总是替代硬约束：论文给出一个双状态示例，其中任何有限惩罚仍会在违规概率足够小时，让高奖励的风险动作保持最优。

## 方法
- SARC 将智能体指定为 `<S,A,R,C>`：状态、动作空间、奖励或目标，以及约束。
- 每条约束记录 `src`、`class`、`pred`、`verif`、`resp` 和一个运行点。类别包括硬约束、软约束和升级约束。
- 该规范把检查编译到四个运行时位置：行动前门控、行动时监控器、行动后审计器和升级路由器。
- 原型检查器测试有限 SARC 规范和轨迹之间的规范-轨迹对应关系：哪些约束适用、在哪里评估、产生了什么结果，以及随后采取了什么响应。
- 多智能体扩展会在智能体之间传播约束，取代理权限的交集，并为跨智能体工作流保留可保持归因的轨迹树。

## 结果
- 在一项覆盖 50 个种子的合成采购任务中，SARC 在精确谓词下产生了零次硬约束违规。
- 行动后审计器的限流响应相对于仅 policy-as-code 基线，将软窗口超限减少了 89.5%。
- 评估将 SARC 与 4 个基线比较：事后审计、输出过滤、工作流规则，以及仅 policy-as-code。
- 论文报告了合成评估的 95% 置信区间，但摘录未提供区间数值。
- 谓词噪声和执行失败扫描支持这一主张：SARC 下残余硬违规随执行栈错误扩大，而不是随环境中的违规机会扩大。
- 作者将结果限制在受控的合成采购运行中，并未声称其具备部署级采购性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07728v1](https://arxiv.org/abs/2605.07728v1)
