---
source: hn
url: https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md
published_at: '2026-03-04T23:34:26'
authors:
- sbw70
topics:
- byzantine-fault-tolerance
- quorum-audit
- multi-region-failover
- distributed-systems
- observability
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# Show HN: One provider starts lying at request 50. The quorum catches it

## Summary
This is a replayable distributed demo: in a dual-region, dual-relay hub, three-provider architecture, it deliberately causes one provider to start “lying” later in the run, and uses 2-of-3 quorum auditing to detect reporting drift. It emphasizes that **authority resides only with the provider**, while the front entrypoint and hubs perform only mechanical forwarding and observability collection.

## Problem
- The problem it addresses is: when a replica in a multi-replica/multi-provider system begins exhibiting **Byzantine drift** (its internal real execution logic remains unchanged, but the results it reports outward become inconsistent), how can anomalies be detected **without moving decision-making authority up to the gateway or relay**.
- This matters because cross-region disaster recovery, multi-provider model/service integration, and neutral front layers often need to preserve a unified request interface; if the boundaries between the observability layer and execution authority are blurred, systems become harder to audit and harder to isolate responsibility for failures.
- The demo also focuses on failover scenarios: requests are sent to Region 1 before `FAILOVER_AT`, then switched to Region 2 afterward, while preserving constant HTTP 204 interface semantics for the requester.

## Approach
- Architecturally, each region contains a **NUVL front**, two peer relay hubs, and three providers. NUVL only receives requests, computes `SHA-256(request_bytes)` and `binding`, and then forwards the artifact; the hubs only perform peer relay, fanout, and `/outcome` collection, and do not perform authorization, consensus, or threshold decisions.
- The actual decision of “whether to initiate execution” is made independently only by the provider: the provider checks `binding_ok`, domain thresholds, and internally generates a provider-boundary artifact; thus, authority location is explicitly constrained to the provider boundary.
- To simulate Byzantine behavior, after a deterministic `byz_start`, `Provider_B` flips about **50%** of `initiated_reported` results, while its internal “real” initiation logic remains unchanged. This models **reporting-layer drift** rather than complete corruption of the execution layer.
- The audit layer performs **2-of-3 quorum** aggregation over provider-reported outcomes for observability only, not as an authorization input; this allows reporting divergence to be detected without turning the hubs into adjudicators.
- The entire run is **deterministically replayable**: the request sequence, domain selection, payload construction, and Byzantine starting point are all determined by the seed and index, making it easy to compare drift events before and after failover and across different runs.

## Results
- The core claimed result of the demo is that when a provider begins lying about roughly **50%** of outcomes after about the **50th** request, **2-of-3 quorum auditing can catch the drift**, even though neither the hubs nor the front entrypoint hold decision authority.
- Under the default configuration, `TOTAL_REQUESTS = 100`, `FAILOVER_AT = TOTAL_REQUESTS // 2 = 50`, and `QUORUM_THRESHOLD = 2`; the system uses Region 1 for the first **50** requests and Region 2 for the remaining **50**, demonstrating a unified interface and observability under dual-region failover.
- Output metrics include counts of HTTP **204** successes/errors, total elapsed time, average time per request, total quorum audit successes/failures, and success/failure counts by domain; these are explicitly labeled as **observability metrics rather than authorization results**.
- The text does not provide a specific experimental table, accuracy figures, latency values, or quantitative comparison against other systems/baselines, so there are **no formal benchmark numbers that can be extracted**.
- The strongest concrete claim is that in a **dual-region + dual-hub mesh + three-provider** topology, it can simultaneously demonstrate client-side failover, provider-only authority, and replayable detection of adversarial replica reporting drift.

## Link
- [https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md](https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md)
