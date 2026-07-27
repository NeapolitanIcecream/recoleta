# GitHub launch handoff

Last updated: 2026-07-25

External changes: not applied

Use this file when the promotion release has passed the gates in
[`release-process.md`](./release-process.md). Versioned launch kits in this
directory are historical release records, not current positioning guidance.

## Repository surface

Description:

> Continuously operated research radars for traceable trends, ideas, and living
> research sites.

Website:

> https://neapolitanicecream.github.io/recoleta/

Topics:

- `research-tools`
- `research`
- `arxiv`
- `rss`
- `hacker-news`
- `openreview`
- `trend-analysis`
- `knowledge-management`
- `python`
- `llm`

Do not add `local-first` as a positioning topic. Do not make a starter preset
the repository's primary example.

## Social preview

Do not upload the old social preview or either unapproved banner candidate.
The current candidates and review state are recorded in
[`../promotion/visuals/README.md`](../promotion/visuals/README.md). After the
maintainer selects a direction, prepare an exact-text social card and current
fleet screenshots, obtain a second review, and only then upload the approved
asset in the repository's **Settings → General → Social preview** control.

## Community surface

Keep GitHub Issues as the initial support and activation surface. Enable
Discussions only when repeated public questions or showcases justify another
inbox; do not create an empty community surface solely for launch.

Private vulnerability reporting should be enabled through the repository
settings before broad distribution. The exact account steps are in
[`../promotion/maintainer-actions.md`](../promotion/maintainer-actions.md).

## Promotion release

Current sources:

- changelog: [`../../CHANGELOG.md`](../../CHANGELOG.md)
- release and artifact procedure:
  [`release-process.md`](./release-process.md)
- production proof:
  [`../guides/production-fleet-case-study.md`](../guides/production-fleet-case-study.md)
- release and channel copy:
  [`../promotion/channel-kit.md`](../promotion/channel-kit.md)
- attempt and activation ledger:
  [`../promotion/launch-log.md`](../promotion/launch-log.md)

The draft promotion target is `v0.7.0`. Do not tag it until Huldra `0.4.2` is
published, Recoleta uses the index-hosted Huldra constraint, and the repeated
clean-install gates pass. Those three conditions passed locally on 2026-07-27;
remote PR CI and review remain before tagging.

## Execution checklist

1. Complete the Huldra and Recoleta Trusted Publisher setup.
2. Publish and independently verify Huldra `0.4.2`.
3. Replace Recoleta's direct Git dependency and repeat all release gates.
4. Publish the Recoleta GitHub Release, PyPI distributions, and GHCR image.
5. Make the verified GHCR image public, acknowledging that the visibility
   change cannot be reversed.
6. Deploy the refreshed production fleet and verify its public sitemap, feeds,
   canonical URLs, language alternates, robots policy, and representative brief.
7. Apply the approved About text, topics, and social preview.
8. Start the channel sequence and record every attempt, including zero-result
   outcomes.
