# Promotion status

Last updated: 2026-07-25

## Current state

- Branch: `codex/promotion-readiness`
- Recoleta implementation commit: `2e79f8b7`
- Huldra release-preparation commit: `0e8f8f4`
- Remote publication: neither branch has been pushed
- Phase: waiting for maintainer; automatic execution paused at external gates
- External publication: not started
- Visual publication: two local banner directions await maintainer review
- Credentials requested: none
- Maintainer account actions requested: PyPI/GitHub configuration documented
- Primary example: the running three-stream production fleet published at
  <https://neapolitanicecream.github.io/recoleta/>

## Evidence produced

- Added a bundled no-key production-fleet brief and `recoleta demo`; focused
  CLI tests pass and the wheel contains the snapshot.
- Built the full production fleet into an isolated output directory:
  5,284 HTML pages and 8,999 total files.
- Added site discovery metadata and verified 986 curated sitemap URLs, 4,298
  `noindex,follow` pages, English and Chinese Atom XML, canonical URLs, and
  language alternates.
- Prepared Huldra `0.4.2` with Trusted Publishing, release documentation,
  security policy, and passing release gates: Ruff, Pyright, 274 tests, wheel,
  source distribution, and Twine checks.
- Added Recoleta release workflows, package metadata, security policy, a dated
  production fleet case study, and a three-child redacted fleet example. Its
  full fleet day dry-run passes without contacting Huldra or a model.
- Generated two banner candidates under `docs/promotion/visuals/`; neither is
  referenced by a product surface.
- Added exact maintainer account instructions, a release process, channel-ready
  copy, an append-only launch ledger, and a voluntary public usage-receipt
  issue form.
- Passed the post-refactor Recoleta release gates: Ruff, Pyright, 1,047 tests,
  and Cremona with no new or worsened structural debt.
- Rebuilt the `0.6.1` wheel and source distribution, passed Twine checks,
  verified the bundled fleet snapshot and absence of `.DS_Store`, installed the
  wheel into a fresh Python 3.14 environment, and generated the no-key demo.
- Rebuilt the `runtime` container and passed main CLI, doctor-help, bundled
  demo, and Huldra CLI smoke checks.
- Captured and inspected five current live-fleet views—English desktop,
  Simplified Chinese desktop, representative Trend, source-linked finding, and
  mobile home—under the ignored local Playwright output for visual review.
- Archived all approved-for-review code, tests, workflows, copy, and evidence in
  local Git commits. The two generated banner candidates remain deliberately
  untracked, so pushing the branch cannot publish them before visual approval.
- Corrected the dry-run persistence leak found by the redacted fleet example:
  missing databases now use in-memory planning state, existing databases are
  opened read-only, and the real three-child dry-run creates no `.state`.

## Active work

1. Obtain maintainer visual direction; then create the exact-text social card
   and select from the fresh fleet screenshots for a second visual review.
2. Configure Huldra's PyPI Trusted Publisher, approve its release changes, and
   publish `huldra-arxiv 0.4.2`.
3. Replace Recoleta's Git dependency with the published Huldra range, update the
   lock, and repeat the clean-index and release gates.
4. Configure Recoleta's pending PyPI publisher and private vulnerability
   reporting; approve the final candidate and publish the release.
5. Verify PyPI, GHCR, the deployed fleet discovery files, and final URLs before
   submitting any channel material.

## Approval gates

The maintainer has already approved:

- rewriting or deleting stale generated documentation;
- using the current production fleet as the flagship example;
- maintaining Huldra as part of the dependency and release chain without making
  it a separate promotion campaign;
- preparing Show HN material, with the maintainer reviewing, submitting, and
  participating in the discussion;
- requesting narrowly scoped account access when an external action requires it.

Still requires explicit review or action:

- every replacement visual asset;
- disclosure of private fleet cost, failure, recipient, or team-identity data;
- PyPI Trusted Publisher, GitHub environment, and package-visibility settings;
- any external post or directory submission;
- routine autonomous posting under a project social account.

## Current bottleneck

Clean Recoleta index publication is sequenced behind Huldra `0.4.2` publication.
That external step requires the maintainer to configure PyPI and approve or
merge the prepared repository changes. Visual publication independently waits
for selection or rejection of the two local directions.

The third consecutive gate audit on 2026-07-25 confirmed that PyPI still serves
`huldra-arxiv 0.4.1`, returns 404 for `recoleta`, and has neither local
promotion branch on the GitHub remotes. There is no remaining in-scope action
that can advance publication without the maintainer's visual decision and
account-side configuration. See
[`checkpoints/2026-07-25-maintainer-gate.md`](./checkpoints/2026-07-25-maintainer-gate.md).

## Approach registry

| Family | Evidence | Exact gap | Status |
| --- | --- | --- | --- |
| No-key evaluation | bundled real brief, CLI tests, wheel inspection | clean index install | active |
| Production proof | public fleet case, redacted topology, full isolated build | external-user evidence | active |
| Search and syndication | metadata, Atom, sitemap, robots, full fleet validation | production deployment | ready |
| Package distribution | Huldra release candidate and both release workflows | account configuration and tags | blocked externally |
| Visual identity | two archived candidates | maintainer direction | awaiting review |
| Channel distribution | channel kit, account instructions, launch ledger | release URL, approved visuals, account actions | ready behind gates |
