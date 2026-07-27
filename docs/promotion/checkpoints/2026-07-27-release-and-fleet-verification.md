# Recoleta 0.7.0 release and fleet verification

Date: 2026-07-27

State: Recoleta `0.7.0` is published; the production fleet has been rebuilt
from the exact release commit and deployed through GitHub Pages.

## Release identity

- [PR 78](https://github.com/NeapolitanIcecream/recoleta/pull/78) was
  squash-merged as `3e2a59c572f2eff40bdbdbe625938a7ee70fe5e5`.
- Annotated tag `v0.7.0` resolves to that exact commit.
- The matching
  [GitHub Release](https://github.com/NeapolitanIcecream/recoleta/releases/tag/v0.7.0)
  was published at 2026-07-27T08:17:01Z.
- [PyPI workflow 30249302633](https://github.com/NeapolitanIcecream/recoleta/actions/runs/30249302633)
  and
  [container workflow 30249302675](https://github.com/NeapolitanIcecream/recoleta/actions/runs/30249302675)
  both completed successfully on the merge commit.

## Public artifacts

[PyPI](https://pypi.org/project/recoleta/0.7.0/) reports:

- version `0.7.0`;
- Python requirement `>=3.14`;
- standard dependency `huldra-arxiv>=0.4.2,<0.5`;
- wheel `recoleta-0.7.0-py3-none-any.whl`, SHA-256
  `50534122b760b83ef03e1abd0b537c46fa790fad2d6a39399477dbba70f3b38b`;
- source distribution `recoleta-0.7.0.tar.gz`, SHA-256
  `60aeaad579834ee73f04dc90595001a38c97d6f1863b464b3d681c324329899e`.

Anonymous GHCR manifest requests returned HTTP 200 for `0.7.0`, `0.7`, and
`latest`. All three tags resolve to the same OCI image index:

`sha256:9e11855ad4ae2f96fe851151124864c6ac2c34890ccc4dc28520dc8d00a9ad79`

This anonymous check also establishes that the container is already public; no
separate visibility change is required.

### Container architecture correction

A later runtime smoke found that the public OCI index contains one
`linux/amd64` image plus its attestation manifest. It does not contain a
`linux/arm64` image, so a default pull fails on Apple Silicon with `no matching
manifest`.

The explicit `linux/amd64` image passed CLI startup and reported Recoleta
`0.7.0` with Huldra `0.4.2`. A native local `linux/arm64` build of the same
runtime target also passed those checks. This isolates the defect to publication
configuration rather than application or Dockerfile compatibility.

PR 79 corrected the publication workflow and was squash-merged as
`89116739bfed3c57b17a7b4f44f1c1925197eeab`. Guarded replay run
[30259934268](https://github.com/NeapolitanIcecream/recoleta/actions/runs/30259934268)
then succeeded with `version=0.7.0` and `update_floating_tags=true`.

Anonymous registry requests now show that `0.7.0`, `0.7`, and `latest` all
resolve to:

`sha256:829e5dcf6239e0f84ae06353e7c676060f7fab508301a119902e6c1f013772ba`

The index contains real `linux/amd64` and `linux/arm64` images plus matching
attestations. A default pull on an arm64 Docker host selected the native arm64
image; Recoleta and Huldra CLI smokes passed, and installed metadata reported
Recoleta `0.7.0` with Huldra runtime and distribution version `0.4.2`. The
container correction gate is closed.

## Fleet deployment

The fleet was rebuilt with translation disabled from a clean worktree pinned to
the release commit. Existing maintained outputs were materialized and deployed;
no source ingestion or model synthesis was rerun.

- GitHub Pages branch commit:
  `2855fd0ebda2f50ac575d9f73d9374733bf3c82b`
- GitHub Pages build: `built`, with no reported error
- Public site: <https://neapolitanicecream.github.io/recoleta/>
- Languages: English and Simplified Chinese
- Trend briefs: 244
- Idea briefs: 244
- Linked source notes: 1,362
- Indexable pages: 986
- Reachable but `noindex,follow` pages: 4,298

The visible research snapshot remains dated through 2026-07-23. This step
verifies release rendering and deployment; it does not claim that new research
content was generated on release day.

## Independent HTTPS checks

The following public surfaces returned HTTP 200 after the Pages build:

- root and public manifest;
- `sitemap.xml` and `robots.txt`;
- root, English, and Simplified Chinese Atom feeds;
- the selected English Software Intelligence brief and its Chinese counterpart.

Additional checks established:

- the sitemap is valid XML and contains 986 unique URLs;
- no sitemap URL contains an unencoded space, fragment delimiter, or query
  delimiter;
- all three Atom documents are valid XML, contain 13 entries, declare
  `Recoleta` as feed author, and identify their own public URL in `rel=self`;
- the representative trend declares `index,follow`, a canonical URL, Open Graph
  fields, and English, Chinese, and `x-default` alternates;
- a linked source note declares `noindex,follow` while retaining its canonical
  URL and source link;
- Chromium loaded the home page and representative trend at desktop and mobile
  widths with no console errors or warnings; navigation, language switching,
  source links, and the responsive reading layout remained present.

These checks establish that the release and maintained fleet surfaces are
public and internally consistent. They do not count as an external activation.

## Security intake

Private vulnerability reporting was enabled for both Recoleta and Huldra
through the GitHub repository API. Independent reads of both settings returned
`enabled=true`.

## Repository social preview

The maintainer selected
`docs/assets/recoleta-social-preview.png` in GitHub's authenticated repository
settings. The post-upload settings view displayed the approved composition and
copy. GitHub GraphQL then returned the public repository-image URL, and a fresh
download was byte-identical to the versioned PNG.

- source dimensions: 1200 by 630 pixels;
- source SHA-256:
  `b246908fca0a9eea4f773b194a66c32fb447fc5a64c53ae6e97b4a61ce883ab1`;
- headline: `Research radars that publish traceable trends and ideas.`;
- supporting copy names the Software Intelligence and Embodied AI public
  research and invites readers to try Recoleta without an API key.

The public download and versioned source have the same SHA-256 listed above.
The social-preview gate is closed.

## Next gate

Use the non-postable Show HN fact sheet and checklist in
[`../show-hn-handoff.md`](../show-hn-handoff.md). The maintainer must write and
submit all Hacker News text by hand under the current platform rules. No channel
submission has been made.
