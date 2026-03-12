# Trends Hotspot Study

## Scope

This note quantifies three `trends` optimization directions against the current
post-`PR #10` code:

1. Run-local caching for repeated `ensure_summary_vectors_for_period()` calls.
2. Batching item document indexing plus FTS sync on the cold path.
3. Removing stage-level representative enforcement / re-backfill.

Backfill is intentionally out of scope for this study.

## Method

Benchmarks are implemented in
[scripts/bench_trends_hotspots.py](/Users/chenmohan/gits/recoleta/scripts/bench_trends_hotspots.py).

Properties of the benchmark:

- Uses a temporary SQLite workspace and temporary LanceDB directory.
- Seeds analyzed items directly into the repository, then exercises current
  `trends` helpers.
- Uses deterministic fake embeddings, so no LLM tokens are consumed.
- Emits one JSON document to stdout by default, with no log noise.
- Measures wall time plus coarse SQL diagnostics.

Command used for the reported numbers:

```bash
uv run python scripts/bench_trends_hotspots.py --items 64 --queries 6 --clusters 18 --repeats 3
```

## Results

### 1. Semantic Corpus Cache

Repeated semantic queries against the same period and corpus:

- Baseline: `29 ms` median wall time, `6` SQL queries, `6` ensure misses.
- Cached: `19 ms` median wall time, `1` SQL query, `1` ensure miss, `5` cache hits.
- Delta: `34.5%` wall-time improvement, `83.3%` fewer SQL queries.

Interpretation:

- The current repeated warm-up is real, but with the latest code it is no
  longer the dominant cost.
- A run-local corpus cache still looks worthwhile because it is simple and
  structurally clean, and it removes repeated repository scans almost entirely.

### 2. Index Batching

Cold-path item indexing for the same 64-item analyzed corpus:

- Baseline: `467 ms` median wall time, `2242` SQL queries, `448` commits.
- Batched prototype: `34 ms` median wall time, `513` SQL queries, `1` commit.
- Delta: `92.7%` wall-time improvement, `77.1%` fewer SQL queries, `99.8%` fewer commits.

Interpretation:

- This is the clear top optimization target in current code.
- The current indexer is heavily transaction-amplified: per-item document
  upserts, per-chunk upserts, and per-chunk FTS sync dominate the path.
- Even a cold-path-only prototype captures most of the available gain.

### 3. Representative Enforcement

Two scenarios were measured:

1. `pass_through_item_reps`

- Models the current expected path where the agent already returns valid item
  representatives.
- Result: `2 ms` median wall time, `20` SQL queries, `0` semantic re-searches.

2. `forced_rebackfill_upper_bound`

- Models an upper bound where stage receives non-item reps and must drop them,
  perform text search, then semantic fallback.
- Result: `91 ms` median wall time, `90` SQL queries, `54` text searches,
  `18` semantic searches, `18` clusters backfilled.

Interpretation:

- After the recent code changes, stage representative enforcement is **not**
  an urgent optimization when agent output is already item-first.
- It only becomes expensive in the fallback / re-backfill path.
- That means point (3) should probably be treated as a cleanup / guardrail
  simplification, not the next main performance project.

## Recommendation

Priority order after this study:

1. Batch item document indexing and FTS sync.
2. Add run-local semantic corpus caching.
3. Defer representative-enforcement removal unless production metrics show
   non-trivial `rep_enforcement.backfilled_total` or frequent non-item reps.

## Caveats

- The batching benchmark is a cold-path prototype, not a production-faithful
  incremental updater.
- The representative benchmark includes a synthetic upper-bound scenario by
  design; it should not be mistaken for the common path.
- All numbers are local synthetic medians and should be used for prioritization,
  not SLA claims.
