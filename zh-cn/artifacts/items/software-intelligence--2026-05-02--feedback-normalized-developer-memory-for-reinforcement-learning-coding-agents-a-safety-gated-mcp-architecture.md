---
source: arxiv
url: https://arxiv.org/abs/2605.01567v1
published_at: '2026-05-02T18:37:36'
authors:
- Mehmet Iscan
topics:
- coding-agents
- developer-memory
- reinforcement-learning
- model-context-protocol
- contextual-bandits
- off-policy-evaluation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture

## Summary
## 摘要
RL Developer Memory 是一个面向 RL 编码代理的本地 MCP 内存控制层。它会记录检索决策，规范化开发者反馈，并在离线证据通过安全门之前阻止学习型重排序。它面向 RL 代码修复场景，在这些场景中，错误的记忆可能改变训练目标、终止掩码、梯度流或验证结论。

## 问题
- 编码代理需要在长会话中持续保留仓库记忆，但通用向量检索可能返回看似合理、却对 RL 代码不安全的记录。
- RL 实现错误常常取决于细节，例如 Bellman 目标、目标网络 detach、PPO 裁剪、SAC 熵符号和终止掩码，所以误报式记忆检索会生成无效补丁或无效结论。
- 开发者反馈以混合标签和延迟修复的形式出现；如果不记录并规范化，系统就无法学习哪条检索记忆真的有帮助。

## 方法
- 系统作为一个本地优先的 Model Context Protocol 服务器运行，工具名为 issue_match、issue_feedback 和 issue_record_resolution。
- issue_match 会规范化查询、检索候选项、用确定性的加权评分器排序，并根据分数、差距和特异性检查返回 match、ambiguous 或 abstain。
- issue_feedback 将原始标签映射为有界奖励在 [-1, 1] 的规范反馈类型，而中性标签不会更新学习状态。
- issue_record_resolution 会通过显式 ID，或通过会话、仓库和查询兼容性，把后续验证过的修复关联回早先的检索事件。
- 一个对角线式上下文 bandit 残差策略以 shadow mode 运行，记录 propensity，只能通过保守的 OPE gate 进入 active canary；RL/control 记忆还需要 theory-to-code 元数据、validation tier 和 review gate。

## 结果
- 在一个确定性的 200 案例 RL 开发者记忆基准上，确定性 control path 达到了 80.0% 的 expected-decision accuracy。
- 完整的 shadow/OPE 配置也达到了 80.0% 的 expected-decision accuracy，因此论文没有显示出相对于同一提交版本的确定性 control 的准确率提升。
- 两种配置都达到了 100.0% 的 hard-negative suppression。
- 静态验证通过了 11/11 项检查，动态集成通过了 10/10 个案例。
- Patch-replay 审计显示离线通过率和 recall-delta 指标有较好的原始增量，但论文没有据此声称方法优越性。
- 报告的限制包括：没有启用学习策略的正式部署、没有官方客户端的 MCP 互操作性、线上完整配置的 p95 延迟回退，以及在非 RL 路径、scope 和别名兼容性案例中仍有 40 个残余失败。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01567v1](https://arxiv.org/abs/2605.01567v1)
