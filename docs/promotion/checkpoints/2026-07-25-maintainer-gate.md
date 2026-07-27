# Maintainer-gate audit

Date: 2026-07-25

State: local preparation complete; external execution paused.

This audit tests the full promotion-preparation objective against current local
and public state. It does not treat the existence of a plan as evidence that a
requirement is complete.

## Requirement audit

| Requirement | Authoritative evidence | Finding |
| --- | --- | --- |
| Use the real production fleet as the primary example | README, dated fleet case study, public three-stream site, redacted topology, isolated full build | complete locally |
| Replace stale positioning | active README, package metadata, current GitHub handoff, channel kit | complete locally; `local-first` appears only in historical context or explicit prohibitions |
| Improve first evaluation | bundled fleet brief, `recoleta demo`, fresh-wheel install, container smoke, demo tests | complete locally |
| Improve public discovery | canonical and social metadata, language alternates, Atom, curated sitemap, robots policy, full-fleet validation | complete locally; production deployment awaits release |
| Prepare a package and container release chain | Recoleta commit `2e79f8b7`, Huldra commit `0e8f8f4`, Trusted Publishing workflows, GHCR workflow, release runbooks | complete locally; account and publication gates remain |
| Prepare executable channel materials | release body, Show HN title and fact card, Changelog and PyCoder fields, optional Bluesky pilot, response boundaries | complete locally |
| Preserve process and conclusions outside chat | promotion archive, decisions, research baseline, validation checkpoint, launch ledger, local Git commits | complete |
| Keep visuals private until review | two banner candidates untracked; five fleet captures ignored; neither promotion branch exists remotely | satisfied; selection pending |
| Avoid unauthorized account or external actions | no remote promotion branch, no external submission, no Recoleta PyPI project, Huldra remains at `0.4.1` | satisfied; authorization/configuration pending |

## Public-state recheck

- `https://pypi.org/pypi/recoleta/json`: HTTP 404.
- `https://pypi.org/pypi/huldra-arxiv/json`: latest version `0.4.1`.
- Recoleta remote branch `codex/promotion-readiness`: absent.
- Huldra remote branch `codex/promotion-readiness`: absent.
- External attempts recorded in the launch ledger: zero.

## Why execution pauses here

No remaining safe local edit can substitute for either missing input:

1. choosing a banner direction is a visual judgment explicitly reserved for the
   maintainer;
2. creating GitHub environments and PyPI Trusted Publishers requires the
   maintainer's signed-in account;
3. Recoleta cannot replace its direct Git dependency with an index constraint
   until Huldra `0.4.2` exists on PyPI;
4. release URLs, container digests, refreshed production discovery files, and
   channel submissions cannot be truthfully verified before publication.

Further speculative copy, visual variants, or release changes would add review
surface without advancing a blocked dependency.

## Resume signals

Any one of these responses resumes useful work:

```text
Banner: A
Banner: B
Banner: neither — <revision direction>
Huldra publisher ready
Recoleta pending publisher ready
```

Visual approval and publisher configuration are independent; the maintainer may
provide them in separate messages. No password, token, app password, recovery
code, cookie, or other secret should be sent.
