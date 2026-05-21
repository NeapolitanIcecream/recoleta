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
RL Developer Memory 是一个面向 RL 编码代理的本地 MCP 记忆控制层。它记录检索决策，规范化开发者反馈，并在离线证据通过安全门控前阻止学习型重排序进入生效路径。它面向 RL 代码修复场景，因为错误记忆可能改变训练目标、终止掩码、梯度流或验证声明。

## 问题
- 编码代理在长会话中需要持久的代码库记忆，但通用向量检索可能返回看似合理、却对 RL 代码不安全的记录。
- RL 实现缺陷常取决于 Bellman 目标、目标网络 detach、PPO clipping、SAC 熵符号和终止掩码等细节，因此误检索记忆可能生成无效补丁或无效声明。
- 开发者反馈包含混合标签和延迟的解决结果；如果没有日志记录和规范化，系统无法学习哪些被检索的记忆有帮助。

## 方法
- 系统作为本地优先的 Model Context Protocol 服务器运行，工具名为 issue_match、issue_feedback 和 issue_record_resolution。
- issue_match 规范化查询，检索候选项，用确定性的加权评分器排序，并根据分数、边际和特异性检查返回 match、ambiguous 或 abstain。
- issue_feedback 将原始标签映射为规范反馈类型，并给出 [-1, 1] 范围内的有界奖励；中性标签不更新学习状态。
- issue_record_resolution 使用显式 ID，或会话、代码库和查询兼容性，将后续已验证修复关联回更早的检索事件。
- 对角上下文 bandit 残差策略以影子模式运行，记录倾向概率，并且只有通过保守 OPE 门控后才能进入主动 canary；RL/control 记忆还需要理论到代码元数据、验证层级和评审门控。

## 结果
- 在一个确定性的 200 例 RL 开发者记忆基准上，确定性控制路径达到 80.0% 的期望决策准确率。
- 完整 shadow/OPE 配置同样达到 80.0% 的期望决策准确率，因此论文报告称，相比同一提交版本的确定性控制，没有证明准确率提升。
- 两种配置都达到 100.0% 的 hard-negative 抑制率。
- 静态验证通过 11/11 项检查，动态集成通过 10/10 个用例。
- 补丁重放审计显示，离线通过率和 recall-delta 指标的原始差值有利，但论文没有据此声称方法更优。
- 报告的限制包括：没有部署主动学习策略，没有官方客户端 MCP 互操作性，实时完整配置存在 p95 延迟回退，以及非 RL 路径、作用域和别名兼容性用例中有 40 个残余失败。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01567v1](https://arxiv.org/abs/2605.01567v1)
