---
kind: trend
trend_doc_id: 635
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
topics:
- coding-agents
- token-cost
- repo-level-generation
- verification
- traceability
- agent-safety
run_id: materialize-outputs
aliases:
- recoleta-trend-635
tags:
- recoleta/trend
- topic/coding-agents
- topic/token-cost
- topic/repo-level-generation
- topic/verification
- topic/traceability
- topic/agent-safety
language_code: en
pass_output_id: 106
pass_kind: trend_synthesis
---

# Practical limits are now the main story in AI coding research

## Overview
Today’s coding research is strongest on practical limits. RealBench shows repo-level generation still breaks down on full projects, and the token-cost study shows agentic coding can be vastly more expensive than chat-style help. The most credible improvements come from tighter structure: verifier feedback, adaptive retrieval, and explicit guardrails around database access.

## Clusters

### Cost control is now part of the coding-agent research agenda
Token cost is the clearest practical constraint in this batch. The strongest evidence comes from a trajectory study on SWE-bench Verified with eight frontier models in OpenHands. Agentic coding used about 3500× more tokens than single-round code reasoning and about 1200× more than multi-turn code chat. Cost also swung hard on the same task, with runs differing by up to 30×. The paper ties expensive failures to repeated file viewing and editing, and it shows that models are poor at predicting their own token bill before execution. A second paper, R2Code, points to one concrete response: tighter retrieval and smaller context. It reports an average F1 gain of 7.4% on five traceability datasets while cutting token use by up to 41.7% through adaptive context control.

#### Evidence
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Main evidence for token cost scale, variance, and weak self-prediction in agentic coding.
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): Evidence that adaptive retrieval can cut token use while improving a maintenance task.

### Repo-scale benchmarks are exposing how little current models automate end-to-end implementation
Repo-level generation is still weak when the task looks like real software work. RealBench builds 61 Python repositories from 20 domains, each with natural-language requirements, UML package and class diagrams, and human-verified tests. The best average Pass@1 is 19.39%. Repository size matters a lot: scores are above 40% below 500 lines of code and below 15% above 2000 lines. The benchmark also shows why small benchmark wins do not carry over cleanly. Only 44.73% of methods are standalone on average, and in the largest tier that drops to 26.23%, so dependency handling is the core problem. The paper also reports that whole-repo generation works better on smaller projects, while incremental generation works better once repositories get larger.

#### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): Primary evidence for repo-level benchmark design, low pass rates, and size effects.

### Structured evidence and executable checks are carrying more of the load
Verification and maintenance work remain a productive place for structured assistance. One paper on natural-language-to-Dafny generation reports near-universal failure with plain prompting, then much better results when the model gets method signatures and verifier feedback. On sampled tasks, Gemma 4-31B reaches 90.91% verification success and GPT-OSS 120B rises from 0% to 81.82% with signature-guided feedback. Another paper, R2Code, breaks requirements and code into aligned semantic parts, adds a consistency check, and reports gains on five datasets. Together these papers point to the same pattern: coding help improves when the model works against explicit structure, executable checks, and narrow evidence slices.

#### Evidence
- [From Natural Language to Verified Code: Toward AI Assisted Problem-to-Code Generation with Dafny-Based Formal Verification](../Inbox/2026-04-24--from-natural-language-to-verified-code-toward-ai-assisted-problem-to-code-generation-with-dafny-based-formal-verification.md): Evidence for verifier-guided gains in Dafny code generation.
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): Evidence for structured traceability and adaptive retrieval in maintenance tasks.

### Operational safety work is getting more specific about agent permissions
A smaller but concrete thread covers operational guardrails around agent access to real systems. QueryBear argues that database safety needs layered controls, not a single read-only rule. The stack it describes includes SQL parsing, table and column allowlists, AST-level query rewriting, pre-execution cost checks, statement timeouts, and audit logging. The examples are practical: blocking comment-hidden DELETE statements, `pg_sleep(3600)` denial-of-service queries, oversized joins, and joins that expose `oauth_tokens`. This is not a benchmark paper, but it fits the day’s emphasis on making agent actions reviewable before they touch production resources.

#### Evidence
- [Giving AI Agents Database Access Is Way Harder Than It Looks](../Inbox/2026-04-24--giving-ai-agents-database-access-is-way-harder-than-it-looks.md): Primary evidence for layered database guardrails and concrete failure modes.
