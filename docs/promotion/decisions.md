# Promotion decision log

Entries are append-only. Supersede an older decision with a new dated entry
rather than silently changing its historical rationale.

## 2026-07-25 — Keep a tracked promotion archive

Decision:

- Store strategy, evidence, decisions, and current execution state under
  `docs/promotion/`.
- Make `AGENTS.md` point future maintainers and agents to the archive.

Reason:

- Promotion work spans repository changes, external rules, account approvals,
  experiments, and long feedback windows. Chat context is not a durable system
  of record.

Consequence:

- Material work is incomplete until the archive reflects the new state.
- Only public-safe information may be committed.

## 2026-07-25 — Use the production fleet as the flagship example

Decision:

- Build the main case study from the fleet already deployed to GitHub Pages.
- Do not build the launch narrative around a lightly maintained preset.

Reason:

- The production fleet demonstrates sustained operation, multi-stream
  orchestration, evidence-linked output, suppression, localization, and
  publishing under real use.

Consequence:

- Presets remain onboarding aids rather than proof of product value.
- Production evidence must still be distinguished from independent adoption.

## 2026-07-25 — Remove local-first from the main positioning

Decision:

- Do not lead marketing copy with `local-first`.
- Lead with continuously operated research intelligence, traceable output, and a
  living publication.

Reason:

- `local-first` came from older generated documentation and is not the
  maintainer's product thesis.

Consequence:

- State ownership may still be documented accurately as an implementation
  property.

## 2026-07-25 — Manage Huldra as infrastructure, not a campaign

Decision:

- Maintain and publish Huldra as part of the Recoleta release chain.
- Do not spend launch attention on Huldra unless its own users create a separate
  reason to do so.

Reason:

- Huldra was extracted from Recoleta and is required infrastructure. Its missing
  current PyPI release blocks clean Recoleta distribution.

Consequence:

- Huldra compatibility and publication precede the Recoleta package release.

## 2026-07-25 — Require maintainer review for visual assets

Decision:

- Generate visual alternatives locally and present them for review.
- Do not replace or publish screenshots, social previews, diagrams, or generated
  promotional art before approval.

Reason:

- Visual direction requires maintainer judgment even when copy and engineering
  work are delegated.

Consequence:

- Visual approval is an explicit execution gate, not a final polish task.

## 2026-07-25 — Treat Show HN as human-in-the-loop

Decision:

- The agent prepares a tryable release, launch page, factual briefing, and title
  candidates.
- The maintainer reviews and submits the link and writes discussion comments in
  their own words.

Reason:

- Hacker News requires maker participation and prohibits generated or AI-edited
  comments.

Consequence:

- Show HN can be a core launch event, but it cannot be an agent-only
  communication channel.

## 2026-07-25 — Keep the no-key demo below the activation metric

Decision:

- Bundle one curated production-fleet brief and let `recoleta demo` render it
  without configuration, network calls, or model calls.
- Report the command explicitly as an evaluation event, not an activation.

Reason:

- The artifact reduces installation and output uncertainty but does not show
  that an external user generated a new artifact from non-bundled input.

Consequence:

- Demo runs never enter the qualified-activation count.
- The bundled brief must retain its production date, source, and limitations.

## 2026-07-25 — Curate search exposure instead of indexing every page

Decision:

- Index home, collection indexes, trend and idea details, the topics directory,
  and the first archive page.
- Mark source-note pages, individual thin topic aggregations, and pagination
  pages `noindex,follow`.

Reason:

- The fleet produces thousands of useful inspection pages, but exposing all of
  them as search landing pages would dilute the research publication and create
  many repetitive or thin entry points.

Consequence:

- The sitemap contains the curated indexable set.
- Source trails remain reachable from briefs and crawlable through links.

## 2026-07-25 — Publish Huldra before Recoleta

Decision:

- Prepare and publish `huldra-arxiv 0.4.2` through Trusted Publishing before
  replacing Recoleta's reviewed Git dependency with an index-compatible
  version range.

Reason:

- PyPI cannot be the clean installation path while Recoleta requires an
  unpublished direct Git dependency.

Consequence:

- The Recoleta publishing workflow explicitly rejects direct dependencies.
- Huldra account configuration and release are the current external blocker
  for Recoleta's clean index release.

## 2026-07-27 — Separate visual structure from palette and texture

Decision:

- Treat the preference for Candidate B as a preference between the two complete
  candidates, not as a request for a dark-blue background.
- Preserve Candidate B's legible three-stream-to-publication topology as the
  current hypothesis.
- Test that topology without its cyanotype, collage, map, and paper texture
  before choosing a palette.
- Use GOV.UK, Carbon, and Primer as constraints for usefulness, grid, tokens,
  hierarchy, accessibility, and asset consistency. Do not copy their visual
  surfaces.

Reason:

- The maintainer used “dark blue” only to identify the second file and then
  explicitly corrected the possibility of a colour inference.
- Candidate B reads more directly than Candidate A, but its many bespoke
  details are hard to systematize and compete with the product model.

Consequence:

- Palette remains an open design variable.
- The next candidate is a neutral, deterministic SVG structure study rather
  than another generated art direction.
- Exact copy and real fleet screenshots are separate layers that remain behind
  the visual review gate.

## 2026-07-27 — Approve the structure and theme it from the live fleet

Decision:

- Approve the three-peer-streams-to-one-publication structure.
- Apply the role values already used by the current fleet site for the second
  review set.
- Keep the repository banner free of marketing text, use exact deterministic
  text on the social card, and show real product output on a separate proof
  board.

Reason:

- The maintainer approved Candidate C's visual direction.
- Reusing current site roles makes the assets consistent with the product while
  preserving the earlier decision that no background colour is a requirement.
- Separate assets let the structural diagram, launch claim, and product evidence
  each perform one job.

Consequence:

- The structure is no longer under review.
- Theme values and the three complete assets require one final visual review
  before public replacement.
- Future palette changes can replace role values without redesigning the
  composition.

## 2026-07-27 — Approve the revised visual set after copy simplification

Decision:

- Approve the repository banner, social card, and production-fleet proof board
  in the second review set.
- Replace the social card's operational shorthand with a direct invitation to
  inspect the maintained research radar.
- Describe the proof board as a bilingual public demo tracing Software
  Intelligence and Embodied AI, without foregrounding internal stream count or
  independence.
- Publish the set only after the `0.7.0` package, container, and refreshed fleet
  gates pass, using a separate versioned repository change.

Reason:

- The maintainer accepted the visual direction but found “a running
  three-stream fleet” and “a no-key offline demo” unclear as promotional copy.
- The public value is the inspectable research output and supported languages,
  not the deployment topology itself.

Consequence:

- Visual review is closed for the current files.
- Later visual changes return to maintainer review.
- The approved files can now replace public assets without reopening palette or
  structural exploration.
