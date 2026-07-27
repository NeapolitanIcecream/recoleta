# Promotion status

Last updated: 2026-07-27

## Current state

- Branch: `codex/promotion-readiness`
- Recoleta implementation commit: `2e79f8b7`
- Huldra release merge: `1b9a671`
- Remote publication: Huldra PR 7 is merged and
  <https://github.com/NeapolitanIcecream/huldra/releases/tag/v0.4.2> is
  published; its PyPI workflow is running. The Recoleta branch remains local.
- Phase: execution resumed after maintainer account confirmation and visual
  feedback
- External publication: not started
- Visual publication: no asset is public; the structure is approved and a
  themed three-asset replacement set awaits final review
- Credentials requested: none
- Maintainer account actions: both PyPI/GitHub publisher configurations
  confirmed complete on 2026-07-27
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
- Researched GOV.UK, Carbon, and Primer guidance and converted it into a
  Recoleta-specific visual contract: semantic images, replaceable colour roles,
  fixed grid and spacing, deliberate hierarchy, accessible fallbacks, and
  thumbnail verification.
- Produced an untracked deterministic SVG structure study that preserves three
  peer streams and one dominant publication while removing the generated
  collage layer. It passes browser rendering, 240 by 120 thumbnail, and
  grayscale legibility checks.
- Revalidated Huldra `0.4.2` after the maintainer configured publishing: Ruff,
  Pyright, 274 tests, clean wheel and source distribution, Twine, a fresh Python
  3.13 wheel install, and installed CLI smoke checks. PR 7 is open for CI and
  cloud review.
- Addressed PR 7's valid release review finding by comparing Huldra runtime and
  distribution versions before publication and adding an invariant test. Ruff,
  Pyright, and all 275 tests pass. Fresh CI succeeded, cloud Codex approved the
  current head, and all review threads were resolved.
- Squash-merged Huldra PR 7, created annotated tag `v0.4.2`, and published the
  matching GitHub Release. Trusted Publishing workflow 30235829971 is running.
- Promoted the approved visual structure into a local second-review set:
  repository banner, exact-text social card, and real-fleet proof board. The set
  uses current site roles, not a colour inferred from the first comparison.
- Verified all three assets with Chromium and SVG parsing. The banner remains
  legible at 240 by 120, the social card at 300 by 158, both survive grayscale,
  and all text-role pairs meet at least 4.5:1 contrast.

## Active work

1. Obtain maintainer approval or revisions for the themed banner, social card,
   and real-fleet proof board.
2. Verify Huldra workflow 30235829971 and `huldra-arxiv 0.4.2` on PyPI.
3. Replace Recoleta's Git dependency with the verified Huldra range, update the
   lock, and repeat the clean-index and release gates.
4. Use Recoleta's configured pending publisher, enable private vulnerability
   reporting, approve the final candidate, and publish the release.
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
- container package visibility after its first publication;
- private vulnerability reporting;
- any external post or directory submission;
- routine autonomous posting under a project social account.

## Current bottleneck

Clean Recoleta index publication remains sequenced behind Huldra `0.4.2`, but
the account-side blocker is resolved. Huldra PR 7 is merged, its `v0.4.2`
Release exists, and the Trusted Publishing workflow is running. Recoleta still
returns HTTP 404 on PyPI until the Huldra artifact is verified and its Git
dependency is replaced.

Visual publication remains independently gated. The structure is approved. The
current banner, social card, and real-fleet proof board need one final review
before they replace public assets.

## Approach registry

| Family | Evidence | Exact gap | Status |
| --- | --- | --- | --- |
| No-key evaluation | bundled real brief, CLI tests, wheel inspection | clean index install | active |
| Production proof | public fleet case, redacted topology, full isolated build | external-user evidence | active |
| Search and syndication | metadata, Atom, sitemap, robots, full fleet validation | production deployment | ready |
| Package distribution | Huldra PR merged, v0.4.2 Release published, configured publishers, both release workflows | Huldra workflow result, Recoleta dependency and release | active |
| Visual identity | approved structure, sourced constraints, themed banner, social card, real-fleet proof board | final asset review and public replacement | awaiting review |
| Channel distribution | channel kit, account instructions, launch ledger | release URL, approved visuals, account actions | ready behind gates |
