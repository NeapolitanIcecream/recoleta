# 2026-04-13 Fleet Day E2E Hotspot Study: Stage 1

## Scope

This note records the first completed measurement wave for the UTC day
`2026-04-13`, using the live fleet manifest at
`/Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml`.

The intent of this stage was:

- add the missing DFX comparison tool and metrics needed to explain wins
- run one live baseline against real state
- derive one reusable shadow control from that baseline backup set
- implement and measure the first prepare/enrich treatment branch
- decide whether that branch meets the acceptance rule before moving on

`bench-out*` remains generated output and is intentionally not committed.

## Commands Run

### Live preflight

```bash
uv run recoleta inspect health --config /Users/chenmohan/Playground/recoleta-playground/fleet/instances/embodied_ai/recoleta.yaml
uv run recoleta inspect health --config /Users/chenmohan/Playground/recoleta-playground/fleet/instances/software_intelligence/recoleta.yaml
uv run recoleta inspect health --config /Users/chenmohan/Playground/recoleta-playground/fleet/instances/cross_platform/recoleta.yaml
```

All three children passed with `settings=ok`, `paths=ok`, `lease=free`.

### Live baseline

```bash
uv run python scripts/bench_fleet_day_e2e.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --output-dir bench-out/e2e-20260413-baseline
```

### Reusable shadow control

```bash
uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-control
```

### First treatment candidate

```bash
uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-arxiv-html-reuse
```

### Formal comparison

```bash
uv run python scripts/compare_shadow_day_runs.py \
  --baseline bench-out/shadow-20260413-control \
  --candidate bench-out/shadow-20260413-arxiv-html-reuse \
  --output-dir bench-out/compare-shadow-20260413-arxiv-html-reuse
```

## Artifacts

- Live baseline:
  `bench-out/e2e-20260413-baseline/summary.json`
- Shadow control:
  `bench-out/shadow-20260413-control/summary.json`
- First treatment:
  `bench-out/shadow-20260413-arxiv-html-reuse/summary.json`
- Formal delta report:
  `bench-out/compare-shadow-20260413-arxiv-html-reuse/delta.json`
  and `report.md`

## Baseline Findings

Live baseline fleet wall time was `565.77s`.

The live aggregate step ranking was:

| step | duration_ms | share |
| --- | ---: | ---: |
| ingest | 167,937 | 29.80% |
| translate | 128,952 | 22.88% |
| analyze | 90,018 | 15.97% |
| ideas:day | 82,775 | 14.69% |
| trends:day | 75,012 | 13.31% |
| site-build | 18,860 | 3.35% |

Per-child hotspot evidence from the live baseline:

- `embodied_ai`
  - prepare: `65.8s`
  - translate: `56.5s`
  - analyze: `43.0s`
  - top enrich fetch source: `hn=43.0s`
  - top arXiv extract: `8.0s`
- `software_intelligence`
  - prepare: `90.4s`
  - translate: `55.1s`
  - analyze: `36.6s`
  - top enrich fetch source: `hn=31.4s`
  - top arXiv extract: `39.6s`
- `cross_platform`
  - ideas:day: `24.4s`
  - trends:day: `19.1s`
  - translate: `17.3s`

Interpretation:

- `prepare/enrich` remained the highest-value first branch.
- The branch selector did **not** point to HN fetch reuse, because HN fetch did
  not dominate both heavy children.
- The first concrete treatment therefore targeted arXiv
  `html_document` reuse.

## Code Added In This Stage

- `scripts/compare_shadow_day_runs.py`
  - compares shadow control vs candidate
  - emits `delta.json` and `report.md`
- translation metrics
  - `pipeline.translate.scanned_total`
  - `pipeline.translate.translated_total`
  - `pipeline.translate.mirrored_total`
  - `pipeline.translate.skipped_total`
  - `pipeline.translate.skipped_total.up_to_date_source_hash`
  - `pipeline.translate.materialize_localized.duration_ms`
- arXiv treatment branch
  - reuse existing `html_document` + `html_document_md`
  - do not rerun cleanup or pandoc just to backfill `html_references`
- site-build instrumentation interface
  - `export_trend_static_site(..., metrics_recorder=None)`
  - low-cardinality multilingual substep timing callbacks
  - workflow wiring to emit `pipeline.site_build.*.duration_ms`

## First Treatment Result

The correct comparison baseline is the shadow control, not the live baseline.

### Fleet result

| run | real_seconds_total |
| --- | ---: |
| shadow control | 706.11 |
| arxiv html reuse | 701.55 |

Fleet wall-time delta: `-4.56s` (`0.65%` faster).

### Dominant-step result

Aggregate step deltas vs shadow control:

| step | baseline_ms | candidate_ms | delta_ms | improvement |
| --- | ---: | ---: | ---: | ---: |
| ingest | 265,426 | 265,951 | +525 | -0.20% |
| translate | 137,195 | 127,467 | -9,728 | 7.09% |
| analyze | 99,556 | 90,324 | -9,232 | 9.27% |
| ideas:day | 82,168 | 90,474 | +8,306 | -10.11% |
| trends:day | 87,135 | 85,706 | -1,429 | 1.64% |
| site-build | 14,457 | 19,476 | +5,019 | -34.72% |

### Supporting metric result

The target mechanism was real inside `software_intelligence`:

| metric | control | candidate | delta |
| --- | ---: | ---: | ---: |
| `pipeline.enrich.arxiv.html_document.fetch_ms_sum` | 59,971 | 51,398 | -8,573 |
| `pipeline.enrich.arxiv.html_document.cleanup_ms_sum` | 59,238 | 44,513 | -14,725 |
| `pipeline.enrich.arxiv.html_document.pandoc_ms_sum` | 80,330 | 64,880 | -15,450 |
| `pipeline.enrich.arxiv.html_document.db_write_ms_sum` | 8,656 | 8,049 | -607 |

Step-level effect inside `software_intelligence`:

- `ingest`: `179,433ms -> 169,506ms` (`-9,927ms`, `5.53%`)
- `translate`: `58,831ms -> 55,302ms` (`-3,529ms`, `6.00%`)

But the branch did not hold fleet-wide because:

- `embodied_ai ingest`: `71,405ms -> 86,606ms` (`+15,201ms`)
- `embodied_ai real_seconds`: `245.57s -> 256.75s`
- `software_intelligence real_seconds`: `350.31s -> 350.96s`

## Acceptance Verdict

This branch is **not accepted**.

The acceptance rule required:

- fleet wall time improvement `>= 8%`, or
- target dominant step improvement `>= 15%`
- no child regression worse than `5%`
- unchanged terminal state behavior

Observed:

- fleet wall time improvement: `0.65%`
- target step improvement on `software_intelligence ingest`: `5.53%`
- `embodied_ai` regressed by `4.55%` real time and its `ingest` step regressed by
  `21.29%`
- terminal state behavior stayed unchanged

So the branch produced useful localized savings but failed the promotion bar.

## What This Stage Clarified

- The new translation counters confirmed that current shadow control still does
  no translation skipping on this window:
  - `embodied_ai`: scanned `26`, translated `26`, skipped `0`
  - `software_intelligence`: scanned `26`, translated `26`, skipped `0`
  - `cross_platform`: scanned `3`, translated `3`, skipped `0`
- `materialize_localized.duration_ms` is measurable but not the main translation
  cost driver on this window:
  - `embodied_ai`: `3.8s`
  - `software_intelligence`: `8.7s`
  - `cross_platform`: `0.3s`
- `trends:day + ideas:day` exceeded the plan threshold in the live baseline, so a
  dedicated trends/ideas hotspot branch is justified after the next measured
  translation attempt.
- `site-build` qualified for deeper instrumentation because
  `software_intelligence` exceeded `10s`.

## Next Branch Order

The measured next-step order remains:

1. translation
2. trends/ideas
3. site-build only if still needed after the first two

Translation is next because:

- it is still the second-largest live aggregate step
- the new counters now separate translation request volume from localized
  projection rebuild time
- the first prepare/enrich branch did not clear acceptance

## Continuation Update

After opening the draft PR for this stage, the experiment continued with one
exploratory translation replay and one repeat, followed by the planned
trends/ideas hotspot microbench.

### Exploratory stacked translation replay

Command run:

```bash
TRANSLATION_PARALLELISM=12 uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-translate-p12
```

Compared against the already-modified `shadow-20260413-arxiv-html-reuse` run:

```bash
uv run python scripts/compare_shadow_day_runs.py \
  --baseline bench-out/shadow-20260413-arxiv-html-reuse \
  --candidate bench-out/shadow-20260413-translate-p12 \
  --output-dir bench-out/compare-shadow-20260413-translate-p12-vs-arxiv
```

Headline result:

| run | real_seconds_total |
| --- | ---: |
| arxiv html reuse | 701.55 |
| translate p12 | 565.79 |

Fleet delta vs `arxiv-html-reuse`: `-135.76s` (`19.35%` faster).

But this run is **not promotable as a translation win**, because the observed
speedup was not isolated to translation:

| aggregate step | baseline_ms | candidate_ms | delta_ms | improvement |
| --- | ---: | ---: | ---: | ---: |
| ingest | 265,951 | 158,614 | -107,337 | 40.36% |
| translate | 127,467 | 114,172 | -13,295 | 10.43% |
| site-build | 19,476 | 2,598 | -16,878 | 86.66% |
| analyze | 90,324 | 114,432 | +24,108 | -26.69% |

The key confounder is that the env change was only
`TRANSLATION_PARALLELISM=12`, yet the dominant savings landed in `ingest` and
`site-build`. That makes the replay directionally interesting, but not a clean
single-factor treatment.

The translation-specific signals were real but smaller:

- `software_intelligence`
  - `pipeline.workflow.step.translate.duration_ms`: `55,302 -> 39,202`
  - `pipeline.translate.parallelism.effective`: `8 -> 12`
  - `pipeline.translate.materialize_localized.duration_ms`: `4,897 -> 624`
- `embodied_ai`
  - `pipeline.workflow.step.translate.duration_ms`: `55,765 -> 55,792`
  - `pipeline.translate.parallelism.effective`: `8 -> 12`
  - `pipeline.translate.materialize_localized.duration_ms`: `4,190 -> 536`

### Translation repeat disproved stability

To measure replay variance, the same `TRANSLATION_PARALLELISM=12` candidate was
run a second time from the same backup root:

```bash
TRANSLATION_PARALLELISM=12 uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-translate-p12-r2
```

This repeat **failed** on `embodied_ai` during the `translate` step.

Failure evidence from the shadow run:

- terminal state: `failed`
- failure point: `translate`
- recorded translation metrics before abort:
  - `pipeline.translate.parallelism.effective = 12`
  - `pipeline.translate.scanned_total = 26`
  - `pipeline.translate.translated_total = 25`
  - `pipeline.translate.failed_total = 1`
  - `pipeline.translate.failed_total.empty_content = 1`
  - `pipeline.translate.llm_requests_total = 30`
- emitted error:
  `translation failed error_type=TranslationLLMOutputError error=translation LLM returned empty content`

This repeat is enough to reject `TRANSLATION_PARALLELISM=12` as a formal branch
result under the current acceptance rule. Even if the first replay was faster,
the second replay introduced a workflow terminal-state regression.

### Trends/ideas direction check

Because `trends:day + ideas:day` was already above the `15%` threshold in the
baseline, the next decision gate was the existing microbench:

```bash
uv run python scripts/bench_trends_hotspots.py --repeats 3
```

Measured hotspot directions:

- `semantic_corpus_cache`
  - wall time median: `40ms -> 26ms` (`35.0%` improvement)
  - SQL queries median: `6 -> 1` (`83.33%` reduction)
- `index_batching`
  - wall time median: `42ms -> 65ms` (`54.76%` slower)
- `rep_enforcement`
  - forced rebackfill upper bound: `93ms` median
  - pass-through item reps: `3ms` median

These microbench results match the actual `shadow-20260413-control` metrics:

- `overview_pack.duration_ms` is tiny
  - `cross_platform`: `9ms`
  - `embodied_ai`: `4ms`
  - `software_intelligence`: `13ms`
- `history.pack.duration_ms` is tiny
  - `cross_platform`: `15ms`
  - `embodied_ai`: `4ms`
  - `software_intelligence`: `31ms`
- dominant trends cost is elsewhere
  - `pipeline.trends.agent_run_sync.duration_ms`: about `28.5s` to `28.8s`
  - `pipeline.trends.semantic_search.item.duration_ms`: `4.1s` to `8.3s`
  - `pipeline.trends.semantic_index.item.duration_ms`: `3.1s` to `7.3s`
  - `pipeline.trends.pass.ideas.duration_ms`: `25.8s` to `29.2s`

Conclusion:

- `context-pack trimming` is not the next high-ROI trends/ideas branch for this
  day window.
- `retrieval-loop reuse`, starting with semantic corpus cache reuse, is the
  better next measured branch.

## Updated Branch Order

Based on the continuation wave, the next measured order is now:

1. trends/ideas retrieval reuse
2. translation only after a stable, isolated candidate is available
3. site-build only if the first two do not move enough wall time

## Continuation Update 2

The next continuation wave returned to `prepare/enrich`, but with a different
mechanism than the first arXiv-focused branch.

The baseline evidence still showed large HN and generic HTML maintext fetch cost
inside the two heavy children, while the existing parallel path only covered the
arXiv `html_document` extractor.

That led to one new candidate:

- add an opt-in `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY` setting
- keep default behavior unchanged at `1`
- run non-arXiv HTML maintext enrichment in parallel when the setting is greater
  than `1`
- emit low-cardinality summary metrics so the branch can be explained in the
  compare report

### Code added for the branch

- `recoleta.config.Settings.enrich_html_maintext_max_concurrency`
  - env alias: `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY`
  - default: `1`
  - bounds: `1..32`
- `recoleta.pipeline.enrich_stage`
  - partition enrich items into
    `arxiv_parallel_items`, `html_parallel_items`, and `serial_items`
  - reuse the existing bounded parallel runner for the new HTML maintext bucket
  - preserve old behavior unless the new setting is explicitly enabled
- new summary metrics
  - `pipeline.enrich.parallel.html_maintext.items_total`
  - `pipeline.enrich.parallel.html_maintext.max_workers`

### Translation side check before the new enrich branch

A direct translation replay with `TRANSLATION_PARALLELISM=10` was also measured
from the same backup root:

```bash
TRANSLATION_PARALLELISM=10 uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-translate-p10
```

That replay failed on `embodied_ai` during `translate` with:

- `pipeline.translate.parallelism.effective = 10`
- `pipeline.translate.translated_total = 25`
- `pipeline.translate.failed_total = 1`
- `pipeline.translate.failed_total.empty_content = 1`

A smaller pilot with `TRANSLATION_PARALLELISM=9` succeeded for
`embodied_ai`, but it did not improve the target step:

- `embodied_ai translate`: `55,765ms -> 56,951ms`

This was enough to deprioritize translation parallelism for the next branch.

### HTML maintext parallel candidate

First measured replay:

```bash
ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4 uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-html-maintext-p4
```

That run produced a strong fleet improvement, but one child regressed:

- fleet wall time: `701.55s -> 548.23s` vs `shadow-20260413-arxiv-html-reuse`
- `cross_platform` real time regressed by `11.62%`

Because that violated the child-regression rule, the branch was repeated from
the same backup root before drawing a conclusion.

Repeat replay:

```bash
ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4 uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --output-dir bench-out/shadow-20260413-html-maintext-p4-r2
```

Formal comparison against the real control:

```bash
uv run python scripts/compare_shadow_day_runs.py \
  --baseline bench-out/shadow-20260413-control \
  --candidate bench-out/shadow-20260413-html-maintext-p4-r2 \
  --output-dir bench-out/compare-shadow-20260413-control-vs-html-maintext-p4-r2
```

### Accepted result

The repeat cleared the acceptance bar against the shadow control.

#### Fleet result

| run | real_seconds_total |
| --- | ---: |
| shadow control | 706.11 |
| html maintext p4 repeat | 533.62 |

Fleet wall-time delta: `-172.49s` (`24.43%` faster).

#### Dominant-step result

| step | baseline_ms | candidate_ms | delta_ms | improvement |
| --- | ---: | ---: | ---: | ---: |
| ingest | 265,426 | 80,351 | -185,075 | 69.73% |
| translate | 137,195 | 138,222 | +1,027 | -0.75% |
| analyze | 99,556 | 107,752 | +8,196 | -8.23% |
| ideas:day | 82,168 | 112,469 | +30,301 | -36.88% |
| trends:day | 87,135 | 87,870 | +735 | -0.84% |
| site-build | 14,457 | 2,496 | -11,961 | 82.74% |

The win is first-order `ingest` time, not translation or trends time.

#### Child-level result

| child | control_s | candidate_s | delta_s | improvement |
| --- | ---: | ---: | ---: | ---: |
| `cross_platform` | 110.23 | 89.18 | -21.05 | 19.10% |
| `embodied_ai` | 245.57 | 226.01 | -19.56 | 7.97% |
| `software_intelligence` | 350.31 | 218.43 | -131.88 | 37.65% |

No child regressed in the accepted repeat, and all terminal states remained
`succeeded_clean`.

#### Supporting metric result

The new metrics showed that the branch was actually exercising the intended
parallel path in the two heavy children:

| child | html items | max workers | enrich duration delta |
| --- | ---: | ---: | ---: |
| `embodied_ai` | `50` | `4` | `58,881ms -> 18,071ms` |
| `software_intelligence` | `50` | `4` | `158,072ms -> 40,652ms` |

The HN fetch counters did **not** drop in the same way:

| child | `pipeline.enrich.source.hn.fetch_ms_sum` |
| --- | --- |
| `embodied_ai` | `31,837ms -> 35,650ms` |
| `software_intelligence` | `31,924ms -> 33,942ms` |

This matters because it shows the measured win came from overlapping existing
maintext work, not from skipping fetches through reuse.

### Confounder control: project idempotence

This continuation explicitly avoids attributing cross-run idempotent reuse to
the candidate branch.

What was controlled:

- every treatment replay restored from the same live baseline backup root
- the formal comparison baseline remained `shadow-20260413-control`
- the accepted branch was compared to that same control, not to the live run

What was intentionally **not** removed:

- reuse that is already part of the restored snapshot's normal runtime behavior
- within-run caching or step-local reuse that exists equally inside control and
  candidate

So the accepted `html-maintext` result excludes the usual "second run got faster
because state was already warm" explanation. The control and candidate both
started from the same backup snapshot. The causal evidence also points away from
idempotent skipping:

- `pipeline.enrich.parallel.html_maintext.items_total` moved from `0` to `50`
- `pipeline.enrich.duration_ms` collapsed in the heavy children
- `pipeline.enrich.source.hn.fetch_ms_sum` stayed roughly flat instead of
  falling

That pattern matches concurrency overlap, not pre-existing idempotent reuse.

## Updated Recommendation Order

Based on the accepted repeat, the measured order is now:

1. promote the HTML maintext enrich parallelism branch as the top quantified
   time-saver for `2026-04-13`
2. keep translation parallelism behind a guard until the `empty_content`
   instability is understood
3. only reopen trends/ideas after the enrich win is accounted for, because the
   next largest remaining costs are now mostly LLM-side variance rather than
   fetch/extract wall time

## Continuation Update 3

The next trends/ideas pass focused on deciding whether retrieval-loop reuse was
still a useful branch after the accepted enrich win.

### DFX addition

`trends` debug payloads already contained `raw_tool_trace`, but the `ideas`
debug payload only exposed aggregate tool counts. This made it impossible to
distinguish repeated requests from merely high tool volume.

The DFX gap was closed by adding `raw_tool_trace` to the `ideas` debug payload.
This is a debug artifact only; it does not add high-cardinality metrics or
change default CLI behavior.

### Trace sampling command

A single-child diagnostic replay was run against the accepted enrich setting:

```bash
ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4 \
WRITE_DEBUG_ARTIFACTS=true \
ARTIFACTS_DIR=/Users/chenmohan/gits/recoleta/bench-out/shadow-20260413-trace-si-html-p4/artifacts \
uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --instances software_intelligence \
  --output-dir bench-out/shadow-20260413-trace-si-html-p4
```

This run succeeded with `real_seconds_total=223.65s`. It is not a formal
performance comparison because debug artifact writing was enabled.

Key `software_intelligence` metrics:

| metric | value |
| --- | ---: |
| `trends:day` | `29,878ms` |
| `ideas:day` | `25,609ms` |
| `pipeline.trends.tool_calls_total` | `8` |
| `pipeline.trends.tool.get_doc_bundle.calls_total` | `6` |
| `pipeline.trends.tool.search_hybrid.calls_total` | `1` |
| `pipeline.trends.pass.ideas.tool_calls_total` | `7` |
| `pipeline.trends.pass.ideas.tool.get_doc_bundle.calls_total` | `5` |
| `pipeline.trends.pass.ideas.tool.search_hybrid.calls_total` | `1` |

Trace interpretation:

- within each pass, there were no repeated `get_doc_bundle` calls
- across `trends` and `ideas`, four doc ids repeated
- the repeated cross-pass bundle requests used different parameters
  (`700 chars / 2 chunks` in trends vs `900 chars / 3 chunks` in ideas)
- therefore exact tool-result caching is not a high-ROI next branch for this
  window

### Rejected snapshot-first pilot

A narrow prompt-gating candidate was tested locally: tell `ideas` to use the
trend snapshot evidence first and only call tools for missing or contradictory
evidence.

Pilot command:

```bash
ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4 \
TRENDS_IDEAS_SNAPSHOT_FIRST=true \
WRITE_DEBUG_ARTIFACTS=true \
ARTIFACTS_DIR=/Users/chenmohan/gits/recoleta/bench-out/shadow-20260413-ideas-snapshot-first-si/artifacts \
uv run python scripts/bench_shadow_day_run.py \
  --manifest /Users/chenmohan/Playground/recoleta-playground/fleet/fleet.yaml \
  --date 2026-04-13 \
  --backup-root bench-out/e2e-20260413-baseline/backups \
  --instances software_intelligence \
  --output-dir bench-out/shadow-20260413-ideas-snapshot-first-si
```

Pilot result:

| metric | trace control | snapshot-first pilot | delta |
| --- | ---: | ---: | ---: |
| `real_seconds_total` | `223.65s` | `210.66s` | `-12.99s` |
| `ideas:day` | `25,609ms` | `27,059ms` | `+1,450ms` |
| `pipeline.trends.pass.ideas.tool_calls_total` | `7` | `5` | `-2` |
| `pipeline.trends.pass.ideas.tool.search_hybrid.calls_total` | `1` | `0` | `-1` |
| `pipeline.trends.pass.ideas.tool.get_doc_bundle.calls_total` | `5` | `4` | `-1` |
| `pipeline.trends.pass.ideas.prompt_chars` | `8,919` | `10,575` | `+1,656` |

The pilot reduced tool count but did not improve the target `ideas:day` step.
The apparent whole-child wall-time improvement came from unrelated variance in
`ingest` and `translate`, not from the targeted ideas step.

Verdict: **do not promote** and do not run this branch fleet-wide. The
experimental prompt-gating code was rolled back; only the `ideas` raw tool trace
DFX remains.

## Current Next Step

After this continuation, the experiment should not spend more time on generic
trends/ideas retrieval reuse for this day window. The next plausible work is:

1. promote or productize the accepted HTML maintext enrich parallelism
2. investigate translation `empty_content` stability before trying more
   translation concurrency
3. use the new `ideas` raw tool trace only when a future trends/ideas run shows
   repeated exact tool requests or a clear LLM-loop pathology
