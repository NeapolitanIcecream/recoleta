# [Huldra](https://github.com/NeapolitanIcecream/huldra) arXiv Pool Adapter Proposal

Status: Proposed

Date: 2026-05-21

Related:

- `docs/design/arxiv-paper-pool.md`
- `docs/design/arxiv-pool-worker.md`
- `docs/design/arxiv-pool-maturity-gate.md`
- Huldra `docs/design/local-arxiv-metadata-broker.md`
- Huldra `docs/design/recoleta-compatible-arxiv-broker-proposal.md`

## Summary

Add a Recoleta adapter that can consume arXiv metadata from Huldra while
preserving Recoleta's existing pool-mode ingest semantics.

Huldra becomes the shared local arXiv metadata broker. Recoleta remains
responsible for source-pull behavior: translating workflow periods and
watermarks into submitted-date windows, enforcing readiness gates, emitting
Recoleta diagnostics, and converting metadata into `ItemDraft` rows.

The adapter should be introduced behind configuration and run alongside the
current SQLite-backed Recoleta arXiv pool until parity is proven.

## Goals

- Let Recoleta consume Huldra without reading Huldra's SQLite database.
- Preserve `SOURCES.arxiv.mode=pool` behavior:
  - no direct arXiv API calls from ingest;
  - cache-only reads during ingest;
  - no drafts emitted from immature windows by default;
  - no watermark advancement when required windows are unavailable or immature
    unless Recoleta is running with an explicit unsafe immature-window override.
- Reuse Huldra's public Python client or HTTP API rather than duplicating
  request, queue, rate-limit, or Atom parsing logic.
- Keep Recoleta's metrics, diagnostics, stats JSON, and workflow readiness
  payloads stable.
- Allow a staged rollout and rollback to the current local SQLite pool.

## Non-Goals

- Do not make Recoleta depend on Huldra internals or migrations.
- Do not move Recoleta item storage, trend generation, analyses, or publishing
  into Huldra.
- Do not introduce a second arXiv rate limiter in Recoleta for Huldra mode.
- Do not fetch PDFs, source tarballs, paper HTML, or full text through Huldra in
  this adapter.
- Do not remove the existing Recoleta arXiv pool in the first adapter PR.

## Boundary

### Huldra Owns

- upstream arXiv API fetches;
- global local rate state and cooldown;
- queueing, leases, and request deduplication;
- arXiv Atom parsing;
- metadata cache and cache integrity;
- generic submitted-date cache/maturity facts;
- safe `analysis_ready` serving mode that does not return immature papers;
- generic sync/backfill/worker commands.

### Recoleta Owns

- Recoleta settings and fleet manifest interpretation;
- mapping Recoleta queries, dates, and watermarks into Huldra requests;
- Recoleta readiness policy and workflow decisions:
  - `strict`;
  - `warn`;
  - `off`;
  - `allow_immature_windows`;
- conversion from Huldra `ArxivPaper` to Recoleta `ItemDraft`;
- Recoleta source-state watermark updates;
- Recoleta ingest diagnostics and pipeline metrics;
- workflow blocking before analysis/trends/publishing.

## Configuration

Keep the existing arXiv source mode and add a backend selector under
`ARXIV_POOL`:

```yaml
ARXIV_POOL:
  enabled: true
  backend: huldra
  huldra_base_url: http://127.0.0.1:8765
  huldra_request_timeout_seconds: 30
  huldra_wait_timeout_seconds: null
  maturity_lag_days: 1
  readiness_gate: strict
  allow_immature_windows: false

SOURCES:
  arxiv:
    enabled: true
    mode: pool
    queries:
      - cat:cs.AI AND all:agent
    max_results_per_run: 60
```

Compatibility:

- `backend: local_sqlite` keeps the current `ArxivPoolStore` path.
- `backend: huldra` ignores `ARXIV_POOL.db_path` for reads and uses Huldra's
  public API.
- `ARXIV_POOL.db_path` remains required only for `backend: local_sqlite`.
- Omitted `backend` defaults to `local_sqlite` for the first release.
- A later release may switch the default after parity evidence is collected.

Timeouts:

- `huldra_request_timeout_seconds` controls one HTTP/client request, including
  cache-only ingest reads.
- `huldra_wait_timeout_seconds` controls `sync_windows(wait=True)` and
  `backfill_windows(wait=True)`. If omitted, Recoleta derives
  `max(3600, requested_windows_total * 35)` to preserve the current local SQLite
  pool's long-running multi-window behavior. Operators with a slower Huldra
  arXiv request interval should set this explicitly.

## Adapter Contract

The adapter should call Huldra with ordinary public requests. It must not read
Huldra tables directly.

### Cache-Only Ingest Request

```json
{
  "client_id": "recoleta:embodied_ai",
  "search_query": "cat:cs.AI AND all:agent",
  "sort_by": "submittedDate",
  "sort_order": "descending",
  "start": 0,
  "max_results": 60,
  "submitted_start": "2026-05-20T00:00:00+00:00",
  "submitted_end": "2026-05-21T00:00:00+00:00",
  "cache_policy": "cache_only",
  "readiness": "analysis_ready",
  "maturity_lag_days": 1,
  "timeout_seconds": 30
}
```

Adapter interpretation:

- `status=ready` and `analysis_ready=true`: convert `papers` to `ItemDraft`.
- `status=immature` or `blocked_reason=immature_window`: record immature window,
  emit no drafts unless Recoleta explicitly allows immature windows.
- `status=cache_miss`, `failed`, `cooling_down`, or unreadable result: record
  unavailable window and emit no drafts.
- Huldra `raw_completed` should not be used in production ingest unless
  Recoleta readiness gate is explicitly `off` or `allow_immature_windows=true`.
- In default production mode, Recoleta sends `readiness=analysis_ready`; Huldra
  must return an empty `papers` list for immature windows in that mode.
- Recoleta passes its configured `ARXIV_POOL.maturity_lag_days` as
  request-level `maturity_lag_days`. This field does not affect Huldra cache
  identity; it only controls how Huldra interprets the completed window for this
  caller.
- For explicit unsafe overrides, Recoleta may send `readiness=raw_completed`
  and must record `pool_window_immature_allowed_total`. In that mode, Huldra
  immature windows follow the existing Recoleta local SQLite semantics: drafts
  may be emitted and the query watermark may advance, while diagnostics still
  show `mature=false`, `analysis_ready=false`, and the unsafe override flag.

### ItemDraft Mapping

The adapter should reuse the existing `pool_paper_to_item_draft` behavior where
possible instead of inventing a second mapping. Existing Recoleta raw metadata
keys should remain byte-shape compatible for downstream consumers; Huldra
provenance is additive.

Mapping table:

| Final `ItemDraft` field/key | Local SQLite source | Huldra source | Rule |
| --- | --- | --- | --- |
| `source` | constant | constant | Always `arxiv`. |
| `source_item_id` | `ArxivPoolPaper.arxiv_id` | `ArxivPaper.arxiv_id` | Same normalized arXiv ID string. |
| `canonical_url` | `ArxivPoolPaper.canonical_url` | `ArxivPaper.canonical_url` | Required for both backends. |
| `title` | `ArxivPoolPaper.title` | `ArxivPaper.title` | Required for both backends. |
| `authors` | `ArxivPoolPaper.authors` | `ArxivPaper.authors` | Required for both backends. |
| `published_at` | `ArxivPoolPaper.published_at` | `ArxivPaper.published_at` | Preserve existing timestamp normalization. |
| `raw_metadata.query` | window | window | Existing key, unchanged. |
| `raw_metadata.matched_queries` | window | window | Existing key, unchanged. |
| `raw_metadata.query_period_start` | window | window | Existing key, unchanged. |
| `raw_metadata.query_period_end` | window | window | Existing key, unchanged. |
| `raw_metadata.categories` | paper categories | paper categories | Existing key when present. |
| `raw_metadata.primary_category` | paper primary category | paper primary category | Existing key when present. |
| `raw_metadata.comment` | paper comment | paper comment | Existing key when present. |
| `raw_metadata.journal_ref` | raw Atom or mapped field | `ArxivPaper.journal_ref` | If added explicitly, update the shared mapper so local SQLite and Huldra behave the same. |
| `raw_metadata.doi` | raw Atom or mapped field | `ArxivPaper.doi` | If added explicitly, update the shared mapper so local SQLite and Huldra behave the same. |
| `raw_metadata.huldra_cache_key` | none | Huldra result cache key | Additive Huldra provenance; downstream code must ignore unknown raw metadata keys. |

Implementation path for result-level provenance:

- Extend `pool_paper_to_item_draft(...)` with
  `extra_raw_metadata: Mapping[str, Any] | None = None`.
- Keep local SQLite callers unchanged.
- The Huldra adapter passes `{"huldra_cache_key": readiness.cache_key}` when
  converting papers from a Huldra result.
- `extra_raw_metadata` is applied after existing mapper fields so provenance is
  explicit and tests can assert that only Huldra-owned additive keys differ.

For each Huldra paper:

- `source`: `arxiv`
- `source_item_id`: `paper.arxiv_id`
- `canonical_url`: `paper.canonical_url`
- `title`: `paper.title`
- `authors`: `paper.authors`
- `published_at`: `paper.published_at`
- `summary` or abstract field: use existing Recoleta behavior if available;
  otherwise keep abstract in metadata only.
- `raw_metadata`:
  - `query`;
  - `matched_queries`;
  - `query_period_start`;
  - `query_period_end`;
  - `categories`;
  - `primary_category`;
  - `comment`;
  - `journal_ref` and `doi` only through the shared mapper rule above;
  - additive `huldra_cache_key`.

## Backend Interface Inside Recoleta

Introduce a small protocol to keep ingest code from knowing which pool backend
is active:

```python
@dataclass(frozen=True, slots=True)
class ArxivPoolBackendReadiness:
    query_text: str
    period_start: datetime
    period_end: datetime
    max_results: int
    backend: Literal["local_sqlite", "huldra"]
    cache_status: str
    serving_status: str | None
    cache_readable: bool
    mature: bool
    analysis_ready: bool
    blocked_reason: str | None
    cache_key: str | None = None
    diagnostic: dict[str, Any] | None = None

    @property
    def unavailable(self) -> bool:
        return (
            not self.analysis_ready
            and self.blocked_reason is not None
            and self.blocked_reason != "immature_window"
        )


@dataclass(frozen=True, slots=True)
class ArxivPoolWindowPullResult:
    papers: list[ArxivPoolPaper] | None
    complete: bool
    readiness: ArxivPoolBackendReadiness


class ArxivMetadataPoolBackend(Protocol):
    def cached_papers_for_window(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolWindowPullResult: ...

    def evaluate_window_readiness(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolBackendReadiness: ...
```

The current `ArxivPoolStore` can be wrapped by `LocalSqliteArxivPoolBackend`.
The new Huldra path can be implemented as `HuldraArxivPoolBackend`.
The local SQLite wrapper should adapt the existing `ArxivPoolWindowReadiness`
into `ArxivPoolBackendReadiness`; Huldra must not fabricate local
`ArxivPoolWindowRecord` objects.

Status semantics:

- `cache_status` keeps Recoleta's existing record-status meaning. Local SQLite
  maps `ArxivPoolWindowReadiness.status` into this field. Huldra maps raw cache
  state such as `completed`, `missing`, `failed`, `rate_limited`, `queued`, or
  `skipped`.
- For Huldra cache-only reads, derive `cache_status` from cache facts rather than
  copying serving status: `cache_readable=true` maps to `completed`,
  `status=cache_miss` maps to `missing`, `status=cooling_down` maps to
  `rate_limited`, and `status=failed` maps to `failed`.
- `serving_status` is backend-specific serving interpretation. Local SQLite can
  set it to `None`; Huldra sets it from response values such as `ready`,
  `immature`, `cache_miss`, `cooling_down`, or `timeout`.
- Recoleta diagnostics should keep the existing `record_status` key populated
  from `cache_status`. Huldra-specific serving state should be additive, for
  example `backend`, `huldra_status`, and `huldra_cache_key`.

Status mapping:

| Huldra raw/serving condition | Recoleta `cache_status` | Recoleta `blocked_reason` | Metric effect | Readiness behavior |
| --- | --- | --- | --- | --- |
| `cache_readable=true`, `analysis_ready=true` | `completed` | `null` | `pool_window_analysis_ready_total` | Emit papers. |
| `cache_readable=true`, `mature=false` | `completed` | `immature_window` | `pool_window_immature_total`; plus `pool_window_immature_allowed_total` when unsafe override is active | Default emits no papers; unsafe `off` or `allow_immature_windows=true` may emit papers. |
| `status=cache_miss` | `missing` | `missing_window` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| `status=queued` | `queued` | `queued_window` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| `status=cooling_down` | `rate_limited` | `rate_limited_window` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| `status=failed` | `failed` | `failed_window` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| `status=timeout` | `timeout` | `timeout_window` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| `stale=true`, `analysis_ready=true` | `completed` | `null` | `pool_window_analysis_ready_total` plus additive stale diagnostic | Emit papers; stale is only provenance. |
| maintenance `raw_cache_status=skipped` | `skipped` | `skipped_window` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| malformed response | `failed` | `malformed_huldra_response` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |
| unreachable Huldra endpoint | `failed` | `huldra_unreachable` | `pool_window_unavailable_total` | Emit no papers and preserve watermark. |

Do not push Huldra-specific response parsing into `_ArxivPoolPuller`. The puller
should consume the backend protocol and keep the existing watermark and
diagnostic logic.

### Injection Path

Use explicit backend injection rather than threading Huldra HTTP settings through
source request dataclasses:

1. `IngestStage._arxiv_pull()` builds `ArxivMetadataPoolBackend` from settings
   when `SOURCES.arxiv.mode=pool`.
2. Keep the existing tuple-based source runner. `_arxiv_pull()` returns
   `(source_name, fn, source_request, legacy_kwargs)` and adds
   `pool_backend=backend` to `legacy_kwargs`.
3. `_pull_source()` already calls `_invoke_source_pull(fn, request=source_request,
   **legacy_kwargs)`; no Huldra fields should be added to `ArxivPullRequest`.
4. `sources.fetch_arxiv_drafts(...)` and
   `source_pullers.pull_arxiv_drafts(...)` accept an optional keyword-only
   `pool_backend`.
5. `_ArxivPoolPuller` receives the backend in its constructor and uses it for
   cached window reads and readiness evaluation.
6. Legacy direct callers can omit `pool_backend`; pool mode may build a local
   SQLite backend from `pool_db_path` as a compatibility fallback, but pipeline
   code should use explicit injection.

## Workflow Readiness

Recoleta workflow readiness remains authoritative.

### Backend Descriptor

Workflow readiness and fleet pre-sync should plan against a backend descriptor,
not only a SQLite path:

```python
@dataclass(frozen=True, slots=True)
class ArxivPoolBackendDescriptor:
    kind: Literal["local_sqlite", "huldra"]
    identity: str
```

Descriptor identity rules:

- `local_sqlite`: normalized resolved `ARXIV_POOL.db_path`.
- `huldra`: normalized `ARXIV_POOL.huldra_base_url`.

First release fleet rules:

- fail/block mixed pool backends in one fleet run with a machine-readable
  `mixed_arxiv_pool_backends` reason;
- fail/block multiple Huldra endpoints in one fleet run with
  `multiple_huldra_endpoints`;
- fail/block multiple local SQLite DB paths in one fleet run with
  `multiple_pool_db_paths`;
- keep mixed direct arXiv and pool-mode arXiv behavior unchanged: pre-sync and
  readiness planning are skipped when direct arXiv sources are present.

For each required window, the Huldra backend should return a Recoleta-shaped
readiness object:

- `cache_status`;
- `serving_status`;
- `cache_readable`;
- `mature`;
- `analysis_ready`;
- `blocked_reason`.

Recoleta then applies existing rules:

- `strict`: block before analysis if any required window is not analysis-ready.
- `warn`: continue but do not ingest immature/unavailable arXiv windows.
- `off`: allow raw completed/immature windows only when explicitly configured.

## Sync and Backfill

For `backend=huldra`, Recoleta should not implement another arXiv fetcher.

Preferred path:

- call `HuldraClient.sync_windows(...)` and
  `HuldraClient.backfill_windows(...)`, or their HTTP equivalents
  `POST /v1/sync` and `POST /v1/backfill`;
- use `wait=True` for Recoleta pre-sync so Huldra drains the requested windows in
  the calling process without requiring an external worker;
- Huldra enqueues/fetches under its limiter;
- Recoleta reads readiness and results through cache-only requests.

Recoleta must not shell out to `huldra` for normal operation. The Huldra CLI is
for humans and supervisors; the adapter should use typed Python or HTTP
interfaces.

## Command Surface

Every Recoleta `arxiv-pool` command needs an explicit Huldra-mode behavior so the
old local SQLite worker path cannot run by accident.

For `backend=huldra`:

- `recoleta arxiv-pool sync`: delegate to `HuldraClient.sync_windows(...)` with
  generated submitted-date window requests and return the existing Recoleta sync
  JSON shape. Huldra `requested_total` maps to
  `requested_windows_total`. If `--force` is requested before Huldra exposes a
  public force-refresh contract, reject with reason
  `huldra_force_refresh_unsupported` rather than silently ignoring it.
- `recoleta arxiv-pool backfill`: delegate to
  `HuldraClient.backfill_windows(...)` and return the existing Recoleta sync JSON
  shape. The same `--force` rule applies.
- `recoleta arxiv-pool worker`: reject with `status=skipped` or an equivalent
  non-zero CLI error carrying reason `huldra_backend_uses_huldra_worker`. It must
  not instantiate `ArxivPoolWorker`, `ArxivPoolStore`, or a direct arXiv client.
- `recoleta inspect arxiv-pool freshness`: narrow Huldra-mode semantics to
  configured-window readiness, because Huldra V1 does not expose arbitrary recent
  cache listing. The JSON payload should include `backend=huldra`,
  `huldra_base_url`, `inspect_scope=configured_windows`, `pool_db_path=null`,
  `cache_listing_supported=false`, maturity policy, and per-configured-window
  readiness diagnostics.
  Window selection must be deterministic: use the configured arXiv source
  queries and `max_results_per_run`, walk UTC days from the current UTC date
  backwards, and stop after the existing `--limit` number of windows. The command
  does not add a new workflow-period argument in the first adapter PR.
- `recoleta admin arxiv-pool gc`: reject with reason
  `huldra_backend_gc_not_supported` unless a future Huldra public GC endpoint is
  added. It must not prune Recoleta's local SQLite pool by default in Huldra mode.

## Implementation Runbook

This runbook is meant for a local Codex agent. All implementation work below
must happen in one Recoleta PR. Each numbered implementation step ends with
exactly one commit after that step's checks pass.

Do not start this PR until the Huldra PR from
`docs/design/recoleta-compatible-arxiv-broker-proposal.md` has either shipped or
is available as a pinned dependency/source checkout for local testing. The
available Huldra surface must include request-level `maturity_lag_days`,
`cache_readable`, `mature`, `ArxivResult.serving_mode`, additive-field-compatible
response parsing, `HuldraClient.sync_windows(...)`,
`HuldraClient.backfill_windows(...)`, `POST /v1/sync`, `POST /v1/backfill`, and
maintenance `wait_timeout_seconds` plus per-request `raw_cache_status` /
`serving_status`.

### Step 0: Prepare

```bash
cd /path/to/recoleta
git checkout -b codex/huldra-arxiv-pool-adapter
uv sync --group dev
uv run ruff check .
uv run pyright
uv run pytest tests/test_arxiv_pool.py -q
```

Do not commit Step 0 unless branch setup changes repository files.

### Step 1: Add Configuration and Dependency Surface

Implement:

- `ARXIV_POOL.backend` with values `local_sqlite` and `huldra`;
- `ARXIV_POOL.huldra_base_url`;
- `ARXIV_POOL.huldra_request_timeout_seconds`;
- `ARXIV_POOL.huldra_wait_timeout_seconds`;
- validation that `SOURCES.arxiv.mode=pool` with `backend=huldra` has a Huldra
  endpoint configured;
- validation that `ARXIV_POOL.db_path` is required for `backend=local_sqlite`
  and not required for `backend=huldra`;
- pinned Huldra client dependency according to the project's dependency policy;
- `tests/test_huldra_public_contract.py` that imports the pinned Huldra package
  and asserts the required public fields and methods exist.

Use the typed Huldra client/models when available. Plain `httpx` should only be
used inside a small fallback wrapper if packaging constraints make direct import
impossible, and the public-contract test must still validate the HTTP schema.
Step 1 must fail fast if the installed Huldra package or source checkout does
not expose the complete contract. Recoleta must not add fallback logic that
guesses missing Huldra fields.

Tests:

- settings load huldra backend;
- settings separate Huldra request timeout from Huldra maintenance wait timeout;
- huldra backend works without `ARXIV_POOL.db_path`;
- local SQLite backend still requires `ARXIV_POOL.db_path`;
- invalid backend is rejected;
- existing local SQLite pool configs keep working;
- pinned Huldra exposes `ArxivRequest.maturity_lag_days`,
  `ArxivResult.cache_readable`, `ArxivResult.mature`,
  `ArxivResult.serving_mode`, additive-field-compatible response parsing,
  `HuldraClient.sync_windows`, `HuldraClient.backfill_windows`,
  `wait_timeout_seconds`, and maintenance per-request `raw_cache_status` /
  `serving_status`.

Checks:

```bash
uv run pytest tests/test_recoleta_specs_settings.py tests/test_huldra_public_contract.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "feat(arxiv): add huldra pool settings"
```

### Step 2: Introduce the Backend Protocol

Implement:

- `ArxivMetadataPoolBackend` protocol;
- `ArxivPoolBackendReadiness` backend-neutral DTO;
- split `cache_status` from `serving_status`;
- `LocalSqliteArxivPoolBackend` wrapper around current `ArxivPoolStore`;
- `ArxivPoolBackendDescriptor` with local SQLite and Huldra identities;
- backend factory from settings;
- no behavior change in `_ArxivPoolPuller` yet.

Tests:

- local backend returns the same readiness and cached papers as current store;
- backend factory picks local SQLite by default;
- local backend populates `cache_status` from the existing readiness status and
  leaves `serving_status=None`;
- backend descriptor blocks mixed backends, mixed Huldra endpoints, and mixed
  local SQLite DB paths in fleet planning with machine-readable reasons.

Checks:

```bash
uv run pytest tests/test_arxiv_pool.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "refactor(arxiv): isolate pool backend interface"
```

### Step 3: Implement Huldra Backend Adapter

Implement:

- `HuldraArxivPoolBackend`;
- typed request construction for submitted-date windows;
- request-level `maturity_lag_days` propagation from Recoleta settings;
- request construction that sends the base arXiv query in `search_query` and
  date bounds only through `submitted_start` / `submitted_end`;
- cache-only `readiness=analysis_ready` requests by default;
- mapping from Huldra raw cache state to `cache_status`, and from Huldra
  serving `status` to additive `serving_status` diagnostics;
- mapping from Huldra `cache_readable`, `mature`, `analysis_ready`, and
  `blocked_reason` to Recoleta readiness fields;
- `pool_paper_to_item_draft(..., extra_raw_metadata=...)` support for additive
  Huldra provenance;
- conversion from Huldra papers to existing `ArxivPoolPaper`-compatible objects
  or directly reusable draft conversion inputs.

Tests should use a fake Huldra client or `respx`; do not require a live Huldra
daemon.

Test cases:

- ready Huldra result returns papers;
- Huldra request construction does not duplicate submitted-date clauses inside
  `search_query`;
- immature `analysis_ready` result records blocked reason and no papers;
- explicit unsafe override sends `raw_completed`, emits papers, and records
  `pool_window_immature_allowed_total` while preserving `mature=false` and
  `analysis_ready=false` in diagnostics;
- `readiness_gate=off` and `allow_immature_windows=true` each send
  `raw_completed`; default strict/warn send `analysis_ready`;
- cache miss/rate limited/failed result is unavailable;
- malformed or unreachable Huldra response is unavailable with a structured
  diagnostic, not a direct arXiv fallback.

Checks:

```bash
uv run pytest tests/test_arxiv_pool_huldra_adapter.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "feat(arxiv): add huldra pool backend"
```

### Step 4: Route Pool-Mode Ingest Through the Backend

Implement:

- `IngestStage._arxiv_pull()` builds and injects `ArxivMetadataPoolBackend`;
- `sources.fetch_arxiv_drafts(...)` and
  `source_pullers.pull_arxiv_drafts(...)` accept optional keyword-only
  `pool_backend`;
- `IngestStage._arxiv_pull()` passes the backend through `legacy_kwargs` so the
  current `_invoke_source_pull(..., **legacy_kwargs)` path receives it;
- `_ArxivPoolPuller` consumes the injected `ArxivMetadataPoolBackend`;
- local SQLite behavior remains unchanged;
- Huldra backend preserves:
  - no direct upstream arXiv calls;
  - no immature drafts unless explicitly allowed;
  - no watermark advancement when any required window is unavailable, or immature
    while unsafe overrides are disabled;
  - current `off` / `allow_immature_windows=true` behavior where explicitly
    allowed immature drafts may advance the query watermark;
  - existing metrics and diagnostics names.

Regression tests:

- existing `tests/test_arxiv_pool.py` still passes;
- `IngestStage` injects a fake Huldra backend through the tuple/`legacy_kwargs`
  path and does not instantiate `ArxivPoolStore` for `backend=huldra`;
- `pool_window_unavailable_total` and `pool_window_immature_total` are emitted
  for Huldra backend;
- watermark is preserved for immature Huldra windows by default and for
  unavailable Huldra windows always;
- unsafe override emits immature Huldra drafts and may advance the query
  watermark, matching local SQLite semantics;
- `readiness_gate=off` and `allow_immature_windows=true` are the only paths that
  emit immature drafts.

Checks:

```bash
uv run pytest tests/test_arxiv_pool.py tests/test_recoleta_specs_ingest.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "feat(arxiv): use huldra backend for pool ingest"
```

### Step 5: Wire Workflow Readiness and CLI Output

Implement:

- readiness plan evaluation uses `ArxivPoolBackendDescriptor` and can evaluate
  local SQLite or Huldra backends;
- `recoleta inspect arxiv-pool freshness` reports configured-window readiness for
  Huldra mode with backend, Huldra endpoint, inspect scope, and
  `cache_listing_supported=false`;
- `recoleta arxiv-pool worker` and `recoleta admin arxiv-pool gc` do not touch
  local SQLite pool internals in Huldra mode and return stable reasons;
- fleet planning blocks mixed pool backends and mixed Huldra endpoints with
  machine-readable reasons;
- fleet/day/week/month workflow blocking behavior remains unchanged in strict
  mode;
- warn/off behavior remains unchanged.

Tests:

- strict mode blocks on Huldra immature window;
- warn mode continues but reports blocked windows;
- inspect JSON includes backend, maturity policy, and per-window diagnostics;
- inspect JSON documents Huldra-mode `configured_windows` scope rather than
  pretending to list arbitrary recent Huldra cache entries;
- inspect JSON uses configured arXiv queries and current-UTC-day lookback windows
  capped by the existing `--limit` option;
- Huldra-mode worker returns `huldra_backend_uses_huldra_worker`;
- Huldra-mode GC returns `huldra_backend_gc_not_supported`;
- mixed local SQLite/Huldra fleet configs block with
  `mixed_arxiv_pool_backends`;
- multiple Huldra endpoints block with `multiple_huldra_endpoints`;
- local SQLite readiness tests still pass.

Checks:

```bash
uv run pytest tests/test_arxiv_pool.py tests/test_recoleta_specs_trends.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "feat(arxiv): evaluate huldra pool readiness"
```

### Step 6: Integrate Sync and Fleet Pre-Sync

For `backend=huldra`:

- fleet pre-sync calls `HuldraClient.sync_windows(...)` instead of Recoleta's
  local SQLite `ArxivPoolSync`;
- one-shot `recoleta arxiv-pool sync/backfill` delegates to
  `HuldraClient.sync_windows(...)` or `HuldraClient.backfill_windows(...)`;
- Huldra-mode sync/backfill with unsupported `--force` returns
  `huldra_force_refresh_unsupported`;
- Recoleta uses `wait=True` for deterministic pre-sync before cache-only child
  ingest and passes a maintenance wait timeout from
  `ARXIV_POOL.huldra_wait_timeout_seconds` or the derived
  `max(3600, requested_windows_total * 35)` fallback;
- Huldra maintenance counters are copied into Recoleta's existing pre-sync JSON
  fields without before/after global-status inference;
- direct upstream arXiv calls remain impossible from Recoleta in Huldra mode.

Tests:

- fleet pre-sync calls fake Huldra sync once for shared windows;
- multiple child instances share deduped Huldra windows;
- 429/cooldown result is reported without fallback to direct mode;
- pre-sync passes explicit `huldra_wait_timeout_seconds` when configured and
  otherwise uses `max(3600, requested_windows_total * 35)`;
- Huldra-mode sync/backfill with unsupported `--force` returns
  `huldra_force_refresh_unsupported`;
- no-direct-fetch guards cover ingest, fleet pre-sync, one-shot sync/backfill,
  worker, GC, and inspect freshness in Huldra mode;
- Recoleta exposes Huldra `requested_total` as `requested_windows_total` and
  carries through `completed_windows_total`, `upstream_requests_total`,
  `upstream_429_total`, `cache_hit_total`, `cache_miss_total`,
  `rate_limited_windows_total`, `skipped_windows_total`,
  `failed_windows_total`, and `papers_total` in the same shape as local SQLite
  pool pre-sync.

Checks:

```bash
uv run pytest tests/test_arxiv_pool.py tests/test_recoleta_specs_ingest.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "feat(arxiv): delegate pool sync to huldra"
```

### Step 7: Parity Test and Documentation

Add a parity test module that compares local SQLite pool and Huldra backend on
the same fixture windows:

- same paper IDs emitted for ready windows;
- same unavailable/immature metrics;
- same watermark behavior;
- same workflow readiness summary;
- same existing `ItemDraft.raw_metadata` keys for local SQLite and Huldra ready
  windows, with `huldra_cache_key` treated as additive provenance.

Update docs:

- `docs/design/arxiv-paper-pool.md` with the Huldra backend option;
- CLI or guide docs with optional Huldra daemon/worker setup for continuous
  warming, noting that deterministic Recoleta pre-sync uses `wait=True` and does
  not require an external worker;
- migration notes explaining rollback to `backend=local_sqlite`.

Checks:

```bash
uv run pytest tests/test_arxiv_pool.py tests/test_arxiv_pool_huldra_adapter.py -q
uv run ruff check .
uv run pyright
```

Commit:

```bash
git add .
git commit -m "docs(arxiv): document huldra pool adapter"
```

### Step 8: Full PR Verification

Before opening the PR:

```bash
uv run ruff check .
uv run pyright
uv run pytest
uv run recoleta --help
git log --oneline --decorate -n 12
```

PR checklist:

- The PR contains all implementation commits from this runbook.
- Each step maps to one commit.
- The PR description includes the commands run.
- The PR explains the pinned Huldra version or source checkout used for tests.
- The PR includes rollback instructions: set `ARXIV_POOL.backend=local_sqlite`.
- The PR does not change Huldra code.

## Acceptance Criteria

- Recoleta can ingest arXiv pool windows from Huldra without direct arXiv API
  calls.
- Recoleta has a public-contract test that fails fast if the pinned Huldra
  client/model surface is missing required fields or methods.
- Recoleta emits the same core `ItemDraft` fields and existing
  `ItemDraft.raw_metadata` keys for ready Huldra windows as for the current local
  SQLite pool, with additive Huldra provenance allowed.
- Recoleta does not emit immature Huldra windows in default production mode.
- Recoleta unsafe override can consume raw completed immature Huldra windows
  while diagnostics still report `mature=false`, `analysis_ready=false`, and
  `pool_window_immature_allowed_total`.
- Recoleta does not advance arXiv watermarks when Huldra windows are missing,
  rate-limited, failed, or immature unless an explicit unsafe immature-window
  override is enabled.
- Recoleta preserves existing `off` / `allow_immature_windows=true` semantics for
  unsafe immature ingest, including possible watermark advancement and visible
  diagnostics.
- Recoleta diagnostics keep `record_status` semantics stable via `cache_status`
  and expose Huldra serving state only as additive diagnostics.
- Recoleta defines Huldra-mode behavior for sync, backfill, worker, inspect
  freshness, and GC; none of those paths accidentally instantiates the local
  SQLite worker/store in Huldra mode.
- Huldra-mode inspect freshness reports configured-window readiness rather than
  claiming arbitrary recent-cache listing support.
- Recoleta fleet planning rejects mixed pool backends and mixed Huldra endpoints
  in the first release with machine-readable reasons.
- Recoleta Huldra pre-sync uses `wait=True` and does not require an external
  Huldra worker for deterministic fleet pre-sync.
- Existing arXiv pool tests pass for the local SQLite backend.
- New Huldra adapter tests pass without a live network or live Huldra daemon.
- Fleet readiness and strict blocking semantics remain unchanged.
- `uv run ruff check .`, `uv run pyright`, and `uv run pytest` pass.

## Rollout Plan

1. Ship Huldra broker compatibility changes.
2. Add Recoleta adapter behind `ARXIV_POOL.backend=huldra`.
3. Run local SQLite pool and Huldra backend against the same fixture windows in
   tests.
4. Run one real local fleet in warn mode with Huldra and compare paper IDs,
   metrics, and watermarks against local SQLite pool output.
5. Switch selected fleet configs to `backend=huldra`.
6. Keep `backend=local_sqlite` as rollback until at least one full weekly cycle
   is clean.
