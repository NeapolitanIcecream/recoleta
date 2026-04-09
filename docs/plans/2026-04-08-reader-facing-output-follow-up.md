# Reader-Facing Output Follow-up

Date: 2026-04-08

Status: implemented on `codex/reader-facing-output-deformalization` and tracked in PR #40

## Purpose

Record the research findings on reader-facing output quality, the conclusions
reached in the April 8 discussion, and the implementation direction that was
later applied.

The findings section below is intentionally historical: it captures the
pre-change state that motivated this work. The current implemented state is
summarized separately below.

This document supersedes my earlier rough proposal in one important way:
`item docs` are **not** part of the planned structural change. The follow-up is
mainly about `trends`, `ideas`, and the prompts that drive them.

One correction from the discussion:

- `item docs` keep their current four-part structure
- `item docs` should still adopt the same stricter anti-tropes prompt

## Evidence Reviewed

### Code paths

- `recoleta/analyzer.py`
- `recoleta/item_summary.py`
- `recoleta/prompt_style.py`
- `recoleta/rag/agent.py`
- `recoleta/rag/ideas_agent.py`
- `recoleta/presentation.py`
- `recoleta/publish/trend_notes.py`
- `recoleta/publish/idea_notes.py`
- `recoleta/site.py`
- `recoleta/site_presentation.py`
- `recoleta/trends_overview.py`

### Tests and fixtures

- `tests/test_ideas_agent_prompt.py`
- `tests/test_publish_idea_notes.py`
- `tests/test_trends_static_site.py`
- `tests/test_output_quality_2026w12_regression.py`
- `tests/fixtures/output_quality/2026w12/software_intelligence-trend.json`
- `tests/fixtures/output_quality/2026w12/software_intelligence-ideas.json`

### Local fleet outputs inspected

The default `RECOLETA_CONFIG_PATH` in the current environment points to
`<playground-root>/recoleta.yaml`, but the actual multi-instance outputs under
review live in the local fleet manifest:

- `<playground-root>/fleet/fleet.yaml`
- `<playground-root>/fleet/instances/embodied_ai/recoleta.yaml`
- `<playground-root>/fleet/instances/software_intelligence/recoleta.yaml`

The current child `markdown_output_dir` values are:

- `<playground-root>/fleet/instances/embodied_ai/outputs`
- `<playground-root>/fleet/instances/software_intelligence/outputs`

Concrete reader-facing artifacts inspected from those output trees:

- `.../software_intelligence/outputs/Trends/day--2026-03-30--trend--29.md`
- `.../software_intelligence/outputs/Ideas/day--2026-03-30--ideas.md`
- `.../software_intelligence/outputs/Inbox/2026-03-30--pi-another-ai-agent-toolkit-but-this-one-is-interesting.md`
- the corresponding `site/en/...` artifacts and HTML pages
- `.../embodied_ai/outputs/Trends/day--2026-03-30--trend--8.md`
- `.../embodied_ai/outputs/Ideas/day--2026-03-30--ideas.md`

## Pre-change Findings

### 1. The main problem is not missing structure

The main problem is that internal analysis structure is being exposed as the
reader-facing interface.

The current pipeline does not merely guide the model internally. It asks the
model for explicit public sections, then preserves those sections through
presentation building, markdown rendering, site rendering, tests, and fixtures.

This is most visible in `ideas` and `trends`.

### 2. `trends` currently expose too much analysis scaffolding

Current public trend surfaces explicitly render:

- `Overview`
- `Counter-signal`
- `Clusters`
- `Representative sources`

The live `software_intelligence` day brief for 2026-03-30 shows the problem
directly:

- `## Counter-signal` is a full public section
- `Pi` appears there as an example of tooling that is "still pre-benchmark"
- the same output then renders `Clusters` as another explicit analysis surface

This structure makes the final note read like an agent worksheet instead of a
finished brief.

### 3. `ideas` currently expose the methodology almost verbatim

Current public idea surfaces explicitly render:

- `Best bet`
- `Alternate`
- `Type`
- `Horizon`
- `Role`
- `Thesis`
- `Anti-thesis`
- `Why now`
- `What changed`
- `Validation next step`
- `Evidence`

The live `software_intelligence` ideas note for 2026-03-30 shows the issue in
two layers:

- the `Summary` section already previews `Best bet` and `Alternate 1/2`
- the `Opportunities` section then repeats the same ranking and expands each
  opportunity into labeled field blocks

The result is structurally valid but reads like a prompt template rendered back
to the reader.

### 4. The output contract itself now reinforces formalism

The current public contract is not just a prompt problem.

- `recoleta/rag/ideas_agent.py` explicitly asks for a clear `best bet`,
  explicit `alternates`, and an `anti-thesis`
- `recoleta/presentation.py` converts idea order into `best_bet` and
  `alternate` tiers
- `recoleta/publish/idea_notes.py` renders those tiers and field labels into
  markdown
- `recoleta/site.py` renders the same fields into public cards
- tests and golden fixtures assert that these labels must appear

The same pattern exists for trend `counter_signal`.

### 5. The current anti-tropes prompt is still too soft

The shared style prompt in `recoleta/prompt_style.py` is directionally correct,
but it still frames several bad patterns as things that may happen once in
isolation.

That is too permissive for this project.

In practice, once a phrase family such as `not X but Y` or Chinese
`不是……而是……` is allowed as an occasional flourish, the model reuses it as a
default rhetorical move across many outputs. The result is the "uncanny valley"
effect noted in the discussion.

### 6. `item docs` stay out of scope structurally, but not stylistically

I originally treated the `Pi` item note as part of the same fix surface because
its prose includes phrases such as:

- `Strongest concrete claim`
- `Strongest concrete evidence of maturity`

After discussion, the decision is different:

- the four-part item structure is acceptable
- this follow-up must not reopen `item docs` structure
- the trends and ideas redesign should not be blocked on revisiting item notes
- but `item docs` should still use the stricter shared anti-tropes prompt

This means the current follow-up should not change:

- `recoleta/item_summary.py`
- item-note rendering contracts

But it should later revisit:

- `recoleta/analyzer.py`
- shared prompt wiring for reader-facing prose

## Discussion Conclusions

The following points reflect the agreed direction from the April 8 discussion.

### 1. Internal analysis structure is allowed

Internal structure can still exist in prompts and analysis methodology.

Examples:

- asking the model to reason about strongest claim, weak evidence, buyer,
  timing, failure conditions, or contradictory evidence
- using hidden fields or structured intermediate reasoning for ranking and
  quality control

That is acceptable as long as it remains internal.

### 2. Reader-facing output must be a finished short piece, not the worksheet

The public artifact should be the finished piece of writing.

It must not render each analysis axis as its own explicit section just because
that axis was useful during reasoning.

The key distinction is:

- structure may organize blocks
- the prose inside each block should read like normal writing
- the analysis worksheet must not be shown verbatim to the reader

### 3. Removed sections must disappear, not be folded back into prose as labels

This was the main correction to my earlier proposal.

If `Counter-signal`, `Best bet`, `Alternate`, `Thesis`, `Anti-thesis`, and
similar fields are merely collapsed into paragraph text with different wording,
the formalism still survives.

That is not acceptable.

The actual requirement is stricter:

- do not ask the agent to emit these reader-facing sections
- do not preserve them in the public presentation schema
- do not render them in markdown or site output

### 4. `item docs` remain unchanged

The four-part item structure is considered reasonable and readable.

This follow-up should leave item docs alone structurally and focus the output
surface redesign on trends and ideas.

But item docs should still participate in the shared anti-tropes discipline.
The current gap is that item generation does not yet reuse the same
reader-facing prompt contract.

### 5. Anti-tropes enforcement should stay in prompts

No lint layer is planned for this work.

No retry-based style enforcement is planned for this work.

The change should happen in prompt wording itself:

- change soft suggestions into hard requirements
- remove the current tolerance for "one isolated instance"
- require the model to choose a different formulation every time instead of
  falling back to trope patterns

### 6. Translation should optimize for accuracy, not separate style policing

Translation should remain accuracy-first.

If source-language prose is good, faithful translation is acceptable.

The translation prompt can be improved if needed, but this follow-up should not
introduce separate Chinese-only rewrite rules or a Chinese-only trope filter.

## Agreed Design Direction

### Trends

Reader-facing trend output should keep only the high-level surfaces that are
useful to a reader:

- `Overview`
- `Clusters`

The deleted sections should not survive in disguised form.

Specifically, the reader-facing trend output should stop exposing:

- `Top shifts`
- `Counter-signal`
- top-level `Representative sources`

Those can still influence internal reasoning, but they should not be emitted as
public sections.

Within the remaining trend surfaces, the reader-facing primitive should be
simple:

- `title`
- `content`
- `evidence`

In practice that means:

- the page has a title
- the overview block is prose content
- each cluster is a block with a title, a short finished piece of prose, and
  supporting evidence

This is a design proposal, not just a restatement of the complaint: use one
small reader-facing block shape repeatedly instead of exposing analysis fields.

### Ideas

Reader-facing ideas output should keep only a very small number of useful
blocks, and the content inside each block must read like a finished short note
rather than a field dump.

The intended reader-facing shape is:

- page title
- one short overview/content block
- one or more idea blocks

Each idea block should contain only:

- `title`
- `content`
- `evidence`

Ordering can still express priority, but the note should not spell that
priority out as a methodological label.

The public output should stop exposing:

- `Best bet`
- `Alternate`
- `Type`
- `Horizon`
- `Role`
- `Thesis`
- `Anti-thesis`
- `Why now`
- `What changed`
- `Validation next step`
- `Source type`
- `Confidence`

Ranking may still exist internally, and ordering may still matter, but the
public note should not spell out the methodology as labels.

The concrete implication is important:

- do not replace `Best bet` with a hidden first paragraph that still reads like
  a best-bet field
- do not flatten `Thesis`, `Why now`, and `Validation next step` into adjacent
  mini-sections without headings
- instead, synthesize them into one coherent short piece of prose for that idea

### Prompts

Prompt work should do three things:

1. Keep internal reasoning aids available to the model.
2. Stop instructing the model to emit those aids as public sections.
3. Turn the anti-tropes rules from permissive guidance into hard requirements.

That includes an explicit hard ban on negative-parallelism patterns such as:

- `not X but Y`
- `It is not X. It is Y.`
- Chinese `不是……而是……`

The prompt should require a different formulation, not merely suggest one.

This stricter anti-tropes rule should also be shared by `item docs`, even
though their section structure stays unchanged.

## Implemented State

- `item docs` keep the same four-part reader-facing structure
- `item docs` now share the stricter anti-tropes prompt discipline
- reader-facing `trends` keep only `Overview` and `Clusters` as public blocks
- each reader-facing trend cluster is a finished prose block with `title`,
  `content`, and `evidence`
- reader-facing `ideas` keep a short page summary plus ordered idea blocks
- each reader-facing idea block is a finished prose block with `title`,
  `content`, and `evidence`
- removed worksheet labels no longer appear in the public presentation schema,
  markdown notes, or site output

## Implemented Change Set

This direction was not a prompt-only change.

The implemented change set included at least:

1. Prompt contract updates in `recoleta/rag/agent.py` and
   `recoleta/rag/ideas_agent.py`
2. Shared anti-tropes prompt adoption for item analysis in
   `recoleta/analyzer.py`
3. A stricter shared style prompt in `recoleta/prompt_style.py`
4. Presentation-contract simplification in `recoleta/presentation.py`
5. Markdown renderer changes in `recoleta/publish/trend_notes.py` and
   `recoleta/publish/idea_notes.py`
6. Site renderer changes in `recoleta/site.py` and
   `recoleta/site_presentation.py`
7. Regression-fixture and test updates so the suite stops requiring the
   removed public labels and sections

## Non-Goals

- Do not redesign `item docs` structure
- Do not add a lint or retry enforcement layer
- Do not add Chinese-only style rules
- Do not solve this by merely hiding section titles while preserving the same
  public field-by-field content

## Summary

The current problem is not that Recoleta lacks structure. The problem is that
too much internal structure is being shown to the reader.

The agreed next-step direction is:

- leave `item docs` alone
- connect `item docs` to the same stricter anti-tropes prompt
- reduce `trends` and `ideas` to reader-useful top-level blocks
- keep analysis scaffolding inside prompts and internal logic
- stop rendering that scaffolding as public sections
- make anti-trope rules hard requirements inside prompts rather than soft
  suggestions

## Proposal

One useful generalization from this discussion is to standardize the
reader-facing block shape across `trends` and `ideas`:

- `title`
- `content`
- `evidence`

This is not another abstraction layer for its own sake. It is a way to stop the
system from inventing a different visible worksheet for every surface.

The internal methodology can stay richer than this. The public writing should
not.
