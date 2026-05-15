# arXiv Pool Fetcher Control Proposal

Status: Accepted and implemented

Date: 2026-05-15

Related notes:

- `docs/design/arxiv-paper-pool.md`
- `docs/design/arxiv-pool-worker.md`
- `docs/design/arxiv-429-access-strategy.md`

## Summary

Move arXiv pool upstream fetching away from `arxiv.Client().results(...)` and
into a pool-owned fetcher that performs exactly one HTTP request per pool window
attempt. The pool should own status handling, `Retry-After`, cooldown state, and
retry policy instead of letting `arxiv.py` retry internally before Recoleta can
record a 429.

The arXiv paper pool already solves fleet-level amplification: child instances
can ingest from the shared pool without directly calling `export.arxiv.org`.
This proposal tightens the remaining upstream control path so a single
rate-limited window does not still produce several hidden requests inside the
dependency wrapper.

## Background

A local smoke test on 2026-05-15 used:

- shared pool DB:
  `/Users/chenmohan/Playground/recoleta-playground/fleet/arxiv_pool.db`
- `SOURCES.arxiv.mode=pool` for `embodied_ai` and `software_intelligence`
- `ARXIV_POOL.request_interval_seconds=10`
- W18 backfill for `2026-04-27` through `2026-05-03`

The important observations:

- `arxiv-pool backfill` entered the new pool path and stopped the batch after
  the first rate-limited window.
- The pool persisted `cooldown_until` and the worker slept without issuing more
  upstream requests.
- `fleet run day` pre-sync saw active cooldown and child ingest did not emit
  new `export.arxiv.org` requests.
- Inside the first pool window, `arxiv.py` still emitted `try: 0` through
  `try: 3` before Recoleta received the final `HTTP 429`.

That means the pool-level behavior is directionally correct, but the fetcher
does not yet fully control upstream request count. Recoleta records one pool
attempt, while the wrapper may have sent multiple HTTP requests for that
attempt.

## Problem

`ArxivApiFetcher.fetch()` currently relies on `arxiv.Client().results(search)`.
The dependency has its own retry loop, request delay, and status handling. That
creates several operational problems:

- A single pool window can produce multiple upstream HTTP requests before
  Recoleta records cooldown.
- `ARXIV_POOL.request_interval_seconds` only applies between pool windows, not
  within the dependency's retry loop.
- `upstream_requests_total` describes pool fetch attempts, not actual HTTP
  attempts made by the wrapper.
- `Retry-After` handling is mostly unavailable because the raised `arxiv`
  exception does not expose response headers.
- Operators cannot distinguish "one polite request got 429" from "one pool
  attempt triggered several wrapper retries and then got 429".

This is especially undesirable during an arXiv cooldown. The feature is meant
to stop quickly and sleep; dependency-managed retries keep probing before the
pool can enforce that decision.

## Goals

- Make one pool window attempt equal exactly one HTTP request.
- Let Recoleta classify HTTP 429 immediately and persist cooldown before any
  retry.
- Honor `Retry-After` when present and fall back to `ARXIV_POOL.cooldown_seconds`.
- Keep all upstream access under the pool sync lease and durable rate state.
- Preserve the existing pool schema, CLI behavior, and `ItemDraft` output
  contract.
- Record request-attempt diagnostics that match actual HTTP requests.

## Non-goals

- Do not bypass or loosen arXiv rate limits.
- Do not add browser automation, proxies, alternate identities, or parallel
  upstream fetches.
- Do not change instance-local ingest semantics beyond improving the pool
  source's upstream behavior.
- Do not cache PDFs, source archives, or full text.
- Do not remove direct arXiv mode in this change.

## Design

Replace `ArxivApiFetcher` with a pool-owned HTTP fetcher:

1. Build the arXiv API URL from `ArxivPoolWindow` using the same query window
   semantics as direct ingest:
   - query text plus `submittedDate:[start TO inclusive_end]`
   - `sortBy=submittedDate`
   - `sortOrder=descending`
   - `start=0`
   - `max_results=window.max_results`
2. Send one `GET` request with a clear Recoleta user agent.
3. If status is `429`, raise `ArxivPoolRateLimitedError` with parsed
   `Retry-After`.
4. If status is `5xx` or a request error, raise a transient fetch error and let
   the worker/backfill retry on a later pass.
5. If status is another non-2xx, record a failed window with the HTTP status.
6. Parse the Atom feed into `ArxivPoolPaper` rows.
7. Store papers and query matches exactly as the current pool sync does.

Use `httpx` for transport, consistent with Recoleta's dependency policy. Use
`feedparser` for Atom parsing unless a smaller local parser is clearly safer.
Both are already runtime dependencies.

## Retry Policy

The fetcher itself should not retry HTTP status failures. Pool retry should
happen at the sync or worker level:

- `429`: set cooldown and stop the current sync pass.
- transient network error: record the failed window and let worker backoff
  schedule the next pass.
- completed cached window plus forced refresh failure: preserve the completed
  cache and attach refresh failure diagnostics, matching the current pool
  behavior.

This keeps retry decisions durable and visible. A future enhancement can add a
single immediate retry for connection resets, but only if request-attempt
metrics remain exact and tests cover the behavior.

## Observability

Add or clarify diagnostics:

- `upstream_requests_total`: actual HTTP requests, not wrapper-level attempts.
- `upstream_status`: HTTP status returned by the single request.
- `retry_after_seconds`: parsed value when arXiv returns `Retry-After`.
- `cooldown_until`: persisted absolute cooldown deadline.
- `fetcher`: `httpx_atom` or equivalent, so inspect output can reveal the active
  implementation.

The CLI JSON payloads for `sync`, `backfill`, `worker`, and `inspect
arxiv-pool freshness` should remain stable. New fields should be additive.

## Compatibility

Direct arXiv ingest can continue using `arxiv.Client()` for now. Pool mode is
the higher-control path because it is the only path intended for long-running
fleet operation and shared cache population.

`pool_paper_to_item_draft` should keep producing the same item identity:

- `source=arxiv`
- stable `source_item_id`
- canonical `/abs/{id}` URL
- title
- authors
- `published_at`
- raw metadata with pool provenance

## Acceptance Criteria

- A mocked `429` response causes exactly one HTTP request for one pool window.
- A `429` response records cooldown and prevents later windows in the same pass
  from issuing upstream requests.
- `Retry-After` is parsed from both integer seconds and HTTP date forms.
- A mocked successful Atom feed produces the same `ArxivPoolPaper` fields used
  by pool-backed ingest today.
- Repeated sync of a completed window still performs zero upstream requests
  unless `--force` or worker refresh semantics require it.
- The W18 local fleet smoke path shows no child `export.arxiv.org` requests and,
  when arXiv is rate-limited, no more than one upstream request before pool
  cooldown is persisted.

## Test Plan

Add focused tests around the new fetcher:

- `test_arxiv_pool_fetcher_sends_single_request_per_window`
- `test_arxiv_pool_fetcher_429_raises_rate_limited_with_retry_after`
- `test_arxiv_pool_sync_stops_after_first_429_without_fetching_later_windows`
- `test_arxiv_pool_fetcher_parses_atom_feed_to_pool_papers`
- `test_arxiv_pool_fetcher_preserves_old_style_arxiv_ids`
- `test_arxiv_pool_fetcher_records_http_status_for_non_retryable_failure`

Extend existing pool tests to assert that `upstream_requests_total` matches
actual HTTP calls, not just logical fetch attempts.

## Rollout

1. Implement the new fetcher behind the existing `ArxivApiFetcher` name. Keep
   public config unchanged.
2. Run the existing `tests/test_arxiv_pool.py` suite and full local tests.
3. Repeat the local W18 smoke test after cooldown expires.
4. Keep the current pool config active for the two arXiv-enabled fleet
   instances.
5. If the smoke test succeeds, restart the long-running worker under tmux or the
   chosen process supervisor.

## Open Questions

- Should direct arXiv mode also move to the pool-owned fetcher, or should that
  wait until pool mode proves stable?
- Should `ARXIV_POOL.request_interval_seconds` default to `10` instead of `5`
  for a more conservative production posture?
- Should inspect output expose a short "effective upstream policy" block so
  operators can see interval, cooldown, and fetcher implementation in one place?
