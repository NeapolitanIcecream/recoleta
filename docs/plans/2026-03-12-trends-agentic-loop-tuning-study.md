# Trends Agentic Loop Tuning Study

Date: 2026-03-12  
Status: Draft

## Scope

This note studies how to improve the `trends` agentic loop so it produces more
useful and more reliable research trend reports. The focus is not only raw
latency or cost. The main target is output quality under bounded tool/token
budgets.

The study covers:

- tool design and tool granularity
- tool budgets and prompt budgets
- retrieval and ranking algorithms
- corpus quality and evidence packaging
- observability and evaluation

## Current Loop

As of the current codebase, the `trends` loop has four strong foundations:

1. A self-similar corpus plan for `day|week|month`, with overview-pack prompt
   pre-injection and multi-level RAG source routing.
2. Typed `TrendPayload` validation at the agent boundary.
3. Deterministic post-processing that enforces paper-level representatives.
4. Existing quality regressions around published markdown shape and citation
   hygiene.

However, the actual model-facing loop is still fairly low-level:

- tools are mostly primitive navigation tools (`list_docs`, `get_doc`,
  `read_chunk`, `search_text`, `search_semantic`)
- semantic retrieval only searches summary chunks
- the model has very little built-in guidance on which tool to use first and
  when to stop
- tuning is mostly blind because the default metrics emphasize whole-run usage
  but not tool mix or prompt size

## Findings

### 1. Tool schemas were under-descriptive

Before this change, the trend tools exposed no docstring-derived descriptions.
For `pydantic-ai`, that means the model saw tool names and JSON schemas, but
not much semantic guidance about when each tool should be used.

Impact:

- weaker tool selection
- more exploratory calls to discover obvious behavior
- lower chance that the model follows the intended retrieval sequence

### 2. Retrieval primitives were too split for discovery

The previous loop forced the model to choose between:

- lexical search over all chunks
- semantic search over summary chunks

This is workable, but it makes the first retrieval step harder than necessary.
In practice, trend discovery usually benefits from combining exact phrase hits
and semantic neighbors, then drilling deeper only on the strongest overlaps.

Impact:

- extra planning burden on the model
- higher probability of missing evidence when a query is paraphrased
- more tool hops (`search_* -> get_doc -> read_chunk`) before synthesis starts

### 3. Tuning signals were too coarse

The pipeline recorded `pipeline.trends.tool_calls_total`, but that signal was
not reliable for normal runs because tool-call counting was tied to the debug
artifact path. Even when present, a single total count is not enough to tune the
loop.

What was missing:

- which tools dominate a run
- whether the loop leans on search or on document inspection
- how large the final prompt payload is
- how much of the prompt budget is consumed by `overview_pack_md`

Impact:

- budget tuning is guesswork
- tool additions/removals are hard to validate
- regressions can hide behind unchanged total call counts

### 4. The loop still lacks higher-level evidence tools

The current tools are good building blocks, but not ideal final abstractions.
The model still needs multiple calls to answer simple questions such as:

- “show me the best evidence bundle for this paper”
- “give me the strongest evidence for this cluster hypothesis”
- “compare this week against prior day trends”

Impact:

- too much low-value navigation
- risk of early summarization before enough evidence is collected
- high variance in clustering quality when the model stops exploring too early

### 5. Semantic retrieval is summary-only

Summary-only vectors are cheap and robust, but they cap the ceiling:

- they miss terminology that only appears in content chunks
- they compress away disagreements, limitations, and result details
- they make cluster evidence look more homogeneous than the underlying corpus

Impact:

- weaker support for nuanced claims
- lower recall on cross-paper theme discovery
- legacy ranked-reading-list logic can over-index on summary style instead of
  paper substance

### 6. Output quality gates are still mostly formatting-oriented

The existing regressions do a good job preventing embarrassing publish-time
leaks. They do not yet act as a strong harness for agent behavior quality.

What is still missing:

- fixed-window eval sets for day/week/month
- tool-trace regressions
- tool-output quality tracking
- cluster coverage/diversity checks
- an automated “judge” or rubric pass over generated reports

## Local Spot Checks

I manually spot-checked the local tool outputs on a tiny seeded corpus after the
tooling changes.

Observed behavior:

1. `search_text` can return useful `content`-chunk snippets when the query is
   short and lexical, for example `retrieval`, `memory loop`, or
   `retrieval coordinator`.
2. `search_text` is brittle for long conjunctive queries. On the local sample,
   `agent memory retrieval loops` returned zero hits despite an obviously
   relevant document.
3. `search_semantic` was much more robust for theme discovery, but it only
   returned summary-chunk previews, not deeper evidence.
4. `search_hybrid` therefore improved the entry-point behavior, but in cases
   where lexical search misses entirely it still collapses to semantic-only
   retrieval.
5. `get_doc` plus `read_chunk` provided enough follow-up evidence, but it still
   required multiple tool hops to inspect one promising paper.

Interpretation:

- `search_text` is useful as a precision tool, not as the only discovery tool.
- `search_semantic` is useful as a recall tool, but its evidence is too shallow.
- `search_hybrid` is the right direction, but the next step should be better
  lexical backoff / query rewriting plus a higher-level `get_doc_bundle` tool.

## Changes Landed In This Pass

This study landed a first tranche of low-risk loop improvements:

1. Tool descriptions
   Existing trend tools now expose docstring-derived descriptions so the model
   sees when to use them, not just their names.

2. Hybrid retrieval
   Added `search_hybrid`, which fuses lexical and semantic results with
   reciprocal-rank fusion and returns richer document metadata on hits.

3. Richer retrieval payloads
   Search hits now carry document metadata such as title, canonical URL, and
   authors when available. This lowers the need for follow-up probing calls.

4. Default-on tool diagnostics
   Tool-call totals are now computed for normal runs, not only when debug
   artifacts are enabled.

5. Per-tool metrics
   The pipeline now records low-cardinality metrics such as:
   - `pipeline.trends.tool.search_hybrid.calls_total`
   - `pipeline.trends.tool.search_text.calls_total`
   - `pipeline.trends.tool.read_chunk.calls_total`

6. Prompt budget signals
   The pipeline now records:
   - `pipeline.trends.prompt_chars`
   - `pipeline.trends.overview_pack.chars`

These changes do not solve the full quality problem, but they create a much
better tuning surface.

## Must-Read Workflow

The old Top-N must-read workflow should be treated as legacy.

Reason:

- it is no longer a primary user-facing deliverable
- it biases the agent toward ranking behavior that does not obviously improve
  the published note
- it consumes prompt and retrieval budget that is often better spent on
  clustering, evidence quality, and synthesis

Recommendation:

- stop treating must-read as a required section
- keep `ranking_n` only as backward-compatibility metadata for now
- optimize for grounded clusters and concise overview quality instead

## Context7-Inspired Lessons

From the official Context7 docs and repository, three practices are especially
relevant here:

1. Resolve to the right corpus/tool target before broad retrieval.
   Context7 treats “find the right library ID” as a first-class step, instead of
   immediately retrieving arbitrary snippets.

2. Keep retrieval queries narrow and task-shaped.
   Context7 explicitly recommends detailed natural-language questions over vague
   keywords, and warns that narrower queries retrieve better context.

3. Cache and reuse stable retrieval context.
   Context7 recommends caching docs responses because the source corpus changes
   relatively infrequently. Recoleta already does this for summary-vector warmup;
   the same idea can be extended to higher-level evidence bundles.

Applied to `trends`, that suggests:

- more explicit retrieval stages
- fewer low-level navigation hops
- stronger bundle-style tools instead of more primitive snippet fetches

## Recommended Next Steps

### P0: Highest ROI

1. Add `get_doc_bundle`
   Return one compact evidence bundle per document:
   - doc metadata
   - summary chunk
   - top content chunks
   - extracted problem / approach / results fields when available

   Why:
   This removes repeated `get_doc + read_chunk` loops and gives the model a
   higher-quality evidence primitive.

2. Make agent budgets explicit and configurable
   Add settings for:
   - request limit
   - tool-calls limit
   - optional input/output token limits

   Why:
   Once tool breakdown metrics exist, budget tuning becomes empirical instead of
   speculative.

### P1: Quality ceiling work

1. Add selective semantic search over content chunks
   Do not embed the entire corpus blindly. Start with:
   - top-ranked items only
   - abstracts / main results chunks
   - cluster-backfill queries only

2. Add cluster validation and repair
   After the model drafts clusters, run deterministic checks for:
   - duplicate cluster titles
   - representative overlap between clusters
   - clusters with no evidence support
   - clusters dominated by a single document

3. Add a compare-period tool
   Let weekly/monthly synthesis explicitly compare:
   - carry-over themes
   - genuinely new themes
   - dropped themes
   - evidence disagreements

### P2: Evaluation infrastructure

1. Build a fixed-window eval suite
   Curate representative daily and weekly windows with reference expectations:
   - expected evidence bundles
   - expected themes
   - citation quality
   - unacceptable failure patterns

2. Store tool-trace summaries per eval run
   Track:
   - per-tool counts
   - prompt chars
   - output tokens
   - retrieval overlap statistics

3. Add a rubric-based report evaluator
   Even a lightweight LLM-as-judge or heuristic scorer would help compare:
   - grounding
   - novelty
   - non-redundancy
   - readability

## Suggested Experiments

### Experiment A: Hybrid search adoption

Question:
Does `search_hybrid` reduce tool hops while improving theme recall?

Compare:

- baseline tools only
- hybrid enabled + tool descriptions

Track:

- per-tool call mix
- average `read_chunk` calls per report
- citation coverage
- judged theme recall

### Experiment B: Overview-pack budget sweep

Question:
Where is the quality/cost knee for `overview_pack_max_chars`?

Sweep:

- `2000`
- `4000`
- `8000`
- `12000`

Track:

- prompt chars
- input tokens
- cluster duplication
- evidence quality
- judged synthesis depth

## Recommendation

Priority order for the next tuning cycle:

1. `get_doc_bundle`
2. explicit agent budget settings
3. lexical-backoff improvements for `search_text`
4. selective content-chunk semantic retrieval
5. offline eval harness

The general principle should be:

- move more repetitive navigation into deterministic tools
- keep synthesis inside the model
- make tool/budget tradeoffs observable
- evaluate on fixed windows before changing defaults
