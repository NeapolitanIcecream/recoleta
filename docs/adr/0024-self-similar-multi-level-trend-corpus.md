---
title: "ADR 0024: Self-similar multi-level trend corpus"
status: Accepted
---

## Context
Weekly/monthly trend quality degrades when the corpus is restricted to lower-level trend documents, which collapses paper-level evidence and breaks citations and ranking outputs.

## Decision
Adopt a self-similar trend generation plan: for any target granularity \(N\), pre-inject all \(N-1\) overviews into the prompt and enable RAG over all \(\le N-1\) levels. Enforce that cluster representatives are always `doc_type=item` so citations remain paper-grounded.

## Consequences
Trends keep stable paper-level citations and can produce a reliable Top-N must-read list, at the cost of additional indexing/search work. Metrics reuse `pipeline.trends.*` with low-cardinality counters for overview-pack truncation and representative enforcement.

