# Instance-first Breaking Refactor And DB Split Plan

Date: 2026-03-25

Status: Landed for current deployment cutover; product de-migration decision recorded and migration-tooling follow-up intentionally dropped

## Executive Summary

Yes, Recoleta can move from `topic_streams` to an instance-first model with a
single operator surface that runs multiple isolated instances.

This should be treated as a deliberate breaking refactor plus an explicit data
migration, not as a startup-safe schema bump.

Recommendation:

- hard-delete `topic_streams` from the product/runtime surface
- introduce a fleet/portfolio layer that runs multiple full instances
- split the current shared DB into one DB per instance
- archive mixed operational history instead of trying to preserve it verbatim

The key constraint is not data size. The current main DB is moderate and
tractable. The real constraint is semantics: stream-scoped historical content
can be split cleanly, but source pull state and old run history cannot be
derived from DB scope alone.

## Current Deployment Closure Note

Implementation note as of 2026-03-28:

- for the active playground deployment, this refactor is considered complete for
  the purpose of future incremental operation
- the fleet cutover is done and the runtime now runs from child instance configs
  plus child instance DBs
- the live child configs were hand-cleaned so each instance keeps only its own
  arXiv query, while `hn` and `hf_daily` remain enabled in both children by
  design
- matching stale per-query `source_pull_states` were removed from each child DB
  so future incremental pulls follow the live child config
- historical migrated user-facing rows were intentionally left in place; they
  may remain duplicated across child DBs and that is accepted for this
  deployment

Therefore the remaining work in this plan should be read as product/tooling
hardening, migration auditability, or optional cleanup work. It is no longer a
blocker for the current deployment as long as future incremental ingestion and
publish flows continue to run from the cleaned child configs.

## De-migration Decision Note

Decision recorded as of 2026-03-28:

- the one-time migration and manual child-config cleanup performed for the live
  playground deployment are considered sufficient
- Recoleta will not continue productizing or maintaining in-tree migration
  tooling for the old shared `topic_streams` world
- the runtime and CLI should expose only the instance-first model
- configs that still contain `TOPIC_STREAMS` / `topic_streams` are treated as
  unsupported input and should fail fast without migration guidance
- historical migration plans, runbooks, backups, and old git history remain the
  recovery boundary; they are not a promise of future product support

As a result, the migration-tooling hardening items elsewhere in this document
should now be read as superseded historical context unless a future plan
explicitly revives productized migration support.

## Goals

- replace `topic_streams` with a true instance boundary
- preserve a unified operator surface for one deployment running many radars
- make state ownership obvious: one DB and one lease per instance
- migrate valuable historical user-facing data out of the current shared DB
- keep the migration auditable, reversible, and explicit

## Non-goals

- preserving backward compatibility with `TOPIC_STREAMS`
- automatic startup migration of old shared-stream DBs
- perfectly reconstructing mixed historical operational telemetry per instance
- retaining shared mutable state across instances after the cutover
- solving cross-instance deduplication or shared fetch caching in the same
  change

## Why This Is The Right Break

The current `topic_streams` model was intentionally designed as:

- shared ingest/enrich state
- isolated analyze/publish/trends scopes

That design is now the mismatch.

The current implementation only lets a stream override a narrow downstream
subset of settings, not the full instance behavior. In practice this means
`topic_streams` cannot express genuinely heterogeneous radars such as:

- blog-only vs arXiv-only
- different source query sets
- different triage/trend policies
- different localization or output trees
- different future model/provider choices

At the same time, the stream abstraction has already leaked deeply into storage,
repair flows, trend generation, site rendering, billing, and tests.

Current code inventory:

- `62` files in `recoleta/`, `tests/`, and `docs/` reference stream/scope
  behavior directly
- the main hotspots are `recoleta/config.py`, `recoleta/pipeline/service.py`,
  `recoleta/storage/*`, `recoleta/site.py`, and the stream-specific spec suite

This means the architecture should stop pretending that a stream is a light
configuration convenience. It is a real tenancy boundary, and tenancy
boundaries belong at the instance/workspace layer.

## Compatibility Stance

This refactor should be intentionally strict.

After the break lands:

- single-instance configs without `TOPIC_STREAMS` continue to work with the
  existing `recoleta ...` command surface
- configs that still contain `TOPIC_STREAMS` must fail fast with an explicit
  migration-required error
- legacy commands such as `repair streams` should fail with an operator-facing
  replacement message rather than silently doing nothing
- the migration command is the only supported path from the old shared-stream
  model to the new instance-first model

Important sequencing rule:

- the runtime may only start rejecting `TOPIC_STREAMS` after a frozen read-only
  legacy migration reader exists in-tree

## Legacy Migration Boundary

The migration toolchain cannot depend on the post-refactor runtime still being
able to parse old configs.

Therefore the migration command must ship with a deliberately frozen, read-only
compatibility layer for the old world.

This layer should be separate from the new primary runtime and should cover at
least:

- old `TOPIC_STREAMS` parsing
- old stream-name normalization
- old source-assignment interpretation
- old DB schema version recognition needed by the migrator

Design rule:

- new runtime: free to reject old configs
- migration reader: permanently responsible for reading old configs and old DBs
  for the purpose of one-way migration

## Recommended Target Model

### 1. Make instance the only execution boundary

One instance should own:

- one full `Settings` object
- one SQLite DB
- one workspace lease
- one Markdown output root
- one LanceDB root
- one artifacts root
- one source config
- one analyze/publish/trends/translation history

No operational state is shared across instances.

### 2. Add a fleet layer above instances

The unified operator surface should move up one level:

- one fleet manifest references multiple instance configs
- `fleet run day|week|month|deploy` loops child instances
- fleet-level output is an aggregate summary, not shared pipeline state

This preserves the “one deployment, many radars” UX without preserving shared
mutable state.

Recommended command model:

- keep existing single-instance commands unchanged for child instances
- add a fleet wrapper namespace rather than teaching every stage command about
  multi-instance fan-out

Example shape:

- `recoleta run day|week|month|deploy` for one instance
- `recoleta fleet run day|week|month|deploy` for many instances
- `recoleta fleet site build` for aggregate presentation only
- `recoleta admin migrate topic-streams-to-instances` for the one-time split

### 3. Move aggregation to presentation/orchestration, not storage

Things that should stay aggregated:

- operator entry points
- summary tables
- aggregate site/home page
- aggregate billing/reporting

Things that should not stay aggregated:

- item state machines
- analysis state
- trend/idea document state
- source pull state
- repair semantics

## Target Config Model

### Single-instance config

The child-instance config should stay close to the current `Settings` model.

In practical terms:

- keep `TOPICS`
- remove `TOPIC_STREAMS`
- keep one `RECOLETA_DB_PATH`
- keep one `MARKDOWN_OUTPUT_DIR`
- keep one `RAG_LANCEDB_DIR`
- keep one scheduler/workflow policy
- allow full per-instance source configuration

This minimizes churn for the core runtime.

Migration rule:

- generated child configs must materialize every path-bearing setting that would
  otherwise collapse back to a shared default across instances

At minimum this includes:

- `RECOLETA_DB_PATH`
- `MARKDOWN_OUTPUT_DIR`
- `RAG_LANCEDB_DIR`
- `ARTIFACTS_DIR` when used
- `OBSIDIAN_BASE_FOLDER` when multiple instances share one vault

### Fleet manifest

The new top-level aggregation file should be intentionally small. It should
point at child configs rather than duplicate the full settings schema again.

Suggested shape:

```yaml
version: 1
instances:
  - name: embodied_ai
    config_path: /abs/path/instances/embodied_ai/recoleta.yaml
    enabled: true
    site_label: "Embodied AI"
  - name: software_intelligence
    config_path: /abs/path/instances/software_intelligence/recoleta.yaml
    enabled: true
    site_label: "Software Intelligence"
site:
  mode: aggregate_index
  output_dir: /abs/path/fleet/site
```

Design rule:

- the fleet manifest owns orchestration and aggregate presentation
- child configs own all pipeline semantics
- in v1, child configs referenced by a fleet manifest must not define their own
  `DAEMON` schedules

## Runtime Invariants

The refactor should preserve or introduce these invariants:

1. One active writer per instance DB.
2. No child instance depends on state in another child instance DB.
3. Fleet orchestration must not require shared child-instance storage.
4. The migration command must not mutate the source DB in place.
5. If source ownership is ambiguous, the migration must fail closed unless the
   operator selects an override mode explicitly.
6. Fleet-managed instances should not each run their own daemon schedule in the
   same deployment topology.

Recommended lease model:

- keep the existing workspace lease per child instance
- add a separate fleet-level lease only for fleet aggregate outputs and
  orchestration bookkeeping if fleet commands write shared aggregate artifacts

Recommended v1 scheduler rule:

- fleet-managed child configs may not enable `DAEMON`
- fleet config validation should reject any manifest that references a child
  config with daemon schedules present
- migration-generated child configs should omit `DAEMON` by default

## V1 Decisions Already Locked

- `default` scope handling:
  default migration behavior is `archive`; do not generate a `legacy_default`
  child instance unless the operator opts in explicitly
- scheduler/orchestration:
  v1 uses external scheduling plus `recoleta fleet run ...` one-shot commands;
  a fleet-native scheduler is a deferred follow-up, not a blocker for the
  breaking refactor

## Recommended Breaking Shape

### Product/runtime break now

Remove from the primary product surface:

- `TOPIC_STREAMS`
- `repair streams`
- stream-scoped stage loops
- `stream_results`
- stream pages as a first-class storage concept

Replace with:

- one-instance config files
- one fleet manifest
- instance-local output roots

Recommended output model:

- child instances write only their own canonical outputs
- the fleet layer may build an aggregate site/index, but it should read from
  child outputs or child DBs as projections, not become a new truth store

Recommended `fleet site build` contract for v1:

- read child output trees only
- do not read child DBs directly
- do not write back into child canonical output roots

This keeps the aggregate layer projection-only in the first cut.

## Fleet Site Read Model: Outputs vs DB

The current site/export pipeline is already intentionally filesystem-first.

Today:

- `site build` and `site stage` can run from explicit `--input-dir` /
  `--output-dir` arguments without loading runtime settings
- the exporter discovers `Inbox/`, `Trends/`, `Ideas/`, `Localized/<language>/`,
  and legacy `Streams/<stream>/...` trees from the input snapshot
- it builds pages by parsing Markdown frontmatter, Markdown body content,
  sibling PDFs, and directory layout

For the current public content site, the required content metadata is already
projected into outputs.

Projected site-critical fields today:

- item notes:
  `source`, `url`, `published_at`, `authors`, `topics`, `relevance_score`,
  `run_id`, optional `language_code`
- trend notes:
  `kind`, `trend_doc_id`, `granularity`, `period_start`, `period_end`,
  `topics`, optional `stream`, optional `site_exclude`, optional
  `language_code`, and projection provenance such as `pass_output_id` /
  `pass_kind`
- idea notes:
  `kind`, `granularity`, `period_start`, `period_end`, `status`, `topics`,
  `stream`, optional `language_code`, and projection provenance including the
  upstream pass pointer
- directory structure:
  stream grouping, localized language roots, sibling PDF availability, and
  canonical page routing

DB-only information still exists, but it is mostly not required to render the
public site.

### DB-only information that the current output tree does not fully expose

- operational state:
  `runs`, `metrics`, `workspace_leases`, `source_pull_states`, `deliveries`,
  `trend_deliveries`, `artifacts`
- retrieval/search internals:
  `contents`, `document_chunks`, `chunk_embeddings`
- richer canonical/debug payloads:
  full `pass_outputs.payload_json`, pass/localization diagnostics,
  `items.raw_metadata_json`, internal repair metadata

### What direct child-DB reads would buy

- operator/admin views such as run history, source freshness lag, delivery/send
  state, failure diagnostics, and ingest cursors
- richer aggregate analytics without expanding the output projection schema
- potentially more efficient incremental site rebuild heuristics

### What direct child-DB reads would not buy for the current site

- a piece of public site content that cannot be projected into outputs
- a correctness requirement for content pages, topic pages, stream pages,
  localized pages, or sibling-PDF linking
- a simpler isolation story; reading child DBs would couple the aggregate
  surface back to child runtime state

Therefore the right v1 boundary is:

- `fleet site build` remains outputs-only
- if a future content site needs more child-instance facts, first project them
  into a child-owned output artifact such as enriched note frontmatter or a
  small site manifest under the child output root
- direct child-DB reads should be treated as a separate operator/admin surface
  decision, not as a prerequisite for the public aggregate site

In plain terms:

- DB reads are useful for dashboards and diagnostics
- they do not currently look irreplaceable for the public site
- the burden of proof should stay on the DB-reading path, not the
  projection-only path

### Storage simplification

Recommended practical path:

1. Remove `item_stream_states` in the breaking refactor.
2. Split shared DB content into one DB per instance.
3. Normalize migrated per-scope rows to instance-local state.
4. Keep `scope` columns as a temporary always-`default` compatibility shim for
   one migration window if needed.
5. Drop dead `scope` columns in a later explicit schema rewrite once the fleet
   model is stable.

Why not drop every scope column immediately?

- it combines fleet UX changes with a full historical table rewrite
- it enlarges the blast radius without changing the instance-first semantics
- it is not required to get the architectural win you want

If desired, a one-shot total schema cleanup is still feasible, but it is not the
lowest-risk form of the break.

## Recommended Fleet And Output Layout

For migration-generated assets, prefer a dedicated fleet root rather than
continuing to reuse the old shared output directory.

Suggested layout:

```text
<fleet-root>/
  fleet.yaml
  instances/
    embodied_ai/
      recoleta.yaml
      recoleta.db
      outputs/
      lancedb/
      artifacts/
    software_intelligence/
      recoleta.yaml
      recoleta.db
      outputs/
      lancedb/
      artifacts/
  aggregate/
    site/
    migration-manifest.json
```

This keeps cutover and rollback mechanical:

- point deployment to `<fleet-root>/fleet.yaml`
- leave the old DB and old output root untouched

## Current Main Config And DB Findings

The active config and DB already show both the opportunity and the migration
constraints.

Current config:

- config: `/Users/chenmohan/Playground/recoleta-playground/recoleta.yaml`
- DB: `~/.local/share/recoleta/recoleta.db`
- streams: `embodied_ai`, `software_intelligence`
- sources are still globally shared across both streams

Important config detail:

- the current file defines stream-local topics
- but `sources.arxiv.queries` is one shared list containing both the embodied
  AI query and the software intelligence query
- `hn` and `hf_daily` are also shared

This means the current config is only partially separable by inspection:

- the two arXiv queries are plausibly assignable one-to-one to the two future
  instances
- `hn` and `hf_daily` are ambiguous shared sources and should not be guessed by
  default

Current path-risk detail:

- the current config does not set `rag_lancedb_dir`
- in the new model, letting both child configs inherit the same default LanceDB
  root would recreate hidden shared state
- the current config uses one shared Obsidian vault path and global publish
  targets including `obsidian`
- in the new model, child configs must not keep the same bare
  `obsidian_base_folder` unless their outputs are meant to collide

Current DB size and row counts:

- DB size: about `232 MB`
- `items`: `1792`
- `analyses`: `4379`
- `item_stream_states`: `4509`
- `documents`: `769`
- `document_chunks`: `5611`
- `pass_outputs`: `76`
- `localized_outputs`: `5904`
- `metrics`: `24916`
- `runs`: `93`
- `source_pull_states`: `4`

Current scope distribution:

- analyses:
  - `default`: `1661`
  - `embodied_ai`: `1359`
  - `software_intelligence`: `1359`
- documents:
  - no `default` trend/idea docs
  - `embodied_ai`: `174` item docs, `24` trend docs, `8` idea docs
  - `software_intelligence`: `529` item docs, `24` trend docs, `10` idea docs
- pass outputs:
  - only explicit stream scopes
- localized outputs:
  - `default` exists only for item analyses
  - trend/idea localized rows are already split cleanly by explicit scope

Current overlap pattern:

- only-default analyzed items: `267`
- default + embodied only: `35`
- default + software only: `35`
- default + embodied + software: `1324`

Implication:

- the two explicit streams overlap heavily
- splitting into separate instances will intentionally duplicate a large amount
  of historical content across child DBs
- that duplication is acceptable if instance isolation is the primary goal

Current operational-history signal:

- `runs.scope` is mostly `NULL`
- stream-scoped metrics exist, but many runs and metrics represent mixed
  multi-stream executions rather than one future child instance

This confirms that historical operational rows are archive material, not clean
per-instance truth.

## Recommended Child Config Defaults For The Current Deployment

If the migration tool is pointed at the current config and the current main DB,
the generated child configs should default to:

### `embodied_ai`

- copy shared non-source settings such as model, localization, workflows,
  triage, analyze, and trend settings
- set `topics` from the old `embodied_ai` stream
- set `min_relevance_score` from the old `embodied_ai` stream
- assign the embodied-AI arXiv query only
- generate dedicated paths for DB, outputs, LanceDB, and artifacts
- if `obsidian` remains enabled, generate a unique `obsidian_base_folder`

### `software_intelligence`

- copy shared non-source settings such as model, localization, workflows,
  triage, analyze, and trend settings
- set `topics` from the old `software_intelligence` stream
- set `min_relevance_score` from the old `software_intelligence` stream
- assign the software-intelligence arXiv query only
- generate dedicated paths for DB, outputs, LanceDB, and artifacts
- if `obsidian` remains enabled, generate a unique `obsidian_base_folder`

### Ambiguous shared sources

For `hn` and `hf_daily`, the migration should not guess by default.

Recommended behavior with the default `--ambiguous-source-mode fail`:

- generate no child config until the operator chooses whether those sources are
  copied to both children, disabled, or otherwise remapped

If the operator chooses `copy_all`, the migration manifest should record that
decision explicitly because future ingest behavior will diverge independently in
each child DB after the split.

Important operator-facing consequence:

- `copy_all` is not only a source-ownership choice
- it can also change delivery semantics if multiple child instances keep the
  same publish destination
- current Telegram dedupe and `max_deliveries_per_day` accounting are enforced
  per repository and per destination, not across repositories

Therefore v1 should fail closed here too:

- if `copy_all` is selected and two or more generated child configs still
  enable Telegram delivery to the same destination, migration must fail by
  default
- the operator must either remap destinations, disable Telegram on at least one
  child, or explicitly allow the semantic drift

If the operator explicitly allows the drift, both the CLI summary and the
migration manifest must state that:

- duplicate delivery for overlapping source coverage is now possible
- `max_deliveries_per_day` becomes an effective per-instance budget rather than
  the old shared-DB budget boundary

## What Can Be Migrated Cleanly

These tables can be migrated per target instance with deterministic rules:

### `items`

Copy items referenced by the target instance’s selected scope.

Instance-local `items.state` should be derived as:

1. selected stream state, if present
2. otherwise the old global item state

This replaces the old dual state machine.

### `contents`

Copy all content rows for copied items.

### `analyses`

Copy rows for the selected scope only.

Preferred migration behavior:

- preserve original integer IDs
- rewrite `scope` to `default` if the landing schema still has a scope column

### `documents` and `document_chunks`

Copy rows for the selected scope only, preserving document IDs and chunk foreign
keys.

### `chunk_fts`

Treat `chunk_fts` as a derived retrieval index, not as canonical history.

Recommended v1 behavior:

- do not copy `chunk_fts` rows verbatim
- after migrated `document_chunks` land in the child DB, rebuild `chunk_fts`
  from non-`meta` chunks before any lexical retrieval or agent workflow is
  considered ready
- if that rebuild fails, the migration must fail or mark the child instance as
  not ready for retrieval-facing runtime use

Reason:

- `init_schema()` ensures the FTS table exists and prunes stale `meta` rows, but
  it does not backfill historical `document_chunks`
- lexical retrieval tools search `chunk_fts`, not `document_chunks` directly

### `pass_outputs`

These are migratable, but not as a pure row copy.

Current blocker:

- `pass_outputs.run_id` has a foreign-key reference to `runs.id`
- v1 does not want to preserve mixed historical `runs` verbatim

Recommended v1 behavior:

- copy rows for the selected scope only, preserving `pass_outputs.id`
- rewrite migrated `pass_outputs.run_id` to a synthetic per-child migration run
  instead of preserving the old mixed-history `run_id`
- record the original source `run_id` values in the migration manifest, and
  optionally stamp them into migrated diagnostics metadata if later auditability
  needs the pointer in-db

Design rule:

- child DBs must not contain orphan `pass_outputs`
- v1 preserves canonical pass payloads, not historical run topology

### `localized_outputs`

Copy rows for:

- `analysis` records whose `source_record_id` points at copied `analyses.id`
- `trend_synthesis` rows whose `source_record_id` points at copied trend
  `documents.id`
- `trend_ideas` rows whose `source_record_id` points at copied idea
  `documents.id`

Preserve IDs in referenced tables so this remains a pure row copy, not an ID
remapping exercise.

### `deliveries` and `trend_deliveries`

These are conditionally migratable, not default-safe.

Rules:

- if destination ownership can be mapped cleanly to one child instance, copy
  the matching rows
- if historical deliveries came from ambiguous shared/default behavior, prefer
  dropping them rather than guessing

For the current main DB this is moot because both tables are empty, but the
general migration design should still define the rule.

### Output trees

Do not treat current Markdown/site output as primary migration material.

Recommended behavior:

- create new instance-local output roots
- rebuild Markdown/site/localized output from migrated DB state
- archive the old combined output root

Path-safety rule:

- no migrated child config may point its outputs, LanceDB, or artifacts back at
  the legacy shared root

## What Should Not Be Migrated Verbatim

### `runs`, `metrics`, `artifacts`

Do not attempt default migration of historical operational rows into child
instance DBs.

Why:

- current `runs.scope` is mostly `NULL`
- many runs reflect mixed multi-stream operations
- metrics are aggregated and often encode old stream-oriented naming
- artifact/debug history is operational, not primary user-facing content

Recommended handling:

- archive the source DB intact
- optionally export a JSON manifest summarizing old run history
- start child DB operational history fresh
- create only the minimal synthetic migration-run shell rows required for
  migrated `pass_outputs` foreign-key integrity and migration auditability

Default migration mode should therefore be:

- `runs`: do not copy verbatim
- `metrics`: do not copy
- `artifacts`: do not copy

### `source_pull_states`

These cannot be split correctly from DB scope alone.

Current problem:

- source pull state is keyed by source scope such as `arxiv query`, `hn feed`,
  `hf_daily global`
- the DB does not record which stream “owned” which source entry
- the current config file also models sources as shared, not stream-local

Recommended handling:

- migration tool must read the old config file
- config generation must decide how each source config maps into new instances
- source pull states are then copied according to that config mapping

For the current setup this means:

- the embodied AI arXiv query can be assigned to the embodied instance
- the software intelligence arXiv query can be assigned to the software instance
- `hn` and `hf_daily` can either be copied to both instances or intentionally
  disabled per instance during the split

This is the main migration step that needs operator input or a config-side
mapping manifest.

Recommended migration flag:

- `--ambiguous-source-mode fail|copy_all|disable`

Recommended default:

- `fail`

Reason:

- `copy_all` preserves continuity but bakes in a guess
- `disable` is safer than guessing but may silently change coverage
- `fail` forces the operator to make the ambiguity explicit

Recommended shared-delivery guard flag:

- `--shared-delivery-mode fail|allow`

Recommended default:

- `fail`

Reason:

- allowing overlapping source coverage to continue with the same Telegram
  destination would silently change dedupe and daily-budget semantics after the
  split
- failing closed keeps the operator from mistaking a source mapping choice for
  a no-behavior-change migration

## Recommended Handling Of The Current `default` Scope

The explicit stream history splits cleanly. The `default` scope is different:

- it has `1661` analyses
- it has `2276` localized analysis rows
- it has `1791` stream-state rows
- it has no trend/idea documents or pass outputs

Recommended default behavior:

- do not migrate `default` into every child instance
- keep it only in the archived source DB

Optional behavior:

- generate a third `legacy_default` instance if that history is still valuable

This should be a migration flag, not mandatory behavior.

Suggested migration flag:

- `--default-scope-mode archive|child-instance`

Recommended default:

- `archive`

Manifest requirement when `archive` is chosen:

- report the count of `only-default` items and analyses
- include a small sample of item IDs or canonical URLs
- record whether a `legacy_default` child instance was intentionally not
  generated

## Explicit Migration Command Requirements

This refactor needs a dedicated migration command. It should not be hidden in
normal startup.

Suggested responsibilities:

1. validate the old DB schema
2. create a fresh timestamped DB backup bundle
3. read the old config file
4. generate new instance config files
5. create one new DB per instance
6. enforce the shared-delivery guard before writing child configs that would
   preserve overlapping source coverage to the same destination
7. create any synthetic migration-run shell rows needed for migrated
   `pass_outputs`
8. copy rows per instance while preserving primary keys where needed
9. rebuild `chunk_fts` from migrated non-`meta` `document_chunks`
10. rebuild instance-local outputs
11. emit a machine-readable migration manifest

Suggested dry-run support:

12. support `--dry-run` that emits the split plan without writing child DBs

Suggested command shape:

```text
recoleta admin migrate topic-streams-to-instances --config <old-config> --db <old-db> --out <fleet-dir>
```

The exact name can change, but the migration should live under an explicit admin
or migration namespace.

Suggested migration manifest fields:

- source DB path and checksum
- source config path and checksum
- generated child instance names
- per-instance source-assignment decisions
- per-instance synthetic migration runs created and the legacy `run_id` values
  they absorb for migrated `pass_outputs`
- per-instance copied row counts by table
- per-instance `chunk_fts` rebuild status and expected-vs-actual indexed row
  counts
- skipped tables
- ambiguous-source decisions
- shared-delivery guard decisions and any explicit semantic-drift overrides
- intentionally dropped history with explicit reasons
- output rebuild status
- warnings

## Migration Phases

### Phase 0: Runtime break preparation

- freeze and land the read-only legacy migration reader
- land fleet manifest support
- land explicit migration command scaffolding
- only after that, teach new binaries to reject `TOPIC_STREAMS` with a
  migration-required error

### Phase 1: Runtime storage simplification

- remove new runtime dependence on `item_stream_states`
- make the instance runtime assume one logical scope only
- keep legacy `scope` columns only as a compatibility shim if needed

### Phase 2: Explicit DB split migration

- read old config + old DB
- choose source-assignment mapping
- enforce shared-delivery guard decisions
- generate child configs
- create child DBs
- create synthetic migration runs for migrated `pass_outputs`
- copy user-facing historical rows
- rebuild derived retrieval indexes such as `chunk_fts`
- rebuild child outputs

### Phase 3: Cutover

- switch scheduler/deployment from one shared instance config to one fleet
  manifest
- keep the old DB and output root unchanged and read-only

### Phase 4: Post-cutover cleanup

- after soak, optionally land a second explicit schema rewrite that drops dead
  `scope` columns and other legacy stream scaffolding

## Recommended Execution Order

1. Land the instance-first runtime and fleet manifest support.
2. Land schema changes that remove `item_stream_states` and stop all new writes
   from depending on stream state.
3. Land the explicit migration command.
4. Snapshot the current main DB and output root.
5. Generate new child configs and DBs from the old config + old DB.
6. Rebuild `chunk_fts` and outputs for each instance.
7. Switch the deployment to fleet mode.
8. Keep the old combined DB as a cold archive until the new fleet has passed a
   soak period.
9. Only after that, consider dropping legacy scope columns in a second explicit
   schema rewrite.

## Validation Requirements

The migration command should fail if any of these checks do not pass:

### Structural checks

- source DB schema version is supported
- source DB is readable
- source config exists and parses
- every generated child DB initializes successfully
- no copied row produces foreign-key or uniqueness violations

### Data integrity checks

- per-instance `items` and `contents` counts match copied source references
- per-instance `analyses` count matches the selected source scope count
- per-instance `documents` and `document_chunks` counts match copied references
- per-instance `chunk_fts` row count matches the migrated non-`meta`
  `document_chunks` count
- per-instance `pass_outputs` counts match selected source scope rows
- every migrated `pass_outputs.run_id` resolves to the synthetic migration run
  created for that child instance
- per-instance `localized_outputs` counts match selected source scope rows
- per-instance `source_pull_states` copied/skipped counts match the migration
  manifest
- `deliveries` and `trend_deliveries` copied/skipped counts match the migration
  manifest
- migrated `item.state` distribution matches the expected derivation policy
- orphan checks for localized outputs and chunks return zero
- when `copy_all` is selected, shared-destination guard outcomes match the
  manifest and requested override mode

### Runtime checks

- each child instance can run a read-only inspect command successfully
- each child instance with migrated non-`meta` chunks can execute a lexical
  retrieval smoke query successfully after `chunk_fts` rebuild
- each child instance can rebuild outputs from the migrated DB
- fleet site/index build succeeds from child outputs only when enabled

### Current-main-DB acceptance targets

For the current snapshot, the migration should be able to prove at minimum:

- `embodied_ai` child DB receives `1359` analyses
- `software_intelligence` child DB receives `1359` analyses
- trend/idea documents split as observed in the source DB
- the source DB remains unchanged
- migrated non-`meta` chunks are indexed into `chunk_fts`
- no migrated child DB contains orphan `pass_outputs`
- the migration manifest reports any intentionally dropped `default`-only,
  delivery, or source-state history explicitly

## Rollback Plan

Rollback should be operationally simple.

Required properties:

- the source DB is never modified in place
- the source output root is never mutated in place by the migration
- cutover changes are limited to config/scheduler/deployment pointers

Rollback semantics must be stated precisely:

- lossless rollback is only guaranteed until the first successful write in the
  new fleet-managed child DBs after cutover
- after new child-instance writes exist, pointing back to the old shared DB is a
  disaster-recovery rollback and may discard post-cutover data and send-state
  history unless a later replay/export tool exists
- v1 does not promise child-DB-to-legacy replay

Rollback procedure before first successful child write:

1. stop fleet-triggered runs
2. point deployment back to the old single-instance config
3. point outputs/site publishing back to the old combined root if needed
4. resume from the archived source DB

Rollback procedure after successful child writes:

1. stop fleet-triggered runs
2. decide explicitly whether disaster rollback with data loss is acceptable
3. if yes, point deployment back to the old single-instance config and source DB
4. if no, keep fleet active and repair forward instead of rolling back

## Key Risks

- ambiguous shared sources create migration choices that the DB cannot answer
- duplicated items across child DBs increase storage and future compute
- aggregate site behavior may accidentally reintroduce hidden coupling if it
  reads/writes child canonical state
- concurrent fleet scheduling plus child daemons could create overlapping runs
- migrated historical chunks would become non-searchable if `chunk_fts` rebuild
  is omitted or only assumed implicitly
- `copy_all` plus shared Telegram destinations would change dedupe and
  `max_deliveries_per_day` semantics unless blocked explicitly
- dropping legacy scope columns too early would enlarge the migration blast
  radius without improving the initial cutover semantics

## Acceptance Criteria

This refactor is only complete when all of the following are true:

- `TOPIC_STREAMS` is no longer accepted by the runtime
- one deployment can run multiple isolated instances through a fleet manifest
- no new runtime code depends on `item_stream_states`
- the explicit migration command can split the current source DB into child DBs
- child outputs rebuild correctly from migrated data
- cutover does not require in-place mutation of the old DB
- migrated historical `document_chunks` remain lexically searchable because
  `chunk_fts` is rebuilt explicitly
- migrated `pass_outputs` never rely on missing historical `runs`
- `copy_all` cannot silently preserve old shared-delivery semantics; shared
  destinations must be remapped, disabled, or explicitly overridden
- rollback semantics are documented accurately:
  lossless before first successful child write, disaster-recovery after that

## Deferred Follow-ups

- fleet-native scheduler/orchestration above the v1 external-scheduler model
- a possible future operator/admin read model that consumes child DB state
  directly for diagnostics or dashboards
- W12 post-cutover replay validation showed that canonical weekly outputs are
  idempotent, but `pass_outputs` remain append-only historical snapshots rather
  than latest-only canonical rows; treat this as a historical-retention follow-up,
  not a cutover blocker
- W12 deploy smoke showed that `fleet run deploy` still triggers child
  `translate` and `materialize` before aggregate site deploy; if deploy should
  become a pure outputs-only publish step, split that behavior into a later
  follow-up rather than extending this cutover

## Open Decisions

- whether non-empty `deliveries` / `trend_deliveries` migration support should
  be implemented now or deferred until a real operator case appears

## Feasibility Verdict

This design is feasible.

Recommended answer to the product/architecture question:

- yes to hard-deleting `topic_streams` as a runtime feature
- yes to an instance-first breaking refactor
- yes to migrating the current main DB data
- no to doing that migration implicitly at startup
- no to assuming DB rows alone are sufficient to derive future source config
- no to preserving old mixed run/metric history as if it were per-instance truth

The refactor is large but proportionate. The current main DB is small enough to
split safely. The main engineering work is semantic cleanup, not raw data
movement.
