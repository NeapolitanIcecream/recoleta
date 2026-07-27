# Promotion status

Last updated: 2026-07-27

## Current state

- Release branch: `codex/promotion-readiness`, squash-merged by PR 78 as
  `3e2a59c5`
- Recoleta release: `0.7.0`
- Huldra release merge: `1b9a671`
- Remote publication: Huldra PR 7 is merged and
  <https://github.com/NeapolitanIcecream/huldra/releases/tag/v0.4.2> is
  published; its release workflow succeeded and PyPI serves version `0.4.2` of
  `huldra-arxiv`. Recoleta
  [PR 78](https://github.com/NeapolitanIcecream/recoleta/pull/78) is merged,
  the [0.7.0 release](https://github.com/NeapolitanIcecream/recoleta/releases/tag/v0.7.0)
  is published, PyPI serves `recoleta 0.7.0`, and the public GHCR tags
  `0.7.0`, `0.7`, and `latest` resolve to the same OCI image. That image
  currently contains `linux/amd64` only.
- Phase: repair and replay the `0.7.0` container as a verified amd64/arm64 image,
  then publish the approved visual set
- External publication: package, source distribution, and release complete; the
  public container is available for amd64 while the arm64 repair is pending; no
  channel submission attempted
- Visual publication: the maintainer approved the final three-asset set on
  2026-07-27; stable copies are on the current branch and remain unpublished
  until that versioned change is reviewed and merged
- Credentials requested: none
- Maintainer account actions: both PyPI/GitHub publisher configurations
  confirmed complete on 2026-07-27
- Primary example: the maintained bilingual production fleet published at
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
  matching GitHub Release. Trusted Publishing workflow 30235829971 succeeded,
  and PyPI serves the matching wheel and source distribution.
- Replaced Recoleta's pinned Huldra Git revision with
  `huldra-arxiv>=0.4.2,<0.5`, resolved the lock to the PyPI wheel and source
  distribution hashes, set the candidate version to `0.7.0`, and dated the
  changelog.
- Revalidated the exact `0.7.0` candidate: Ruff, Pyright, all 1,049 tests,
  wheel and source distribution, Twine, package contents, index-only fresh
  installation, no-key demo, three-child dry-run, and runtime container all
  passed. Fresh and container checks both reported Recoleta `0.7.0` with
  Huldra runtime and distribution version `0.4.2`.
- Addressed PR 78's valid site-command review finding. Configured public URLs
  now reach the build exporter through `SiteExportOptions`, while source staging
  omits the rendering-only option. Two regression tests failed before the fix
  and pass after it; Ruff, Pyright, the 28-test site CLI file, and all 1,049
  tests pass.
- Addressed two further PR 78 findings. `repair outputs --site` now preserves
  the configured public URL and generates canonical discovery artifacts; the
  bundled demo now rewrites both returned and persisted manifest paths to the
  final snapshot instead of a deleted temporary tree. Both regression tests
  failed for the reported reasons before the fixes and pass afterward. Ruff,
  Pyright, both affected test files, and all 1,051 tests pass. A rebuilt wheel
  and source distribution pass Twine, and a fresh Python 3.14 wheel install
  produces a demo whose manifest paths all resolve inside the final snapshot.
- Addressed PR 78's deployment-manifest finding. GitHub Pages manifest
  sanitization now preserves the exporter-owned `discovery` field while still
  removing private source and output paths. The deployed-branch regression
  failed with a missing field before the fix and passes afterward; Ruff,
  Pyright, all 11 deployment tests, and all 1,051 tests pass. Rebuilt
  distributions pass Twine.
- Addressed PR 78's Atom conformance finding. Every generated language feed now
  supplies a feed-level `Recoleta` author inherited by its entries, including
  the default-language root feed. The XML regression failed with no
  author before the fix and passes afterward; Ruff, Pyright, both discovery
  tests, and all 1,051 tests pass.
- Addressed two more PR 78 findings. Manual PyPI recovery now checks out the
  requested existing tag and verifies that tag against the checked-out `HEAD`.
  Explicit-path build and build-before-serve commands now accept
  `--public-site-url` or `PUBLIC_SITE_URL` without loading full runtime
  settings. Three regressions failed before the fixes and pass afterward;
  Ruff, Pyright, 29 affected-file tests, and all 1,052 tests pass. A real
  explicit-path build produced discovery files, and rebuilt distributions pass
  Twine.
- Addressed two current-head PR 78 findings. Public URL validation now happens
  before either managed exporter can replace prior output, and the multilingual
  root Atom alias now declares its own `/feed.xml` self URL. Three regression
  cases failed before the fixes and pass afterward; all 29 export/discovery
  tests pass.
- Addressed the current-head container publication findings. The workflow now
  rejects a release tag that differs from the package version before registry
  login, and only stable releases can move `latest`. Two workflow regressions
  failed before the fixes and pass afterward.
- Addressed two current-head discovery findings. Every generated public page
  path is now percent-encoded before it reaches canonical, alternate, sitemap,
  or Atom URLs, and the feed resolver decodes internal homepage href paths
  before checking the corresponding file. Both regressions failed for their
  reported symptoms before the fix and pass afterward; Ruff, Pyright, all 31
  export/discovery tests, and all 1,058 tests pass. A real Chromium navigation
  followed a link containing spaces, `#`, `?`, and CJK text to the intended
  page over HTTP.
- Promoted the approved visual structure into a local second-review set:
  repository banner, exact-text social card, and real-fleet proof board. The set
  uses current site roles, not a colour inferred from the first comparison.
- Verified all three assets with Chromium and SVG parsing. The banner remains
  legible at 240 by 120, the social card at 300 by 158, both survive grayscale,
  and all text-role pairs meet at least 4.5:1 contrast.
- Squash-merged Recoleta PR 78 as `3e2a59c5`, pushed annotated tag `v0.7.0` at
  that exact commit, and published the matching GitHub Release.
- Both release workflows passed on the merge commit. PyPI exposes the
  `0.7.0` wheel and source distribution with the expected Python requirement
  and `huldra-arxiv>=0.4.2,<0.5` dependency. Anonymous GHCR requests resolve
  `0.7.0`, `0.7`, and `latest` to
  `sha256:9e11855ad4ae2f96fe851151124864c6ac2c34890ccc4dc28520dc8d00a9ad79`.
- A post-release runtime smoke found that the OCI index contains one
  `linux/amd64` image plus its attestation, not an arm64 image. A default pull
  therefore fails on Apple Silicon. The published amd64 variant runs Recoleta
  `0.7.0` with Huldra `0.4.2`, and a native local arm64 build of the same
  runtime target also passes CLI and version smokes.
- The maintainer approved the revised banner, social card, and fleet proof
  board after the social-card and proof-board copy was simplified.
- Rebuilt and deployed the maintained fleet from a clean worktree pinned to
  release commit `3e2a59c5`, without rerunning translation or model synthesis.
  GitHub Pages built branch commit `2855fd0e` successfully.
- Independently verified the public manifest, 986-URL sitemap, robots policy,
  three Atom feeds, English and Chinese representative briefs, canonical and
  language metadata, index/no-index policy, and desktop/mobile Chromium
  rendering. All checked URLs returned HTTP 200 and the browser reported no
  console errors or warnings.
- Enabled private vulnerability reporting for both Recoleta and Huldra through
  the GitHub repository API, then independently read both settings back as
  enabled.
- Replaced the repository's stale `local-first` About description and removed
  `local-first`, `digital-garden`, `obsidian`, generic `ai`, and
  `developer-tools` topics. The public About text, website, and ten focused
  topics now match the approved handoff.

## Active work

1. Add amd64/arm64 container publication and a safe existing-tag replay path,
   merge it, replay `v0.7.0`, and verify both public platforms.
2. Publish the approved visual set through a separate versioned change and
   upload the approved social preview.
3. Prepare the maintainer-reviewed Show HN package, then stage later channel
   submissions according to the launch order.

## Approval gates

The maintainer has already approved:

- rewriting or deleting stale generated documentation;
- using the current production fleet as the flagship example;
- maintaining Huldra as part of the dependency and release chain without making
  it a separate promotion campaign;
- preparing Show HN material, with the maintainer reviewing, submitting, and
  participating in the discussion;
- requesting narrowly scoped account access when an external action requires it;
- the final revised banner, social card, and production-fleet proof board.

Still requires explicit review or action:

- disclosure of private fleet cost, failure, recipient, or team-identity data;
- any external post or directory submission;
- routine autonomous posting under a project social account.

## Current bottleneck

The package and fleet deployment gates are complete, but the first public
container is amd64-only. The next outcome-facing gate is republishing the same
release tag as a verified amd64/arm64 image without weakening tag/version or
stable-`latest` safeguards.

## Approach registry

| Family | Evidence | Exact gap | Status |
| --- | --- | --- | --- |
| No-key evaluation | bundled real brief, CLI tests, public wheel and source distribution, successful public-index `uvx` smoke | external-user evidence | ready |
| Production proof | public fleet case, redacted topology, refreshed public deployment | external-user evidence | active |
| Search and syndication | deployed metadata, Atom, 986-URL sitemap, robots, HTTPS and Chromium validation | syndication discovery | ready |
| Package distribution | Huldra 0.4.2 and Recoleta 0.7.0 on PyPI; public versioned and stable GHCR tags; clean public-index command smoke | arm64 GHCR variant | repair active |
| Visual identity | approved banner, social card, and real-fleet proof board | versioned public replacement | approved |
| Channel distribution | channel kit, account instructions, launch ledger, live release URL | merged visuals and maintainer-reviewed Show HN package | ready behind gates |
