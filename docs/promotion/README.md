# Promotion archive

This directory is the durable handoff for Recoleta promotion work. It exists so
that a new maintainer or agent can recover the strategy, evidence, decisions, and
current execution state without relying on a chat transcript.

Read in this order:

1. [`status.md`](./status.md) — current phase, open work, and approval gates.
2. [`strategy.md`](./strategy.md) — positioning, success definitions, routes,
   and stop conditions.
3. [`research-baseline.md`](./research-baseline.md) — dated facts, inferences,
   limitations, and external references.
4. [`decisions.md`](./decisions.md) — append-only decisions that materially
   change the plan.
5. [`visual-system-review.md`](./visual-system-review.md) — sourced visual
   constraints, the first-candidate diagnosis, and the current review test.
6. [`maintainer-actions.md`](./maintainer-actions.md) — exact one-time account
   and approval steps that cannot be completed from the repository.
7. [`channel-kit.md`](./channel-kit.md) — launch copy, channel order, and
   platform-specific boundaries.
8. [`launch-log.md`](./launch-log.md) — attributable attempts and outcomes.
9. [`checkpoints/2026-07-25-release-readiness.md`](./checkpoints/2026-07-25-release-readiness.md)
   — implementation, validation, corrections, and exact next gate for this
   sprint checkpoint.
10. [`checkpoints/2026-07-25-maintainer-gate.md`](./checkpoints/2026-07-25-maintainer-gate.md)
   — requirement-by-requirement completion audit and exact resume signals.
11. [`checkpoints/2026-07-27-index-release-candidate.md`](./checkpoints/2026-07-27-index-release-candidate.md)
   — Huldra publication proof and the exact Recoleta `0.7.0` index-only
   release-candidate gates.
12. [`checkpoints/2026-07-27-release-and-fleet-verification.md`](./checkpoints/2026-07-27-release-and-fleet-verification.md)
    — final release identity, public PyPI and GHCR proof, production fleet
    deployment, and independent HTTPS checks.

## Update contract

- Update `status.md` before and after a material implementation or launch step.
- Add dated evidence to `research-baseline.md`; do not silently rewrite an old
  snapshot as though it were current.
- Add a decision entry when positioning, audience, measurement, disclosure,
  publication, or approval policy changes.
- Keep secrets, account recovery material, private recipients, message IDs,
  private team identity, and machine-specific paths out of this directory.
- Separate facts from inferences. Link to code, public artifacts, or a dated
  local report when possible.
- A generated sample proves that the product can render an artifact. It does not
  count as an external user activation.
- Record every external submission before making it, then append its URL and
  outcome. Do not replace an unsuccessful attempt with a cleaner narrative.

## Public-safety boundary

Files in this directory are expected to be safe to commit to the public
repository. Private operational evidence may be summarized only after the
maintainer approves the disclosure and the summary has been redacted.
