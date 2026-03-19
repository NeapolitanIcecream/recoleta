# Bilingual Localization Rollout Follow-up

Date: 2026-03-19

## Goal

Capture the remaining follow-up work after the English-canonical / Chinese-derived localization rollout, historical backfill, and live site rebuild.

## What Landed

- `recoleta translate run` and `recoleta translate backfill` now persist translated and mirror variants in `localized_outputs`.
- Historical backfill was executed against the live database, producing:
  - `translation=2952`
  - `mirror=2952`
- `materialize outputs --site` now builds a multilingual static site with:
  - `default_language_code=en`
  - root redirect
  - browser language memory
  - per-page language switcher
- Live site verification confirmed:
  - root redirect prefers remembered language, otherwise falls back to `en`
  - `en` and `zh-cn` trend / idea / item pages resolve correctly
  - item coverage is symmetric across both languages after stale-output cleanup
  - browser console is clean in the checked flows

## Residual Issues

### 1. Translate commands still have no internal run or billing records

- `translate run` and `translate backfill` currently acquire a workspace lease only.
- They do not create `runs` rows.
- They do not record `metrics`, token counters, or estimated cost metrics.
- Result: provider-side billing exists, but the repo cannot show an internal billing report for translation activity.

### 2. English trend evolution prose still has light punctuation artifacts

- A small number of translated trend evolution sections still read awkwardly in English after history-link injection.
- The issue is not factual drift or broken linking.
- The issue is local prose polish: extra quotes, stiff punctuation, or slightly unnatural transitions around inserted history references.

### 3. Hybrid translation assist is implemented but not rollout-validated

- `--context-assist hybrid` now has a real code path and fail-open behavior.
- The production rollout used `--context-assist direct`, by design.
- We therefore have not yet done a live acceptance pass on hybrid retrieval quality against the existing local index.

### 4. Multilingual output tools still depend on implicit directory-shape contracts

- One concrete bug already surfaced here during review: `site stage -> site build` could drop stream-localized language roots.
- That specific defect is now fixed, but the broader risk remains: `materialize outputs`, `site stage`, and `site build` still coordinate through implicit directory layout conventions rather than an explicit shared contract.
- This area needs broader round-trip regression coverage so future changes do not silently reintroduce missing-language or missing-stream pages.

### 5. Localization coverage still requires manual auditing

- During the live rollout, coverage checks required ad hoc queries against `localized_outputs`, filesystem counts, and site manifests.
- There is no dedicated command that answers:
  - how many item / trend / idea rows have localized variants
  - which pages are missing peer-language variants
  - whether materialized markdown and site manifests are in sync
- Result: operational verification is possible, but more manual than it should be.

### 6. Translation quality control is still mostly manual

- The rollout relied on spot checks for translation quality.
- That was enough to prove the system is usable, but it does not scale well for future incremental runs or provider/model changes.
- High-value automated checks are still missing for:
  - preserved numbers and benchmark names
  - preserved research-native terms and abbreviations
  - unusual length deltas
  - punctuation/link artifacts in rendered markdown and HTML

### 7. Large backfills still have no preflight estimator

- Before the historical backfill, there was no built-in way to estimate:
  - source record count by surface
  - expected translation call volume
  - rough token or cost exposure
- This became more important in practice once provider availability and credit limits affected the rollout.

### 8. Presentation-canonical and retrieval-canonical still diverge

- The current rollout makes English the effective canonical language for rendered markdown and the static site.
- Historical retrieval state is different:
  - canonical `documents`
  - canonical `document_chunks`
  - existing RAG/index state
  still reflect the historical source language unless separately regenerated.
- This is not a correctness bug for the site, but it is a real product boundary that should stay explicit.

### 9. Some language metadata still blur code vs slug semantics

- In manifests and CLI-facing metadata, some fields use names like `default_language_code` while storing normalized slug-shaped values such as `zh-cn`.
- This is currently workable because the accepted language codes also normalize cleanly, but it is still schema debt for any future automation or external consumers.

## Recommended Next Steps

### High priority

- Add `runs` creation and translation-specific metrics to `translate run` and `translate backfill`.
- Record at least:
  - translation call count
  - translated / mirrored / skipped / failed counts
  - prompt / completion tokens when available
  - estimated cost metrics when available
- Add a dedicated localization audit command or doctor mode.
- It should report at least:
  - localized coverage by surface
  - missing peer-language pages
  - orphan localized outputs
  - materialized/site-level mismatches
- Add more round-trip regression coverage for multilingual output layout contracts across:
  - `materialize outputs`
  - `site stage`
  - `site build`

### Medium priority

- Add a narrow post-processing pass for English trend evolution text that normalizes punctuation around inserted history links.
- Keep this post-processing structural and conservative; it should not rewrite evidence content or alter linked titles.
- Add lightweight translation QA checks for terminology preservation, numeric fidelity, and rendered-link punctuation anomalies.
- Add a preflight estimator for large `translate backfill` runs so operators can see candidate counts and rough model spend before starting.

### Lower priority

- Run a dedicated live validation pass for `--context-assist hybrid` against the current local search index.
- Explicitly check:
  - no implicit vector rebuilds
  - fail-open behavior when the index is unavailable
  - whether hybrid context measurably improves terminology disambiguation
- Decide whether the project wants to keep the current split between presentation-canonical output and retrieval-canonical history, or add an optional path to regenerate English-facing document projections.
- Normalize manifest and CLI metadata so fields named `*_language_code` always store language codes rather than slug-shaped display keys.

## Why These Are Deferred

- The rollout is already functionally complete: backfill succeeded, multilingual site output is live, and the main correctness bugs found during real-data verification are fixed.
- The remaining items improve observability, maintainability, and operator confidence more than they change the core localization workflow.
