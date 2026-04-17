---
source: arxiv
url: http://arxiv.org/abs/2604.10842v2
published_at: '2026-04-12T22:23:55'
authors:
- Justice Owusu Agyemang
- Jerry John Kponyo
- Elliot Amponsah
- Godfred Manu Addo Boakye
- Kwame Opuni-Boachie Obour Agyekum
topics:
- llm-coding-agents
- mcp-tools
- durable-file-writes
- code-intelligence
- agent-reliability
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents

## Summary
Resilient Write is an MCP server that makes file writes from LLM coding agents harder to lose, corrupt, or retry blindly. It adds six independent protections around the write path and reports large gains over naive and partially defensive baselines.

## Problem
- LLM coding agents write files through tools such as MCP, but writes can fail with no machine-readable signal when content filters block payloads, large outputs get truncated, or sessions stop mid-write.
- When that happens, agents may lose the draft, repeat the same write several times, waste tokens, and fail to recover because the error comes back as plain text or no error at all.
- This matters for autonomous coding loops because file mutation is a core step in edit-test-commit workflows, and a weak write path can break the whole task.

## Approach
- The system inserts a six-layer write surface between the agent and the filesystem: pre-flight risk scoring, atomic transactional writes, resumable chunking, typed JSON errors, out-of-band scratch storage, and cross-session handoff files.
- Risk scoring scans draft content with deterministic regex and size rules to flag patterns likely to trigger host-side content filters. It returns a score in `[0,1]`, a verdict (`safe`, `low`, `medium`, `high`), matched pattern families, and suggested actions.
- Safe writes use a temp-file, `fsync`, read-back SHA-256 verification, and atomic rename. Optional `expected_prev_sha256` adds optimistic concurrency checks so stale writes fail cleanly.
- Large writes are split into numbered chunks that are stored durably and later composed only if chunk indices are contiguous and match the expected count.
- Failures return typed envelopes with fields such as `error`, `reason_hint`, `detected_patterns`, `suggested_action`, and `retry_budget`, so the agent can change strategy instead of retrying the same blocked write.

## Results
- The implementation provides 16 MCP tools and is validated by a 186-test suite covering all six layers plus extensions; the breakdown includes 28 tests for risk scoring, 17 for safe write and journaling, 27 for chunking, 27 for error handling, 21 for scratchpad, 8 for handoff, 42 for extensions, and 16 for server/infrastructure.
- In the replayed case study, write attempts dropped from 6 to 2. The original run lost content, had no structured error, did not self-correct, and needed manual intervention; the Resilient Write run lost no content, returned structured errors, self-corrected, and needed no manual intervention.
- In the quantitative comparison, recovery time fell from 10.0 s for the naive baseline and 5.5 s for the defensive baseline to 2.0 s with Resilient Write.
- Estimated data-loss probability dropped from 5.0% (naive) and 1.0% (defensive) to 0.1% with Resilient Write.
- Estimated self-correction rate rose from 5% (naive) and 15% (defensive) to 65% with Resilient Write, which the paper states as a 13x improvement over naive.
- Estimated wasted calls fell from 25% (naive) and 12.5% (defensive) to 3.0% with Resilient Write. The paper also claims a 5x reduction in recovery time and a 50x reduction in data-loss probability versus naive.

## Link
- [http://arxiv.org/abs/2604.10842v2](http://arxiv.org/abs/2604.10842v2)
