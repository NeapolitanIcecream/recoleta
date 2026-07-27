# GitHub launch handoff

Last updated: 2026-07-27

External changes: release, fleet deployment, container visibility, private
vulnerability reporting, repository About, and topics applied; social preview
pending the current versioned change

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

The maintainer approved the revised deterministic social card on 2026-07-27.
After the versioned asset change merges, upload
[`../assets/recoleta-social-preview.png`](../assets/recoleta-social-preview.png)
in the repository's **Settings → General → Social preview** control. Do not
upload either rejected generated candidate.

## Community surface

Keep GitHub Issues as the initial support and activation surface. Enable
Discussions only when repeated public questions or showcases justify another
inbox; do not create an empty community surface solely for launch.

Private vulnerability reporting is enabled for Recoleta and Huldra. GitHub's
repository API returned `enabled=true` for both settings after the change.

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

The promotion release is
[`v0.7.0`](https://github.com/NeapolitanIcecream/recoleta/releases/tag/v0.7.0),
tagged at exact merge commit `3e2a59c5`. PyPI and the refreshed production
fleet are verified. The first GHCR publication is public but contains
`linux/amd64` only; the current branch repairs and replays it as an
amd64/arm64 image before channel submissions.

## Execution checklist

1. Complete the Huldra and Recoleta Trusted Publisher setup. **Done.**
2. Publish and independently verify Huldra `0.4.2`. **Done.**
3. Replace Recoleta's direct Git dependency and repeat all release gates.
   **Done.**
4. Publish the Recoleta GitHub Release, PyPI distributions, and GHCR image.
   **Done.**
5. Republish and verify the public GHCR image for amd64 and arm64. **In
   progress.**
6. Deploy the refreshed production fleet and verify its public sitemap, feeds,
   canonical URLs, language alternates, robots policy, and representative brief.
   **Done.**
7. Apply the approved About text, topics, and social preview. **About and topics
   done; social preview pending current versioned change.**
8. Start the channel sequence and record every attempt, including zero-result
   outcomes. **Not started.**
