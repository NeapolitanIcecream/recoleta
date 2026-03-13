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
