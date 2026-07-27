# Release process

Recoleta releases are published from a tagged commit through GitHub Actions.
PyPI authentication uses Trusted Publishing; the container workflow publishes
the same GitHub Release to GHCR for `linux/amd64` and `linux/arm64`, with
provenance and an SBOM.

## Dependency order

Recoleta's standard installation contains Huldra. Publish a compatible
`huldra-arxiv` release before creating a Recoleta tag:

1. Complete Huldra's release checks and publish `huldra-arxiv 0.4.2`.
2. Confirm the version through <https://pypi.org/pypi/huldra-arxiv/json>.
3. Replace Recoleta's reviewed Git direct reference with
   `huldra-arxiv>=0.4.2,<0.5`.
4. Run `uv lock` and inspect the dependency diff.
5. Set Recoleta's promotion release version and date the changelog.

The publishing workflow rejects any project dependency containing a direct
reference, so the sequence fails closed if Huldra is not ready.

## Validate the candidate

Run:

```bash
uv sync --group dev
uv run ruff check .
uv run pyright
uv run pytest
uv build
uv run --with twine twine check dist/*
```

Install the built wheel in a temporary Python 3.14 environment and verify the
no-key path:

```bash
release_tmp=$(mktemp -d)
uv venv "$release_tmp/venv" --python 3.14
uv pip install --python "$release_tmp/venv/bin/python" dist/*.whl
"$release_tmp/venv/bin/recoleta" demo \
  --output-dir "$release_tmp/demo" \
  --json
"$release_tmp/venv/bin/recoleta" --help
```

Build the default container and inspect both entry points:

```bash
docker build --target runtime -t recoleta:release-candidate .
docker run --rm recoleta:release-candidate --help
docker run --rm --entrypoint huldra recoleta:release-candidate --help
```

Run the redacted fleet topology without source or model side effects:

```bash
cd examples/production-fleet
uv run --project ../.. recoleta fleet run day \
  --manifest fleet.yaml \
  --dry-run \
  --json
```

Build the private production fleet into an isolated output path and verify
representative English and Chinese pages, canonical URLs, language alternates,
feeds, sitemap XML, robots policy, no-index counts, and a generated page whose
filename requires URL percent-encoding. Do not overwrite the public deployment
during validation.

## Tag and publish

After the candidate commit is merged:

```bash
git tag -a v0.7.0 -m "Release v0.7.0"
git push origin main v0.7.0
```

Create and publish a GitHub Release for that exact tag. The PyPI workflow checks
that the tag, package version, and checked-out commit match before building. Its
unprivileged job produces and checks the distributions; a separate job receives
only `id-token: write` and publishes the stored artifacts.

To retry PyPI publication for an existing tag, run **Publish to PyPI** manually
and enter the version without the `v` prefix. The workflow checks out that exact
tag before verification and build, regardless of the branch selected when the
manual run is started.

The release event also publishes:

- `ghcr.io/neapolitanicecream/recoleta:0.7.0`
- `ghcr.io/neapolitanicecream/recoleta:0.7`
- `ghcr.io/neapolitanicecream/recoleta:latest`

The container workflow checks out the release tag and rejects it unless it
matches both the package version and checked-out commit before registry login or
image publication. Prereleases receive versioned tags but never move the stable
`latest` tag.

To rebuild an existing tag—for example, to repair a missing target
architecture—run **Publish container** manually, enter the version without the
`v` prefix, and select whether a stable `X.Y.Z` release should update `latest`.
The workflow checks out that exact tag and repeats the tag, commit, and package
version checks before publishing. A prerelease-shaped version cannot update
`latest` through the manual path.

Verify anonymous registry access after the first publication. If the package is
not public, follow
[`docs/promotion/maintainer-actions.md`](../promotion/maintainer-actions.md)
before advertising the image.

## Post-release checks

From a clean environment:

```bash
uvx recoleta==0.7.0 demo --output-dir recoleta-demo --json
docker pull ghcr.io/neapolitanicecream/recoleta:0.7.0
docker run --rm ghcr.io/neapolitanicecream/recoleta:0.7.0 --help
docker run --rm --platform linux/amd64 \
  ghcr.io/neapolitanicecream/recoleta:0.7.0 --help
docker run --rm --platform linux/arm64 \
  ghcr.io/neapolitanicecream/recoleta:0.7.0 --help
```

Then:

1. deploy the full production fleet site with its canonical public URL;
2. validate the sitemap, feeds, and selected public brief over HTTPS;
3. confirm the PyPI metadata, release artifacts, and both container platforms;
4. confirm private vulnerability reporting;
5. start the channel sequence only after all checks pass.
