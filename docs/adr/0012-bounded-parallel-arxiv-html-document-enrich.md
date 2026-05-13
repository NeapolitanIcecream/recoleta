# ADR 0012: Bounded Parallelism for arXiv html_document Enrichment

## Status
Accepted

## Context
The `html_document` enrichment path is dominated by network fetch latency, HTML cleanup, and Pandoc conversion. The previous serial loop underutilized CPU cores and spent significant wall time waiting on I/O.

## Decision
Implement bounded parallelism in `PipelineService.enrich` when `SOURCES.arxiv.enrich_method=html_document`, controlled by `SOURCES.arxiv.html_document_max_concurrency`. Each worker uses its own `httpx.Client`, and concurrency is capped to avoid excessive load or instability.

## Consequences
Wall time for `enrich(html_document)` can improve substantially on local backfills when operators explicitly raise concurrency. The default remains serial and throttled to roughly one request every 15 seconds so automated access to arXiv HTML pages is conservative by default. SQLite write contention is mitigated by batched writes; operators should lower concurrency or request rate if they see rate limits or DB lock contention.
