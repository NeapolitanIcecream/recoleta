---
source: hn
url: https://github.com/dogtorjonah/context-warp-drive
published_at: '2026-07-13T23:32:39'
authors:
- Dr_Jonah
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Show HN: Context Warp Drive – deterministic, zero-LLM context compaction

## Summary
Context Warp Drive is a deterministic, zero-LLM context compaction engine for long-running tool-using agents. It preserves exact identifiers, raw history, and reusable provider prompt prefixes while keeping the visible context within a token budget.

## Problem
- Long agent sessions exceed context limits, forcing truncation or LLM summarization.
- Truncation can remove older evidence and identifiers; summarization adds a model call, latency, non-determinism, and cache-prefix rewrites.
- Long-running software agents need continuity across folds, process restarts, and hard context resets.

## Approach
- Fold older turns into deterministic structural skeletons while keeping recent turns at full fidelity.
- Extract UUIDs, hashes, paths, ports, and issue references into a budgeted Coordinate Closet so key identifiers remain verbatim.
- Freeze sealed prompt prefixes so identical inputs produce byte-identical output and provider prompt caches can reuse them across turns and epochs.
- Build recall indexes that page folded evidence back into the prepared context when later activity touches a related path, claim, or identifier.
- Add model-aware pressure budgets, hard Rebirth seeds, provider adapters, episodic storage, and a dependency-free Task Rail for execution state outside the prompt.

## Results
- A production Claude deployment recorded a 92.6% cache-read hit rate across 954 tool calls over 1 hour 49 minutes; the paper also reports about 90% cache-served input tokens in high-turn workloads.
- In a deterministic 16-turn outage-debugging benchmark using exact o200k_base BPE counts and Claude Sonnet pricing, the method reduced cost by 63% versus truncation and 72% versus summarization.
- The fold and recall core made zero extra LLM calls and used zero I/O; the repository includes more than 900 deterministic tests across folding, recall, freezing, provider adapters, task rails, and integration.
- The bundled Rebirth continuity study reports first-action non-inferiority against a full-context summary, stable behavior through the 684th consecutive Rebirth, and 92.8% cache-read on first-boundary rows versus 94.5% on ordinary warm rows.
- Production cache telemetry is from a single deployment without a real-workload A/B control arm, while the offline comparison is small; larger controlled long-horizon evaluations remain future work.

## Link
- [https://github.com/dogtorjonah/context-warp-drive](https://github.com/dogtorjonah/context-warp-drive)
