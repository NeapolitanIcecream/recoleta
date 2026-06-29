---
source: hn
url: https://byteiota.com/claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents/
published_at: '2026-06-13T23:17:22'
authors:
- sscaryterry
topics:
- claude-code
- nested-agents
- context-management
- agentic-workflows
- token-cost
- multi-agent-systems
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents

## Summary
Claude Code v2.1.172 lets sub-agents spawn their own sub-agents, up to five levels deep, so noisy work can stay out of the parent context. The main value is cleaner agent workflows when raw output would otherwise pollute the top-level session.

## Problem
- Sub-agents used to stop at one level, which made multi-step agent workflows harder to isolate.
- Long intermediate output, like logs or search traces, could flood the parent context and waste tokens.
- Teams needed a way to keep debugging and analysis chains inside separate context frames without losing the final answer.

## Approach
- Claude Code now allows nested sub-agents, with server-side enforcement of a hard five-level cap.
- Each agent frame keeps its own system prompt, model choice, and 200K-token context window.
- The parent receives only the child’s summary, while intermediate searches, file reads, and reasoning stay inside the lower frame.
- The feature is controlled through the new `Agent()` allowlist in agent definitions.
- The article recommends tiered routing: Opus at orchestration, Sonnet for mid-level work, and Haiku for leaf tasks.

## Results
- The feature supports nesting up to 5 levels deep.
- The article reports roughly 7x token overhead per branch per level from orchestration, context setup, and summary passing.
- A tiered setup is reported at about $0.98 per session versus $2.02 for uniform Opus, a 51% cost reduction with no quality loss on leaf tasks.
- A community example is cited at 887,000 tokens per minute before the user noticed the spend.
- A reported production case reached a $47,000 invoice in 3 days after running 23 sub-agents.
- No benchmark suite or controlled evaluation is given in the excerpt; the strongest claims are context isolation, cleaner outputs, and lower cost with tiered model routing.

## Link
- [https://byteiota.com/claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents/](https://byteiota.com/claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents/)
