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

