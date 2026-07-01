---
source: arxiv
url: https://arxiv.org/abs/2606.31498v1
published_at: '2026-06-30T11:16:56'
authors:
- Richard Kang
- Yudho Diponegoro
topics:
- agent-interoperability
- multi-agent-governance
- protocol-analysis
- agent-coordination
- enterprise-ai
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express

## Summary
## 摘要
本文认为，MCP、A2A、ACP、ANP 和 ERC-8004 支持智能体协调，但缺少面向智能体社区的协议原生治理能力。文章的主要主张是，治理需要位于当前互操作标准之上的独立架构层。

## 问题
- 企业正在部署异构智能体集群。这些智能体可以发现工具、交换消息、委派任务并记录信任信号，但这些协议没有定义智能体如何作出受治理的群体决策。
- 在受监管或高风险场景中，这些缺失能力很关键，例如生产代码变更、合规审查和研究仲裁。在这些场景中，决策需要成员控制、审议、投票、异议记录、人工升级和审计。
- 如果没有共享的治理原语，每个应用都必须实现自己的决策流程，这会削弱互操作性和审计一致性。

## 方法
- 论文定义了一个六部分治理分类法：G1 成员资格、G2 审议、G3 投票、G4 异议保留、G5 人工升级、G6 审计/重放。
- 论文评估了五个协议：MCP v1.1、A2A v1.0.1、ACP、ANP 和 ERC-8004。
- 每个“协议-维度”组合都按 Supported、Partial 或 Absent 分类，依据是协议规范本身编码了什么，而不是应用可以在其上构建什么。
- 作者区分了可通过协议扩展处理的缺口，以及可能需要新层处理的缺口。

## 结果
- 在五个协议和六个治理维度中，报告的矩阵显示没有任何协议完全支持任一治理维度。
- 投票、异议保留和人工升级在全部 5/5 个协议中都是 Absent。
- 覆盖分数很低：MCP v1.1 得分 1/12，A2A v1.0.1 得分 1/12，ACP 得分 2/12，ANP 得分 0/12，ERC-8004 得分 2/12。
- 成员资格在 A2A、ACP 和 ERC-8004 中是 Partial，但在 MCP 和 ANP 中是 Absent。
- 审议仅在 ACP 中是 Partial，在其他 4 个协议中是 Absent。
- 审计/重放在 MCP 和 ERC-8004 中是 Partial，但在 A2A、ACP 和 ANP 中是 Absent；论文称，这些部分支持来自会话状态或区块链历史，而不是治理专用的重放语义。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31498v1](https://arxiv.org/abs/2606.31498v1)
