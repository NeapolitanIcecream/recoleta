# Trends Agent Loop Phase 2 Plan

Date: 2026-03-12
Status: Draft

## Context

PR #12 established a better baseline for the `trends` agent loop:

- richer RAG tools (`search_hybrid`, `get_doc_bundle`)
- lexical backoff for `search_text`
- per-tool observability and prompt-budget metrics
- must-read workflow downgraded to legacy guidance

The next phase should not continue by adding low-level tools blindly. The main
goal is to improve report quality with a tighter evaluation loop and better
retrieval strategy.

Related note:

- `docs/plans/2026-03-12-trends-agentic-loop-tuning-study.md`

## Goals

1. Raise report quality on fixed historical windows.
2. Reduce failure modes where the agent either misses key evidence or overfits
   shallow summary chunks.
3. Make loop changes measurable with a repeatable eval harness.

## Non-Goals

- redesigning the publish format
- reintroducing must-read / Top-N output requirements
- adding many more primitive navigation tools

## Priority Tracks

### 1. Offline eval harness

Build a fixed-window evaluation set for `day|week|month` trend generation.

Current live-fixture constraint:

- the default live eval fixture should only include `day` and `week` windows for
  now
- `month` remains supported by the harness, but it should stay disabled in the
  default fixture until one calendar month has enough real weekly coverage to
  make quality judgments meaningful
- as of 2026-03-12, the live corpus only has week `2026-W10`, so month scoring
  would mostly measure sparse backfill behavior rather than report quality

Deliverables:

- a small benchmark set of representative historical windows
- a repeatable command or script that runs the trend pipeline on those windows
- stored artifacts for prompt, tool trace, candidate evidence, and final output
- a lightweight scoring rubric for grounding, distinctness, representative
  quality, readability, and cost/latency

Exit criteria:

- we can compare two loop variants on the same windows without manual setup
- failures can be bucketed by retrieval miss, synthesis error, or formatting

### 2. Query rewriting and decomposition

Investigate whether the agent should emit a few shorter task-shaped queries
instead of one long conjunctive query.

Directions:

- split discovery, verification, and counter-signal search intents
- bias toward short lexical queries plus semantic recall
- preserve explicit query budgets to avoid latency blowups

Exit criteria:

- lower miss rate on long-query discovery
- no regression in tool cost on eval windows

### 3. Selective content-chunk retrieval

Current retrieval is still too summary-centric. Add a follow-up retrieval path
that drills into candidate documents and returns only the most relevant content
chunks.

Directions:

- summary-level search to identify candidate docs
- bounded content-chunk semantic retrieval inside those docs only
- evidence packaging that stays smaller than full-document reads

Exit criteria:

- improved grounding for nuanced claims
- fewer cases where reports repeat summary wording without deeper evidence

### 4. Evidence-set ranking

Investigate a higher-level evidence tool or post-processing helper that returns
small, diverse, cluster-ready evidence sets.

Directions:

- dedupe near-identical evidence
- prefer source diversity and time coverage
- avoid over-concentrating on one paper or one trend doc

Exit criteria:

- cluster representatives look more diverse and less redundant on eval samples

### 5. Corpus quality audit

Review whether corpus quality, not loop policy, is the current bottleneck.

Focus areas:

- summary section extraction quality
- content chunk boundaries
- document metadata completeness
- duplicate or near-duplicate trend docs

Exit criteria:

- a concrete list of corpus fixes ranked by expected impact

## Proposed Execution Order

1. Land the offline eval harness.
2. Add query rewriting/decomposition behind an experiment flag.
3. Add selective content-chunk retrieval behind an experiment flag.
4. Evaluate whether evidence-set ranking is necessary after the first two steps.
5. Remove remaining `ranking_n` / legacy must-read plumbing once the new loop is
   stable.

## Experiment Protocol

Each substantive loop change should include:

- one local manual spot check of final trend output
- one spot check of the raw tool outputs
- one eval-harness run against fixed windows
- a short note on quality delta, tool-cost delta, and observed failure modes

## First Concrete Tasks For This PR

1. Add the eval harness scaffold and window fixtures.
2. Capture baseline outputs from the current merged loop.
3. Use those outputs to decide the first query rewriting experiment.
