# Index release-candidate checkpoint

Date: 2026-07-27

State: Huldra published; Recoleta `0.7.0` validated and committed as
`07ce0946`; [Recoleta PR 78](https://github.com/NeapolitanIcecream/recoleta/pull/78)
is open; no Recoleta package publication attempted.

## Huldra publication proof

- PR 7 was squash-merged as `1b9a671`.
- The annotated `v0.4.2` tag and
  [GitHub Release](https://github.com/NeapolitanIcecream/huldra/releases/tag/v0.4.2)
  point to that merge.
- [Trusted Publishing workflow 30235829971](https://github.com/NeapolitanIcecream/huldra/actions/runs/30235829971)
  completed successfully.
- PyPI reports `huldra-arxiv 0.4.2`.
- Wheel SHA-256:
  `98f0cc6cc11de44641829e89affbf9fe7c2d682be7d0c7e81598aaa69d95d34d`.
- Source-distribution SHA-256:
  `d865f4160eb72194a4e7b10573103f89d08cb03329ef5c8abb5ac97a079567bb`.

## Recoleta candidate

- Version: `0.7.0`.
- Standard dependency: `huldra-arxiv>=0.4.2,<0.5`.
- Lock source: PyPI registry, with the published wheel and
  source-distribution hashes above.
- Changelog date: 2026-07-27.
- No direct Git dependency remains in project or wheel metadata.

## Verification

| Gate | Result |
| --- | --- |
| Ruff | passed |
| Pyright | 0 errors, 0 warnings |
| Pytest | 1,051 passed after five PR review corrections |
| Wheel and source distribution | built |
| Twine | both distributions passed |
| Wheel contents | bundled fleet brief present; `.DS_Store` absent |
| Wheel metadata | Recoleta `0.7.0`; Huldra range present; no direct reference |
| Fresh Python 3.14 install | resolved Huldra `0.4.2` from PyPI; CLI and no-key demo passed |
| Redacted fleet | three-child day dry-run passed; no example `.state` created |
| Runtime container | Recoleta `0.7.0`; Huldra runtime and distribution `0.4.2`; CLI and demo passed |

No new test was added for the source change. The changed contract is package
metadata and index resolution, so wheel inspection and an unlocked install in a
fresh environment are more direct oracles than a unit test. The existing
source-adapter tests and full suite protect runtime API compatibility.

## PR review correction

Cloud review found that configured-path `site build` and `site stage` still
passed `public_site_url` as a direct keyword after the build exporter moved that
value into `SiteExportOptions`. Both commands failed before producing output.

Two CLI regression tests reproduce the direct `PUBLIC_SITE_URL` build path and
the inherited `EMAIL.public_site_url` staging path. Both failed with the
reported unexpected-keyword error before the fix. The build command now creates
`SiteExportOptions`, while staging omits the rendering-only value.

A same-mode search ruled out the same removed-keyword failure in workflow,
fleet, deploy, demo, and materialization call sites. It did not prove that every
separate rebuild path propagated the configured URL; the later repair finding
below closes that distinct omission. No new log or metric was added because the
existing command success and exception boundary already identifies this wiring
failure.

## Further PR review corrections

Current-head reviews identified four additional output-contract defects:

1. `repair outputs --site` did not propagate the configured public URL through
   `MaterializeOutputsRequest`, so a repaired site silently lost canonical
   links, feeds, sitemap, and robots metadata.
2. `recoleta demo` loaded its manifest before atomically moving the generated
   site. The returned JSON and persisted `manifest.json` therefore named a
   deleted temporary output directory and an installation-specific source
   directory.
3. GitHub Pages preparation generated discovery metadata and files, then
   removed the safe `discovery` field while sanitizing public manifests. The
   deployed branch therefore kept sitemap and feed files but stopped exposing
   their canonical manifest metadata.
4. Generated Atom feeds provided no author on the feed or its entries. Feeds
   with entries therefore violated Atom's author requirement and could be
   rejected by standards-compliant consumers.

An end-to-end repair regression test asserts that a configured public URL
reaches the final discovery manifest and produces `sitemap.xml` and
`robots.txt`. A demo regression test asserts that returned and persisted
manifests agree and that their output and source-artifact paths exist inside the
final snapshot. Both tests failed for the reported reasons before the fixes.

The repair command now uses the shared settings resolver, carries the URL
through the typed materialization request, and constructs `SiteExportOptions`
at the exporter boundary. The demo rewrites the manifest to its final output
and copied `artifacts` directory before the atomic move. Deployment sanitization
now preserves the exporter-owned `discovery` field while continuing to omit
private input, output, and generation metadata. A same-mode search found no
other product command that moves a generated site while returning its pre-move
manifest, and the single public-manifest sanitizer covers root and language
manifests. The shared feed writer now adds a feed-level `Recoleta` author, which
all entries and the copied default root feed inherit. The existing JSON, XML,
and manifest artifacts are the direct observable contracts, so no additional
log or metric was warranted.

After these changes, Ruff, Pyright, the 22 tests across the repair and demo
files, all 11 deployment tests, both discovery tests, and all 1,051 tests pass.
The exact corrected source rebuilt into a wheel and source distribution that
pass Twine. The fresh Python 3.14 wheel install performed after the repair and
demo corrections resolved `huldra-arxiv 0.4.2`, reported Recoleta `0.7.0`, and
generated a no-key demo whose persisted manifest paths all resolve inside the
final snapshot.

## Remaining gates

1. Complete PR CI, cloud review, and thread resolution.
2. Merge, tag, and publish the Recoleta GitHub Release.
3. Verify PyPI and GHCR artifacts, then deploy and inspect the refreshed fleet.
4. Obtain final review before publishing any replacement visual.
5. Complete the account-only GHCR visibility and private vulnerability
   reporting actions before channel submissions.

No channel submission or external activation occurred at this checkpoint.
