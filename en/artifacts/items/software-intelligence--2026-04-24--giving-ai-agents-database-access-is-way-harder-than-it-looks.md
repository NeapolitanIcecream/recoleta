---
source: hn
url: https://querybear.com/blog/architecture-of-querybear
published_at: '2026-04-24T23:06:19'
authors:
- dispencer
topics:
- ai-agents
- database-security
- sql-guardrails
- prompt-injection
- defense-in-depth
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Giving AI Agents Database Access Is Way Harder Than It Looks

## Summary
The piece argues that giving AI agents safe database access needs multiple guardrails, not a single read-only check. It describes QueryBear's defense-in-depth design for limiting harmful SQL, data leakage, and resource abuse.

## Problem
- AI agents with database access can issue destructive, expensive, or over-broad queries even when they use a nominally read-only account.
- Simple controls fail in common cases: regex SQL filters miss tricks, read-only roles do not stop `pg_sleep` or huge joins, and valid joins can still expose sensitive columns such as credentials or tokens.
- Database contents can also inject adversarial text into the agent's context, which creates prompt-injection risk from stored data.

## Approach
- The core method is a layered "onion" design: start from default-deny access, then add back only the exact tables, columns, and query capabilities the agent needs.
- QueryBear's stated layers include a strict SQL parser, table and column allowlists, AST-level query rewriting for limits and timeouts, a pre-execution cost check, database-level read-only transactions, statement timeouts, and full audit logging.
- The mechanism is simple: each guardrail covers a failure mode that another guardrail can miss, so the system does not depend on one perfect check.
- The testing method is adversarial. The post calls for prompt-injection payloads, multi-statement attacks, and queries that are syntactically valid but operationally unsafe.

## Results
- No quantitative benchmark results are provided in the excerpt.
- The strongest concrete claim is architectural: QueryBear says it already runs a stack with SQL parsing, allowlists, AST rewriting, cost checks, database read-only enforcement, statement timeouts, and audit logs.
- The post gives concrete failure examples that the layers aim to block: `DELETE` hidden by comment tricks, `SELECT pg_sleep(3600)` connection exhaustion, a 12-table Cartesian join returning half a billion rows, and joins that expose `oauth_tokens`.
- The claimed benefit is safer agent database access under realistic failure modes such as prompt injection, expensive queries, and unauthorized reads, but the excerpt does not report measured reductions in incidents, latency, or attack success rate.

## Link
- [https://querybear.com/blog/architecture-of-querybear](https://querybear.com/blog/architecture-of-querybear)
