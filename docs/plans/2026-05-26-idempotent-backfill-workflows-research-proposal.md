# Idempotent Backfill Workflows Research Proposal

Date: 2026-05-26

Status: proposed

## Goal

Research the W21 fleet cost regression, refine the product and engineering
model for idempotent backfill workflows, and produce a second implementation
proposal that can be executed in one pull request.

The second proposal must include complete execution steps. Each step must have
its own acceptance criteria, and each step must be committed only after its
acceptance criteria pass.

## Background

The W21 fleet run exposed a costly workflow semantics problem:

- The operator ran seven `fleet run day` jobs and then one `fleet run week`.
- `fleet run week` expanded lower-level daily work again because weekly
  workflows currently recurse into day-level invocations by default.
- Some stages were idempotent enough to skip work, but the weekly workflow still
  made substantial new LLM calls in day-level `analyze`, `trends:day`,
  `ideas:day`, and translation work.
- The observed extra API cost was material enough that this should be handled
  as a product and workflow design issue, not as operator training.

The current user-facing mental model is too imperative: users must know which
steps are safe to skip and which lower-level work has already been completed.
The desired model is declarative: users ask Recoleta to make a period complete,
and Recoleta reconciles missing work without repeating completed expensive work.

## Research Questions

The research pass should answer these questions with code references, runtime
evidence, and concrete tradeoffs:

1. What exact workflow states should `run day`, `run week`, `run month`, and
   `fleet run ...` guarantee?
2. Which existing tables and files are authoritative enough to decide that a
   stage is complete and fresh?
3. Which stage outputs are historical user-facing results that should not be
   replayed automatically?
4. Which outputs are rebuildable cache or presentation material that may be
   refreshed automatically?
5. What freshness fingerprint is needed for each expensive stage?
6. How should Recoleta distinguish "ensure missing work" from "force
   regeneration"?
7. Which existing CLI flags, workflow policy settings, or configuration knobs
   can be removed, hidden, or demoted to repair-only paths?
8. What low-cost dry-run or plan output is needed so operators can see why work
   will run before LLM calls are made?
9. What guardrails should prevent a future weekly run from silently redoing a
   complete daily week?
10. What migration path preserves existing local databases and scripts while
    reducing the default cognitive load?

## Scope

In scope:

- `run day`, `run week`, `run month`.
- `fleet run day`, `fleet run week`, `fleet run month`, and deploy interaction.
- Planner behavior for lower-level backfill and idempotent skipping.
- Stage-level completion and freshness checks for ingest, analyze, publish,
  trends, ideas, translation, site build, and deploy.
- Cost accounting and planned-work reporting.
- Tests and docs needed to prove the new semantics.

Out of scope for the research proposal:

- Implementing the final workflow changes.
- Changing provider pricing logic.
- Replacing SQLite, Huldra, or the current run model.
- Designing a distributed scheduler.

The implementation proposal may recommend small enabling refactors, but it
should avoid a broad workflow-engine rewrite unless the research shows no
smaller path can meet the acceptance criteria.

## Working Hypothesis

The expected direction is to make backfill the default, but make backfill an
idempotent reconciliation operation:

- A week run should ensure all required day and week outputs exist.
- If a day window is already complete and fresh, the week run should skip its
  expensive day-level work.
- If a day window is incomplete, the week run should backfill only the missing
  or stale pieces.
- If an operator really wants regeneration, they should use an explicit force
  or repair command.

This hypothesis must be validated against existing state transitions and
storage contracts before implementation is proposed.

## Required Evidence

The research pass should collect and summarize:

- The current week workflow invocation graph from `recoleta.cli.workflow_runner`.
- The current default policy path from `recoleta.config`.
- The exact metrics and output rows that prove W21 did real repeated LLM work.
- The stage-level idempotency behavior that already exists today.
- The gaps where Recoleta cannot currently determine freshness cheaply.
- Existing tests that lock in current behavior and tests that need to change.
- Any fleet scripts or docs that would break under the new semantics.

Evidence should be included in the second proposal as short references, not as a
large transcript dump.

## Deliverable: Implementation Proposal

The final deliverable of this research task is a second document, tentatively:

`docs/plans/YYYY-MM-DD-idempotent-backfill-workflows-implementation-plan.md`

That document must be directly executable by one PR. It must include:

- Problem statement and target user-facing semantics.
- Current-state findings with file and behavior references.
- Proposed final CLI and configuration shape.
- Backward compatibility and migration notes.
- Detailed implementation steps.
- Step-by-step acceptance criteria.
- Commit gates for every step.
- Final PR validation checklist.
- Rollback plan.
- Open questions that block implementation, if any.

## Implementation Proposal Step Format

Every step in the second proposal must use this format:

```markdown
### Step N: <short name>

Intent:
<what this step changes and why>

Files likely touched:
- <path>

Acceptance criteria:
- <observable behavior or test condition>
- <required command output or new/updated test>

Commit gate:
- Run: `<command>`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `<imperative subject>`
```

The implementation PR should not batch multiple accepted steps into one final
commit. Each accepted step should be committed before starting the next step, so
reviewers can bisect behavior and cost-risk changes.

## Candidate Implementation Steps To Validate

The research pass should validate, revise, or replace this initial sequence:

### Step 1: Add a workflow planning inspection layer

Intent:
Introduce a read-only planner view that can report which period windows and
stage outputs are already complete, stale, missing, or forced.

Acceptance criteria:

- Tests cover a complete daily week producing skip decisions for day-level
  expensive stages.
- Tests cover an incomplete daily week producing run decisions only for missing
  pieces.
- The planner can be exercised without making LLM calls.

### Step 2: Make period workflows reconcile desired state

Intent:
Change `run week` and `fleet run week` from unconditional lower-level execution
to ensure-style execution. Lower-level backfill remains default, but completed
lower-level windows skip expensive work.

Acceptance criteria:

- A week workflow over seven successful day runs does not execute day-level
  `analyze`, `trends:day`, or `ideas:day` LLM work.
- A week workflow over missing day windows backfills only those missing windows.
- Existing day workflow behavior remains stable.

### Step 3: Add force and repair semantics

Intent:
Keep regeneration explicit and reduce routine CLI complexity. Provide one clear
force path for deliberate recomputation and keep ordinary runs safe by default.

Acceptance criteria:

- Forced runs can intentionally recompute selected stages.
- Non-forced runs skip fresh expensive work.
- Deprecated or confusing options are documented as compatibility aliases or
  repair-only controls.

### Step 4: Improve translation freshness attribution

Intent:
Make translation skip/run decisions and billing attribution inspectable without
time-order reconstruction.

Acceptance criteria:

- Translation metrics or diagnostics can be grouped by source kind and, for
  trend/idea documents, granularity.
- Tests prove unchanged source hashes skip translation.
- Billing reports can distinguish repeated day translations from weekly-only
  translations.

### Step 5: Add cost guardrails and dry-run output

Intent:
Prevent expensive surprises by showing planned LLM work before execution and
warning or failing when a run would redo completed lower-level work.

Acceptance criteria:

- A dry-run or plan output lists planned expensive steps and skip reasons.
- A week run over a complete daily week plans no day-level LLM work.
- A guard test proves silent repeated lower-level LLM work cannot regress.

### Step 6: Update docs and fleet runbook

Intent:
Make the default operator story simple: "run the target period; Recoleta ensures
it." Move advanced repair controls out of the common path.

Acceptance criteria:

- User-facing docs and fleet runbook describe ensure/backfill semantics.
- Docs state when to use force or repair.
- Existing examples no longer teach manual `--skip` recipes for normal weekly
  operation.

## PR Operating Rules

The implementation PR produced from the second proposal must follow these rules:

- One PR owns the full workflow semantics change.
- The PR may contain multiple commits, one per accepted step.
- Each step starts from a clean working tree except for intentional prior
  commits in the same PR branch.
- Each step must update tests before or with behavior changes when feasible.
- Each step must record the command(s) run for acceptance.
- If a step discovers the proposal is wrong, stop and update the proposal before
  continuing.
- Do not merge compatibility cleanup with behavior changes unless the proposal
  explicitly calls for it.

## Final PR Acceptance

The final PR should be accepted only when:

- Unit and focused workflow tests prove idempotent week behavior.
- A dry-run or equivalent planner report demonstrates skip reasons.
- Re-running a week after seven successful days does not produce day-level LLM
  metrics.
- Running a week on an incomplete database still backfills missing day windows.
- Translation freshness and billing attribution are understandable without
  manual log reconstruction.
- Docs describe the new low-cognitive-load path.
- The PR description includes before/after cost behavior for the W21 scenario.

## Risks

- Existing operators may rely on week runs replaying lower-level work. The
  implementation proposal must identify whether this was intended behavior or
  accidental behavior.
- Freshness fingerprints can become too broad and cause unnecessary reruns, or
  too narrow and miss required refreshes.
- Removing flags too early can make repair harder. The proposal should prefer
  compatibility aliases first, then removal after one release if needed.
- Site build and deploy semantics can be confused with content generation
  semantics. The plan should keep rebuildable presentation work separate from
  expensive historical generation work.

## Non-Acceptance

The research task is not complete if it only says "use `--skip`". That is an
operator workaround, not a product solution.

The research task is also not complete if it proposes "week never backfills
days". That reduces one cost risk but makes historical backfill fragile and
keeps users responsible for knowing hidden prerequisites.
