# Index release-candidate checkpoint

Date: 2026-07-27

State: Huldra published; Recoleta `0.7.0` validated locally; no Recoleta
publication attempted.

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
| Pytest | 1,047 passed |
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

## Remaining gates

1. Commit and push the candidate.
2. Complete PR CI, cloud review, and thread resolution.
3. Merge, tag, and publish the Recoleta GitHub Release.
4. Verify PyPI and GHCR artifacts, then deploy and inspect the refreshed fleet.
5. Obtain final review before publishing any replacement visual.
6. Complete the account-only GHCR visibility and private vulnerability
   reporting actions before channel submissions.

No channel submission or external activation occurred at this checkpoint.
