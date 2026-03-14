# Ideas Real-Data Smoke And Calibration

Date: 2026-03-14  
Branch: `codex/trends-pass-architecture`

## Goal

Validate `recoleta ideas` against the live local workspace on real windows, then
decide whether prompt changes are required before broader use.

This pass was intentionally limited to:

- real corpus runs, not synthetic fixtures
- output quality and failure-mode inspection
- user-facing CLI and documentation gaps discovered during the runs

It explicitly did not target scheduler or long-term operations work.

## Runtime Context

The runs used the operator's active local workspace and current configured
model stack:

- database: `~/.local/share/recoleta/recoleta.db`
- markdown output root: `~/.local/share/recoleta/outputs`
- vector store: `~/Library/Application Support/recoleta/lancedb`
- model: `openai/openai/gpt-5.4`
- output language: `Chinese (Simplified)`

Active topic streams in this workspace:

- `embodied_ai`
- `software_intelligence`

## Method

First, create the needed upstream canonical trend outputs:

```bash
uv run recoleta trends --granularity day --date 2026-03-09
uv run recoleta trends --granularity week --date 2026-03-05 --backfill
```

Then run the ideas pass on the same windows:

```bash
uv run recoleta ideas --granularity day --date 2026-03-09
uv run recoleta ideas --granularity week --date 2026-03-05
```

Windows audited:

- `day` window for `2026-03-09`
- `week` window anchored by `2026-03-05`  
  This resolves to ISO week 10, starting `2026-03-02`.

Per-stream audited outputs:

- `embodied_ai` day
- `software_intelligence` day
- `embodied_ai` week
- `software_intelligence` week

## Results

### Run health

- matching upstream `trend_synthesis` pass outputs were created successfully
- `recoleta ideas` succeeded for all four audited stream-window combinations
- markdown idea briefs were written for all four successful runs

Observed note paths:

- `~/.local/share/recoleta/outputs/Streams/embodied_ai/Ideas/day--2026-03-09--ideas.md`
- `~/.local/share/recoleta/outputs/Streams/software_intelligence/Ideas/day--2026-03-09--ideas.md`
- `~/.local/share/recoleta/outputs/Streams/embodied_ai/Ideas/week--2026-W10--ideas.md`
- `~/.local/share/recoleta/outputs/Streams/software_intelligence/Ideas/week--2026-W10--ideas.md`

### Quality readout

The outputs cleared the minimum bar for rollout.

Positive signals:

- ideas stayed tightly grounded in trend evidence rather than drifting into
  generic product advice
- each idea consistently included a concrete `why now`, `what changed`, and
  `validation next step`
- the software-intelligence stream especially produced strong infrastructure
  wedges such as prompt CI/CD, safety monotonicity checks, harness generation,
  and production gating
- the embodied-ai stream found clear deployment-era wedges rather than
  defaulting to "build a bigger foundation model"

What did not show up:

- no obvious prompt collapse
- no repeated boilerplate titles across the four outputs
- no need for emergency schema or normalization changes

## Findings

### 1. No prompt rewrite is required from this sample

The first real-data sample is good enough to keep the current prompt.

Interpretation:

- the existing prompt already pushes the model toward evidence-grounded,
  opportunity-shaped outputs
- prompt tuning should now be incremental and evidence-driven, not a reset

Recommendation:

- keep the current prompt as the baseline
- gather more windows before making quality-driven prompt changes

### 2. The main defect found was in CLI presentation, not content quality

In topic-stream mode, `recoleta ideas` originally printed only the first stream
result even though all stream outputs were created and persisted.

Impact:

- operators could misread a successful multi-stream run as a single-stream run
- the missing output made real-data audits harder than necessary

Action taken in this pass:

- update the CLI to print an aggregate line plus one per-stream line, mirroring
  `recoleta trends`
- add a regression spec for the multi-stream CLI behavior

### 3. The more urgent gap was user documentation

Before this pass, the command existed but README usage guidance did not explain:

- that `recoleta ideas` depends on existing `trend_synthesis` outputs
- where idea briefs are written
- what `suppressed` means
- what multi-stream output looks like

Action taken in this pass:

- add a dedicated README subsection for `recoleta ideas`
- add the command to the CLI command list

## Conclusion

`recoleta ideas` looks ready to keep behind the current manual workflow without
additional prompt surgery. The right next step is not scheduler work; it is more
selective real-window auditing as new topic windows accumulate.

The concrete follow-up from this study was therefore:

1. keep the prompt baseline unchanged
2. fix the multi-stream CLI presentation bug
3. document the command and its output contract
