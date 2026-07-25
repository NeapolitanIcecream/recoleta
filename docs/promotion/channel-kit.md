# Promotion channel kit

Last updated: 2026-07-25

Publication status: draft; wait for the release gates

## Source-of-truth links

- Repository: <https://github.com/NeapolitanIcecream/recoleta>
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

Staggering submissions makes failures diagnosable and attribution less
ambiguous. It also avoids asking several communities to inspect a release while
its permanent distribution surfaces are still changing.

## GitHub Release

Suggested title:

> Recoleta v0.7.0: production-fleet demo and research-site discovery

Suggested body:

> Recoleta runs long-lived research radars across arXiv, Hacker News,
> OpenReview, Hugging Face Daily Papers, and RSS. This release makes the
> maintained production deployment directly inspectable before a user
> configures sources or a model.
>
> Run `uvx recoleta demo`, then open the generated site. The command builds one
> curated 2026-07-23 production-fleet brief without source fetches, model calls,
> or an API key. It verifies installation and rendering; it does not reproduce
> synthesis or count as an external activation.
>
> The public three-stream fleet now serves as the reference deployment. Its
> 2026-07-24 snapshot contains 244 trend briefs, 244 idea briefs, and 1,362
> linked source notes in English and Simplified Chinese. The release adds a
> dated case study and a redacted, runnable three-child fleet topology.
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

Append the final changelog diff and exact artifact links after the version, tag,
and container digest exist.

## Show HN

Submit the repository URL, not a landing page. Recommended title:

> Show HN: Recoleta – research radars that publish traceable trends and ideas

Alternatives:

- `Show HN: Recoleta, a Python research radar running as a three-stream fleet`
- `Show HN: Recoleta – continuously turn technical sources into a research site`

Do not use a first comment prepared by an agent. Hacker News requires something
people can try, asks the maker to be present, and prohibits generated or
AI-edited comments:
<https://news.ycombinator.com/showhn.html> and
<https://news.ycombinator.com/newsguidelines.html>.

The maintainer can use this fact card while writing their own comments:

- Why it exists: the maintainer and team needed several research scopes to stay
  current without losing the source trail.
- What is personally operated: the linked three-stream bilingual fleet.
- Fastest trial: `uvx recoleta demo`; no account, key, source fetch, or model
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
> three-stream bilingual fleet rather than a staged preset. The new release adds
> a no-key offline demo from a real fleet brief, a redacted fleet example, Atom
> feeds and curated search discovery, PyPI distribution, and a public container
> image. Low-evidence synthesis windows can be suppressed instead of padded.

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
> multilingual research sites. A no-key `uvx recoleta demo` renders a curated
> output from the running three-stream fleet before users configure a model or
> source account.

The newsletter explicitly accepts projects from the Python community but does
not guarantee inclusion: <https://pycoders.com/submissions>.

## Bluesky pilot

Run only after account and automation approval. The account must self-label as a
bot, and automated interaction is allowed only after a user tags the account.

Launch post:

> Recoleta v0.7.0 is out: run long-lived research radars across technical
> sources, publish traceable trends and ideas, and inspect a real three-stream
> production fleet. `uvx recoleta demo` needs no API key or model call.
> https://github.com/NeapolitanIcecream/recoleta

Fleet proof post:

> What sustained dogfooding looks like: Recoleta's 2026-07-24 fleet snapshot
> contains 244 trends, 244 ideas, and 1,362 linked source notes across three
> isolated streams in English and Simplified Chinese. Limits and reproduction:
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
