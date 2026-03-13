# Peer-History Trends Eval

Date: 2026-03-13  
Branch: `codex/trends-history-evolution`

## Goal

Validate that same-granularity peer history:

1. produces a dedicated `Evolution` section when prior windows exist
2. stays suppressed when prior windows do not exist
3. does not require replaying the live workspace directly

## Method

Used the existing eval harness in `scripts/eval_trends_agent_loop.py` with
`--capture-mode existing-corpus`, which:

- clones the configured SQLite + LanceDB workspace under the eval output root
- reruns real `recoleta trends` generation against the copied corpus
- writes payload, tool trace, debug artifacts, and published notes for audit

Baseline command:

```bash
TRENDS_PEER_HISTORY_ENABLED=false \
uv run python scripts/eval_trends_agent_loop.py \
  --out bench-out-peer-history-control-v2 \
  --capture-baseline \
  --capture-mode existing-corpus
```

Treatment command:

```bash
TRENDS_PEER_HISTORY_ENABLED=true \
TRENDS_PEER_HISTORY_WINDOW_COUNT=3 \
TRENDS_PEER_HISTORY_MAX_CHARS=3000 \
TRENDS_EVOLUTION_MAX_SIGNALS=4 \
uv run python scripts/eval_trends_agent_loop.py \
  --out bench-out-peer-history-treatment-v2 \
  --capture-baseline \
  --capture-mode existing-corpus
```

Windows used:

- `day-2026-03-05-software-intelligence`
- `week-2026-03-05-software-intelligence`

## Results

### Day window: history available

- Control:
  - no `history_pack_md`
  - no `evolution` payload section
  - published note has no `## Evolution`
  - tool calls: `10`
- Treatment:
  - `history_pack_chars=2415`
  - history coverage: `requested=3`, `available=3`, `missing=0`
  - `evolution` payload present with `4` signals
  - published note contains `## Evolution`
  - tool calls: `7`

Interpretation:

- The new feature activated on a real historical window with no manual seeding.
- The resulting note added the intended section without increasing tool usage.

### Week window: no history available

- Control:
  - no `history_pack_md`
  - no `evolution`
  - published note has no `## Evolution`
- Treatment:
  - `history_pack_chars=324`
  - history coverage: `requested=3`, `available=0`, `missing=3`
  - `evolution` was suppressed deterministically
  - published note still has no `## Evolution`
  - tool calls: `9`

Interpretation:

- The feature degrades safely when prior same-granularity windows are missing.
- Prompt-only behavior was not considered sufficient; the implementation now
  enforces suppression without history as a hard invariant.

## Audit Artifacts

- Control: `bench-out-peer-history-control-v2/`
- Treatment: `bench-out-peer-history-treatment-v2/`

Useful files per window:

- `payload.json`
- `tool-trace.json`
- `published/Trends/*.md`
- `debug-artifacts/**/llm_response*.json`

## Conclusion

The peer-history design is effective on real day-level windows with available
history and safe on week-level windows without it. The current rollout looks
good enough to keep behind config and iterate on prompt quality rather than
changing the storage model again.

## Follow-up Tightening (v3)

After the initial rollout, two follow-up constraints were added:

1. `evolution.signals[].change_type` is now constrained to a fixed enum
   (`continuing`, `emerging`, `fading`, `shifting`, `polarizing`) with a small
   alias normalizer for common variants such as `strengthening`.
2. `evolution.signals[].history_windows` is now constrained to valid historical
   `prev_n` window ids. The history pack explicitly exposes
   `current_period_token`, `requested_window_ids`, `available_window_ids`, and
   `missing_window_ids`, and pipeline normalization drops current-window or
   invalid references.

Follow-up control command:

```bash
TRENDS_PEER_HISTORY_ENABLED=false \
uv run python scripts/eval_trends_agent_loop.py \
  --out bench-out-peer-history-control-v3 \
  --capture-baseline \
  --capture-mode existing-corpus
```

Follow-up treatment command:

```bash
TRENDS_PEER_HISTORY_ENABLED=true \
TRENDS_PEER_HISTORY_WINDOW_COUNT=3 \
TRENDS_PEER_HISTORY_MAX_CHARS=3000 \
TRENDS_EVOLUTION_MAX_SIGNALS=4 \
uv run python scripts/eval_trends_agent_loop.py \
  --out bench-out-peer-history-treatment-v3 \
  --capture-baseline \
  --capture-mode existing-corpus
```

### Day window follow-up audit

- Control:
  - `history_pack_chars=0`
  - `evolution=null`
  - published note still has no `## Evolution`
  - tool calls: `7`
- Treatment:
  - `history_pack_chars=2621`
  - history coverage: `requested=3`, `available=3`, `missing=0`
  - published note contains `## Evolution` with `4` signals
  - every `change_type` is within the enum
  - every `history_windows` entry is a canonical `prev_n` id
  - normalization stats stayed at zero:
    - `history_windows_normalized_total=0`
    - `history_windows_dropped_total=0`
    - `signals_dropped_total=0`
  - tool calls: `10`

Interpretation:

- The tightened contract held on a real rerun without needing post-hoc repairs.
- The final published note remained readable and the `Evolution` section now
  uses stable machine-readable identifiers instead of raw dates.

### Week window follow-up audit

- Treatment:
  - `history_pack_chars=528`
  - history coverage: `requested=3`, `available=0`, `missing=3`
  - `available_window_ids=[]`
  - `evolution=null`
  - published note still has no `## Evolution`

Interpretation:

- The richer history pack metadata does not weaken the safe-degradation path.
- The system still refuses to fabricate temporal comparisons when same-level
  history does not exist.

### Manual Output Quality Notes

- Audit focus:
  - `payload.json`
  - `tool-trace.json`
  - `published/Trends/*.md`
- Day treatment quality is better than the first rollout in two specific ways:
  - the `Evolution` section is now structurally clean and easy to audit
  - the model no longer emits raw dates or free-text window references
- Remaining quality issue:
  - note rendering still surfaces the enum token as English (`Change:
    continuing`) inside an otherwise Chinese note. This is acceptable for now
    because it preserves the machine-readable contract, but it is a clear
    presentation refinement target.

## Reader-Facing Iteration (v5)

This follow-up iteration targeted two practical quality issues:

1. history window mentions such as `prev_1` / `prev_2` should render as
   publish-target-friendly links inside the `Evolution` body, not only in the
   separate `history_windows` bullet
2. `Evolution` should become more evidence-dense by favoring named papers,
   systems, and concrete numbers over generic temporal prose

Additional changes:

- render-time linkification now rewrites inline `prev_n` mentions inside
  `Evolution.summary_md` and `Evolution.signals[].summary`
- the trend prompt now explicitly requires named historical anchors from
  `history_pack_md` and instructs the model to keep inline historical mentions
  as `prev_n` tokens so publishing can linkify them
- context budgets were raised again:
  - app defaults:
    - `overview_pack_max_chars=16000`
    - `item_overview_top_k=28`
    - `item_overview_item_max_chars=800`
    - `peer_history_max_chars=12000`
  - eval harness defaults:
    - `overview_pack_max_chars=14000`
    - `item_overview_top_k=20`
    - `item_overview_item_max_chars=600`
    - `peer_history_max_chars=12000`

Control command:

```bash
TRENDS_PEER_HISTORY_ENABLED=false \
uv run python scripts/eval_trends_agent_loop.py \
  --out bench-out-peer-history-control-v5 \
  --capture-baseline \
  --capture-mode existing-corpus
```

Treatment command:

```bash
TRENDS_PEER_HISTORY_ENABLED=true \
TRENDS_PEER_HISTORY_WINDOW_COUNT=3 \
TRENDS_EVOLUTION_MAX_SIGNALS=4 \
uv run python scripts/eval_trends_agent_loop.py \
  --out bench-out-peer-history-treatment-v5 \
  --capture-baseline \
  --capture-mode existing-corpus
```

### Day window v5 audit

- Control:
  - no `## Evolution`
  - `prompt_chars=16284`
  - LLM usage: `input_tokens=47920`, `output_tokens=1802`, `requests=3`
  - tool calls: `8`
- Treatment:
  - published note contains `## Evolution`
  - inline history mentions are now linkified inside prose, e.g.
    `[prev_1 (2026-03-04)](...)`, not just listed separately
  - `Evolution` now names concrete works and metrics:
    - CodeScout: up to `+27` resolved issues
    - RepoLaunch: build success rate about `70%`
    - Tool-Genesis: `gpt-5.1` SR `0.372 -> 0.604`
    - TML-Bench: only `23/40` scaling curves monotonic
    - OpenDev: `5` safety layers and `4` architectural layers
  - `prompt_chars=18995`
  - LLM usage: `input_tokens=53078`, `output_tokens=2311`, `requests=3`
  - tool calls: `9`

Interpretation:

- The extra budget stayed well below the informal `100k` per-run ceiling.
- Cost increased modestly for the day treatment, but the additional evidence
  materially improved `Evolution` specificity and fixed the reader-facing
  `prev_n` leakage problem from v3.

### Week window v5 audit

- Treatment:
  - published note still has no `## Evolution`
  - `prompt_chars=8161`
  - LLM usage: `input_tokens=66157`, `output_tokens=2269`, `requests=5`
  - tool calls: `24`
- Control:
  - published note has no `## Evolution`
  - LLM usage: `input_tokens=89544`, `output_tokens=2527`, `requests=5`
  - tool calls: `24`

Interpretation:

- Safe degradation remains intact even after budget increases.
- The richer peer-history path did not inflate the week run beyond the control;
  in this capture the control week actually used more input tokens.

### Manual quality comparison

- Versus v3:
  - better: no reader-facing `Change: continuing`
  - better: inline historical references are now clickable in body prose
  - better: evolution paragraphs are more concrete and paper-specific
- Versus the historical pre-evolution note:
  - better: now expresses an actual cross-window delta instead of only a
    same-window topical summary
  - better: keeps claims grounded with concrete metrics
  - tradeoff: the note is longer and the added `Evolution` section still shares
    some vocabulary with `Overview`, so there is still room to tighten prose
