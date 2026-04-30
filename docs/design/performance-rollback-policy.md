# Performance rollback policy

Use this policy for bounded enrich parallelism and related write-path
optimizations. The rollback target is always the documented default behavior.

## Kill switches

### arXiv html_document -> html_document_md

- `SOURCES.arxiv.html_document_max_concurrency=1` or `SOURCES.arxiv.html_document_enable_parallel=false`: disable parallel enrich.
- `SOURCES.arxiv.html_document_skip_cleanup_when_complete=false`: re-enable cleanup/conversion checks on warm DB runs.
- `SOURCES.arxiv.html_document_use_batched_db_writes=false`: revert to per-content upserts (more commits, simpler behavior).
- `SOURCES.arxiv.html_document_requests_per_second=<lower>`: reduce arXiv request rate if you see HTTP 429 or instability.
- `SOURCES.arxiv.html_document_log_sample_rate=0`: silence per-item html_document info logs in parallel runs (keeps errors/warnings).

### Non-arXiv HTML maintext

- `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=1` or unset: restore default
  sequential HTML maintext enrich.
- `enrich_html_maintext_max_concurrency: 1`: config-file equivalent for child
  instances that set the knob in YAML/JSON.

## Rollback thresholds

- If `pipeline.enrich.failed_total` increases by **> 1% absolute** or new dominant errors appear (e.g., SQLite lock, HTTP 429), disable parallelism first.
- If `html_document_md` / `html_references` become missing or inconsistent on previously passing cases, disable the skip-cleanup optimization.
- If DB metrics show no reduction in `pipeline.enrich.db.sql_commits_total` or correctness regresses, disable batched DB writes.
- For `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4`, also watch
  `pipeline.enrich.parallel.html_maintext.items_total`,
  `pipeline.enrich.parallel.html_maintext.max_workers`, source HTTP 5xx/429
  rates, and `html_maintext` coverage. Roll back to `1` if failures rise,
  source throttling appears, SQLite lock errors appear, or comparable fleet-day
  wall time no longer improves.
