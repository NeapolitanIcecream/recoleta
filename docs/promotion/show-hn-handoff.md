# Show HN maintainer handoff

Last verified: 2026-07-27

Status: Recoleta is tryable, the release and distribution checks pass, and the
approved repository social preview is live. No Hacker News submission has been
made.

## Do not copy this file into Hacker News

This is an internal fact sheet and checklist. Do not paste or adapt its prose
into a Hacker News submission or comment.

The current Hacker News guidelines prohibit generated or AI-edited comments.
The Show HN presentation tips, updated 2026-03-28, extend that instruction to
all text posted to Hacker News, including submission copy. Earlier title
candidates in this repository are retired.

Sources:

- <https://news.ycombinator.com/showhn.html>
- <https://news.ycombinator.com/newsguidelines.html>
- <https://news.ycombinator.com/item?id=22336638>
- <https://news.ycombinator.com/showlim>

## Maintainer-only steps

1. Use an ordinary personal Hacker News account, not a project-named account.
2. Confirm that the account can submit a Show HN. Hacker News currently
   restricts Show HN submissions from accounts that are not yet familiar with
   the community. Do not create a replacement account to bypass a restriction.
3. Open <https://news.ycombinator.com/submit>.
4. Use <https://github.com/NeapolitanIcecream/recoleta> as the submission URL.
5. Write the title by hand. It must begin with `Show HN:` and should state what
   Recoleta does without release numbers, praise, or sales language.
6. Write the submission text by hand. If it does not appear above the thread,
   add the same human-written context as the first comment.
7. Submit only when you can remain available to answer questions. Write every
   reply yourself without AI generation or editing.
8. Do not ask anyone to vote or add a supporting comment. Do not delete and
   repost a quiet submission.

Before pressing submit, record the date in
[`launch-log.md`](./launch-log.md). After submission, add the public thread URL.

## Questions to answer in your own words

Use these questions as a writing checklist, not as text to copy:

1. What does Recoleta do from input to published output?
2. What recurring research problem led you and your team to build it?
3. What do you personally operate, and what can a reader inspect today?
4. What is the shortest way to try a real output without configuring sources
   or a model?
5. Which design choices differ from a feed reader or a one-shot research
   report?
6. Which limitations should a reader know before trusting generated claims?
7. What specific technical or product feedback would help next?

## Verified fact sheet

These facts are for checking the maintainer's independently written text.

| Topic | Verified fact | Public source |
| --- | --- | --- |
| Project | Recoleta is an Apache-2.0 Python 3.14+ system for running long-lived research radars. | [README](../../README.md) |
| Inputs | Supported sources include arXiv, Hacker News RSS, OpenReview, Hugging Face Daily Papers, and custom RSS feeds. | [README](../../README.md) |
| Outputs | Stored evidence can be published as traceable trend and idea briefs, Markdown, PDF, email artifacts, or a static research site. | [README](../../README.md) |
| Evidence behavior | Retained briefs link to the material read, and low-evidence synthesis windows can be suppressed instead of padded. | [README](../../README.md) |
| Fast evaluation | `uvx recoleta==0.7.0 demo --output-dir recoleta-demo` renders one bundled production-fleet brief. | [README](../../README.md#bundled-output-demo-no-api-key) |
| Demo boundary | The first `uvx` run may download packages from PyPI. After installation, the demo performs no source fetches and makes no model or embedding calls. It does not reproduce synthesis. | [README](../../README.md#bundled-output-demo-no-api-key) |
| Public proof | The maintained public fleet traces Software Intelligence and Embodied AI in English and Simplified Chinese. | [Live fleet](https://neapolitanicecream.github.io/recoleta/) |
| Snapshot | The 2026-07-27 deployment contains 244 trend briefs, 244 idea briefs, and 1,362 linked source notes, with visible briefs through 2026-07-23. | [Fleet case study](../guides/production-fleet-case-study.md) |
| Distribution | Recoleta 0.7.0 is on PyPI and GitHub Releases. Public GHCR tags contain native `linux/amd64` and `linux/arm64` images. | [Release checkpoint](./checkpoints/2026-07-27-release-and-fleet-verification.md) |
| Limits | Recoleta is alpha software. A read trace records the material used but is not sentence-level entailment, so generated claims still require source inspection. The public fleet is maintainer dogfooding, not independent adoption. | [Fleet case study](../guides/production-fleet-case-study.md) |

## Public inspection links

- Repository: <https://github.com/NeapolitanIcecream/recoleta>
- Running fleet: <https://neapolitanicecream.github.io/recoleta/>
- Selected Software Intelligence brief:
  <https://neapolitanicecream.github.io/recoleta/en/trends/software-intelligence--day--2026-07-23--trend--2079.html>
- Production fleet case study:
  <https://github.com/NeapolitanIcecream/recoleta/blob/main/docs/guides/production-fleet-case-study.md>
- Release: <https://github.com/NeapolitanIcecream/recoleta/releases/tag/v0.7.0>
- PyPI: <https://pypi.org/project/recoleta/0.7.0/>
- Container:
  <https://github.com/NeapolitanIcecream/recoleta/pkgs/container/recoleta>

## Preflight

- The repository, live fleet, selected brief, release, PyPI page, and container
  package are public.
- The bundled evaluation path has no account or API-key gate after package
  installation.
- The repository social preview is byte-identical to the approved 1200 by 630
  image.
- The title and submission text were written by the maintainer without AI
  generation or editing.
- The maintainer can stay present for the initial discussion.
- The attempt is recorded before submission.
- No votes, comments, or reposts will be solicited.

## After submission

The agent may validate technical facts, monitor public availability, and record
the thread and attributable outcomes. The maintainer writes all Hacker News
comments. Record checks at 24 hours, 7 days, and 28 days without treating
points, traffic, package downloads, or stars as qualified activation.
