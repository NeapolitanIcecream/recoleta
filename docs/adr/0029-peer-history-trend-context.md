---
title: "ADR 0029: Peer-history trend context via bounded history packs"
status: Accepted
---

## Context

Recoleta's trend pipeline already uses lower-granularity corpora inside the
current target window, but it did not expose same-granularity history from
earlier windows. That made trend outputs good at summarizing "what happened in
this window" while staying weak at explaining how themes persisted, emerged,
faded, or shifted across time.

At the same time:

- same-period multi-version history is out of scope
- unconstrained historical retrieval would increase tool ambiguity and token
  cost
- user-facing outputs need a dedicated evolution section rather than more prose
  hidden inside `overview_md`

## Decision

Adopt a bounded peer-history design:

1. Define a small list of same-granularity previous windows in the generation
   plan.
2. Materialize those windows into a deterministic `history_pack_md` prompt
   block.
3. Add a structured `evolution` section to `TrendPayload`.
4. Keep agent tools scoped to the active target period; historical context is
   injected, not freely searched.

## Consequences

- Trend outputs can discuss longitudinal change explicitly.
- Historical context remains bounded, inspectable, and cheap to audit.
- Existing storage stays simple because no same-period versioning is added.
- If future quality work shows the history pack is too lossy, historical
  retrieval can be added later as a separate capability rather than being
  coupled to the first rollout.
