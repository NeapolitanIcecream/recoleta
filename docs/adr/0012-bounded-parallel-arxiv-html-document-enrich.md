# ADR 0012: Bounded Parallelism for arXiv html_document Enrichment

## Status
Accepted

## Context
The `html_document` enrichment path is dominated by network fetch latency, HTML cleanup, and Pandoc conversion. The previous serial loop underutilized CPU cores and spent significant wall time waiting on I/O.

## Decision
Implement bounded parallelism in `PipelineService.enrich` when `SOURCES.arxiv.enrich_method=html_document`, controlled by `SOURCES.arxiv.html_document_max_concurrency`. Each worker uses its own `httpx.Client`, and concurrency is capped to avoid excessive load or instability.

## Consequences
Wall time for `enrich(html_md)` improves substantially on typical workloads. SQLite write contention is mitigated by conservative defaults and batched writes; operators can lower concurrency if they see rate limits or DB lock contention.

