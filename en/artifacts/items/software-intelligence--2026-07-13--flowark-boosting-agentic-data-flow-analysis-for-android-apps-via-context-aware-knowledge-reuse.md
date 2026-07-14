---
source: arxiv
url: https://arxiv.org/abs/2607.11308v1
published_at: '2026-07-13T09:21:38'
authors:
- Yiming Zhang
- Jiangrong Wu
- Yuhong Nan
topics:
- code-intelligence
- agentic-software-engineering
- android-security
- data-flow-analysis
- agent-memory
- knowledge-reuse
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# FlowArk: Boosting Agentic Data-flow Analysis for Android Apps via Context-Aware Knowledge Reuse

## Summary
FlowArk reduces repeated code analysis in batch Android data-flow tasks by sharing verified knowledge between otherwise isolated coding-agent sessions. On 4,685 tasks across 50 open-source Android apps, it cuts API cost by 26.83% while preserving comparable analysis quality.

## Problem
- Batch source-to-sink analysis assigns separate agents to different taint sources, but shared callbacks, dispatchers, and cross-file logic cause repeated analysis.
- Context isolation prevents later agents from using earlier reasoning, increasing token use, API cost, and limiting the number of tasks completed under a fixed budget.
- General memory systems can store imprecise information and often retrieve it too late because the active agent must request it.

## Approach
- FlowArk distills completed analysis histories into evidence-backed, bounded, and actionable knowledge about recurring shared code fragments.
- It packages each knowledge item with code-based matching rules using exact symbols, calls, symbol suffixes, and package prefixes.
- During later analysis, it monitors tool outputs and injects a matched knowledge block as soon as the runtime context exposes the relevant code anchors.
- The injected block identifies which shared steps can be skipped and which parameter-dependent downstream handlers still need checking.
- Admission checks reject or repair entries with weak evidence, unclear boundaries, or unreliable matching rules.

## Results
- Evaluation covered 4,685 source-to-sink data-flow analysis tasks from 50 open-source Android apps using an OpenCode implementation.
- Compared with standard OpenCode, FlowArk reduced end-to-end LLM API cost by 26.83% while maintaining comparable analysis quality.
- Under a USD 100 budget, FlowArk completed 1,060 tasks versus 776 for standard OpenCode, a 36.66% increase.
- FlowArk reported larger cost savings than Mem0-enabled OpenCode and Analysis-Log RAG while maintaining comparable analysis quality.

## Link
- [https://arxiv.org/abs/2607.11308v1](https://arxiv.org/abs/2607.11308v1)
