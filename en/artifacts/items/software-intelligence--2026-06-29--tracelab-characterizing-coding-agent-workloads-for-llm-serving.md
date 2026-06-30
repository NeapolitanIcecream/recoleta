---
source: arxiv
url: https://arxiv.org/abs/2606.30560v1
published_at: '2026-06-29T16:59:05'
authors:
- Kan Zhu
- Mathew Jacob
- Chenxi Ma
- Yi Pan
- Stephanie Wang
- Arvind Krishnamurthy
- Baris Kasikci
topics:
- coding-agents
- llm-serving
- workload-traces
- kv-cache
- tool-calling
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# TraceLab: Characterizing Coding Agent Workloads for LLM Serving

## Summary
TraceLab releases and analyzes a real coding-agent trace for LLM serving: 4,265 sessions, 357,161 LLM steps, and 432,510 tool calls from Claude Code and Codex. The paper claims coding-agent serving cost comes mainly from repeated long-context reads, autonomous tool loops, and prefix-cache misses.

## Problem
- Public LLM serving traces and coding benchmarks miss day-to-day coding-agent behavior across persistent sessions, tool calls, long contexts, and human-paced gaps.
- SWE-bench and Terminal-Bench measure task success on isolated tasks, so they do not show how sessions grow or how serving systems spend time and tokens.
- This matters because KV-cache policy, prefill routing, tool runtime design, and latency targets depend on real traffic patterns.

## Approach
- The authors collect default local logs from Claude Code and Codex used by 43 developers over roughly eight months.
- They normalize provider-specific logs into a step-level schema where each row covers one LLM invocation and its tool calls.
- They split input tokens into prefix tokens, append tokens, and output tokens, then analyze cost, latency, context growth, compaction, tool use, and cache behavior.
- They anonymize the trace by replacing identifiers and dropping raw user text and tool I/O while keeping timestamps, token counts, tool types, and pseudonymous users.
- They release the dataset, collection pipeline, and analysis code.

## Results
- Dataset scale: 4,265 sessions, 43 users, 23 model versions, 357,161 LLM steps, 432,510 tool calls, 54.90B total input tokens, and 186.9M output tokens.
- Agent loops are long: a session averages 9.2 requests, 82.5 steps, and 101.4 tool calls; a request averages 8.8 LLM calls and 10.8 tool calls.
- Token shape favors long reads and short generations: the median step has about 119K prefix tokens, 875 append tokens, and 214 output tokens.
- Cost is driven by prefix reads: prefix tokens are 52.56B of 54.90B input tokens and 59.5% of estimated API cost, compared with 29.2% for append tokens and 11.2% for output tokens.
- Prefix caching helps but misses still hurt: the global prefix-cache hit rate is 95.7%, while cache misses cause 3.8x more prefilling than truly new input tokens.
- Tool behavior is skewed: more than 80 tool types appear, the top 3 tools per provider account for more than 80% of tool calls, and tool calls over 1 minute are 4% of calls but 85% of total tool-call time.

## Link
- [https://arxiv.org/abs/2606.30560v1](https://arxiv.org/abs/2606.30560v1)
