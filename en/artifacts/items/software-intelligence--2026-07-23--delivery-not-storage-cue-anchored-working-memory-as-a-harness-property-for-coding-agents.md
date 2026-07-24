---
source: arxiv
url: https://arxiv.org/abs/2607.20972v1
published_at: '2026-07-23T06:50:04'
authors:
- Swapnanil Saha
topics:
- coding-agents
- agent-memory
- context-compaction
- software-engineering
- agent-harnesses
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents

## Summary
The paper argues that reliable long-running coding-agent memory must be delivered by the harness at situation-specific cues rather than retrieved voluntarily from documents or tools. Its cue-anchored working-memory design injects scoped memories deterministically and shows reliable delivery across compaction boundaries, while voluntary memory use is nearly absent.

## Problem
- Coding agents mainly use documents and optional memory tools, which require the model to decide what to save and retrieve; this fails to reproduce cue-driven operational memory during long tasks.
- Context compaction can remove facts that remain relevant, forcing re-exploration or unsanctioned searches through session artifacts.
- This matters because missing situational knowledge can increase tool use, context waste, and the risk of losing task-critical constraints in extended software work.

## Approach
- Model each memory as content, kind, scope, decay, and composable triggers based on path, symbol, semantic similarity, event, and time.
- Evaluate triggers deterministically in the harness at events such as session start, prompt submission, file access, and post-compaction, rather than relying on model initiative.
- Use budgeted, provenance-framed injection with deduplication, compaction-boundary resets, audit logs, and staleness checks.
- Implement the mechanism in Vectr and connect it to Claude Code through both native lifecycle hooks and an API proxy.
- Evaluate a reverse-option feature for Apache Camel's stream-mode Resequencer on a pinned approximately 169,000-chunk codebase, plus a repeated-compaction probe with ten synthetic facts.

## Results
- In the strongest voluntary control, the agent made 0 memory calls in 114 turns despite having four task-relevant seeded notes, connected tools, and explicit guidance.
- Native delivery injected the cue-anchored gotcha on the first touch of its file in both runs, with 0 false-alarm injections across 40 and 35 audit-logged trigger evaluations; the proxy processed 241 injection decisions, injecting 5 and correctly skipping 236.
- All 12 graded coding runs passed the unmodified acceptance test and the 42-test Resequencer regression suite; the paper reports no correctness harm from injection.
- Across nine pilot transcripts, 24 of 61 intra-session re-reads, or 39%, repeated content encountered before a compaction boundary; approximately 78,000 result tokens were re-paid, with a worst run re-paying approximately 31,600 tokens.
- In the repeated-compaction probe, conversation-only facts were absent from 106 of 108 summaries, while harness injection delivered all ten facts at 139 audited points, including the launch and all 138 compact-resumes; the injected arm produced a clean 10/10 endpoint without relying on the final summary.
- The reported efficiency direction is positive but inconclusive: tool-equipped runs averaged 79.8 versus 137.3 tool calls and $5.08 versus $7.20 cost for vanilla runs, while the memory comparison used only two native runs versus one voluntary run and one task, so it does not establish a significant speed or cost benefit.

## Link
- [https://arxiv.org/abs/2607.20972v1](https://arxiv.org/abs/2607.20972v1)
