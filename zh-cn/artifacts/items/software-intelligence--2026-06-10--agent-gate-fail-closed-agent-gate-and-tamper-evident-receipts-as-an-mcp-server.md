---
source: hn
url: https://github.com/Jott2121/agent-gate
published_at: '2026-06-10T23:15:41'
authors:
- jott2121
topics:
- ai-agents
- mcp-server
- agent-verification
- software-quality
- audit-logging
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server

## Summary
## 总结
agent-gate 是一个 MCP 服务器，它要求 AI 代理先通过明确的完成检查，才可以把工作报告为已完成。它把决策记录到 SHA-256 哈希串联账本里，后续如果有人修改或删除记录，就能被发现。

## 问题
- AI 代理可能会在测试、审查、密钥检查或人工批准缺失时仍然声称成功，这会造成静默的工作流失败。
- 这个项目面向部署工作流里的代理可靠性，在这些流程里，对外动作或不可逆动作需要证据、复核和审计轨迹。
- 同一个代理做自我复核被视为不够，所以这个门要求先经过独立的、先反驳再确认的审查，才能完成。

## 方法
- 这个 MCP 服务器暴露 `verify_gate(...)`，这样代理就能先检查自己的证据，再说任务已经完成。
- 默认的交付门有 5 项必需检查：`deterministic_checks_pass`、`independent_refute_review`、`no_secrets`、`human_gated_if_irreversible` 和 `honest_receipt_logged`。
- 这个清单是 fail-closed 的：任何缺失或不为真的字段都会阻止完成。在示例里，如果省略 `honest_receipt_logged`，会返回 `passed: false`，并把该项放进 `blocking`。
- 账本会把收据按 `(decision, metric, value, verdict)` 追加写入，并用 SHA-256 哈希把它们链接起来。只要修改或删除过去的一条收据，`verify_chain()` 就会返回 false。
- 核心门和账本模块只用 Python 标准库；MCP 服务器只是一个薄适配层，运行时依赖是 `mcp`。

## 结果
- 这段摘录没有提供与其他代理验证系统的基准对比，也没有给出代理错误减少的测量结果。
- 演示显示，当缺少 2 项检查时会失败：`human_gated_if_irreversible` 和 `honest_receipt_logged`。
- 演示还显示，当默认 5 项检查都为真时会通过：`passed: true`，`blocking: []`。
- 账本演示记录了 2 条收据，`seq: 1` 对应 `ship v0.1`，`seq: 2` 对应 `deploy`，随后验证 `chain_intact: True`。
- 该项目声称在 Python 3.11、3.12 和 3.13 上测试通过，并且说明 MCP 工具是通过实际调用来测试的，而不只是导入它们。

## Problem

## Approach

## Results

## Link
- [https://github.com/Jott2121/agent-gate](https://github.com/Jott2121/agent-gate)
