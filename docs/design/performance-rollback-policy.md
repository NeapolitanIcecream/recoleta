# Performance rollback policy (arXiv html_document -> html_document_md)

## Kill switches
- `SOURCES.arxiv.html_document_max_concurrency=1` or `SOURCES.arxiv.html_document_enable_parallel=false`: disable parallel enrich.
- `SOURCES.arxiv.html_document_skip_cleanup_when_complete=false`: re-enable cleanup/conversion checks on warm DB runs.
- `SOURCES.arxiv.html_document_use_batched_db_writes=false`: revert to per-content upserts (more commits, simpler behavior).
- `SOURCES.arxiv.html_document_requests_per_second=<lower>`: reduce arXiv request rate if you see HTTP 429 or instability.
- `SOURCES.arxiv.html_document_log_sample_rate=0`: silence per-item html_document info logs in parallel runs (keeps errors/warnings).

## Rollback thresholds
- If `pipeline.enrich.failed_total` increases by **> 1% absolute** or new dominant errors appear (e.g., SQLite lock, HTTP 429), disable parallelism first.
- If `html_document_md` / `html_references` become missing or inconsistent on previously passing cases, disable the skip-cleanup optimization.
- If DB metrics show no reduction in `pipeline.enrich.db.sql_commits_total` or correctness regresses, disable batched DB writes.

