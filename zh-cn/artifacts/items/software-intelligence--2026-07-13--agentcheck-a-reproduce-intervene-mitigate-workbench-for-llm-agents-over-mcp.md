---
source: arxiv
url: https://arxiv.org/abs/2607.11098v1
published_at: '2026-07-13T05:14:12'
authors:
- Aritra Mazumder
- Nusrat jahan Lia
topics:
- llm-agents
- mcp-security
- fault-injection
- agent-evaluation
- tool-use-reliability
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP

## Summary
## 摘要
AgentCheck 是一个开源 MCP 工作台，用于复现 LLM 智能体的工具故障、测试缓解措施，并确认相同故障是否已修复。它能在部署前暴露智能体对过时、错误、失败或被污染的工具响应进行无提示误用的情况。

## 问题
- 大多数智能体评测都假设工具会返回有效响应，因此会漏掉超时、数据过时、模式变更、错误结果和指令污染导致的故障。
- 这些故障会造成实际影响，因为智能体经常会自信地依据错误的工具输出采取行动，或在没有崩溃的情况下执行不安全指令。

## 方法
- AgentCheck 先让智能体使用真实工具运行一次，并缓存每个工具响应。
- 随后，它在相同任务中通过注入器修改一个选定的响应。该注入器覆盖工具执行、数据质量和安全性方面的 12 种故障类型。
- 它比较无故障轨迹和故障轨迹，找出首次分歧，并结合针对具体故障的确定性通过/失败检查和基于 LLM 的诊断标签进行评估。
- 针对相同的缓存故障重新运行缓解措施。如果此前失败的检查通过，系统就会给出修复已确认的判定。
- 该工作台包含覆盖五个领域的 120 个场景，也可以连接开发者自己的 MCP 服务器和智能体运行框架。

## 结果
- 在五种智能体配置中，表现最强的智能体通过了 105/120 个场景，表现最弱的通过了 77/120 个场景。
- 评测发现，故障通常表现为智能体无提示地接受或传播错误的工具输出，而不是智能体崩溃。
- 对表现最弱的智能体，重试缓解措施将超时故障的成功率从最低 30% 提高到 100%。
- 过时数据故障仍然难以处理：在不同缓解措施下，成功率都维持在 10 个案例中的约 3-4 个。
- 场景套件包含 120 个案例，每种故障类型对应 10 个案例；评分检查已通过人工标注进行验证。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11098v1](https://arxiv.org/abs/2607.11098v1)
