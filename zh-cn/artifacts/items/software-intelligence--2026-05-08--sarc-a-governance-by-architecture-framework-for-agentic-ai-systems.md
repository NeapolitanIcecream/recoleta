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
SARC 把面向使用工具的代理的监管和运营义务变成运行时检查，放进代理循环里。论文的核心主张是架构层面的：约束应在系统运行时阻止、监控、审计或升级处理动作。

## 问题
- 使用工具的代理可以先调用 API、子代理和外部服务，之后提示规则、仪表板或事后审计才发现违规；在受监管部署中，这个时序可能让不允许的动作先执行。
- 人类监督、可追溯性和上市后监测等监管义务需要可执行检查，因为只有文档不足以阻止一次错误的工具调用。
- 有限的奖励惩罚并不总能替代硬约束：论文给出一个双状态示例，当违规概率足够小，即使有任何有限惩罚，高收益但有风险的动作仍可能是最优选择。

## 方法
- SARC 把代理写成 `<S,A,R,C>`：状态、动作空间、奖励或目标，以及约束。
- 每个约束记录 `src`、`class`、`pred`、`verif`、`resp` 和一个运行点。类别分为硬约束、软约束和升级约束。
- 该规格会把检查编译到四个运行时位置：Pre-Action Gate、Action-Time Monitor、Post-Action Auditor 和 Escalation Router。
- 原型检查器测试有限的 SARC 规格和轨迹，检查规格与轨迹是否对应：哪些约束生效、在哪个位置评估、得到什么结果、随后采取了什么响应。
- 多代理扩展会在代理之间传播约束，交叉裁定委托权限，并为跨代理工作流保留带归因的轨迹树。

## 结果
- 在一个合成采购任务、50 个随机种子的实验中，SARC 在精确谓词下没有出现任何硬约束违规。
- Post-Action Auditor 的节流响应把软窗口超限次数相对仅使用 policy-as-code 的基线降低了 89.5%。
- 评估把 SARC 与 4 个基线比较：事后审计、输出过滤、工作流规则和仅 policy-as-code。
- 论文报告了合成评估的 95% 置信区间，但摘录没有给出具体区间值。
- 谓词噪声和执行失败扫描支持这样一个说法：SARC 下残余的硬违规会随着执行栈误差变化，而不是随环境中的违规机会变化。
- 作者把结果限定在受控的合成采购运行中，没有声称它已经达到可直接部署的采购性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07728v1](https://arxiv.org/abs/2605.07728v1)
