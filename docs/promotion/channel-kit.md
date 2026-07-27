# Promotion channel kit

Last updated: 2026-07-27

Publication status: draft; release and fleet are live, but wait for the
multi-architecture container replay and social-preview gate

## Source-of-truth links

- Repository: <https://github.com/NeapolitanIcecream/recoleta>
- Release:
  <https://github.com/NeapolitanIcecream/recoleta/releases/tag/v0.7.0>
- PyPI: <https://pypi.org/project/recoleta/0.7.0/>
- Container: <https://github.com/NeapolitanIcecream/recoleta/pkgs/container/recoleta>
- Running fleet: <https://neapolitanicecream.github.io/recoleta/>
- Fleet case study:
  <https://github.com/NeapolitanIcecream/recoleta/blob/main/docs/guides/production-fleet-case-study.md>
- Selected public brief:
  <https://neapolitanicecream.github.io/recoleta/en/trends/software-intelligence--day--2026-07-23--trend--2079.html>
- Voluntary usage receipt:
  <https://github.com/NeapolitanIcecream/recoleta/issues/new?template=activation_receipt.yml>

Do not submit the old preset as the primary example. Do not call the project
`local-first`, a fact checker, or independently adopted. The public fleet is
sustained maintainer dogfooding.

## Launch order

1. Publish `huldra-arxiv 0.4.2`.
2. Replace Recoleta's Git dependency with the published version range, set the
   promotion release version, and pass clean-install gates.
3. Publish the Recoleta GitHub Release, PyPI distribution, public GHCR image,
   and refreshed fleet site.
4. Wait for the release smoke checks, then submit Show HN.
5. Submit the release to PyCoder's Weekly and Changelog News on separate days.
6. If approved, start a four-post, 28-day Bluesky pilot.
7. Record each attempt and attributable outcome in
   [`launch-log.md`](./launch-log.md).

Steps 1–3 are complete except for repairing the public container's missing
arm64 variant. Do not begin step 4 until the replayed image passes anonymous
amd64 and arm64 checks and the approved social preview is uploaded.

Staggering submissions makes failures diagnosable and attribution less
ambiguous. It also avoids asking several communities to inspect a release while
its permanent distribution surfaces are still changing.

## GitHub Release

Published release:

> [Recoleta 0.7.0](https://github.com/NeapolitanIcecream/recoleta/releases/tag/v0.7.0)

Reusable release summary:

> Recoleta runs long-lived research radars across arXiv, Hacker News,
> OpenReview, Hugging Face Daily Papers, and RSS. This release makes the
> maintained production deployment directly inspectable before a user
> configures sources or a model.
>
> Run `uvx recoleta demo`, then open the generated site. `uvx` may first install
> the package from PyPI; the demo itself builds one curated 2026-07-23
> production-fleet brief without source fetches, model calls, or an API key. It
> verifies installation and rendering; it does not reproduce synthesis or count
> as an external activation.
>
> The maintained bilingual fleet now serves as the reference deployment. Its
> current snapshot contains 244 trend briefs, 244 idea briefs, and 1,362 linked
> source notes, with visible briefs through 2026-07-23. The release adds a dated
> case study and a redacted, runnable fleet topology.
>
> Generated research sites now include canonical and social metadata,
> multilingual alternates, Atom feeds, a curated sitemap, and an explicit
> robots policy. Source-note and thin aggregation pages remain reachable but
> are not promoted as search landing pages.
>
> Distribution now uses PyPI Trusted Publishing and a provenance- and
> SBOM-enabled GHCR image. Recoleta remains alpha software: generated claims
> require source inspection, and the public fleet is maintainer dogfooding
> rather than independent validation.

The exact release, package hashes, first container digest, and fleet deployment
checks are recorded in
[`checkpoints/2026-07-27-release-and-fleet-verification.md`](./checkpoints/2026-07-27-release-and-fleet-verification.md).

## Show HN

Submit the repository URL, not a landing page. Recommended title:

> Show HN: Recoleta – research radars that publish traceable trends and ideas

Alternatives:

- `Show HN: Recoleta, a Python research radar with a live bilingual deployment`
- `Show HN: Recoleta – continuously turn technical sources into a research site`

Do not use a first comment prepared by an agent. Hacker News requires something
people can try, asks the maker to be present, and prohibits generated or
AI-edited comments:
<https://news.ycombinator.com/showhn.html> and
<https://news.ycombinator.com/newsguidelines.html>.

The maintainer can use this fact card while writing their own comments:

- Why it exists: the maintainer and team needed several research scopes to stay
  current without losing the source trail.
- What is personally operated: the linked bilingual deployment tracing
  Software Intelligence and Embodied AI.
- Fastest trial: `uvx recoleta demo`; the initial package install may use PyPI,
  while the demo needs no account or key and performs no source fetch or model
  call.
- What a full deployment adds: source ingestion, durable state, evidence-gated
  synthesis, localization, publication, and scheduled fleet operation.
- What is unusual: low-evidence windows can be suppressed rather than padded;
  retained briefs link back to the material read.
- Candid limit: an attached read trace is not sentence-level entailment, and
  production dogfooding is not independent adoption.
- Useful feedback to ask for in the maintainer's own words: whether the output
  is inspectable enough to trust as a reading queue, and where the full setup
  becomes too expensive or complex.
- Never request votes or comments, and do not repost if the submission is quiet.

## Changelog News

Form: <https://changelog.com/news/submit>

URL:

> https://github.com/NeapolitanIcecream/recoleta

Title:

> Recoleta: continuously operated research radars with traceable output

What's interesting:

> Recoleta is an Apache-2.0 Python system that monitors arXiv, Hacker News,
> OpenReview, Hugging Face Daily Papers, and RSS, then publishes traceable trend
> and idea briefs as a living research site. The project is backed by a running
> bilingual deployment rather than a staged preset. The new release adds a
> `uvx recoleta demo` command that renders a real curated fleet brief without
> requiring an API key, plus a redacted fleet example, Atom feeds and curated
> search discovery, PyPI distribution, and a public container image.
> Low-evidence synthesis windows can be suppressed instead of padded.

Changelog accepts self-submissions, asks why the link is newsworthy, and
excludes commercial products and generic tutorials. Recoleta is open source and
the submission should remain project- and mechanism-focused:
<https://changelog.com/news/submit>.

## PyCoder's Weekly

Form: <https://pycoders.com/submissions>

Title:

> Recoleta: continuously operated research radars in Python

URL:

> https://github.com/NeapolitanIcecream/recoleta

Description:

> Recoleta is an Apache-2.0 Python 3.14 system for operating one research radar
> or a fleet of isolated streams. It ingests technical sources, retains durable
> state, produces evidence-linked trend and idea briefs, and publishes
> multilingual research sites. `uvx recoleta demo` renders a curated output
> from the maintained bilingual deployment before users configure a model,
> source account, or API key.

The newsletter explicitly accepts projects from the Python community but does
not guarantee inclusion: <https://pycoders.com/submissions>.

## Bluesky pilot

Run only after account and automation approval. The account must self-label as a
bot, and automated interaction is allowed only after a user tags the account.

Launch post:

> Recoleta v0.7.0 is out: run long-lived research radars across technical
> sources, publish traceable trends and ideas, and inspect a maintained
> bilingual deployment tracing Software Intelligence and Embodied AI.
> `uvx recoleta demo` needs no API key or model call.
> https://github.com/NeapolitanIcecream/recoleta

Fleet proof post:

> What sustained dogfooding looks like: Recoleta's current public snapshot
> contains 244 trends, 244 ideas, and 1,362 linked source notes in English and
> Simplified Chinese, tracing Software Intelligence and Embodied AI. Limits and
> reproduction:
> https://github.com/NeapolitanIcecream/recoleta/blob/main/docs/guides/production-fleet-case-study.md

Selected-brief post:

> This Software Intelligence brief connects five public preprints on coding
> agent evaluation, working memory, deterministic MCP reasoning, and
> human-in-the-loop workflows. Read the claim, then follow its source trail:
> https://neapolitanicecream.github.io/recoleta/en/trends/software-intelligence--day--2026-07-23--trend--2079.html

Pilot invitation:

> Operating a Recoleta radar on your own non-bundled sources? A public,
> voluntary usage receipt helps us distinguish real activation from downloads
> and demo runs. Do not include private sources or credentials:
> https://github.com/NeapolitanIcecream/recoleta/issues/new?template=activation_receipt.yml

Stop after 28 days or four posts if the channel produces no attributable
qualified activation.

## Response boundaries outside Hacker News

The agent may prepare answers for GitHub, PyCoder, Changelog, and an authorized
project social account when the service permits it. Responses must:

- answer only from public project facts or information supplied by the user;
- distinguish product behavior, inference, and roadmap;
- avoid private fleet operations, recipients, costs, failures, and team
  identity;
- avoid claiming independent adoption until a qualifying public reference
  exists;
- route security reports to the private reporting flow;
- route legal, policy, payment, or hostile-security matters to the maintainer.
