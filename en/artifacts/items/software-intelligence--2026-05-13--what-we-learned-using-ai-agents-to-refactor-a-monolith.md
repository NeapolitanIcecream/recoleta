---
source: hn
url: https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith
published_at: '2026-05-13T23:33:13'
authors:
- cdrnsf
topics:
- agentic-refactoring
- code-intelligence
- software-engineering-agents
- monolith-decomposition
- production-migration
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# What we learned using AI agents to refactor a monolith

## Summary
1Password reports that AI agents helped refactor parts of a multi-million-line Go monolith when the work had clear specs, deterministic analysis tools, and human review for sequencing risk.

## Problem
- 1Password needs to split service boundaries inside B5, a large Go monolith, while preserving privacy, performance, reliability, and security under production traffic.
- Extraction order matters because wrong sequencing in shared schemas, write paths, or ownership boundaries can cause subtle production failures.
- A separate cleanup required changing more than 3,000 `MustBegin` transaction call sites, a backlog item too broad for manual cleanup alone.

## Approach
- The team built an agentic toolchain using Go SSA analysis, SQL parsing, and DataDog MCP runtime data to map domain ownership, coupling, and extraction order.
- Agents helped write deterministic analyzers and manifests; engineers then reviewed stable artifacts instead of relying on repeated model interpretation.
- For the `MustBegin` migration, the team generated a manifest of call sites, grouped them into patterns, wrote templates, and gave agents a playbook with stop-and-escalate rules.
- Multiple agents ran in parallel through git worktrees so each change set stayed isolated.
- For service extraction, engineers found that agents needed explicit invariants, schema ordering rules, deployment sequencing, and shared-data ownership constraints.

## Results
- The extraction analysis covered millions of lines of Go and produced an order that matched senior engineering judgment: Vault first, then Billing, then AuthN and AuthZ, with Identity kept as the core.
- The `MustBegin` migration covered more than 3,000 production and test call sites; agent execution took hours after the team built the tooling and specification.
- The service extraction task showed only about a 20-30% productivity gain because agents made sequencing errors and needed human coordination.
- One failure case backfilled UUID columns before changing insertion code, which could have caused silent data loss.
- Another failure inferred an identifier was a ULID and spread that assumption through changes, forcing a rollback of the session.
- Added instrumentation for the analysis also improved end-to-end transaction visibility in DataDog beyond the refactor project.

## Link
- [https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith](https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith)
