---
source: hn
url: https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md
published_at: '2026-03-04T23:34:26'
authors:
- sbw70
topics:
- distributed-systems
- byzantine-faults
- quorum-audit
- failover
- observability
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: One provider starts lying at request 50. The quorum catches it

## Summary
This is a replayable distributed demo system: two regions, a two-hub relay per region, and three providers executing independently, using a 2-of-3 quorum audit to detect report drift when one provider starts “lying” after about the 50th request. Its core value is to show that even with region failover and Byzantine-style reporting drift, anomalies can still be observed without giving decision authority to the hubs.

## Problem
- The problem it aims to solve is: in a multi-provider, multi-region execution topology, how to detect when one provider’s output reports begin to diverge from its true internal execution logic **without letting the middle layer gain execution authority or adjudication authority**.
- This matters because real systems encounter region failover, replica drift, and malicious or distorted state reporting; if the observability layer cannot detect these inconsistencies, both auditing and reliability break down.
- The text also emphasizes authority placement: hubs must not be mistakenly given authorization or consensus responsibilities just because they are used for auditing or quorum counting.

## Approach
- It designs two regions (R1/R2), each containing a NUVL front end, two hubs that perform only mechanical forwarding (A↔B mesh), and three providers (A/B/C) that are the actual execution authorities.
- Requests go to Region 1 first, then switch to Region 2 when `FAILOVER_AT` is reached; clients always receive a fixed `HTTP 204`, thereby separating “ingress path availability” from “execution result semantics.”
- NUVL does only three things: accept opaque bytes, compute `SHA-256(request_bytes)` to obtain `request_repr`, then generate `binding = nuvl_bind(...)` and forward it; it **does not hold secrets, decide initiation, or interpret outcomes**.
- Providers independently evaluate `binding_ok` and the domain threshold, and **only providers can initiate**; hubs are responsible only for relay/fanout and receiving `/outcome` observability signals, and do not participate in authorization, threshold judgment, or consensus.
- A deterministic Byzantine drift is injected: after `byz_start`, `Provider_B` flips about **50%** of `initiated_reported`, while its “real” internal initiation logic remains unchanged; then a **2-of-3 quorum audit** is used to aggregate provider-reported observations and detect divergence.

## Results
- The demo claims to successfully cover a topology of **2 regions**, **2 hubs** per region, and **3 providers** per region, and to run under the default settings **`TOTAL_REQUESTS=100`**, **`FAILOVER_AT=50`**, and **`QUORUM_THRESHOLD=2`**.
- The key breakthrough claim is that when one provider begins lying in about **50%** of outcome reports after the computed `byz_start` (the title example points to around the **50th** request), the **2-of-3 quorum audit** can still detect drift at the observability layer **without moving authority to the hubs**.
- The system also claims to preserve the same request interface semantics before and after failover: the client always hits `/nuvl` and receives **HTTP 204**, while region switching occurs only at the ingress selection layer and the downstream remains provider-controlled and hub-neutral.
- When complete, it outputs quantifiable observability metrics: total requests, failover point, `byz_start`, requester HTTP success/error counts, total duration, average per-request latency, total quorum success/failure counts, and per-domain success/failure statistics.
- But the provided excerpt **does not include concrete experimental numbers** (for example, actual success rate, false positive rate, detection latency, or the degree of improvement over a no-quorum baseline), so it is not possible to report standard academic-style quantitative SOTA or numbers showing significant superiority over a baseline. The strongest specific conclusion remains: under replayable conditions, with the default setup of 100 requests, 2-region failover, and one provider flipping about 50% of reports, quorum auditing can observe Byzantine-style reporting drift.

## Link
- [https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md](https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md)
