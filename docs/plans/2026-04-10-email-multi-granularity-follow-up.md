# Email Multi-Granularity Follow-up

Date: 2026-04-10

Status: proposed clean-break follow-up to the shipped `v1` manual trend email surface

## Purpose

Record the recommended design for extending manual trend email selection from
one configured granularity to an ordered set of supported granularities.

This note is intentionally a follow-up to
`docs/plans/2026-04-09-manual-email-delivery-notes.md`.

That earlier note remains the source of truth for the currently shipped `v1`
behavior:

- one configured trend granularity
- one selected trend document
- one rendered email batch
- one send attempt across the configured recipient set

This document describes the next step only.

## Current Implementation Constraint

The current repository hard-codes a single-granularity selection path:

- `EmailConfig` accepts one `EMAIL.granularity` value.
- trend email selection computes one target period for one granularity.
- preview and send build one `_TrendEmailBundle`.
- CLI payloads and console output assume one result object.

Relevant code paths:

- `recoleta/config.py`
- `recoleta/trend_email.py`
- `recoleta/cli/email.py`
- `recoleta/cli/fleet.py`
- `recoleta/storage/deliveries.py`

The current persistence model is still compatible with a multi-granularity
follow-up because `trend_deliveries` are already keyed by `doc_id`, `channel`,
and `destination`. Distinct trend docs for `day`, `week`, and `month` do not
collide.

## Goals

- Allow operators to configure more than one eligible trend granularity for
  manual email preview/send.
- Keep the current core semantic intact: one email maps to one selected trend
  document.
- Preserve deterministic ordering.
- Preserve current dedupe and resend behavior within each selected trend
  document.
- Avoid a DB migration for the first follow-up.
- Avoid carrying forward config or CLI compatibility shims for an unused
  feature surface.
- Keep fleet email targeted at one child instance per command.

## Non-Goals

- Do not introduce a many-trend digest rendered into one email body.
- Do not add idea email in this change.
- Do not redesign `TrendDelivery` into a full historical send ledger.
- Do not change public-site link resolution rules.
- Do not silently choose one granularity when multiple are configured.

## Recommended Operator Semantics

The extension should use a fan-out model:

- one command invocation may cover multiple configured granularities
- each granularity still resolves to one trend document
- each resolved trend document still renders one email body
- each rendered body still sends as one recipient batch

In other words:

- multiple granularities means multiple email batches
- not one combined digest
- not one implicit winner

This keeps the mental model aligned with the current `v1` surface and avoids
mixing day/week/month content into a synthetic composite output that would need
new subject, layout, and resend semantics.

## Configuration Design

### Proposed schema

Use a plural field as the only supported configuration shape:

```yaml
email:
  public_site_url: "https://example.github.io/recoleta"
  from_email: "recoleta@example.com"
  to:
    - "you@example.com"
  granularities:
    - "day"
    - "week"
```

### Validation rules

- `EMAIL.granularities` is required.
- `EMAIL.granularity` should be removed in this follow-up rather than kept as an
  alias.
- preserve declared order
- deduplicate repeated entries during validation
- only allow `day`, `week`, and `month`
- reject an empty resolved list after normalization

This follow-up should not spend design or implementation effort on dual-field
compatibility because the email surface has not started real operator use yet.

## Selection Semantics

Selection should remain independent per granularity.

For each configured granularity:

- compute the target period start for that granularity
- filter eligible trend source documents by that granularity
- apply the existing language filter rules
- sort by the existing candidate ordering
- pick one candidate

Concrete anchor-date example for `--date 2026-04-10`:

- `day` resolves to `2026-04-10`
- `week` resolves to `2026-04-06`
- `month` resolves to `2026-04-01`

This means a single operator-supplied date still works, but it anchors each
granularity to its own correct window boundary.

## Command-Level Granularity Selection

The configured list should define the default selected set, but commands should
also support narrowing that set explicitly.

Recommended command rule:

- `run email preview` and `run email send` should accept repeatable
  `--granularity <value>` filters
- allowed values are still only `day`, `week`, and `month`
- every requested CLI granularity must already exist in
  `EMAIL.granularities`
- when a selector is present, keep config order after filtering rather than
  reordering by CLI flag order

Example:

- config: `["day", "week", "month"]`
- command: `run email send --granularity week --granularity month`
- effective selected set: `["week", "month"]`

This selector is the recommended recovery tool for multi-granularity retry and
force scenarios.

## Preview Semantics

`run email preview` should become a batch preview over the effective selected
set.

Recommended behavior:

- resolve and render every selected bundle in memory before writing artifacts
- only write preview artifacts after the whole selected set succeeds
- write one preview artifact directory per bundle under one batch root
- return a batch envelope containing one result entry per bundle
- use the same batch envelope even when only one granularity is configured

Recommended filesystem rule:

- treat `--output-dir` as a root directory
- when `--output-dir` is omitted, create a generated batch root under
  `MARKDOWN_OUTPUT_DIR/.recoleta-email/previews/<invocation-token>/`
- create one child directory per rendered bundle under that root
- keep the current single-bundle naming token:
  `<granularity>--<period_token>--trend--<trend_doc_id>`
- write one batch manifest at the root, for example `batch-manifest.json`

This avoids collisions and keeps the preview layout inspectable.

Failure contract:

- preview is all-or-nothing for the effective selected set
- if any selected granularity fails candidate resolution, link-map resolution,
  or render preparation, the command exits non-zero
- no preview root, per-entry preview directories, or batch manifest should be
  written on failure
- no partial-success preview envelope should be returned
- JSON mode should return the normal command-error payload rather than a mixed
  success/failure `results[]` object

This keeps preview behavior deterministic and prevents stale partial preview
trees from looking authoritative.

## Send Semantics

`run email send` should use a gated two-phase flow:

1. Resolve bundle state and preflight in selected-granularity order.
2. Start provider sends only if no selected bundle ends preflight in an error
   state.

Bundle-state resolution should happen before reachability checks.

For each selected granularity:

1. Resolve the bundle candidate for that granularity.
2. Load existing delivery rows and classify the bundle as one of:
   `skipped`, `send`, or `preflight_failed`.
3. Only if the bundle is classified as `send`, run:
   recipient-batch-size validation and public trend page reachability checks.

Classification rules:

- unchanged content already fully sent -> `skipped`
- mixed partially sent state without force -> `preflight_failed`
- otherwise -> `send`

Important safety rule:

- `skipped` bundles must not be blocked by public URL reachability failures
- `skipped` bundles must not be forced through extra validation just because
  another bundle in the same command still needs send-time checks

Why this matters:

- it avoids sending `day` successfully and only then discovering that `week`
  has no matching candidate
- it preserves the current safe rerun behavior for already-sent unchanged
  bundles
- it keeps operator-visible failures in the validation stage all-or-nothing

After every selected bundle has been resolved and no bundle is marked
`preflight_failed`, actual provider sends should run sequentially in the
selected order.

Failure policy:

- stop on the first send failure
- do not start later granularities after a failed send
- return a batch result that records the completed earlier sends, the failed
  current send, and later bundles as `not_attempted`

This is stricter than a best-effort continue-all policy and is easier to audit.

## Dedupe and Retry Semantics

Dedupe should remain scoped to each resolved trend document.

That means:

- idempotency keys still derive from one bundle plus one recipient batch
- delivery persistence still upserts one row per `doc_id + destination`
- mixed partially sent state is still evaluated per bundle

## Force Semantics

`--force-batch` needs an explicit scope in the multi-granularity design.

Recommended rule:

- `--force-batch` applies only to the effective selected set
- by default, the selected set is every configured granularity
- when the operator passes one or more `--granularity` selectors,
  `--force-batch` applies only to that filtered subset

This yields three predictable cases:

- no selector, no force: use normal skip/send/preflight_failed classification
- no selector, with force: force the whole configured batch
- selector plus force: force only the named granularities

Recovery example:

- `day` already sent successfully
- `week` is blocked by mixed state
- operator reruns with `run email send --granularity week --force-batch`
- `day` is outside the selected set and is therefore not re-sent

This avoids accidental resend of already-completed bundles while keeping force
semantics explicit.

Additional rule:

- `--force-batch` should not silently narrow itself to only blocking bundles
- if the operator wants a narrower force scope, they must express that through
  the `--granularity` selector

No cross-granularity idempotency key is needed in the first follow-up.

That would create unnecessary coupling between independent trend documents.

## Audit Artifacts

The batch-first contract should preserve the current per-entry audit material
rather than collapse everything to only `preview_dir` or `send_dir`.

Recommended artifact model:

- preview writes one preview root directory plus one child directory per entry
- send writes one send root directory plus one child directory per entry
- both commands write a batch manifest at the root
- each successful or resolved entry keeps its own manifest and rendered bodies

Recommended batch-level fields:

- `preview_root_dir` or `send_root_dir`
- `batch_manifest_path`

Recommended per-entry fields, preserving the current single-result audit value
where available:

- `manifest_path`
- `html_path`
- `text_path`
- `primary_page_url`
- `content_hash`
- `subject`
- `trend_doc_id`
- `period_token`
- `granularity`

Field availability rule:

- successful preview entries should always include the full audit field set
- send entries should include the full audit field set whenever bundle render
  completed
- entries that fail before bundle render completes may include only
  `granularity`, `status`, and `error`

## CLI and Result Shape

The current CLI payload shape is single-result oriented and does not expose
`granularity` explicitly.

The follow-up should switch to a batch-first public contract instead of hiding
batch behavior behind compatibility fields.

Recommended preview JSON shape:

```json
{
  "status": "succeeded",
  "command": "run email preview",
  "instance": "default",
  "preview_root_dir": "...",
  "batch_manifest_path": ".../batch-manifest.json",
  "results": [
    {
      "granularity": "day",
      "trend_doc_id": 123,
      "period_token": "2026-04-10",
      "subject": "[Recoleta] Day trends · 2026-04-10",
      "preview_dir": ".../day--2026-04-10--trend--123",
      "manifest_path": ".../day--2026-04-10--trend--123/manifest.json",
      "html_path": ".../day--2026-04-10--trend--123/body.html",
      "text_path": ".../day--2026-04-10--trend--123/body.txt",
      "primary_page_url": "https://public.example/recoleta/trends/...",
      "content_hash": "..."
    },
    {
      "granularity": "week",
      "trend_doc_id": 456,
      "period_token": "2026w15",
      "subject": "[Recoleta] Week trends · 2026w15",
      "preview_dir": ".../week--2026w15--trend--456",
      "manifest_path": ".../week--2026w15--trend--456/manifest.json",
      "html_path": ".../week--2026w15--trend--456/body.html",
      "text_path": ".../week--2026w15--trend--456/body.txt",
      "primary_page_url": "https://public.example/recoleta/trends/...",
      "content_hash": "..."
    }
  ]
}
```

Recommended send top-level status enum:

- `succeeded`: every selected entry finished as `sent` or `skipped`
- `preflight_failed`: no provider sends started because at least one selected
  entry failed preflight
- `send_failed`: provider send started and then stopped on the first failed
  bundle; later send-target entries must be returned as `not_attempted`

Recommended send entry status enum:

- `skipped`
- `ready_to_send`
- `sent`
- `preflight_failed`
- `send_failed`
- `not_attempted`

`ready_to_send` means:

- bundle resolution and render succeeded
- the entry would have been sent
- provider sends never started because another selected entry failed preflight

Recommended send JSON shape:

```json
{
  "status": "send_failed",
  "command": "run email send",
  "instance": "default",
  "send_root_dir": "...",
  "batch_manifest_path": ".../batch-manifest.json",
  "results": [
    {
      "granularity": "day",
      "status": "sent",
      "trend_doc_id": 123,
      "period_token": "2026-04-10",
      "subject": "[Recoleta] Day trends · 2026-04-10",
      "send_dir": ".../day--2026-04-10--trend--123",
      "manifest_path": ".../day--2026-04-10--trend--123/manifest.json",
      "html_path": ".../day--2026-04-10--trend--123/body.html",
      "text_path": ".../day--2026-04-10--trend--123/body.txt",
      "primary_page_url": "https://public.example/recoleta/trends/...",
      "content_hash": "..."
    },
    {
      "granularity": "week",
      "status": "send_failed",
      "trend_doc_id": 456,
      "period_token": "2026w15",
      "subject": "[Recoleta] Week trends · 2026w15",
      "send_dir": ".../week--2026w15--trend--456",
      "manifest_path": ".../week--2026w15--trend--456/manifest.json",
      "html_path": ".../week--2026w15--trend--456/body.html",
      "text_path": ".../week--2026w15--trend--456/body.txt",
      "primary_page_url": "https://public.example/recoleta/trends/...",
      "content_hash": "...",
      "error": "provider failed"
    },
    {
      "granularity": "month",
      "status": "not_attempted",
      "trend_doc_id": 789,
      "period_token": "2026-04",
      "subject": "[Recoleta] Month trends · 2026-04"
    }
  ]
}
```

Recommended preflight-failure shape:

```json
{
  "status": "preflight_failed",
  "command": "run email send",
  "instance": "default",
  "send_root_dir": "...",
  "batch_manifest_path": ".../batch-manifest.json",
  "results": [
    {
      "granularity": "day",
      "status": "skipped",
      "trend_doc_id": 123,
      "period_token": "2026-04-10",
      "send_dir": ".../day--2026-04-10--trend--123",
      "manifest_path": ".../day--2026-04-10--trend--123/manifest.json",
      "html_path": ".../day--2026-04-10--trend--123/body.html",
      "text_path": ".../day--2026-04-10--trend--123/body.txt",
      "primary_page_url": "https://public.example/recoleta/trends/...",
      "content_hash": "..."
    },
    {
      "granularity": "month",
      "status": "ready_to_send",
      "trend_doc_id": 789,
      "period_token": "2026-04",
      "subject": "[Recoleta] Month trends · 2026-04",
      "send_dir": ".../month--2026-04--trend--789",
      "manifest_path": ".../month--2026-04--trend--789/manifest.json",
      "html_path": ".../month--2026-04--trend--789/body.html",
      "text_path": ".../month--2026-04--trend--789/body.txt",
      "primary_page_url": "https://public.example/recoleta/trends/...",
      "content_hash": "..."
    },
    {
      "granularity": "week",
      "status": "preflight_failed",
      "error": "mixed_batch_state"
    }
  ]
}
```

The preflight-failure example above assumes full preflight across the entire
selected set before any provider sends begin.

Recommended human output:

- print one line per result
- keep the command summary visible
- include `granularity`, `trend`, `period`, and artifact path

No single-result compatibility layer is recommended.

That means:

- no top-level `trend_doc_id`, `period_token`, or `subject` mirror fields
- no alternate response shape for the one-granularity case
- scripts should consume `results[]` from the start

## Exit Code Contract

JSON mode should not change shell exit behavior.

Recommended mapping:

- preview `succeeded` -> exit `0`
- preview failure -> exit `1`
- send `succeeded` -> exit `0`
- send `preflight_failed` -> exit `1`
- send `send_failed` -> exit `1`

All-skipped send behavior:

- when every selected entry resolves to `skipped`, top-level send status should
  still be `succeeded`
- that case should still exit `0`

This preserves the current operational meaning that "nothing needed to be sent"
is not an error.

## Why Not Combine Multiple Granularities Into One Email

That path looks simpler than it really is.

A combined digest would immediately need new answers for:

- subject construction across multiple windows
- body hierarchy when day/week/month disagree
- link strategy for multiple primary trend pages
- delivery dedupe identity for a synthetic multi-doc surface
- whether missing one granularity blocks the whole digest
- whether cluster and evidence limits stay per trend or per digest

That is a different product surface.

The recommended fan-out design avoids that explosion in scope.

## Suggested Code Shape

The safest implementation path is to separate single-bundle logic from
multi-bundle orchestration.

Recommended refactor:

- keep one function that builds exactly one bundle for an explicit granularity
- add one function that resolves configured granularities into an ordered list
- add one batch preview orchestrator over the explicit bundle builder
- add one batch send orchestrator over the explicit bundle builder
- make batch result types the only public result types
- keep single-bundle result types as internal entries only if they remain useful

Likely touch points:

- `recoleta/config.py`
- `recoleta/trend_email.py`
- `recoleta/cli/email.py`
- `recoleta/cli/fleet.py`
- `recoleta/cli/app.py`
- `tests/test_trend_email_delivery.py`
- `tests/test_recoleta_specs_settings.py`

## Recommended Delivery Plan

This follow-up should land as one cohesive public-contract cut rather than as a
preview-only intermediate state.

Core cut:

- replace config parsing with `granularities`
- refactor bundle building around an explicit granularity parameter
- add the command-level `--granularity` selector
- add batch preview orchestration
- add batch send orchestration
- add the batch-first preview/send JSON contracts
- update fleet command surfaces in the same change
- update tests, docs, and help text in the same change

Optional polish after the core cut:

- refine console summaries and manifest ergonomics
- add operator-focused examples for retry and force flows
- add any observability counters specific to batch email execution

## Final Recommendation

The recommended extension is:

- add `EMAIL.granularities`
- remove `EMAIL.granularity`
- add an explicit command-level granularity selector for preview/send
- treat multiple configured granularities as an ordered set of independent
  single-trend email batches
- preflight bundle state across the selected set before any sends, but only run
  reachability checks for bundles that actually need to send
- keep dedupe, retry, and persistence scoped per resolved trend document
- make preview/send result shapes batch-first with no single-result compatibility
  shim

That gives operators the flexibility they want without turning the current
manual trend email surface into a digest product or forcing a schema rewrite
up front.
