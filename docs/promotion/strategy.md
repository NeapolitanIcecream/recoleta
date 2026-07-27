# Promotion strategy

Last updated: 2026-07-25

## Product claim

Recoleta is a continuously operated research intelligence system. It monitors
multiple technical sources, turns them into traceable trend and idea briefs, and
publishes the result as a living research site.

The short external claim must remain narrower than the implementation:

> Run long-lived research radars across the technical sources you follow,
> synthesize traceable trends and ideas, and publish a research site that stays
> current.

Do not use `local-first` as the main positioning. It is an implementation
property of state and outputs, not the maintainer's product thesis. Do not call
Recoleta a fact checker or claim that exact read traces prove sentence-level
entailment.

## Flagship proof

The public production fleet is the main example, not a lightly maintained
preset. It currently publishes three research streams:

- Embodied AI
- Software Intelligence
- Cross Platform

The case study should show:

- the multi-stream fleet topology and operating cadence;
- a selected real trend and its source trail;
- a window that was shortened or suppressed instead of padded;
- the public site as the current output, not a staged mockup;
- a redacted path for reproducing one comparable stream.

Private costs, failures, recipient data, machine paths, and team identity are not
public evidence until the maintainer approves their disclosure. Production
dogfooding is strong product evidence, but it is not independent adoption.

## Success definitions

Primary 90-day targets:

- 15 qualified external activations;
- 3 retained external users;
- 3 independent external usage references.

A **qualified activation** is a non-maintainer, non-project-member, non-CI user
who uses non-bundled input to generate a new Recoleta artifact and voluntarily
submits a success receipt or publishes the artifact.

A **retained user** is the same external identity or opted-in installation
producing at least one new artifact in four consecutive calendar weeks.

An **independent usage reference** is a reference controlled by an external user
or organization and based on actual use. Self-submitted directory entries,
mirrors, automated aggregators, stars, downloads, pulls, clones, and visits do
not qualify.

The no-key demonstration is a `T0` evaluation event. It reduces uncertainty but
does not count as an activation.

## Execution gates

### Gate 0 — distribution and evaluation

Deliver:

- matching published Huldra dependency and an index-compatible Recoleta package;
- least-privilege trusted publishing;
- a public container image;
- a no-key evaluation path with a bundled, clearly labeled sample;
- current screenshots and a short demonstration;
- package metadata, security policy, and support boundary.

Pass when at least four of five clean environments can inspect the bundled
sample without cloning the repository, and the median time to a viewable sample
is at most ten minutes.

### Gate 1 — production evidence

Publish a dated fleet case study with public inputs, versions, outputs,
limitations, and reproducible commands. Add a later blind comparison when its
review protocol and sample are ready. Internal post-hoc scoring must be labeled
as directional evidence rather than external validation.

### Gate 2 — persistent distribution

Use the package indexes, container registry, GitHub Releases, the public site,
RSS, and search metadata as the permanent distribution layer. Submit one
audience-specific version of the production evidence to suitable editorial or
directory channels.

Pause a repeatable channel after 28 days or four valid attempts if it produces
zero attributable qualified activations. A platform rejection is a policy or
eligibility result, not a demand result.

### Gate 3 — opt-in adoption

Recruit a small pilot through owned project surfaces and opt-in project posts.
The operator or agent may prepare configurations, answer routine questions, and
collect voluntary receipts. Do not mass-message, auto-reply without opt-in, or
use package downloads as a retention proxy.

## Channel policy

Core:

- GitHub repository, Releases, Discussions, and Pages;
- PyPI and a public container registry;
- curated RSS and search-indexable method, benchmark, and weekly pages;
- suitable editorial submissions such as Changelog News and PyCoder's Weekly.

Conditional:

- Show HN after the project is directly tryable. The maintainer submits and
  writes the title, submission text, and discussion comments without AI
  generation or editing. The agent supplies only a non-postable fact sheet,
  public links, and checks.
- A Bluesky project bot after account authorization. It must identify itself as
  automated and interact only when explicitly tagged.
- Community showcases only when their current rules allow transparent
  project-agent participation.

Excluded from the core loop:

- automated Reddit distribution;
- cold email or unsolicited direct-message campaigns;
- engagement manipulation or vote solicitation;
- paid acquisition before qualified activation is measurable;
- platforms that require undisclosed human authorship or prohibit the planned
  automation.

## Operating boundary

The agent may own research, copy, code, release preparation, routine permitted
responses, attribution reporting, and channel stop decisions. The maintainer
retains account creation, MFA, security and legal escalation, policy appeals,
paid commitments, visual approval, and any platform interaction that must be
authored personally.
