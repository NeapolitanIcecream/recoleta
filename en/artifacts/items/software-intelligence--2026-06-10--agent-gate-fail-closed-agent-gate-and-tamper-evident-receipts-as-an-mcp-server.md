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
language_code: en
---

# Agent-gate – fail-closed agent gate and tamper-evident receipts as an MCP server

## Summary
agent-gate is an MCP server that makes an AI agent pass explicit completion checks before it reports work as done. It records decisions in a SHA-256 hash-chained ledger so later edits or deletions can be detected.

## Problem
- AI agents can claim success while tests, review, secret checks, or human approval are missing, which can create silent workflow failures.
- The project targets agent reliability in deployment workflows where outward or irreversible actions need proof, review, and an audit trail.
- Self-review by the same agent is treated as insufficient, so the gate requires an independent refute-first review before completion.

## Approach
- The MCP server exposes `verify_gate(...)` so an agent can check its evidence before saying the task is complete.
- The default ship gate has 5 required checks: `deterministic_checks_pass`, `independent_refute_review`, `no_secrets`, `human_gated_if_irreversible`, and `honest_receipt_logged`.
- The checklist is fail-closed: any missing or non-true field blocks completion. In the example, omitting `honest_receipt_logged` returns `passed: false` with that item in `blocking`.
- The ledger appends receipts with `(decision, metric, value, verdict)` and links them with SHA-256 hashes. `verify_chain()` returns false after a past receipt is edited or deleted.
- The core gate and ledger modules use the Python standard library; the MCP server is a thin adapter with `mcp` as the runtime dependency.

## Results
- The excerpt provides no benchmark against other agent verification systems and no measured reduction in agent errors.
- The demo shows a gate failure when 2 checks are missing: `human_gated_if_irreversible` and `honest_receipt_logged`.
- The demo shows a pass when all 5 default checks are true: `passed: true` and `blocking: []`.
- The ledger demo records 2 receipts, `seq: 1` for `ship v0.1` and `seq: 2` for `deploy`, then verifies `chain_intact: True`.
- The project claims tests pass on Python 3.11, 3.12, and 3.13, and says MCP tools are tested by calling them rather than only importing them.

## Link
- [https://github.com/Jott2121/agent-gate](https://github.com/Jott2121/agent-gate)
