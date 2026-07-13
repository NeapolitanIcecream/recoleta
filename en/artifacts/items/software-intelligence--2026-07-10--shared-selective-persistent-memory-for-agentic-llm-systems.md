---
source: arxiv
url: https://arxiv.org/abs/2607.09493v1
published_at: '2026-07-10T15:07:00'
authors:
- Sanjana Pedada
- Aditya Dhavala
- Neelraj Patil
topics:
- agentic-llm-systems
- persistent-memory
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Shared Selective Persistent Memory for Agentic LLM Systems

## Summary
The paper presents a shared memory architecture for agentic LLM systems that retains reusable workspace context while discarding session-specific traces. In enterprise and public-dataset evaluations, it reports higher task completion, lower token use, faster execution, and zero-token refresh for schema-compatible data updates.

## Problem
- Agentic LLM sessions discard task rules, data schemas, tool settings, and output requirements, forcing users to repeat specifications for recurring work.
- Persisting full conversation histories adds irrelevant reasoning and tool traces that can bias later generations and reduce quality.
- The problem matters for recurring dashboards, reports, data updates, and collaborative artifact development, where repeated specification increases time, tokens, and error risk.

## Approach
- Store four reusable context categories per workspace: task specifications, data schemas, tool configurations, and output constraints.
- Exclude reasoning traces, tool logs, temporary files, failed recovery paths, unapproved edits, and raw data from persistent memory.
- Inject structured memory into each new session, while providing data through compact statistical schemas instead of raw datasets.
- Require generated artifacts to read data through a runtime injection point, allowing compatible data changes without calling the LLM again.
- Add shared workspaces with role-based access control, git-backed artifact versions, draft isolation, and rollback support.

## Results
- Across 24 enterprise recurring-generation tasks, selective memory reached 96% completion, compared with 79% without memory and 71% with full history.
- Selective memory reduced average user turns to 1.4 versus 4.3 without memory and 3.1 with full history; average time fell to 68 seconds from 285 and 310 seconds.
- Selective memory used 3.4K input tokens and 4.1K output tokens, compared with 18.7K and 9.6K for full history; the paper reports a 97x token-cost reduction for summary-driven generation versus raw data injection.
- Zero-token refresh succeeded for all 18 of 18 enterprise tasks with compatible schemas and reduced recurring task time by 14x in the reported deployment scenario.
- On four public datasets with 36 total trials, selective memory achieved 100% completion in 12 of 12 refresh trials with zero LLM tokens, versus 83% without memory and 75% with full history.
- The strongest reported limitation was a selective-memory failure on cross-file join semantics that the schema summary did not capture.

## Link
- [https://arxiv.org/abs/2607.09493v1](https://arxiv.org/abs/2607.09493v1)
