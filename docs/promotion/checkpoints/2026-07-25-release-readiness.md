# Release-readiness checkpoint

Date: 2026-07-25

State: local implementation and release validation complete; no external
publication attempted.

## Objective and fixed constraints

The sprint is preparing Recoleta for attributable adoption without requiring
the maintainer to write launch material or conduct routine outreach.

The production fleet is the flagship proof. `local-first` is not treated as a
maintainer thesis. Huldra is managed as release infrastructure rather than
promoted as a separate product. Replacement visuals remain unpublished until
the maintainer reviews them. Private fleet costs, failures, recipients, and
team identity are outside the public evidence set.

## Implemented routes

1. A no-key `recoleta demo` path renders a bundled, redacted brief derived from
   the running production fleet and reports that it made no network or model
   calls. The bundled sample is explicitly not counted as activation.
2. The public-site exporter can emit canonical URLs, language alternates,
   Open Graph and Twitter metadata, Atom feeds, a curated sitemap, robots
   policy, and explicit no-index metadata.
3. A dated public case study and a redacted three-stream fleet manifest explain
   the real deployment without publishing private operational data.
4. Recoleta and Huldra have Trusted Publishing release workflows and documented
   release gates. Recoleta also has a GHCR workflow and image smoke coverage.
5. A channel kit, account-action runbook, append-only launch ledger, and public
   voluntary usage-receipt form separate reach from qualified activation.

## Validation evidence

### Recoleta

| Gate | Result |
| --- | --- |
| Ruff | passed |
| Pyright | 0 errors, 0 warnings |
| Pytest | 1,047 passed |
| Cremona | 0 new, 0 worsened structural-debt findings |
| Full isolated fleet build | 5,284 HTML pages; 8,999 total files |
| Discovery output | 986 sitemap URLs; 4,298 no-index pages; English and Chinese Atom feeds |
| Wheel and source distribution | built; Twine checks passed |
| Wheel contents | bundled fleet brief present; `.DS_Store` absent |
| Fresh Python 3.14 wheel install | CLI and no-key demo passed |
| Runtime container | rebuilt; main CLI, doctor-help, no-key demo, and Huldra CLI smokes passed |
| Redacted fleet example | full day dry-run passed without source or model calls |

### Huldra

| Gate | Result |
| --- | --- |
| Candidate version | `0.4.2` |
| Ruff | passed |
| Pyright | passed |
| Pytest | 274 passed |
| Wheel and source distribution | built; Twine checks passed |

## Local Git archive

- Recoleta: branch `codex/promotion-readiness`, implementation commit
  `2e79f8b7`.
- Huldra: branch `codex/promotion-readiness`, release-preparation commit
  `0e8f8f4`.
- Neither branch has been pushed.
- The two generated banner candidates remain untracked local files. The five
  live-fleet screenshots remain under ignored Playwright output. This keeps
  every visual outside remote Git history until the maintainer reviews it.

## Corrections discovered by the gates

- The first real container build found that the builder copied
  `pyproject.toml` but not the referenced `LICENSE`. The Dockerfile now copies
  the license before project installation, and the image rebuild passed.
- The initial site-discovery implementation created new structural hotspots.
  Metadata, language, feed, sitemap, robots, and export orchestration were split
  along their change axes. The focused tests and full suite passed, and Cremona
  then reported no regression.
- The first ad hoc clean-install smoke used a host `python` command that is not
  present in this `uv`-managed environment and passed the obsolete option
  `--output`. The release instructions and final smoke use `uv venv` and
  `--output-dir`.
- Running `doctor` without a database is expected to fail. Container readiness
  therefore claims only a doctor-command help smoke; it does not claim a live
  health check against an uninitialized image.
- The release-process example incorrectly repeated `recoleta` after an image
  whose entry point is already `recoleta`. Both pre-release and post-release
  examples were corrected.
- The redacted fleet dry-run initially created three empty SQLite schemas even
  though it made no source or model calls. Dry-run planning now opens an
  existing database read-only or uses an in-memory empty schema when it is
  absent. Regression tests cover missing and existing single-instance state as
  well as missing fleet-child state; the real three-child example was rerun and
  created no `.state` directory.

## Remaining gate

The next executable dependency is external:

1. the maintainer selects or rejects the two visual directions;
2. the maintainer configures the exact Huldra and Recoleta Trusted Publishers;
3. Huldra `0.4.2` is approved, merged, tagged, and published;
4. Recoleta replaces the Git dependency with the published Huldra constraint
   and repeats clean-index validation;
5. only then are Recoleta, the refreshed fleet site, and channel submissions
   published.

The exact UI steps and confirmation phrases are in
[`../maintainer-actions.md`](../maintainer-actions.md). Channel copy is in
[`../channel-kit.md`](../channel-kit.md). External results must be appended to
[`../launch-log.md`](../launch-log.md), including zero-result attempts.
