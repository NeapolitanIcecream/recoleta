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

## Recommended Next Steps

### High priority

- Add `runs` creation and translation-specific metrics to `translate run` and `translate backfill`.
- Record at least:
  - translation call count
  - translated / mirrored / skipped / failed counts
  - prompt / completion tokens when available
  - estimated cost metrics when available

### Medium priority

- Add a narrow post-processing pass for English trend evolution text that normalizes punctuation around inserted history links.
- Keep this post-processing structural and conservative; it should not rewrite evidence content or alter linked titles.

### Lower priority

- Run a dedicated live validation pass for `--context-assist hybrid` against the current local search index.
- Explicitly check:
  - no implicit vector rebuilds
  - fail-open behavior when the index is unavailable
  - whether hybrid context measurably improves terminology disambiguation

## Why These Are Deferred

- The rollout is already functionally complete: backfill succeeded, multilingual site output is live, and the main correctness bugs found during real-data verification are fixed.
- The remaining items improve observability and polish, not the core localization workflow.
